import tkinter as tk

def key_down(event):
    global key
    key = event.keysym


if __name__ == "__main__":
    # 初期化
    root = tk.Tk()
    root.title("maze")
    key = ""
    root.bind("<KeyPress>", key_down)

    canvas = tk.Canvas(root, width=1500, height=900, bg='black')
    canvas.pack()

    tori = tk.PhotoImage(file = "./ex03/fig/0.png")
    cx, cy = 300, 400
    canvas.create_image(cx, cy, image=tori, tag="tori")

    root.mainloop()