import tkinter as tk
import random

CELL_SIZE = 20
WIDTH = 20
HEIGHT = 20
GAME_SPEED = 150

# 建立主視窗
window = tk.Tk()
window.title("貪食蛇遊戲（版本一）")

# 強制設定視窗大小
window.geometry(f"{WIDTH*CELL_SIZE}x{HEIGHT*CELL_SIZE}")

# 建立畫布
canvas = tk.Canvas(
    window,
    bg="white",
    width=WIDTH * CELL_SIZE,
    height=HEIGHT * CELL_SIZE
)
canvas.pack()

# 強制取得鍵盤焦點（很重要）
window.focus_set()

snake = [(10, 10), (9, 10), (8, 10)]
direction = "Right"
game_over = False

food = (
    random.randint(0, WIDTH - 1),
    random.randint(0, HEIGHT - 1)
)

def draw():
    canvas.delete("all")

    # 畫蛇
    for x, y in snake:
        canvas.create_rectangle(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill="green"
        )

    # 畫食物
    fx, fy = food
    canvas.create_oval(
        fx * CELL_SIZE,
        fy * CELL_SIZE,
        (fx + 1) * CELL_SIZE,
        (fy + 1) * CELL_SIZE,
        fill="red"
    )

def change_direction(event):
    global direction
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        direction = event.keysym

def move():
    global food, game_over

    if game_over:
        return

    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - 1)
    elif direction == "Down":
        new_head = (head_x, head_y + 1)
    elif direction == "Left":
        new_head = (head_x - 1, head_y)
    else:
        new_head = (head_x + 1, head_y)

    # 撞牆或撞自己
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake
    ):
        game_over = True
        canvas.create_text(
            WIDTH*CELL_SIZE/2,
            HEIGHT*CELL_SIZE/2,
            text="遊戲結束",
            font=("Arial", 24)
        )
        return

    snake.insert(0, new_head)

    if new_head == food:
        food = (
            random.randint(0, WIDTH - 1),
            random.randint(0, HEIGHT - 1)
        )
    else:
        snake.pop()

    draw()
    window.after(GAME_SPEED, move)

window.bind("<Key>", change_direction)

draw()
move()
window.mainloop()
