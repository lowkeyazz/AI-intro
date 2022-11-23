from tkinter import CENTER
from tkinter.font import Font

import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from diamond_2d_gui import *

global result_image


class Comparison:
    def __init__(self, canvas, interrupted, done_observer, nb_run=10):
        self.agent_factories = [ ]
        self.mazes2d = [maze30x30, maze6x6, maze8x8, maze10x10]
        self.results = [[] for i in range(len(self.agent_factories))]
        self.a = 0
        self.m = 0
        self.canvas = canvas
        self.nb_run = nb_run
        self.interrupted = interrupted
        self.done_observer = done_observer
        full_ex = len(self.agent_factories)*len(self.mazes2d)
        self.circularProgressbar = CircularProgressbar(canvas, 0, 0,
                                                       canvas.winfo_width(),
                                                       canvas.winfo_height(),
                                                       20,
                                                       full_extent=full_ex)

    def run(self):
        self.circularProgressbar.start()
        self.next_test()

    def next_test(self):
        if self.m >= 4:
            self.m = 0
            self.a += 1
        if self.a < len(self.agent_factories) and not self.interrupted.get():
            agent_factory = self.agent_factories[self.a]
            performances = 0.0
            for i in range(self.nb_run):
                env = build_diamond_explorer_environment(self.mazes2d[self.m], agent_factory)
                env.run()
                performances += env.agents[0].performance
            self.results[self.a].append(performances / self.nb_run)
            self.m += 1
            self.circularProgressbar.step()
            self.canvas.after(self.nb_run, self.next_test)
        else:
            if not self.interrupted.get():
                self.plot()
                self.draw_result()
            self.done_observer()

    def plot(self):
        # Turn interactive plotting off
        plt.ioff()
        # Create a new figure, plot into it, then close it so it never gets displayed
        fig = plt.figure()
        agent_lab = ['random_agent', 'reflex_agent', 'model_based_agent', 'model_based_advanced']
        maze_lab = ['maze30x30', 'maze6x6', 'maze8x8', 'maze10x10', 'maze25x25']
        for i in range(len(self.agent_factories)):
            plt.scatter([1, 2, 3, 4], self.results[i], label=agent_lab[i])
        # Add a legend
        plt.legend()
        plt.xticks(range(1, 1 + len(maze_lab)), maze_lab, size='small')
        plt.savefig('images/compare-result.png')
        plt.close(fig)

    def draw_result(self):
        self.canvas.delete('all')
        image = Image.open('images/compare-result.png')
        min1 = min(int(self.canvas.winfo_width()-5),  int(self.canvas.winfo_height()-5))
        size=(min1, min1)
        if image.size[0] > image.size[1]:
            ratio = float(min1)/image.size[0]
            size=(min1, int(ratio*image.size[1]))
        else:
            ratio = float(min1)/image.size[1]
            size=(int(ratio*image.size[0]), min1 )

        image = image.resize(size)
        global result_image
        result_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(size[0]/2, size[1]/2, image=result_image, anchor=CENTER)


class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=280, start_ang=0, full_extent=12):
        self.custom_font = Font(family="Helvetica", size=16, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0 + width, y0 + width, x1 - width, y1 - width
        self.tx, self.ty = (x1 - x0) / 2, (y1 - y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0 - w2, self.y0 - w2,
                                                self.x1 + w2, self.y1 + w2)
        self.oval_id2 = self.canvas.create_oval(self.x0 + w2, self.y0 + w2,
                                                self.x1 - w2, self.y1 - w2)
        self.running = False
        self.cur_extent = 0
        self.increment = 360 / full_extent  # 30

    def start(self):
        percent = '0%'
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1, start=self.start_ang,
                                             extent=self.cur_extent, width=self.width, style='arc')
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent, font=self.custom_font)

    def step(self):
        self.cur_extent = (self.cur_extent + self.increment) % 360
        self.canvas.itemconfigure(self.arc_id, extent=self.cur_extent)
        percent = '{:.0f}%'.format(round(float((self.cur_extent / self.increment) * 100 / self.full_extent)))
        self.canvas.itemconfigure(self.label_id, text=percent)
