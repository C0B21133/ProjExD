import tkinter as tk

def key_down(event):
    global key
    key = event.keysym
    # print(key)

def key_up(event):
    global key
    key = ""
    # print(key, "aaa")

if __name__ == "__main__":
    # 初期化
    root = tk.Tk()
    root.title("maze")
    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)

    canvas = tk.Canvas(root, width=1500, height=900, bg='black')
    canvas.pack()

    tori = tk.PhotoImage(file = "./ex03/fig/0.png")
    cx, cy = 300, 400
    canvas.create_image(cx, cy, image=tori, tag="tori")

    root.mainloop()