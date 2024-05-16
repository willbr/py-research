# doesnt work on mac

from tkinter import *
root = Tk()
c = Canvas(root, width=500, height=600)
c.pack()

# gray12 gray25 gray50 gray75
def example():
    c.create_oval(100, 375, 200, 425, fill="blue", stipple="gray25")
    c.create_rectangle(300, 375, 400, 425, fill="blue", stipple="gray25")
    root.mainloop()
example()

