import pyxel
import random
import math

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

class Ball:
    def __init__(self, app):
        self.app = app  # Appクラスのインスタンスを保持
        self.x = pyxel.width // 2
        self.y = pyxel.height - 20
        self.radius = 8
        self.color = 9
        self.is_dragging = False
        self.drag_start = (0, 0)
        self.velocity = (0, 0)
        self.is_moving = False

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.is_dragging = True
        else:
            if self.is_dragging:
                # マウスドラッグ中で左ボタンが離れたときに速度を設定
                self.velocity = (
                    (self.drag_start[0] - pyxel.mouse_x) / 10,
                    (self.drag_start[1] - pyxel.mouse_y) / 10,
                )
                self.is_moving = True
            self.is_dragging = False

        if self.is_dragging:
            # マウスドラッグ中はボールの位置を更新
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            self.drag_start = (mx, my)
            self.x = mx
            self.y = my
        else:
            # ボールが飛んでいるときは位置を更新
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            # 画面端で跳ね返る処理
            if self.x - self.radius < 0 or self.x + self.radius > pyxel.width:
                self.velocity = (-0.9 * self.velocity[0], self.velocity[1])
                # 速度の大きさが一定以下の場合は速度をゼロに設定

                if abs(self.velocity[0]) < 0.3:
                    self.velocity = (0, self.velocity[1])
                else:
                    self.velocity = (0.9 * abs(self.velocity[0]), self.velocity[1])
    

            if self.y - self.radius < 0 or self.y + self.radius > pyxel.height:
                self.velocity = (self.velocity[0], -0.9 * self.velocity[1])
                # 速度の大きさが一定以下の場合は速度をゼロに設定
                if abs(self.velocity[1]) < 0.3:
                    self.velocity = (self.velocity[0], 0)
                else:
                    self.velocity = (self.velocity[0], 0.9 * abs(self.velocity[1]))

            # ボールが的に当たったかどうかの判定
            for target in self.app.targets:
                if (
                    (self.x - target.x) ** 2 + (self.y - target.y) ** 2
                    < (self.radius + target.radius) ** 2
                ):
                    # 的に当たったら速度を減衰させる
                    self.velocity = (
                        0.9 * self.velocity[0],
                        0.9 * self.velocity[1],
                    )
                    # ボールが的に当たったらスコアを増やす
                    self.app.score += 10

            # 速度が一定以下の場合は速度をゼロに設定
            if abs(self.velocity[0]) < 0.3:
                self.velocity = (0, self.velocity[1])
            if abs(self.velocity[1]) < 0.3:
                self.velocity = (self.velocity[0], 0)

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.color = 0

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.radius, self.color)

