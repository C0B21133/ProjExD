import pygame as pg
import sys
from random import randint

class Screen():
    def __init__(self, title, wh, path):
        # titlt: "pygame", wh: (1500, 800), path: "fig/pg_bg.jpg"
        # ウィンドウ
        pg.display.set_caption(title)
        self.scrn_sfc = pg.display.set_mode(wh)
        self.scrn_rct = self.scrn_sfc.get_rect()
        # 背景
        self.back_sfc = pg.image.load(path)
        self.back_rct = self.back_sfc.get_rect()



class Bomb():
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
    scr = Screen("pygame", (1500, 800), "fig/pg_bg.jpg")
    # こうかとん
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    # 爆弾
    bombs = []
    bombs.append(Bomb(scr.scrn_rct))
    clock = pg.time.Clock()
    while True:
        # 背景作成
        scr.scrn_sfc.blit(scr.back_sfc, scr.back_rct)
        # ×で終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        # 爆弾追加処理
        Bomb.COUNT -= 1
        if not Bomb.COUNT:
            bombs.append(Bomb(scr.scrn_rct))
        # 左上のパラメータ
        fonts = pg.font.Font(None, 30)
        txt = f"bombs:{Bomb.BOMB_NUM}  next:{Bomb.COUNT//100}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.scrn_sfc.blit(txt, (10, 10))
        # こうかとんキー処理
        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP] or key_lst[pg.K_w]: 
            tori_rct.move_ip(0, -1)
        elif key_lst[pg.K_DOWN] or key_lst[pg.K_s]: 
            tori_rct.move_ip(0, 1)
        elif key_lst[pg.K_RIGHT] or key_lst[pg.K_d]: 
            tori_rct.move_ip(1, 0)
        elif key_lst[pg.K_LEFT] or key_lst[pg.K_a]: 
            tori_rct.move_ip(-1, 0)
        # こうかとんの壁判定
        yoko, tate = check_bound(tori_rct, scr.scrn_rct)
        if yoko == -1:
            if key_lst[pg.K_LEFT] or key_lst[pg.K_a]: 
                tori_rct.centerx += 1
            if key_lst[pg.K_RIGHT] or key_lst[pg.K_d]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_lst[pg.K_UP] or key_lst[pg.K_w]: 
                tori_rct.centery += 1
            if key_lst[pg.K_DOWN] or key_lst[pg.K_s]:
                tori_rct.centery -= 1  
        scr.scrn_sfc.blit(tori_sfc, tori_rct)
        # 爆弾の移動、衝突時gameover
        for b in bombs:
            b.move(scr.scrn_sfc, scr.scrn_rct)
            if tori_rct.colliderect(b.bomb_rct): 
                if gameover(scr.scrn_sfc): return        
        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()