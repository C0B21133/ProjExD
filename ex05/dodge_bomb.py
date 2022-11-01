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

    def update(self):
        # こうかとん位置更新
        key_lst = pg.key.get_pressed()
        for key, delta in key_delta.items():
            if key_lst[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                if check_bound(self.rct, self.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]



class Bomb:
    """
    基本的に爆弾処理をクラス化したもの
    countは次の爆弾を生成するまでの時間を決めている
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
        self.bomb_sfc = pg.Surface((20, 20))
        pg.draw.circle(self.bomb_sfc, (255, 0, 0), (10, 10), 10)
        self.bomb_sfc.set_colorkey((0, 0, 0))
        self.bomb_rct = self.bomb_sfc.get_rect()
        self.bomb_rct.centerx = randint(0, scrn_rct.width)
        self.bomb_rct.centery = randint(0, scrn_rct.height)

    def move(self, scrn_sfc, scrn_rct): 
        # 爆弾の移動処理     
        yoko, tate = check_bound(self.bomb_rct, scrn_rct)
        self.vx *= yoko
        self.vy *= tate        
        self.bomb_rct.move_ip(self.vx, self.vy)
        scrn_sfc.blit(self.bomb_sfc, self.bomb_rct)

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

def gameover(scrn_sfc):
    """gameover処理をしています"""
    fonts = pg.font.Font(None, 80)
    txt = fonts.render(str("GAMEOVER"), True, (255, 0, 0))
    scrn_sfc.blit(txt, (620, 350))
    # こうかとんの画像変えたかった
    # tori_sfc = pg.image.load("fig/8.png")
    # scrn_sfc.blit(tori_sfc, tori_rct)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return True

def main():
    # スクリーン
    scr = Screen("pygame", (1500, 800), "fig/pg_bg.jpg")
    # こうかとん
    bird = Bird("fig/6.png", 2.0, (900, 400))
    # 爆弾
    bombs = []
    bombs.append(Bomb(scr.rct))
    # タイマー
    clock = pg.time.Clock()
    while True:
        # 背景作成
        scr.sfc.blit(scr.back_sfc, scr.back_rct)
        # ×で終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        # 爆弾追加処理
        Bomb.COUNT -= 1
        if not Bomb.COUNT:
            bombs.append(Bomb(scr.rct))
        # 左上のパラメータ
        fonts = pg.font.Font(None, 30)
        txt = f"bombs:{Bomb.BOMB_NUM}  next:{Bomb.COUNT//100}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.sfc.blit(txt, (10, 10))
        # こうかとんキー処理
        bird.update()
        key_lst = pg.key.get_pressed()
        # for key, delta in key_delta.items():
        #     if key_lst[key]:
        #         bird.rct.centerx += delta[0]
        #         bird.rct.centery += delta[1]
        #         if check_bound(bird.rct, bird.rct) != (+1, +1):
        #             bird.rct.centerx -= delta[0]
        #             bird.rct.centery -= delta[1]
        # こうかとんの壁判定
        yoko, tate = check_bound(bird.rct, scr.rct)
        if yoko == -1:
            if key_lst[pg.K_LEFT] or key_lst[pg.K_a]: 
                bird.rct.centerx += 1
            if key_lst[pg.K_RIGHT] or key_lst[pg.K_d]:
                bird.rct.centerx -= 1
        if tate == -1:
            if key_lst[pg.K_UP] or key_lst[pg.K_w]: 
                bird.rct.centery += 1
            if key_lst[pg.K_DOWN] or key_lst[pg.K_s]:
                bird.rct.centery -= 1  
        scr.sfc.blit(bird.sfc, bird.rct)
        # 爆弾の移動、衝突時gameover
        for b in bombs:
            b.move(scr.sfc, scr.rct)
            if bird.rct.colliderect(b.bomb_rct): 
                if gameover(scr.sfc): return        
        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()