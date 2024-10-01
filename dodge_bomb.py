import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP : (0,-5),  #　辞書を定義してまとめる
         pg.K_DOWN : (0,+5),
         pg.K_LEFT : (-5,0),
         pg.K_RIGHT : (+5,0),
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rect:pg.Rect) -> tuple[bool,bool]:  
    """
    引数はこうかとん、または爆弾のrect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内=true 画面外=false
    """
    yoko,tate = True,True
    if obj_rect.left < 0 or WIDTH < obj_rect.right :
        yoko = False
    if obj_rect.top < 0 or HEIGHT < obj_rect.bottom :
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    ok_img = pg.transform.rotozoom(pg.image.load("fig/7.png"),0,0.9)

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  # 初期座標
    ok_rct = ok_img.get_rect()
    ok_rct.center = (WIDTH,HEIGHT/3)


    bb_img = pg.Surface((20,20))
    bb_img.set_colorkey((0,0,0))  # 透過
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)

    go = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(go,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    go.set_alpha(150)
    go_rct = go.get_rect()
  

    vx,vy = +5,+5  # 爆弾の速度
    
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # 貼り付ける

        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾衝突したら
            fonto = pg.font.Font(None,80)
            txt = fonto.render("GameOver",True,(255,255,255))
            screen.blit(go,go_rct)
            screen.blit(txt,[400,300])
            screen.blit(ok_img,[500,250])
            pg.display.update()
            pg.time.wait(5000)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]   # 横、縦座標
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key,tpl in DELTA.items():  
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate :
            vy *= -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
