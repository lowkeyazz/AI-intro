# =======Default mazes=======
import copy
from tkinter import CENTER

from PIL import Image, ImageTk

from agents import Thing, XYEnvironment, Wall, Action
from search import SearchAgent

maze30x30 = ["##############################",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                          ###",
             "#                         ## #",
             "#                        ##  #",
             "#                       ##   #",
             "#                      ##    #",
             "#              A     ##      #",
             "#                  ##        #",
             "#                 ##         #",
             "#               ##           #",
             "#       #########            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                            #",
             "#                           *#",
             "##############################"]



maze6x6 = ["########",
           "#A #   #",
           "# ##   #",
           "#  ### #",
           "#  ##  #",
           "#*  #  #",
           "#*  *  #",
           "########"]

maze8x8 = ["##########",
           "#A #     #",
           "# ##     #",
           "#    # # #",
           "#   *    #",
           "#  #  *  #",
           "#  #    *#",
           "#   *  # #",
           "#*  *  #*#",
           "##########"]

maze10x10 = ["############",
             "#A #       #",
             "# ##       #",
             "# ##       #",
             "#    # #   #",
             "#    #     #",
             "#    #    *#",
             "#    #  *  #",
             "#     *    #",
             "#       #  #",
             "#   *  *#  #",
             "############"]
maze_25x25 = [
    "#########################",
    "#A  #######            ##",
    "#                      ##",
    "#                      ##",
    "######  ##    ####  #####",
    "#                      ##",
    "#                     ###",
    "#                      ##",
    "#  ###        ####  #####",
    "#                      ##",
    "#                      ##",
    "#                ########",
    "############     #####  #",
    "#                      ##",
    "############     #####  #",
    "#                      ##",
    "############     #####  #",
    "#                    ####",
    "#        ###            #",
    "#        ###            #",
    "##                      #",
    "#                       #",
    "###          ####       #",
    "#*                      #",
    "#########################"
]
# =======End default mazes=======
mazes = {0: maze30x30, 1: maze6x6, 2: maze8x8, 3: maze10x10, 4: maze_25x25}


class Diamond(Thing):
    pass


# ____________________Complex Environment ___________________________________`

class DiamondExplorerEnvironment(XYEnvironment):
    def __init__(self, width=10, height=10):
        super().__init__(width, height)
        self.add_walls()

    def thing_classes(self):
        return [Wall, Diamond, SearchAgent]

    def percept(self, agent):
        """The percept is a tuple of ('diamond' or 'None', 'Bump' or 'None').
        Unlike the TrivialDiamondExplorerEnvironment, location is NOT perceived."""
        status = ('diamond' if self.some_things_at(agent.location, Diamond) else None)
        bump = ('bump' if agent.bump else None)
        return status, bump

    def execute_action(self, agent, action):
        agent.bump = False
        if action == Action.Grab:
            d = self.list_things_at(agent.location, Diamond)
            if d:
                diamond = d[0]
                agent.performance += 100
                self.delete_thing(diamond)
        else:
            super().execute_action(agent, action)
            if agent.bump:
                agent.performance -= 5
            elif action != Action.NoOp:
                agent.performance -= 10

    def get_diamond_location(self):
        locations = []
        for thing in self.things:
            if isinstance(thing, Diamond):
                locations.append(thing.location)
        return locations


def build_diamond_explorer_environment(maze, agent_factory):
    env = DiamondExplorerEnvironment(len(maze[0]), len(maze))
    for i in range(1, len(maze) - 1):
        for j in range(1, len(maze[i])):
            if maze[i][j] == '#':
                env.add_thing(Wall(), (j, i))
            elif maze[i][j] == '*':
                env.add_thing(Diamond(), (j, i))
            elif maze[i][j] == 'A':
                env.add_thing(agent_factory(), (j, i))
    return env


global current_robot_img
global current_diamond_photo


