import pygame as pg
import sys
from random import randint

# def koukaton(x, y, sfc):
#     tori_sfc = pg.image.load("fig/6.png")
#     tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
#     tori_rct = tori_sfc.get_rect()
#     tori_rct.center = x, y
#     sfc.blit(tori_sfc, tori_rct)

class bomb():
    count = 0
    def __init__(self, scrn_rct):
        # カウント初期化
        bomb.count = 2300
        self.vx = 1
        self.vy = 1
        self.bomb_sfc = pg.Surface((20, 20))
        pg.draw.circle(self.bomb_sfc, (255, 0, 0), (10, 10), 10)
        self.bomb_sfc.set_colorkey((0, 0, 0))
        self.bomb_rct = self.bomb_sfc.get_rect()
        self.bomb_rct.centerx = randint(0, scrn_rct.width)
        self.bomb_rct.centery = randint(0, scrn_rct.height) 
    def move(self, scrn_sfc, scrn_rct):      
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
    fonts = pg.font.Font(None, 80)
    txt = fonts.render(str("GAMEOVER"), True, (255, 0, 0))
    scrn_sfc.blit(txt, (620, 350))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return True 


def main():
    pg.display.set_caption("pygame")
    scrn_sfc = pg.display.set_mode((1500, 800))
    scrn_rct = scrn_sfc.get_rect()
    # 背景
    back_sfc = pg.image.load("fig/pg_bg.jpg")
    back_rct = back_sfc.get_rect()
    # こうかとん
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    # 爆弾
    # vx = 1; vy = 1
    # bomb_sfc = pg.Surface((20, 20))
    # pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    # bomb_sfc.set_colorkey((0, 0, 0))
    # bomb_rct = bomb_sfc.get_rect()
    # bomb_rct.centerx = randint(0, scrn_rct.width)
    # bomb_rct.centery = randint(0, scrn_rct.height)
    bombs = []
    bombs.append(bomb(scrn_rct))
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        bomb.count -= 1
        if not bomb.count:
            bombs.append(bomb(scrn_rct))


        # こうかとんキー処理
        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP]: 
            tori_rct.move_ip(0, -1)
        elif key_lst[pg.K_DOWN]: 
            tori_rct.move_ip(0, 1)
        elif key_lst[pg.K_RIGHT]: 
            tori_rct.move_ip(1, 0)
        elif key_lst[pg.K_LEFT]: 
            tori_rct.move_ip(-1, 0)
        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if key_lst[pg.K_LEFT]: 
                tori_rct.centerx += 1
            if key_lst[pg.K_RIGHT]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_lst[pg.K_UP]: 
                tori_rct.centery += 1
            if key_lst[pg.K_DOWN]:
                tori_rct.centery -= 1  

        # yoko, tate = check_bound(bomb_rct, scrn_rct)
        # vx *= yoko
        # vy *= tate        
        # bomb_rct.move_ip(vx, vy)

        scrn_sfc.blit(back_sfc, back_rct)
        scrn_sfc.blit(tori_sfc, tori_rct)
        # scrn_sfc.blit(bomb_sfc, bomb_rct)

        for b in bombs:
            b.move(scrn_sfc, scrn_rct)
            if tori_rct.colliderect(b.bomb_rct): 
                if gameover(scrn_sfc): return        
        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()