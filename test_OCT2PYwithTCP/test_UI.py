import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation

import numpy as np

class Spinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        tk.Spinbox.__init__(self, *args, **kwargs)
        self.bind('<MouseWheel>', self.mouseWheel)
        self.bind('<Button-4>', self.mouseWheel)
        self.bind('<Button-5>', self.mouseWheel)
        self.bind('<Shift-MouseWheel>', self.shiftmouseWheel)

    def mouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')

        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')

    def shiftmouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')

        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.running = False
        self.ani = None

        btns = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        btns.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Power")
        lbl.grid(row=1, column=1)

        self.power_ent = tk.Entry(btns, width=8)
        self.power_ent.insert(0, '50')
        #self.points_ent.pack(side=tk.LEFT)
        self.power_ent.grid(row=1,column=2)

        lbl = tk.Label(btns, text="dBm")
        lbl.grid(row=1, column=3)

        lbl = tk.Label(btns, text="DOP")
        lbl.grid(row=2, column=1)

        self.DOP_ent = tk.Entry(btns, width=8)
        self.DOP_ent.insert(0, '1')
        self.DOP_ent.grid(row=2,column=2)

        self.RUN_btn = tk.Button(btns, width=15, text='Start', command=self.on_click)
        self.RUN_btn.grid(row=3,column=1)

        self.QUIT_btn = tk.Button(btns, width=15, text='Quit', command=self.quit)
        self.QUIT_btn.grid(row=3, column=2)

        self.SPINbox = Spinbox(btns, from_=0, to=360, increment=0.5,
                               state='readonly', justify='right',
                               wrap=True)
        self.SPINbox.grid(row=4,column=1)

        self.fig = plt.Figure()
        # self.ax0 = self.fig.add_subplot(411)
        # self.ax1 = self.fig.add_subplot(412)
        # self.ax2 = self.fig.add_subplot(413)
        # self.ax3 = self.fig.add_subplot(414)
        # self.line0, = self.ax0.plot([], [], lw=2)
        # self.line1, = self.ax1.plot([], [], lw=2)
        # self.line2, = self.ax2.plot([], [], lw=2)
        # self.line3, = self.ax3.plot([], [], lw=2)

        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)

        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax2.plot([], [], lw=2)
        self.line3, = self.ax3.plot([], [], lw=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # self.maxS = 65535
        # self.minS = 0
        self.maxS = 1
        self.minS = -1
        # self.ax0.set_ylim(0, self.maxS)
        # self.ax0.set_xlim(0, 500)
        self.ax1.set_ylim(self.minS, self.maxS)
        self.ax1.set_xlim(0, 500)
        self.ax2.set_ylim(self.minS, self.maxS)
        self.ax2.set_xlim(0, 500)
        self.ax3.set_ylim(self.minS, self.maxS)
        self.ax3.set_xlim(0, 500)

        # self.S0 = []
        self.S1 = []
        self.S2 = []
        self.S3 = []
        self.t = []
        self.S0 = 0
        self.DOP = 0

    def on_click(self):
        '''the button is a start, pause and unpause button all in one
        this method sorts out which of those actions to take'''
        if self.ani is None:
            # animation is not running; start it
            return self.start()

        if self.running:
            # animation is running; pause it
            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            # animation is paused; unpause it
            self.ani.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

def main():
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
