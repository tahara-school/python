import pygame
from pygame.locals import *
import random
from enum import Enum
import math

# 2Dベクトル
class Vec:
    # コンストラクタ
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    # 指定角度の単位ベクトルを求める
    @staticmethod
    def from_angle(degree):
        rad = math.radians(degree)
        return Vec(math.cos(rad), math.sin(rad))
    # 内積
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    # 長さ
    def length(self):
        return math.sqrt(self.dot(self))
    # 距離
    def distance(self, other):
        return (self - other).length()
    # 正規化
    def normalized(self):
        result = Vec(self.x, self.y)
        len = result.length()
        return (result / len) if (len != 0.0) else result
    # タプル化
    def to_tuple(self):
        return (self.x, self.y)
    # 逆ベクトル
    def __neg__(self):
        return Vec(-self.x, -self.y)
    # 加算
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    # 減算
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    # 乗算
    def __mul__(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)
    # 除算
    def __truediv__(self, scalar):
        return Vec(self.x / scalar, self.y / scalar)
    # 加算
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    # 減算
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    # 乗算
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
    # 除算
    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self
    # 文字列化
    def __str__(self):
        return '(%s %s)' % (self.x, self.y)

# 入力取得クラス
class Input:
    def __init__(self):
        self.__is_hold_mouse_left_pre = False
        self.__is_hold_mouse_left_cur = False

    def update(self):
        # 前フレームのマウス押下情報を保持
        self.__is_hold_mouse_left_pre = self.__is_hold_mouse_left_cur
        # 今フレームのマウス押下情報を取得
        mouse_button = pygame.mouse.get_pressed()
        self.__is_hold_mouse_left_cur = mouse_button[0]

    @property
    def mouse_position(self):
        # マウス座標を取得
        raw_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = Vec(raw_mouse_pos[0], raw_mouse_pos[1])
        return mouse_pos

    @property
    def is_pressed_mouse_left(self):
        return (self.__is_hold_mouse_left_cur) and (not self.__is_hold_mouse_left_pre)

# マス目の状態
class GridState(Enum):
    Empty = 0
    Maru = 1
    Batsu = 2

# ゲームの状態
class GameState(Enum):
    MaruTurn = 0
    BatsuTurn = 1
    MaruWin = 2
    BatsuWin = 3
    Hikiwake = 4

