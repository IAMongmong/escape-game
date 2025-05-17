import pygame
import sys
import os
import interact

# 初始化 Pygame
pygame.init()
pygame.font.init()

# 畫面大小與設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
SCALE = (80, 80)
ANIMATION_DELAY = 200  # 毫秒
speed = 5

# 資料夾路徑
base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# 載入圖片並縮放
def load_scaled(filename):
    return pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, filename)).convert_alpha(),
        SCALE
    )

# 載入背景圖
background = pygame.image.load(os.path.join(base_path, "background.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 載入角色動畫幀
frames = {
    "down": [
        load_scaled("角色正面靜止.PNG"),
        load_scaled("角色前走1.PNG"),
        load_scaled("角色前走2.PNG")
    ],
    "left": [
        load_scaled("角色側面靜止.PNG"),
        load_scaled("角色側走1.PNG"),
        load_scaled("角色側走2.PNG")
    ]
}
frames["right"] = [pygame.transform.flip(img, True, False) for img in frames["left"]]
frames["up"] = frames["down"]  # 暫時共用向下

# 初始狀態
direction = "down"
frame_index = 0
player_pos = pygame.Vector2(100, 100)
animation_timer = 0
inspection_mode = False
near_object = None

# 主迴圈
while True:
    dt = clock.tick(60)
    moved = False

    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and near_object and not inspection_mode:
                inspection_mode = True
            elif event.key == pygame.K_ESCAPE and inspection_mode:
                inspection_mode = False

    keys = pygame.key.get_pressed()
    if not inspection_mode:  # 觀察模式下不能移動
        if keys[pygame.K_LEFT]:
            new_x = player_pos.x - speed
            if new_x >= 0:
                player_pos.x = new_x
                direction = "left"
                moved = True
        elif keys[pygame.K_RIGHT]:
            new_x = player_pos.x + speed
            if new_x <= WIDTH - SCALE[0]:
                player_pos.x = new_x
                direction = "right"
                moved = True
        elif keys[pygame.K_UP]:
            new_y = player_pos.y - speed
            if new_y >= 170:
                player_pos.y = new_y
                direction = "up"
                moved = True
        elif keys[pygame.K_DOWN]:
            new_y = player_pos.y + speed
            if new_y <= HEIGHT - SCALE[1]:
                player_pos.y = new_y
                direction = "down"
                moved = True

    # 動畫更新
    if moved:
        animation_timer += dt
        if animation_timer >= ANIMATION_DELAY:
            animation_timer = 0
            frame_index = (frame_index + 1) % len(frames[direction])
    else:
        frame_index = 0

    # 檢查是否接近可互動物件
    show_prompt, near_object = interact.check_interaction(player_pos, SCALE)

    # 畫面更新
    if inspection_mode:
        interact.draw_inspection(screen, near_object, WIDTH, HEIGHT)
    else:
        screen.blit(background, (0, 0))
        current_image = frames[direction][frame_index]
        screen.blit(current_image, player_pos)

        if show_prompt:
            interact.draw_prompt(screen, player_pos)

    pygame.display.flip()
