import tkinter as tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym
    main_proc()
    # print(key)

def key_up(event):
    global key
    key = ""
    main_proc()
    # print(key, "aaa")

def main_proc():
    global cx, cy, key
    xd = {"Left":-20, "Right":20}
    yd = {"Up":-20, "Down":20}
    if key in xd:
        cx += xd[key]
    elif key in yd:
        cy += yd[key]
    canvas.coords("tori", cx, cy)
    print(key, key in xd, key in yd)


if __name__ == "__main__":
    # 初期化
    root = tk.Tk()
    root.title("maze")
    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)

    canvas = tk.Canvas(root, width=1500, height=900, bg='black')
    canvas.pack()

    mazelist = mm.make_maze(15, 9)

    tori = tk.PhotoImage(file = "./ex03/fig/0.png")
    cx, cy = 300, 400
    canvas.create_image(cx, cy, image=tori, tag="tori")
    root.mainloop()