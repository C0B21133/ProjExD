import tkinter as tk
import tkinter.messagebox as tkm

class _button():
    def __init__(self, num, index):
        self.button = tk.Button(root, 
                                text=num, 
                                font=("Times New Roman", 30),
                                width=4,
                                height=2)
        self.button.grid(row=index[0], column=index[1])
        self.button.bind("<1>", _button.button_click)

    @staticmethod
    def button_click(event):
        btn = event.widget
        num = btn["text"]
        # tkm.showinfo(num, f"{num}のボタンが押されました")
        entry.insert(tk.END, num)


class sum_button(_button):
    def __init__(self, num, index):
        super().__init__(num, index)
        self.button.bind("<1>", sum_button.button_click)

    @staticmethod
    def button_click(event):
        data = entry.get()
        data = data.split("+")
        data = [int(i) for i in data]
        ans = sum(data)
        entry.delete(0, tk.END)
        entry.insert(tk.END, ans)


# 初期化
root = tk.Tk()
root.title("calc")
root.geometry("293x573")

entry = tk.Entry(justify="right", width=10, font=("Times New Roman", 40))
entry.grid(row=0, column=0,  columnspan=3)

# ボタン作成
index = [[j, k] for j in range(1, 5) for k in range(3)]
index = index[:10]
index.reverse()
buttons = [_button(n, index[n]) for n in range(10)]
plusbutton = _button("+", [4, 1])
sumbutton = sum_button("=", [4, 2])

root.mainloop()

