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
    global cx, cy, mx, my, key
    xd = {"Left":-1, "Right":1}
    yd = {"Up":-1, "Down":1}
    if key in xd:
        mx += xd[key]
        cx = 50 + mx * 100
    elif key in yd:
        my += yd[key]
        cy = 50 + my * 100
    canvas.coords("tori", cx, cy)


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
    mm.show_maze(canvas, mazelist)

    tori = tk.PhotoImage(file = "./ex03/fig/0.png")
    cx, cy = 150, 150
    mx, my = 1, 1
    canvas.create_image(cx, cy, image=tori, tag="tori")
    root.mainloop()