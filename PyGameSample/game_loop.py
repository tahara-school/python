import pygame
from pygame.locals import *
 
# pygameの初期化
pygame.init()
# スクリーンの初期化
screen = pygame.display.set_mode((640, 480))
# ウェイトタイマの作成
clock = pygame.time.Clock()
# ここにゲームの開始処理を書く


# ゲームループ
is_end = False
while is_end == False:
    # ここにゲームの更新処理を書く


    # 画面消去
    screen.fill((0, 128, 255))
    # ここにゲームの描画処理を書く


    # 画面の更新
    pygame.display.update()
    # タイマウェイト
    clock.tick(60)
    # 終了チェック
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            is_end = True


# pygameの終了
pygame.quit()
