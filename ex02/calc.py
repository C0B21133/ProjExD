import tkinter as tk
import tkinter.messagebox as tkm

class _button():
    def __init__(self, num):
        self.button = tk.Button(root, 
                                text=num, 
                                font=("Times New Roman", 30),
                                width=4,
                                height=2)


def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"{txt}のボタンが押されました")

# 初期化
root = tk.Tk()
root.title("calc")
root.geometry("300x500")

# ボタン作成
index = [[j, k] for j in range(4) for k in range(3)]
index = index[:10]
index.reverse()
buttons = [_button(n) for n in range(10)]

for i in range(10):
    buttons[i].button.grid(row=index[i][0], column=index[i][1])
    buttons[i].button.bind("<1>", button_click)

root.mainloop()