class DiamondExplorerEnv4Gui(DiamondExplorerEnvironment):
    def __init__(self, canvas, animation_speed,
                 interrupted,
                 score_lbl,
                 maze_index, done_observer,
                 fn='dfs', prob='DiamondExplorerProblem',
                 heuristic='nullHeuristic'):
        super().__init__(len(mazes.get(maze_index)[0]), len(mazes.get(maze_index)))
        self.maze = copy.deepcopy(mazes.get(maze_index))
        for i in range(1, len(self.maze) - 1):
            for j in range(1, len(self.maze[i])):
                if self.maze[i][j] == '#':
                    self.add_thing(Wall(), (j, i))
                elif self.maze[i][j] == '*':
                    self.add_thing(Diamond(), (j, i))
                elif self.maze[i][j] == 'A':
                    self.agent = SearchAgent(self, fn, prob, heuristic)
                    self.add_thing(self.agent, (j, i))

        self.canvas = canvas
        self.speed = animation_speed
        self.score_lbl = score_lbl
        self.interrupted = interrupted
        self.done_observer = done_observer
        self.steps = 1000
        self.agent_img = Image.open("images/agent.png")
        self.robot_img = None
        self.diamond_img = Image.open("images/diamond.png")
        self.diamond_photo = None

    def delete_thing(self, thing):
        super().delete_thing(thing)
        if isinstance(thing, Diamond):
            x, y = thing.location
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x + 1:]

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        self.steps = steps
        self.start()

    def start(self):
        self.draw_maze()
        self.steps = self.steps - 1
        if not self.is_done() and not self.interrupted.get() and self.steps > 0:
            self.step()
            self.canvas.after(self.speed.get(), self.start)
        else:
            t = self.agent.total_time
            t= float('{0:.2f}'.format(t))
            c = self.agent.total_cost
            e = self.agent.nb_expand
            p = self.agent.performance

            self.score_lbl['text'] = str(tuple((t, c, e, p)))
            self.agent.alive = False
            height = self.canvas.winfo_height()
            width = self.canvas.winfo_width()
            # self.canvas.create_rectangle(0, 0, width, height, fill="#000")
            self.done_observer()

    def draw_maze(self):
        self.canvas.delete('all')
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.create_rectangle(0, 0, width, height, fill="white")
        path = []
        if self.agent.path_solution:
            for node in self.agent.path_solution:
                path.append(node.state)
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                if self.is_wall(x, y):
                    self.draw_wall(x, y)
                elif self.is_diamond(x, y):
                    self.draw_diamond(x, y)
                elif (x, y) in path:
                    self.draw_rec(x, y, color="cyan")
                else:
                    self.draw_rec(x, y, "white")
        self.draw_agent()

    def is_wall(self, x, y):
        return self.maze[y][x] == '#'

    def is_diamond(self, x, y):
        return self.maze[y][x] == '*'

    def draw_wall(self, x, y):
        self.draw_rec(x, y, "#000")

    def draw_diamond(self, x, y):
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width
        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)
        if self.diamond_photo is None:
            width, height = self.diamond_img.size
            if width > x2 - x1:
                image = self.diamond_img.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.diamond_photo = ImageTk.PhotoImage(image)
            else:
                self.diamond_photo = ImageTk.PhotoImage(self.diamond_img)

        global current_diamond_photo
        current_diamond_photo = self.get_diamond_photo()
        self.canvas.create_image((x1 + x2) / 2,
                                 (y1 + y2) / 2,
                                 image=current_diamond_photo,
                                 anchor=CENTER)

    def draw_rec(self, x, y, color):
        x1, y1, x2, y2 = self.convert(x, y)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def convert(self, x, y):
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width
        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)
        return x1, y1, x2, y2

    def draw_agent(self):
        x, y = self.agent.location
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        height = self.canvas.winfo_height() / maze_height
        width = self.canvas.winfo_width() / maze_width
        x1, y1 = (x * width, y * height)
        x2, y2 = (x1 + width, y1 + height)

        if self.robot_img is None:
            width, height = self.agent_img.size
            if width > x2 - x1:
                image = self.agent_img.resize((int(x2 - x1), int(y2 - y1)), Image.NEAREST)
                self.robot_img = ImageTk.PhotoImage(image)
            else:
                self.robot_img = ImageTk.PhotoImage(self.agent_img)

        global current_robot_img
        current_robot_img = self.get_robot_img()
        self.canvas.create_image((x1 + x2) / 2,
                                 (y1 + y2) / 2,
                                 image=current_robot_img,
                                 anchor=CENTER)

    def get_robot_img(self):
        return self.robot_img

    def get_diamond_photo(self):
        return self.diamond_photo
