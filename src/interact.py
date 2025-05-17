import pygame

interactables = {
    "bookshelf": pygame.Rect(20, 80, 50, 120),
    "door": pygame.Rect(260, 80, 2, 100),
    "desk": pygame.Rect(400, 150, 2, 110),
    "bedside": pygame.Rect(420, 150, 2, 60),
    "bed": pygame.Rect(600, 220, 40, 60),
    "carpet": pygame.Rect(570, 430, 1, 1),
    "teatable": pygame.Rect(690, 460, 1, 1),
}

def check_interaction(player_pos, scale):
    player_rect = pygame.Rect(player_pos.x, player_pos.y, scale[0], scale[1])
    for name, rect in interactables.items():
        if player_rect.colliderect(rect.inflate(30, 30)):
            return True, name
    return False, None

def draw_prompt(screen, player_pos):
    font = pygame.font.SysFont(None, 28)  # 現在才初始化
    prompt_text = font.render("Enter C to see more", True, (255, 255, 0))
    screen.blit(prompt_text, (player_pos.x - 10, player_pos.y - 30))

def draw_inspection(screen, near_object, width, height):
    font = pygame.font.SysFont(None, 28)
    screen.fill((30, 30, 30))
    text = font.render(f"Inspecting: {near_object}. Press ESC to exit.", True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))
