from tkinter import *
from tkinter.scrolledtext import ScrolledText

# from tkinter.ttk import Style
from tkinter.ttk import Separator

from agents import *
from comparison import Comparison
from search import get_defined_heuristics
# #########Boolean object used to interrupt agents #########
from diamond_2d_gui import DiamondExplorerEnv4Gui


class Boolean:
    def __init__(self):
        self.b = False

    def get(self):
        return self.b

    def set(self, v):
        self.b = v


class Simulator(Tk):
    def __init__(self):
        super().__init__()
        self.interrupted = Boolean()
        # self.style = Style()
        # ('clam', 'alt', 'default', 'classic')
        # self.style.theme_use("classic")
        ##########################################################
        self.title('UM6P-LSD3: Artificial Intelligence, Unit 3')
        self.geometry('{}x{}'.format(1000, 800))
        # self.resizable(False, False)  # disable window resizing

        # create all of the main containers
        self.top_frame = Frame(self, width=1000, height=50, pady=3)
        self.center = Frame(self, width=1000, height=650, padx=3, pady=3)
        self.btm_frame = Frame(self, width=1000, height=100, pady=3)

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame.grid(row=0, sticky="ew")
        self.center.grid(row=1, sticky="nsew")
        self.btm_frame.grid(row=3, sticky="ew")

        # create the widgets for the top frame
        self.simulator_label = Label(self.top_frame, text='Diamond explorer simulator')
        self.separator1 = Separator(self.top_frame, orient='vertical')
        self.simulator = IntVar()
        self.R1 = Radiobutton(self.top_frame, text="maze30x30", variable=self.simulator, value=0)
        self.R2 = Radiobutton(self.top_frame, text="maze6x6", variable=self.simulator, value=1)
        self.R3 = Radiobutton(self.top_frame, text="maze8x8", variable=self.simulator, value=2)
        self.R4 = Radiobutton(self.top_frame, text="maze10x10", variable=self.simulator, value=3)
        self.R5 = Radiobutton(self.top_frame, text="maze25x25", variable=self.simulator, value=4)
        self.simulator.set(0)
        self.separator2 = Separator(self.top_frame, orient='vertical')

        # layout the widgets in the top frame
        self.simulator_label.grid(row=0, column=0)
        self.separator1.grid(row=0, column=1, padx=10, pady=10)
        self.R1.grid(row=0, column=2)
        self.R2.grid(row=0, column=3)
        self.R3.grid(row=0, column=4)
        self.R4.grid(row=0, column=5)
        self.R5.grid(row=0, column=6)

        # create the center widgets
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        self.ctr_left = Frame(self.center, width=200, height=650)
        self.ctr_mid = Frame(self.center, width=700, height=650, padx=3, pady=3)
        self.ctr_right = Frame(self.center, width=100, height=650, padx=3, pady=3)

        # create the widgets for the left frame
        self.agent_label = Label(self.ctr_left, text="Agent to run:")
        self.btn_dfs = Button(self.ctr_left, text='Depth First Search', bd='5')
        self.btn_bfs = Button(self.ctr_left, text='Breadth First Search', wraplength=100, justify=LEFT, bd='5')
        self.btn_ucs = Button(self.ctr_left, text='Uniform Cost  Search', bd='5')
        self.btn_compare = Button(self.ctr_left, text='Compare all', bd='5')
        self.btn_gs = Button(self.ctr_left, text='Greedy BF Search', bd='5')
        self.btn_a_star = Button(self.ctr_left, text='A_Star', wraplength=100, justify=LEFT, bd='5')
        self.heuristic_txt = Text(self.ctr_left, height=1, width=25, bg="light cyan", fg='black')

        self.heuristics = get_defined_heuristics()
        if 'nullHeuristic' in self.heuristics:
            self.heuristics.remove('nullHeuristic')
        self.heuristics.insert(0, 'nullHeuristic')
        self.heuristic = IntVar()
        self.heuristic.set(0)
        self.radio_heuristic = []
        for i in range(len(self.heuristics)):
            self.radio_heuristic.append(Radiobutton(self.ctr_left, text=self.heuristics[i],
                                                    variable=self.heuristic, value=i))

        self.btn_compare = Button(self.ctr_left, text='Compare all', bd='5')

        self.lbl_explored = Label(self.ctr_left, text='Explored', bd='5')
        self.lbl_explored.configure(foreground="black", background="red")
        self.lbl_frontier = Label(self.ctr_left, text='Frontier', bd='5')
        self.lbl_frontier.configure(foreground="black", background="blue")
        self.lbl_path = Label(self.ctr_left, text='Solution path', bd='5')
        self.lbl_path.configure(foreground="black", background="cyan")

        # self.heuristic_txt.insert(END, "nullHeuristic")
        # self.lbl_explored = Label(self.ctr_left, text='Explored', bd='5')
        # self.lbl_explored.configure(foreground="white", background="red")
        # self.lbl_frontier = Label(self.ctr_left, text='Frontier', bd='5')
        # self.lbl_frontier.configure(foreground="white", background="blue")

        # create the widgets for the right frame

        self.btn_interrupt = Button(self.ctr_right, text='Interrupt agent', command=lambda: self.interrupt())
        self.btn_interrupt['state'] = 'disabled'
        self.label_animation = Label(self.ctr_right, text='Animation speed:')
        self.animation_speed = Scale(self.ctr_right, from_=2, to=1000, orient=HORIZONTAL)
        self.animation_speed.set(5)
        self.text_score_lbl = Label(self.ctr_right, text='Score obtained by ', bd='5')
        self.score_format_lbl = Label(self.ctr_right, text='(t(s), cost, #expanded, performance)', bd='5')

        self.lbl1 = Label(self.ctr_right, text='Depth First Search', bd='5')
        self.score_dfs = Label(self.ctr_right, text='0', bd='5')
        self.lbl2 = Label(self.ctr_right, text='Breadth First Search', justify=LEFT, bd='5')
        self.score_bfs = Label(self.ctr_right, text='0', bd='5')
        self.lbl3 = Label(self.ctr_right, text='Uniform Cost  Search', bd='5')
        self.score_ucs = Label(self.ctr_right, text='0', bd='5')

        self.lbl5 = Label(self.ctr_right, text='Greedy BF Search', bd='5')

        self.score_gs = Label(self.ctr_right, text='0', bd='5')
        self.lbl4 = Label(self.ctr_right, text='A_Star Search', bd='5')
        self.score_a_star = Label(self.ctr_right, text='0', bd='5')

        # create the widgets for the center frame
        self.canvas = Canvas(self.ctr_mid, bg='#A39449', width=560, heigh=560)
        # create the widgets for the bottom frame
        self.text_box = ScrolledText(self.btm_frame, wrap=WORD,
                                     width=97,
                                     height=6,
                                     font=("Times New Roman", 15))

        self.text_box.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))

        # layout the widgets in the left frame
        self.agent_label.grid(row=0, column=0, sticky=W + E)
        self.btn_dfs.grid(row=1, column=0, sticky=W + E)
        self.btn_bfs.grid(row=2, column=0, sticky=W + E)
        self.btn_ucs.grid(row=3, column=0, sticky=W + E)
        self.btn_gs.grid(row=4, column=0, sticky=W + E)

        self.btn_a_star.grid(row=5, column=0, sticky=W + E)

        l = len(self.heuristics)
        for i in range(l):
            self.radio_heuristic[i].grid(row=6 + i, column=0, sticky=W + E)
        l += 1
        self.btn_compare.grid(row=l + 5, column=0, sticky=W + E)

        self.lbl_explored.grid(row=l + 7, column=0, padx=10, pady=20, sticky=W + E)
        self.lbl_frontier.grid(row=l + 8, column=0, padx=10, pady=10, sticky=W + E)
        self.lbl_path.grid(row=l + 9, column=0, padx=10, pady=10, sticky=W + E)
        # self.heuristic_txt.grid(row=5, column=0, padx=10, sticky=W + E)
        # self.btn_compare.grid(row=6, column=0, sticky=W + E)
        # self.lbl_explored.grid(row=7, column=0, padx=10, pady=20, sticky=W + E)
        # self.lbl_frontier.grid(row=8, column=0, padx=10, pady=10, sticky=W + E)

        # layout the widgets in the right frame

        self.btn_interrupt.grid(row=0, column=0, sticky=W + E)
        self.label_animation.grid(row=1, column=0, sticky=W + E)
        self.animation_speed.grid(row=2, column=0, sticky=W + E)
        self.text_score_lbl.grid(row=3, column=0, sticky=W + E)
        self.score_format_lbl.grid(row=4, column=0, sticky=W + E)
        self.lbl1.grid(row=5, column=0, sticky=W + E)
        self.score_dfs.grid(row=6, column=0, sticky=W + E)
        self.lbl2.grid(row=7, column=0, sticky=W + E)
        self.score_bfs.grid(row=8, column=0, sticky=W + E)
        self.lbl3.grid(row=9, column=0, sticky=W + E)
        self.score_ucs.grid(row=10, column=0, sticky=W + E)
        self.lbl4.grid(row=11, column=0, sticky=W + E)
        self.score_a_star.grid(row=12, column=0, sticky=W + E)
        self.lbl5.grid(row=13, column=0, sticky=W + E)
        self.score_gs.grid(row=14, column=0, sticky=W + E)

        # layout the widgets in the center frame
        self.canvas.grid(row=0, column=0)

        # layout the widgets in the bottom frame
        self.text_box.grid(row=0, column=0, sticky="nsew")

        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.ctr_right.grid(row=0, column=2, sticky="ns")

        self.btn_dfs.bind('<Button-1>', self.run_dfs_agent)
        self.btn_bfs.bind('<Button-1>', self.run_bfs_agent)
        self.btn_ucs.bind('<Button-1>', self.run_ucs_agent)
        self.btn_a_star.bind('<Button-1>', self.run_a_star_agent)
        self.btn_gs.bind('<Button-1>', self.run_gs_agent)
        self.btn_compare.bind('<Button-1>', self.run_compare)


    def run_dfs_agent(self, event=None):
        self.run_agent('dfs')

    def run_bfs_agent(self, event=None):
        self.run_agent('bfs')

    def run_ucs_agent(self, event=None):
        self.run_agent('ucs')

    def run_gs_agent(self, event=None):
        self.run_agent('gs')

    def run_a_star_agent(self, event=None):
        self.run_agent('a_star')

    def run_agent(self, algo):
        self.disable_btns()
        score = self.score_dfs
        if algo == 'bfs':
            score = self.score_bfs
        if algo == 'ucs':
            score = self.score_ucs
        if algo == 'a_star':
            score = self.score_a_star
        if algo == 'gs':
            score = self.score_gs
        env = DiamondExplorerEnv4Gui(self.canvas, self.animation_speed,
                                     self.interrupted, score,
                                     self.simulator.get(),
                                     self.enable_btns, fn=algo, heuristic=self.heuristics[self.heuristic.get()])
        self.run_simulation(env)

    def run_simulation(self, env):
        trace_agent(env.agent, self.text_box)
        env.run()

    def interrupt(self):
        self.interrupted.set(True)
        self.enable_btns()

    def disable_btns(self):
        self.canvas.delete('all')
        self.interrupted.set(False)
        self.btn_dfs['state'] = 'disabled'
        self.btn_bfs['state'] = 'disabled'
        self.btn_ucs['state'] = 'disabled'
        self.btn_compare['state'] = 'disabled'
        self.btn_a_star['state'] = 'disabled'
        self.btn_gs['state'] = 'disabled'
        self.btn_interrupt['state'] = 'normal'

    def enable_btns(self):
        self.btn_dfs['state'] = 'normal'
        self.btn_bfs['state'] = 'normal'
        self.btn_ucs['state'] = 'normal'
        self.btn_compare['state'] = 'normal'
        self.btn_a_star['state'] = 'normal'
        self.btn_gs['state'] = 'normal'
        self.btn_interrupt['state'] = 'disabled'
        self.text_box.delete('1.0', END)

    def run(self):
        self.mainloop()

    def run_compare(self, event=None):
        self.disable_btns()
        comp = Comparison(self.canvas, self.interrupted, self.enable_btns)
        comp.run()


if __name__ == '__main__':
    Simulator().run()
