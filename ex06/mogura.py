import pygame as pg
import sys
from random import randint
import numpy as np
import time
from threading import Thread

# タイマー時間を設定git
TIME = 60


class Screen:
    """スクリーンに関する処理"""
    def __init__(self, title, wh, img_path):
        # titlt: "pygame", wh: (800, 800), img_path: "fig/sougenn.jpg"
        # ウィンドウ
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        # 背景
        img = pg.image.load(img_path)
        self.back_sfc = pg.transform.rotozoom(img, 0, 2.0)
        self.back_rct = self.back_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.back_sfc, self.back_rct)


class Hole:
    """穴を生成"""
    R = 120         # 楕円の大きさ参照元
    COUNT = 80      # 追記　スコア表示時間参照元

    def __init__(self, scr:Screen, xy):
        self.scr = scr
        self.sfc = pg.Surface((self.R*2, self.R*2))
        pg.draw.ellipse(self.sfc, (157, 135, 67), (self.R, self.R, self.R, self.R/3)) # (0, 0, 0)だと背景と同化して消えちゃうので注意
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

        self.pos = 0                    # 追記 スコア表示位置
        self.count = 0                  # 追記 スコア表示時間
        self.mogurapoint = 0            # クリックされた対象のスコア

    def blit(self):
        self.scr.sfc.blit(self.sfc, self.rct)

        if self.count:                  # 追記 self.countが0出ない時(スコア表示時間が設定されている時)
            self.count -= 1                 # 表示時間を減らす
            self.p1()                       # スコアを表示する関数を呼び出す

    # Moguraクラスから呼び出される関数
    # 引数1score：モグラの得点
    def set(self, score):
        self.pos = pg.mouse.get_pos()   # 追記 holeクラスにクリックされた位置を渡す
        self.count = Hole.COUNT         # 追記 スコア表示時間を設定
        self.mogurapoint = score        # Holeクラスからpointを取得する
        

    # 追記 モグラの得点に応じて画面にスコアを表示する関数
    def p1(self):
        # モグラの得点が負の処理
        if(self.mogurapoint < 0):
            font2 = pg.font.SysFont(None, 45)
            txt = font2.render("{}".format(self.mogurapoint), True, (0, 0, 0))
            self.scr.sfc.blit(txt, self.pos)
        # モグラの得点が正または0の処理
        else :
            font2 = pg.font.SysFont(None, 45)
            txt = font2.render("+{}".format(self.mogurapoint), True, (0, 0, 0))
            self.scr.sfc.blit(txt, self.pos)
            




class Mogura:
    """モグラを生成、出現処理を実装"""
    LIMIT = 5       # 表示できるモグラの上限
    NUMS = 0        # 表示中のモグラの数
    KILLS = 0       # スコア
    def __init__(self, scr:Screen):
        self.FLAG = False                       # 表示管理
        self.COOL_TIME = randint(100, 2500)     # 処理待機カウント
        self.WAIT_TIME = 0                      # モグラを表示するカウント( 0 は非表示)
        self.scr = scr                          # スクリーンインスタンスを保持
        self.hole = None                        # Holeインスタンスの保持先(初期化)
        
    def set(self, setdata):    
        """pictureを設定、setdata = [[img_path, zoom, point],]"""
        sfc = pg.image.load(setdata[0])
        self.sfc = pg.transform.rotozoom(sfc, 0, setdata[1])
        self.rct = self.sfc.get_rect()
        self.point = setdata[2]                 # ポイントの設定
        

    def cool_time(self):
        """処理待機カウント設定"""
        self.COOL_TIME = randint(800, 1000)

    def blit(self):
        self.scr.sfc.blit(self.sfc, self.rct)

    def update(self, hole:Hole, setdata):
        self.hole = hole                            # Holeインタンスを保持
        if Mogura.NUMS < Mogura.LIMIT or self.FLAG: # 出現上限以下 又は 表示中の時
            if not self.FLAG:                           # 新規表示なら
                self.set(setdata)                           # set呼び出し (画像、ポイントの設定)
                self.FLAG = True                            # 表示状態にする
                self.WAIT_TIME = randint(150, 500)          # モグラを表示するカウント設定(updateメソッドが150~500回呼び出されるまで表示)
                Mogura.NUMS += 1                            # 表示中のモグラの数 +1 
            else:                                       # 既に表示済みなら
                self.WAIT_TIME -= 1                         # モグラを表示するカウント -1
            self.rct.centerx = hole.rct.centerx + 60
            self.rct.centery = hole.rct.centery - 5
            self.blit()
            if not self.WAIT_TIME:                      # モグラを表示するカウントがなくなった時
                self.FLAG = False                           # 非表示にする
                Mogura.NUMS -= 1                            # 表示中のモグラの数 -1 
                self.cool_time()                            # cool_timeメソッド呼び出し(処理待機カウント設定)
        else:                                       # 出現上限以下 又は 表示中の時 以外の時
            self.cool_time()                            # cool_timeメソッド呼び出し(処理待機カウント設定)、ネットワークの衝突回避のイメージ
    
    def check(self, pos):
        """モグラのクリック判定"""
        return self.rct.collidepoint(pos)

    def click(self):
        """モグラがクリックされた時の処理"""
        self.FLAG = False               # 非表示にする
        Mogura.NUMS -= 1                # 表示中のモグラの数 -1 
        Mogura.KILLS += self.point      # スコアにself.point()を加算
        self.cool_time()                # cool_timeメソッド呼び出し(処理待機カウント設定)
        
        # 追記　クリックされた時にholeクラスのset関数を呼ぶ
        # hole(Hole)クラスのset関数にモグラごとの得点Mogura.pointを引数で渡す
        self.hole.set(self.point)          

