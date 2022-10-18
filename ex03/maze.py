import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker as mm
import random
import time
import threading

def key_down(event):
    global key
    key = event.keysym
    main_proc()

def key_up(event):
    global key
    key = ""
    main_proc()

def main_proc():
    global cx, cy, mx, my, key
    xd = {"Left":-1, "Right":1, "a":-1, "d":1}
    yd = {"Up":-1, "Down":1, "w":-1, "s":1}
    # x方向の処理かつ移動先が壁でない
    if (key in xd) and (mazelist[my][mx+xd[key]] != 1):
        mx += xd[key]
        cx = 50 + mx * 100
    # y方向の処理かつ移動先が壁でない
    elif (key in yd) and (mazelist[my+yd[key]][mx] != 1):
        my += yd[key]
        cy = 50 + my * 100
    # 迷路の更新(上書き)
    show_maze2(canvas, mazelist)
    # こうかとん更新
    canvas.coords("tori", cx, cy)
    # こうかとんを最前面にする
    canvas.lift("tori")
    if (mx == goal[1]) and (my == goal[0]):
        # タイマー終了
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # メッセージボックス
        text = f"ゴールしました！おめでとうございます！\n時間: {round(elapsed_time)}s"
        tkm.showinfo("GAME CLEAR!", text)
        # 画面を閉じる
        root.destroy()


def show_maze2(canvas, maze_lst):
    """show_mazeを(mx, my)の周囲3×3だけ表示するようにした関数"""
    # 0:床, 1:壁, 2:スタート, 3:ゴール
    color = ["white", "gray", "green", "red"]
    for y in range(len(maze_lst)):
        for x in range(len(maze_lst[y])):
            if (mx-1 <= x <= mx+1) and (my-1 <= y <= my+1):
                canvas.create_rectangle(x*100, y*100, x*100+100, y*100+100, 
                                    fill=color[maze_lst[y][x]])

def dialog():
    x  = tkm.showinfo("", "Are you ready?")
    print(type(x))
    if x == "ok":
        start_time = time.perf_counter()


if __name__ == "__main__":
    # 初期化
    root = tk.Tk()
    root.title("maze")
    start = [1, 1]; goal = []       # スタートとゴール
    cx, cy = 150, 150               # 位置
    mx, my = start                  # 位置(升目単位)
    key = ""
    # キー設定
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    # canvas作成
    canvas = tk.Canvas(root, width=1500, height=900, bg='black')
    canvas.pack()
    # 2次元リスト作成
    mazelist = mm.make_maze(15, 9)
    #ゴール位置を右上か右下かランダムに設定
    goal_choice = [[7, 13], [1, 13]]
    num = random.randint(0, 1)
    goal = goal_choice[num]

    # スタートとゴールの設定 
    mazelist[start[0]][start[1]] = 2
    mazelist[goal[0]][goal[1]] = 3

    # 初期位置周囲3*3の範囲の迷路を生成
    show_maze2(canvas, mazelist)
    # mm.show_maze(canvas, mazelist)
    
    # こうかとん作成
    tori = tk.PhotoImage(file = "./ex03/fig/0.png")
    canvas.create_image(cx, cy, image=tori, tag="tori")
    # ダイアログ表示(threadingじゃないとうまくいかなかった)
    thread = threading.Thread(target=dialog)
    thread.start()
    # タイマー開始
    root.mainloop()