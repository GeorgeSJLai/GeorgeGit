import tkinter as tk

root = tk.Tk()

options = ["Option 1", "Option 2", "Option 3"]

selected_option = tk.StringVar()
selected_option.set(options[0]) # 預設選取第一個選項

option_menu = tk.OptionMenu(root, selected_option, *options)
option_menu.place(x=50, y=50) # 使用place方法定位

root.mainloop()
