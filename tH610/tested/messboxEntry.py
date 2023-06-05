
# from tkinter import *
# from tkinter.simpledialog import askstring
# from tkinter.messagebox import showinfo

# win=Tk()
# win.geometry("700x300")

# name = askstring('Name', 'What is your name?')
# print(name)
# showinfo('Hello!', 'Hi, {}'.format(name))

# win.mainloop()




from tkinter import *
from tkinter import simpledialog       #askstring
from tkinter import messagebox         #showinfo

# Create an instance of tkinter frame and window
win=Tk()
win.geometry("700x300")

name = simpledialog.askstring('Name', 'What is your name?')
print(name)
messagebox.showinfo('Hello!', 'Hi, {}'.format(name))

win.mainloop()


