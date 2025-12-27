import tkinter as tk
import random
import time
import os

# ======================
# 遊戲基本設定
# ======================
WINDOW_SIZE = 500      # 視窗大小
GRID_SIZE = 20         # 每一格的大小
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# 不同難度對應的速度（毫秒，越小越快）
DIFFICULTY_SPEED = {
    "簡單": 200,
    "普通": 120,
    "困難": 80
}

HIGH_SCORE_FILE = "highscore.txt"


# ======================
# 讀取最高分
# ======================
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            return int(f.read())
    return 0


# ======================
# 儲存最高分
# ======================
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
        f.write(str(score))


# ======================
# 貪食蛇遊戲類別
# ======================
class SnakeGame:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("貪食蛇遊戲")

        # 遊戲狀態
        self.speed = DIFFICULTY_SPEED[difficulty]
        self.score = 0
        self.high_score = load_high_score()
        self.start_time = time.time()
        self.game_running = True

        # 蛇的初始位置（座標）
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"

        # 產生食物
        self.food = self.create_food()

        # ======================
        # 建立畫布
        # ======================
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
            bg="black"
        )
        self.canvas.pack()

        # ⭐⭐⭐ 關鍵：強制鍵盤焦點 ⭐⭐⭐
        self.root.focus_force()
        self.canvas.focus_set()

        # 資訊顯示標籤
        self.info_label = tk.Label(
            self.root,
            font=("微軟正黑體", 12)
        )
        self.info_label.pack(pady=5)

        # 綁定方向鍵
        self.canvas.bind("<Up>", lambda e: self.change_direction("Up"))
        self.canvas.bind("<Down>", lambda e: self.change_direction("Down"))
        self.canvas.bind("<Left>", lambda e: self.change_direction("Left"))
        self.canvas.bind("<Right>", lambda e: self.change_direction("Right"))

        # 開始遊戲迴圈
        self.update_game()

    # ======================
    # 隨機產生食物
    # ======================
    def create_food(self):
        while True:
            pos = (
                random.randint(0, GRID_COUNT - 1),
                random.randint(0, GRID_COUNT - 1)
            )
            if pos not in self.snake:
                return pos

    # ======================
    # 改變移動方向（防止反向）
    # ======================
    def change_direction(self, new_direction):
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    # ======================
    # 遊戲主更新迴圈
    # ======================
    def update_game(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[0]

        # 根據方向計算新頭部位置
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)

        # 撞牆或撞到自己 → 遊戲結束
        if (
            head_x < 0 or head_x >= GRID_COUNT or
            head_y < 0 or head_y >= GRID_COUNT or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # 吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.draw()

        # 下一次更新
        self.root.after(self.speed, self.update_game)

    # ======================
    # 繪製畫面
    # ======================
    def draw(self):
        self.canvas.delete("all")

        # 畫蛇
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * GRID_SIZE,
                y * GRID_SIZE,
                (x + 1) * GRID_SIZE,
                (y + 1) * GRID_SIZE,
                fill="lime"
            )

        # 畫食物
        fx, fy = self.food
        self.canvas.create_oval(
            fx * GRID_SIZE,
            fy * GRID_SIZE,
            (fx + 1) * GRID_SIZE,
            (fy + 1) * GRID_SIZE,
            fill="red"
        )

        # 更新時間
        elapsed = int(time.time() - self.start_time)

        # 更新資訊文字
        self.info_label.config(
            text=f"分數：{self.score} ｜ 最高分：{self.high_score} ｜ 時間：{elapsed} 秒"
        )

    # ======================
    # 遊戲結束
    # ======================
    def game_over(self):
        self.game_running = False

        if self.score > self.high_score:
            save_high_score(self.score)

        self.canvas.create_text(
            WINDOW_SIZE // 2,
            WINDOW_SIZE // 2,
            text="遊戲結束\n請關閉視窗",
            fill="white",
            font=("微軟正黑體", 24),
            justify="center"
        )


# ======================
# 主選單畫面
# ======================
def start_menu():
    root = tk.Tk()
    root.title("貪食蛇 - 選擇難度")

    tk.Label(
        root,
        text="貪食蛇遊戲",
        font=("微軟正黑體", 20)
    ).pack(pady=10)

    def start_game(difficulty):
        # 清除選單畫面
        for widget in root.winfo_children():
            widget.destroy()

        # 啟動遊戲
        SnakeGame(root, difficulty)

    # 建立難度按鈕
    for diff in DIFFICULTY_SPEED:
        tk.Button(
            root,
            text=diff,
            font=("微軟正黑體", 14),
            width=15,
            command=lambda d=diff: start_game(d)
        ).pack(pady=5)

    root.mainloop()


# ======================
# 程式進入點
# ======================
if __name__ == "__main__":
    start_menu()s
