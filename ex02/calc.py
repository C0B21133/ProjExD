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
        # entryから取得
        data = entry.get()
        if data[-1] == "%":
            try:
                ans = int(data[:-1])/100
            except:
                ans = "error"
        else:
            ans = eval(data)
        entry.delete(0, tk.END)
        entry.insert(tk.END, ans)

class del_button(_button):
    def __init__(self, num, index):
        super().__init__(num, index)
        self.button.bind("<1>", del_button.button_click)

    @staticmethod
    def button_click(event):
        entry.delete(0, tk.END)

if __name__ == "__main__":
    # 初期化 "293x573"
    root = tk.Tk()
    root.title("calc")
    root.geometry("400x703")
    # 入力欄作成
    entry = tk.Entry(justify="right", width=13, font=("Times New Roman", 40))
    entry.grid(row=0, column=0,  columnspan=4)
    # ボタン作成
    index = [[j, k] for j in range(1, 5) for k in range(3)]
    index = index[:10]
    index.reverse()
    for n in range(10):
        _button(n, index[n])
    # 演算ボタン作成
    sign1 = ["+", "-", "*", "/"]
    sign2 = [".", "%"]
    for i, n in enumerate(sign1, 2):
        _button(n, [i, 3])
    for i, n in enumerate(sign2, 4):
        _button(n, [i, 2])        
    sum_button("=", [4, 1])
    del_button("del", [1, 3])
    root.mainloop()

