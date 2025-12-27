import tkinter as tk
import random

# =====================
# 基本設定
# =====================
CELL = 20          # 每格大小
WIDTH = 20         # 寬度格數
HEIGHT = 20        # 高度格數
DELAY = 200        # 移動速度（毫秒）

# =====================
# 建立視窗
# =====================
root = tk.Tk()
root.title("貪食蛇（全新版本）")
root.geometry("420x460")
root.resizable(False, False)

# =====================
# 分數顯示
# =====================
score = 0
score_label = tk.Label(root, text="分數：0", font=("Arial", 14))
score_label.pack()

# =====================
# 畫布
# =====================
canvas = tk.Canvas(
    root,
    width=WIDTH * CELL,
    height=HEIGHT * CELL,
    bg="white"
)
canvas.pack()

# =====================
# 遊戲資料
# =====================
snake = [(10, 10), (9, 10), (8, 10)]
direction = "Right"
food = (5, 5)
game_over = False

# =====================
# 重新開始
# =====================
def restart():
    global snake, direction, food, score, game_over

    snake = [(10, 10), (9, 10), (8, 10)]
    direction = "Right"
    food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    score = 0
    game_over = False
    score_label.config(text="分數：0")
    draw()
    move()

# =====================
# 畫圖
# =====================
def draw():
    canvas.delete("all")

    # 畫蛇
    for x, y in snake:
        canvas.create_rectangle(
            x*CELL, y*CELL,
            (x+1)*CELL, (y+1)*CELL,
            fill="green"
        )

    # 畫食物
    fx, fy = food
    canvas.create_oval(
        fx*CELL, fy*CELL,
        (fx+1)*CELL, (fy+1)*CELL,
        fill="red"
    )

# =====================
# 鍵盤控制
# =====================
def key(event):
    global direction
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        direction = event.keysym

# =====================
# 蛇移動
# =====================
def move():
    global food, score, game_over

    if game_over:
        return

    x, y = snake[0]

    if direction == "Up":
        new = (x, y-1)
    elif direction == "Down":
        new = (x, y+1)
    elif direction == "Left":
        new = (x-1, y)
    else:
        new = (x+1, y)

    # 撞牆或撞自己
    if (
        new[0] < 0 or new[0] >= WIDTH or
        new[1] < 0 or new[1] >= HEIGHT or
        new in snake
    ):
        game_over = True
        canvas.create_text(
            WIDTH*CELL/2,
            HEIGHT*CELL/2,
            text="遊戲結束",
            font=("Arial", 24)
        )
        return

    snake.insert(0, new)

    # 吃到食物
    if new == food:
        score += 10
        score_label.config(text=f"分數：{score}")
        food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
    else:
        snake.pop()

    draw()
    root.after(DELAY, move)

# =====================
# 重新開始按鈕
# =====================
btn = tk.Button(root, text="重新開始", font=("Arial", 12), command=restart)
btn.pack(pady=5)

# =====================
# 啟動遊戲
# =====================
root.bind("<Key>", key)
root.focus_force()

draw()
move()
root.mainloop()