class Marubatsu:
    # コンストラクタ
    def __init__(self):
        # マス目の開始位置(左上の座標)
        self.board_origin = Vec(100, 100)
        # マスの大きさ(ピクセル数)
        self.grid_size = 64
        # 盤面の大きさ（マスの数）
        self.board_size = 3
        # 盤面
        self.board = [[GridState.Empty for _ in range(self.board_size)] for _ in range(self.board_size)]
        # 置いた数(引き分け判定用)
        self.count = 0
        # 現在の状況
        self.state = GameState.MaruTurn

    # ゲームの実行
    def run(self):
        # pygameの初期化
        pygame.init()
        # スクリーンの初期化
        self.screen = pygame.display.set_mode((800, 600))
        # ウェイトタイマの作成
        clock = pygame.time.Clock()
        # 入力クラスの初期化
        self.input = Input()
        # 開始
        self.start()
        # ゲームループ
        is_end = False
        while is_end == False:
            # 更新
            self.update(1.0)
            # 画面消去
            self.screen.fill((0, 128, 255))
            # 描画
            self.draw()
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

    # リソースの読み込み
    def load_content(self):
        self.texture_grid = pygame.image.load("assets/grid.png")
        self.texture_maru = pygame.image.load("assets/maru.png")
        self.texture_batsu = pygame.image.load("assets/batsu.png")
        self.texture_nobandesu = pygame.image.load("assets/nobandesu.png")
        self.texture_nokachidesu = pygame.image.load("assets/nokachidesu.png")
        self.texture_hikiwake = pygame.image.load("assets/hikiwake.png")

    # 開始
    def start(self):
        # リソースの読み込み
        self.load_content()

    # 更新
    def update(self, game_time):
        # 入力情報の更新
        self.input.update()

        if self.input.is_pressed_mouse_left:
            self.on_click()

    # 描画
    def draw(self):
        # まるの番なら
        if self.state == GameState.MaruTurn:
            # ○の番です と表示
            self.screen.blit(self.texture_maru, (0, 0))
            self.screen.blit(self.texture_nobandesu, (64, 0))
        # ばつの番なら
        elif self.state == GameState.BatsuTurn:
            # ×の番です と表示
            self.screen.blit(self.texture_batsu, (0, 0))
            self.screen.blit(self.texture_nobandesu, (64, 0))
        # まるの勝ちなら
        elif self.state == GameState.MaruWin:
            # ○の勝ちです と表示
            self.screen.blit(self.texture_maru, (0, 0))
            self.screen.blit(self.texture_nokachidesu, (64, 0))
        # ばつの勝ちなら
        elif self.state == GameState.BatsuWin:
            # ×の勝ちです と表示
            self.screen.blit(self.texture_batsu, (0, 0))
            self.screen.blit(self.texture_nokachidesu, (64, 0))
        # 引き分けなら
        elif self.state == GameState.Hikiwake:
            # 引き分け！ と表示
            self.screen.blit(self.texture_hikiwake, (0, 0))

        # 盤面の描画
        # マスを左上から右へ右へと描画し、一行終わったら、
        # 一つ下がってまた左から右へ右へと描画…
        for y in range(self.board_size):
            for x in range(self.board_size):
                pos = Vec(self.grid_size * x, self.grid_size * y) + self.board_origin
                self.screen.blit(self.texture_grid, pos.to_tuple())

        # 盤面に置かれた記号の描画
        for y in range(self.board_size):
            for x in range(self.board_size):
                data = self.board[y][x]
                pos = Vec(self.grid_size * x, self.grid_size * y) + self.board_origin
                # まるを描画
                if (data == GridState.Maru):
                    self.screen.blit(self.texture_maru, pos.to_tuple())
                # ばつを描画
                elif (data == GridState.Batsu):
                    self.screen.blit(self.texture_batsu, pos.to_tuple())

    # クリック時処理
    def on_click(self):
        # マルの番でもバツの番でもないときは何もしない
        if self.state != GameState.MaruTurn and self.state != GameState.BatsuTurn:
            return

        # マウスカーソルの座標を取得
        mouse_pos = self.input.mouse_position

        # マウス座標が盤面に収まっていない場合は何もしない
        if not self.pos_is_in_range(mouse_pos):
            return

        # マウス座標をマス目番号に変換
        x, y = self.to_board_pos(mouse_pos)
        if self.board[y][x] != GridState.Empty:
            return

        # クリックされたマスに記号を置く
        if self.state == GameState.MaruTurn:
            self.board[y][x] = GridState.Maru
        if self.state == GameState.BatsuTurn:
            self.board[y][x] = GridState.Batsu
        self.count += 1

        # もし揃ったら
        if self.is_matching():
            if self.state == GameState.MaruTurn:
                self.state = GameState.MaruWin;
            else:
                self.state = GameState.BatsuWin;
        # 全てのマスが埋まったら引き分け
        elif self.count == (self.board_size * self.board_size):
            self.state = GameState.Hikiwake
        # 相手の番へ
        else:
            if self.state == GameState.MaruTurn:
                self.state = GameState.BatsuTurn
            else:
                self.state = GameState.MaruTurn

    # 画面座標が盤面に収まっているか
    def pos_is_in_range(self, pos):
        is_left_over = pos.x < self.board_origin.x
        if is_left_over: return False
        
        is_right_over = pos.x >= self.board_origin.x + self.grid_size * self.board_size
        if is_right_over: return False
        
        is_up_over = pos.y < self.board_origin.y
        if is_up_over: return False
        
        is_down_over = pos.y >= self.board_origin.y + self.grid_size * self.board_size
        if is_down_over: return False

        return True

    # 盤面座標が盤面に収まっているか
    def grid_pos_is_in_range(self, x, y):
        return (0 <= y < len(self.board)) and (0 <= x < len(self.board[y])) 

    # 画面上の座標から盤面上の座標に変換
    def to_board_pos(self, pos):
        x = int((pos.x - self.board_origin.x) / self.grid_size)
        y = int((pos.y - self.board_origin.y) / self.grid_size)
        return (x, y)

    # マークの数をカウント
    def count_mark(self, mark, x, y, vx, vy):
        result = 0
        while self.grid_pos_is_in_range(x, y) and self.board[y][x] == mark:
            result += 1
            x += vx
            y += vy
        return result

    # 揃ったか？ 揃ってたらtrue, 揃ってなければfalseを返却する
    def is_matching(self):
        for y, row in enumerate(self.board):
            for x, mark in enumerate(row):
                if mark == GridState.Empty:
                    continue
                for vx, vy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                    if self.count_mark(mark, x, y, vx, vy) == 3:
                        return True
        return False

Marubatsu().run()