import pygame
from pygame.locals import *

# pygameの初期化
pygame.init()
# スクリーンの初期化
screen = pygame.display.set_mode((640, 480))
# ウェイトタイマの作成
clock = pygame.time.Clock()
# 画像の読み込み
image = pygame.image.load("test.png")
# x,y座標
x = 0.0
y = 0.0
# ゲームループ
is_end = False
while is_end == False:
    # キーの入力
    input_key_push = pygame.key.get_pressed()
    if input_key_push[K_LEFT] == True:
        x -= 1.0
    if input_key_push[K_RIGHT] == True:
        x += 1.0
    if input_key_push[K_UP] == True:
        y -= 1.0
    if input_key_push[K_DOWN] == True:
        y += 1.0
    # 画面消去
    screen.fill((0, 128, 255))
    # 画像の表示
    screen.blit(image, (x, y))
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
