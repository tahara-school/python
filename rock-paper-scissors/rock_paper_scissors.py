import pygame
from pygame.locals import *
import random
from enum import Enum

# 手の種別
class Te(Enum):
    GU = 0
    CHOKI = 1
    PA = 2

# 整数から手列挙型へ変換
def convert_number_to_te(n):
    if n == 0: return Te.GU
    if n == 1: return Te.CHOKI
    if n == 2: return Te.PA

# ランダムな手を取得
def get_random_te():
    return convert_number_to_te(random.randrange(3))

# 入力クラス
class Input:
    def __init__(self):
        self.__input_key_push = None
    def update(self):
        self.__input_key_push = pygame.key.get_pressed()
    @property
    def pressed_te(self):
        if self.__input_key_push[pygame.K_1]:
            return Te.GU
        elif self.__input_key_push[pygame.K_2]:
            return Te.CHOKI
        elif self.__input_key_push[pygame.K_3]:
            return Te.PA
        else:
            return None
    @property
    def is_pressed_retry(self):
        return self.__input_key_push[pygame.K_SPACE]

# ジャンケンゲーム
class Janken:
    # ゲームの状態種別
    class State(Enum):    
        READY = 0      # じゃんけん前
        RESULT = 1      # じゃんけん後

    # 勝敗種別
    class Result(Enum):    
        WIN = 0
        LOSE = 1
        AIKO = 2

    # コンストラクタ
    def __init__(self):
        # ゲームの経過時間
        self.game_total_time = 0.0
        # 現在のゲームの状態
        self.state = Janken.State.READY
        # 勝敗を格納するための変数
        self.result = None
        # 自分の手。1:グー, 2:チョキ, 3:パー
        self.jibun = None
        # 相手の手
        self.aite = None
        # 手を決めるまでの、高速で切り替わる相手の手
        self.waiting_hand = Te.GU
        # 切り替わる手の間隔
        self.interval = 5.0
        # 入力取得
        self.input = Input()

    # ゲームの実行
    def run(self):
        # pygameの初期化
        pygame.init()
        # スクリーンの初期化
        self.screen = pygame.display.set_mode((800, 600))
        # ウェイトタイマの作成
        clock = pygame.time.Clock()
        # 開始
        self.start()
        # ゲームループ
        is_end = False
        while is_end == False:
            game_time = 1.0
            self.game_total_time += game_time
            # 更新
            self.update(game_time)
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
        self.texture_anata = pygame.image.load("Assets/anata.png")          # 「あなた」
        self.texture_aite = pygame.image.load("Assets/aite.png")            # 「あいて」
        self.texture_setsumei = pygame.image.load("Assets/setsumei.png")    # 操作説明
        self.texture_gu = pygame.image.load("Assets/janken_gu.png")         # グーの画像
        self.texture_choki = pygame.image.load("Assets/janken_choki.png")   # チョキの画像
        self.texture_pa = pygame.image.load("Assets/janken_pa.png")         # パーの画像
        self.texture_kachi = pygame.image.load("Assets/kachi.png")          # 「勝ち！」
        self.texture_make = pygame.image.load("Assets/make.png")            # 「負け...
        self.texture_aiko = pygame.image.load("Assets/aiko.png")            # 「あいこ」

    # 開始
    def start(self):
        # リソースの読み込み
        self.load_content()
 
    # 更新
    def update(self, game_time):
        # 入力更新
        self.input.update()
        # じゃんけん前
        if self.state == Janken.State.READY:
            self.jibun = self.input.pressed_te
            # ボタンが押されたか？
            if self.jibun != None:
                # 相手の手を決める
                self.aite = get_random_te()
                # 結果を確認
                self.result = self.check_result_of_game(self.jibun, self.aite)
                self.state = Janken.State.RESULT
            else:
                # 手が選ばれるまで
                # 一定間隔毎に手を変えて選んでる演出
                tn = round(self.game_total_time / self.interval) % 3
                self.waiting_hand = convert_number_to_te(tn)
        # じゃんけん後
        elif self.state == Janken.State.RESULT:
            if self.input.is_pressed_retry:
                # じゃんけん前へ戻る
                self.state = Janken.State.READY
                self.result = None

    # 描画
    def draw(self):
        #「あいて」の描画
        self.screen.blit(self.texture_aite, (20, 20))
        # 「あなた」の描画
        self.screen.blit(self.texture_anata, (20, 210))

        # 相手の手の描画
        aite_te_position = (330, 20)

        # じゃんけん前の描画処理
        if self.state == Janken.State.READY:
            # 操作説明の描画
            self.screen.blit(self.texture_setsumei, (330, 160))
            # 選択中の相手の手の描画
            self.screen.blit(self.get_te_texture(self.waiting_hand), aite_te_position)
        # じゃんけん後の描画処理
        elif self.state == Janken.State.RESULT:
            # あいての手の描画
            self.screen.blit(self.get_te_texture(self.aite), aite_te_position)
            # 自分の手の描画
            self.screen.blit(self.get_te_texture(self.jibun), (330, 210))
            # 結果の描画
            self.screen.blit(self.get_result_texture(self.result), (480, 210))

    # 手の番号をテクスチャに変換
    def get_te_texture(self, te):
        if te == Te.GU: return self.texture_gu
        if te == Te.CHOKI: return self.texture_choki
        if te == Te.PA: return self.texture_pa

    # 結果をテクスチャに変換
    def get_result_texture(self, result):
        if result == Janken.Result.WIN: return self.texture_kachi
        if result == Janken.Result.LOSE: return self.texture_make
        if result == Janken.Result.AIKO: return self.texture_aiko

    # ゲームの結果を確認
    def check_result_of_game(self, jibun, aite):
        # 手が選ばれていない
        if jibun == None or aite == None:
            return None
        # 勝敗を判定する
        if jibun == aite:
            # あいこ
            return Janken.Result.AIKO
        # 1行の式を複数行に分ける場合は\でつなげる(日本語フォントだと半角の￥マーク）
        elif (jibun == Te.GU and aite == Te.CHOKI) or (jibun == Te.CHOKI and aite == Te.PA) or (jibun == Te.PA and aite == Te.GU):
            # 勝ち
            return Janken.Result.WIN
        else:
            # 負け
            return Janken.Result.LOSE

# じゃんけんゲームの実行
Janken().run()