class App:
    def __init__(self):
        pyxel.init(200, 300, fps=100)  # 画面サイズ、フレームレート

        self.scene = SCENE_TITLE
        self.score = 0
        self.game_over_count = 0  # ボールが動いていないフレーム数をカウントする変数

        pyxel.load("test.pyxres")

        self.ball = Ball(self)  # AppクラスのインスタンスをBallクラスに渡す
        self.targets = [Target(40, 40), Target(120, 80), Target(80, 100),Target(160,130),Target(30,130),Target(170,30),Target(50,80),Target(50,10),Target(160,60),Target(150,130)]

        pyxel.run(self.update, self.draw)  # 実行開始

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            if pyxel.btnp(13):
                    self.scene = SCENE_PLAY
                    self.score = 0

            self.ball.update()
            for target in self.targets:
                if (
                    (self.ball.x - target.x) ** 2 + (self.ball.y - target.y) ** 2
                    < (self.ball.radius + target.radius) ** 2
                ):
                    target.x = random.randint(20, 300)  # ランダムで繰り返す
                    target.y = random.randint(20, 220)  # ランダムで繰り返す
                    self.score += 10

            # ボールが動いていない場合、game_over_count をインクリメント
            if not self.ball.is_moving:
                self.game_over_count += 1

            # ボールが一定のフレーム数以上動いていない場合、ゲームオーバー
            if self.game_over_count > 300:  # 60フレーム（1秒）以上動いていない場合
                self.scene = SCENE_GAMEOVER
                self.score = 0                         

    def update_title_scene(self):
        if pyxel.btnp(13):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if pyxel.btnp(13):
            self.scene = SCENE_GAMEOVER

        self.ball.update()

        for target in self.targets:
            if (
                (self.ball.x - target.x) ** 2 + (self.ball.y - target.y) ** 2
                < (self.ball.radius + target.radius) ** 2
            ):
                target.x = random.randint(20, 300)  # ランダムで繰り返す
                target.y = random.randint(20, 220)  # ランダムで繰り返す

        # ボールが動いていない場合、game_over_count をインクリメント
        if not self.ball.is_moving:
            self.game_over_count += 1

        # ボールが一定のフレーム数以上動いていない場合、ゲームオーバー
        if self.game_over_count > 300:  # 60フレーム（1秒）以上動いていない場合
            self.scene = SCENE_GAMEOVER
            self.score = 0

    def draw(self):
        # クリアする際に使用する色を指定
        background_color = 11  # 例として1を指定
        # 画面をクリアして背景色を変更
        pyxel.cls(background_color)  # 背景色

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(39, 4, "SCORE {:5}".format(self.score), 7)

    def draw_title_scene(self):
        pyxel.text(69, 200, "SFCmonster", pyxel.frame_count % 30)
        pyxel.text(60, 126, "- PRESS ENTER -", 13)
        pyxel.text(20,30,"bu-bu-smellkun",40)
        pyxel.text(40,90,"kentucky fried chicken",50)
        pyxel.text(110,70,"basuretutyo-da",60)
        pyxel.text(110,150,"risyuukikannsugisaru",20)
        pyxel.text(20,100,"kamo",30)

        # target
        specific_target0 = self.targets[0]
        pyxel.blt(specific_target0.x, specific_target0.y, 0, 0, 0, 17, 12, 0)
        specific_target1 = self.targets[1]
        pyxel.blt(specific_target1.x, specific_target1.y, 0, 1, 16, 15, 20, 0)
        specific_target2 = self.targets[2]
        pyxel.blt(specific_target2.x, specific_target2.y, 0, 0, 40, 17, 20, 0)
        specific_target3 = self.targets[3]
        pyxel.blt(specific_target3.x, specific_target3.y, 0, 0, 64, 19, 14, 0)
        specific_target4 = self.targets[4]
        pyxel.blt(specific_target4.x, specific_target4.y, 0, 0, 88, 14, 14, 0)
        specific_target5 = self.targets[5]
        pyxel.blt(specific_target5.x, specific_target5.y, 0, 24, 0, 17, 14, 0)
        specific_target6 = self.targets[6]
        pyxel.blt(specific_target6.x, specific_target6.y, 0, 48, 0, 17, 14, 0)
        specific_target7 = self.targets[7]
        pyxel.blt(specific_target7.x, specific_target7.y, 0, 24, 16, 17, 14, 0)
        specific_target8 = self.targets[8]
        pyxel.blt(specific_target8.x, specific_target8.y, 0, 24, 40, 17, 14, 0)
        specific_target9 = self.targets[9]
        pyxel.blt(specific_target9.x, specific_target9.y, 0, 24, 64, 17, 14, 0)


    def draw_play_scene(self):
        self.ball.draw()

        # target
        specific_target0 = self.targets[0]
        pyxel.blt(specific_target0.x, specific_target0.y, 0, 0, 0, 17, 12, 0)
        specific_target1 = self.targets[1]
        pyxel.blt(specific_target1.x, specific_target1.y, 0, 1, 16, 15, 20, 0)
        specific_target2 = self.targets[2]
        pyxel.blt(specific_target2.x, specific_target2.y, 0, 0, 40, 17, 20, 0)
        specific_target3 = self.targets[3]
        pyxel.blt(specific_target3.x, specific_target3.y, 0, 0, 64, 19, 14, 0)
        specific_target4 = self.targets[4]
        pyxel.blt(specific_target4.x, specific_target4.y, 0, 0, 88, 14, 14, 0)
        specific_target5 = self.targets[5]
        pyxel.blt(specific_target5.x, specific_target5.y, 0, 24, 0, 17, 14, 0)
        specific_target6 = self.targets[6]
        pyxel.blt(specific_target6.x, specific_target6.y, 0, 48, 0, 17, 14, 0)
        specific_target7 = self.targets[7]
        pyxel.blt(specific_target7.x, specific_target7.y, 0, 24, 16, 17, 14, 0)
        specific_target8 = self.targets[8]
        pyxel.blt(specific_target8.x, specific_target8.y, 0, 24, 40, 17, 14, 0)
        specific_target9 = self.targets[9]
        pyxel.blt(specific_target9.x, specific_target9.y, 0, 24, 64, 17, 14, 0)



        for target in self.targets:
            target.draw()

        if self.ball.is_dragging:
            pyxel.line(
                self.ball.x, self.ball.y, pyxel.mouse_x, pyxel.mouse_y, pyxel.COLOR_WHITE
            )

    def draw_gameover_scene(self):
        pyxel.text(60, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

        # target
        specific_target0 = self.targets[0]
        pyxel.blt(specific_target0.x, specific_target0.y, 0, 0, 0, 17, 12, 0)
        specific_target1 = self.targets[1]
        pyxel.blt(specific_target1.x, specific_target1.y, 0, 1, 16, 15, 20, 0)
        specific_target2 = self.targets[2]
        pyxel.blt(specific_target2.x, specific_target2.y, 0, 0, 40, 17, 20, 0)
        specific_target3 = self.targets[3]
        pyxel.blt(specific_target3.x, specific_target3.y, 0, 0, 64, 19, 14, 0)
        specific_target4 = self.targets[4]
        pyxel.blt(specific_target4.x, specific_target4.y, 0, 0, 88, 14, 14, 0)
        specific_target5 = self.targets[5]
        pyxel.blt(specific_target5.x, specific_target5.y, 0, 24, 12, 14, 14, 0)
        specific_target6 = self.targets[6]
        pyxel.blt(specific_target6.x, specific_target6.y, 0, 48, 0, 17, 14, 0)
        specific_target7 = self.targets[7]
        pyxel.blt(specific_target7.x, specific_target7.y, 0, 24, 16, 17, 14, 0)
        specific_target8 = self.targets[8]
        pyxel.blt(specific_target8.x, specific_target8.y, 0, 24, 40, 17, 14, 0)
        specific_target9 = self.targets[9]
        pyxel.blt(specific_target9.x, specific_target9.y, 0, 24, 64, 17, 14, 0)


app = App()