class Bird:
    """こうかとんによる妨害プログラム"""
    def __init__(self, scr: Screen, img_path, zoom, xy):
        # img_path: "fig/6.png", zoom: 2.0, xy: (900, 400)
        # こうかとん生成
        self.scr = scr
        self.vx = randint(2, 7)     # x方向加速度(2~7のランダム)
        sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
    
    def blit(self):
        self.scr.sfc.blit(self.sfc, self.rct)

    def update(self, basey, height, yn):
        # こうかとん位置更新
        x = self.check_bound(self.scr.rct)
        self.vx *= x
        self.rct.move_ip(self.vx, 0)
        # 端に衝突を検知したら, 1/2の確率で実行
        if x == -1 and randint(0, 1):
            n = randint(0, yn-1)                        # 上から何段目に移動するかランダムで決定
            self.rct.centery = basey + n*height - 10    # y座標の設定
        self.blit()

    def check_bound(self, scr_rct):
        """
        scr_rct: スクリーン
        通常時: -1, 異常時:1
        """
        x = 1
        if self.rct.left < scr_rct.left or scr_rct.right < self.rct.right:
            x = -1
        return x


class Hammer:
    def __init__(self, img, zoom, center):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.scale(sfc, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center

    def update(self, mouse_xy):
        # 位置をマウスカーソルに合わせる
        self.rct.center = mouse_xy 

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)


def timeup(scr:Screen):
    """timeup処理をしています"""
    fonts = pg.font.Font(None, 100)
    txt = fonts.render(str("TIME UP!"), True, (255, 0, 0))
    scr.sfc.blit(txt, (250, 350)) 
    pg.display.update()
    while True:
        # ×で終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return 
 
def timer(secs):
    """timer処理、スレッドで行っている。"""
    global TIME
    TIME += 1 # 同期ずれ修正
    for i in range(secs, -1, -1):
        TIME -= 1
        time.sleep(1)
              
def main():
    # スクリーン
    scr = Screen("pygame", (800, 800), "fig/sougenn.jpg")
    # マウスカーソルの非表示
    pg.mouse.set_visible(False)
    # 穴、モグラ作成
    basex = 40; basey = 150     # x/yの起点
    width = 200; height = 130   # x/y軸方向の幅
    xn = 4; yn = 5              # x/yのインスタンスの数
    holes = [[Hole(scr, (basex + x*width, basey + y*height)), Mogura(scr)]
                for x in range(xn) 
                for y in range(yn)]
    # こうかとん
    bird = Bird(scr, "fig/6.png", 1.8, (basex + 50, basey - 10))
    #ハンマー
    hammer = Hammer("fig/piko.png", (100, 100), (400, 400))
    # クロック
    clock = pg.time.Clock()
    # タイマー
    t = Thread(target=timer,args=(TIME,), daemon=True) # daemon=True でメインとともに終了
    t.start()
    while True:
        # 背景作成
        scr.blit()
        # イベント取得
        events = pg.event.get()
        # ×で終了
        for event in events:            
            if event.type == pg.QUIT: return
        # 左上のパラメータ
        fonts = pg.font.Font(None, 40)
        txt = f"score:{Mogura.KILLS}  time:{TIME}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.sfc.blit(txt, (10, 20))
        # hole処理
        for hole in holes:
            hole[0].blit()
            if not hole[1].COOL_TIME:                                                   # Moguraクラスの処理待機カウントが0なら
                # モグラのデータ、set_data = [[img_path, zoom, point],] 
                set_data = [["fig/mogura1.jpg", 0.13, 1], ["fig/mogura2.jpg", 0.13, 3], ["fig/mogura3.jpg", 0.11, 10], 
                            ["fig/can.jpg", 0.25, -1], ["fig/chinsan.jpg", 0.035, randint(-1, 1)*5]]
                idx = np.random.choice(len(set_data), p=[0.65, 0.1, 0.01, 0.18, 0.06])      # set_dataのインデックス設定(ランダム(確率))
                hole[1].update(hole[0], set_data[idx])                                      # Moguraクラスのupdateメソッド呼び出し
                for event in events:
                    if (event.type == pg.MOUSEBUTTONDOWN) and hole[1].check(event.pos):     # ボタンが押され、かつモグラがクリックされた時
                        hole[1].click()                                                         # Moguraクラスのclickメソッド呼び出し
            else:                                                                       # Moguraクラスの処理待機カウントが0以外なら
                hole[1].COOL_TIME -= 1                                                      # 処理待機カウント -1
        # bird(heightは、穴やモグラのy軸方向の幅)
        bird.update(basey, height, yn)
        # マウスカーソルによる更新処理
        for event in events:
            if event.type == pg.MOUSEMOTION:
                hammer.update(pg.mouse.get_pos())
        hammer.blit(scr)
        # timeup処理
        if not TIME:
            timeup(scr)
            return
        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()