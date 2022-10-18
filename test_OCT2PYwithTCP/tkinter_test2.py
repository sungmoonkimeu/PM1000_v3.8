import tkinter as tk # Python 3 tkinter modules
import tkinter.ttk as ttk

class App(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # 1. Initialise Frame
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # Method1
        name1 = ['Peter', 'Scotty', 'Walter', 'Scott', 'Mary']
        self.lb1_values = tk.StringVar(value=name1)
        self.listbox1 = tk.Listbox(self, listvariable=self.lb1_values)

        # Method2
        self.listbox2 = tk.Listbox(self)
        name2 = ['Sarah', 'Sean', 'Mora', 'Mori', 'Mary']
        for item in name2:
            self.listbox2.insert(tk.END, item)

        self.listbox1.grid(in_=self, row=0, column=0, sticky='nsew')
        self.listbox2.grid(in_=self, row=0, column=1, sticky='nsew')

        # Extract values from listbox and covert to a list
        e1 = self.lb1_values.get()
        print('e1 = ', e1)
        print('type(e1) = ', type(e1))
        e1 = e1.strip(',')
        print('e1 = ', e1)

        e2 = self.listbox1.cget('listvariable')
        print('\ne2 = ', e2)
        print('type(e2) = ', type(e2))
        e2 = e2.split(',')
        print('e2 = ', e2)

        e3 = self.listbox2.cget('listvariable')
        print('\ne3 = ', e3)
        print('type(e3) = ', type(e3))

        e4 = self.listbox2.get(0, tk.END)
        print('\ne4 = ', e4)
        print('type(e4) = ', type(e4))
        e4 = list(e4)
        print('e4 = ', e4)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('App'), root.geometry('400x200')
    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')
    #root.mainloop()