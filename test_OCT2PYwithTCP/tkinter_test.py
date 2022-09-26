from tkinter import *


def retrieve():
    # print(listbox.curselection())
    result = listbox.get(0,END)
    print(result[0]+result[1])

root = Tk()
root.geometry("200x220")
frame = Frame(root)
frame.pack()

label = Label(root, text="A list of Grocery items.")
label.pack()

listbox = Listbox(root)

listbox.insert(1, 0.65)
listbox.insert(2, 3.67)
listbox.insert(3, "Meat")
listbox.insert(4, "Cheese")
listbox.insert(5, "Vegetables")
listbox.pack()

bttn = Button(frame, text="Submit", command=retrieve)
bttn.pack(side="bottom")
root.mainloop()