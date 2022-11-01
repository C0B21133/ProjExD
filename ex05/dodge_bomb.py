import pygame as pg
import sys
from random import randint

key_delta = {
    pg.K_UP:    [0, -1],
    pg.K_DOWN:  [0, +1],
    pg.K_LEFT:  [-1, 0],
    pg.K_RIGHT: [+1, 0],
    pg.K_w:     [0, -1],
    pg.K_s:     [0, +1],
    pg.K_a:     [-1, 0],
    pg.K_d:     [+1, 0]
}

class Screen:
    def __init__(self, title, wh, img_path):
        # titlt: "pygame", wh: (1500, 800), img_path: "fig/pg_bg.jpg"
        # ウィンドウ
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        # 背景
        self.back_sfc = pg.image.load(img_path)
        self.back_rct = self.back_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.back_sfc, self.back_rct)


class Bird:
    def __init__(self, img_path, zoom, xy):
        # img_path: "fig/6.png", zoom: 2.0, xy: (900, 400)
        # こうかとん生成
        sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        # こうかとん位置更新
        key_lst = pg.key.get_pressed()
        for key, delta in key_delta.items():
            if key_lst[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # こうかとんの壁判定
                if check_bound(self.rct, scr.rct) != (1, 1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)


class Bomb:
    """
    基本的に爆弾処理をクラス化したもの
    BOMB_NUMは、爆弾インスタンスの数
    COUNTは、次の爆弾を生成するまでの時間を決めている
    """
    COUNT = 0
    BOMB_NUM = 0

    def __init__(self, scrn_rct):
        # カウント初期化、更新
        Bomb.COUNT = 2000
        Bomb.BOMB_NUM +=1
        # 爆弾生成
        self.vx = 1
        self.vy = 1
        self.sfc = pg.Surface((20, 20))
        pg.draw.circle(self.sfc, (255, 0, 0), (10, 10), 10)
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scrn_rct.width)
        self.rct.centery = randint(0, scrn_rct.height) 

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen): 
        # 爆弾の移動処理     
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate        
        self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)

def check_bound(obj_rct, scr_rct):
    """
    obj_rct: こうかとんor爆弾, scr_rct: スクリーン
    通常時: 0, 異常時:1

    """
    yoko = 1; tate = 1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    elif obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def gameover(scr:Screen):
    """gameover処理をしています"""
    fonts = pg.font.Font(None, 80)
    txt = fonts.render(str("GAMEOVER"), True, (255, 0, 0))
    scr.sfc.blit(txt, (620, 350))
    # こうかとんの画像変えたかった
    # tori_sfc = pg.image.load("fig/8.png")
    # scrn_sfc.blit(tori_sfc, tori_rct)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return 

def main():
    # gameoverフラグ
    FLAG = False
    # スクリーン
    scr = Screen("pygame", (1500, 800), "fig/pg_bg.jpg")
    # こうかとん
    bird = Bird("fig/6.png", 2.0, (900, 400))
    # 爆弾
    bombs = []
    bombs.append(Bomb(scr.rct))
    # クロック
    clock = pg.time.Clock()
    while True:
        # 背景作成
        scr.blit()

        # ×で終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        # 左上のパラメータ
        fonts = pg.font.Font(None, 30)
        txt = f"bombs:{Bomb.BOMB_NUM}  next:{Bomb.COUNT//100}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.sfc.blit(txt, (10, 10))

        # こうかとんキー処理
        bird.update(scr)

        # 爆弾追加処理
        Bomb.COUNT -= 1
        if not Bomb.COUNT:
            bombs.append(Bomb(scr.rct))
        # 爆弾の移動、衝突時gameover
        
        for b in bombs:
            b.update(scr)
            if bird.rct.colliderect(b.rct): 
                FLAG = True
        
        # gameover処理
        if FLAG:
            gameover(scr)
            return

        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()