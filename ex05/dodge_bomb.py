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

    def __init__(self, scr:Screen):
        # カウント初期化
        Bomb.COUNT = 500
        # 爆弾生成
        self.vx = 1
        self.vy = 1
        self.sfc = pg.Surface((20, 20))
        pg.draw.circle(self.sfc, (255, 0, 0), (10, 10), 10)
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height) 

    def __del__(self):
        Bomb.BOMB_NUM +=1

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen): 
        # 爆弾の移動処理     
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate        
        self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)

class Attack:
    """
    init, blit, updateは大体他のクラスと同じ処理をする
    flag_on, flag_offは攻撃状態の制御を行う
    """
    FLAG = False    # 攻撃状態か否か
    ATTACK_TIME = 0 # 攻撃時間
    COOL_TIME = 0   # 攻撃クールタイム
    R = 100         # 攻撃エリアの半径
    def __init__(self, scr:Screen, bird:Bird):
        self.sfc = pg.Surface((self.R*2, self.R*2))
        pg.draw.circle(self.sfc, (0, 0, 0), (self.R, self.R), self.R)
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.update(scr, bird)

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen, bird:Bird):
        if Attack.COOL_TIME:
            Attack.COOL_TIME -= 1   # クールタイムがある場合0になるまでCOOL_TIMEを減らす
        self.rct.center = bird.rct.center
        self.blit(scr)

    def flag_on(self, scr:Screen, bird:Bird):
        Attack.FLAG = True          # 攻撃状態に設定
        Attack.ATTACK_TIME = 1000   # 攻撃時間の設定
        pg.draw.circle(self.sfc, (30, 144, 255), (self.R, self.R), self.R)
        self.update(scr, bird)
    
    def flag_off(self, scr:Screen, bird:Bird):
        Attack.FLAG = False         # 通常状態に設定
        Attack.COOL_TIME = 1500     # 攻撃クールタイムを設定
        pg.draw.circle(self.sfc, (0, 0, 0), (self.R, self.R), self.R)
        self.update(scr, bird)

# 爆発処理(時間なくてできませんでした)
# class explosion:
#     def __init__(self, img_path, zoom, xy, scr:Screen):
#         sfc = pg.image.load(img_path)
#         self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
#         self.rct = self.sfc.get_rect()
#         self.rct.center = xy
#         scr.sfc.blit(self.sfc, self.rct)

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
    attack = Attack(scr, bird)
    # 爆弾
    bombs = []
    bombs.append(Bomb(scr))
    # クロック
    clock = pg.time.Clock()
    while True:
        # 背景作成
        scr.blit()
        attack.blit(scr)
        # ×で終了
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        # 左上のパラメータ
        fonts = pg.font.Font(None, 30)
        txt = f"killed:{Bomb.BOMB_NUM}  "
        if Attack.ATTACK_TIME:
            txt += f"attack_time:{Attack.ATTACK_TIME//100}"
        if Attack.COOL_TIME:
            txt += f"cool_time:{Attack.COOL_TIME//100}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.sfc.blit(txt, (10, 10))

        #　こうかとん攻撃
        key_lst = pg.key.get_pressed()
        if Attack.FLAG:                     # 攻撃状態なら
            Attack.ATTACK_TIME -= 1         # 攻撃時間を1減らす
            if Attack.ATTACK_TIME == 0:     # 攻撃時間がなくなったら
                attack.flag_off(scr, bird)
        elif key_lst[pg.K_SPACE] and (not Attack.COOL_TIME): # spaceキーが押され、かつクールタイムがない時
            attack.flag_on(scr, bird)
        attack.update(scr, bird)

        # こうかとんキー処理
        bird.update(scr)
        # 爆弾追加処理
        Bomb.COUNT -= 1
        if not Bomb.COUNT:
             bombs.append(Bomb(scr))
        # 爆弾の移動
        for i, b in enumerate(bombs):
            b.update(scr)
            if attack.rct.colliderect(b.rct) and attack.FLAG:
                # attackと接触
                del_bomb = bombs.pop(i)
                del del_bomb
            if bird.rct.colliderect(b.rct): 
                # こうかとんと接触
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