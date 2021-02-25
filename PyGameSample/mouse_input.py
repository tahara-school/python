import pygame
from pygame.locals import *

# pygameの初期化
pygame.init()
# スクリーンの初期化
screen = pygame.display.set_mode((640, 480))
# ウェイトタイマの作成
clock = pygame.time.Clock()
# 画像の読み込み
test0 = pygame.image.load("test0.png")
test1 = pygame.image.load("test1.png")
test2 = pygame.image.load("test2.png")
# ゲームループ
is_end = False
while is_end == False:
    # 画面消去
    screen.fill((0, 128, 255))
    # マウスカーソルの座標を取得
    mouse_position = pygame.mouse.get_pos()
    # マウスのボタンの入力情報を取得
    mouse_button = pygame.mouse.get_pressed()
    if mouse_button[0] == True:
        screen.blit(test0, mouse_position)
    if mouse_button[1] == True:
        screen.blit(test1, mouse_position)
    if mouse_button[2] == True:
        screen.blit(test2, mouse_position)
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
