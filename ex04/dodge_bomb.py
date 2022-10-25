import pygame as pg
import sys

# def koukaton(x, y, sfc):
#     tori_sfc = pg.image.load("fig/6.png")
#     tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
#     tori_rct = tori_sfc.get_rect()
#     tori_rct.center = x, y
#     sfc.blit(tori_sfc, tori_rct)


def main():
    pg.display.set_caption("pygame")
    scrn_sfc = pg.display.set_mode((1000, 600))
    # 背景
    back_sfc = pg.image.load("fig/pg_bg.jpg")
    back_rct = back_sfc.get_rect()
    # こうかとん
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        scrn_sfc.blit(back_sfc, back_rct)
        scrn_sfc.blit(tori_sfc, tori_rct)

        key_lst = pg.key.get_pressed()
        if key_lst[pg.K_UP]: 
            tori_rct.move_ip(0, -10)
        elif key_lst[pg.K_DOWN]: 
            tori_rct.move_ip(0, 10)
        elif key_lst[pg.K_RIGHT]: 
            tori_rct.move_ip(10, 0)
        elif key_lst[pg.K_LEFT]: 
            tori_rct.move_ip(-10, 0)

        clock = pg.time.Clock()
        clock.tick(1000)
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()