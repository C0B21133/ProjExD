import tkinter as tk
import tkinter.messagebox as tkm
import numpy as np

class _button():
    def __init__(self, num):
        self.button = tk.Button(root, 
                                text=num, 
                                font=("Times New Roman", 30),
                                width=4,
                                height=2)


# 初期化
root = tk.Tk()
root.title("calc")
root.geometry("300x500")

id = [[j, k] for j in range(4) for k in range(3)]
buttons = [_button(n) for n in range(9, -1, -1)]

for i in range(10):
    buttons[i].button.grid(row=id[i][0], column=id[i][1])

root.mainloop()