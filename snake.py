import pygame
import random
pygame.init()
# 遊戲設定
WIDTH = 1000
HEIGHT = 1000
BLOCK = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("我的貪吃蛇")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 45)
title_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 30)
# 初始化遊戲資料
def reset_game():
    global snake
    global food_x, food_y
    global score
    global snake_speed_x, snake_speed_y
    global game_over
    global game_speed
    snake = [
        [100, 100],
        [80, 100],
        [60, 100],
        [40, 100]
    ]
    food_x, food_y = spawn_food()
    score = 0
    snake_speed_x = BLOCK
    snake_speed_y = 0
    game_speed = 10
    game_over = False
# 產生食物
def spawn_food():
    while True:
        x = random.randint(0, WIDTH//BLOCK-1) * BLOCK
        y = random.randint(0, HEIGHT//BLOCK-1) * BLOCK
        if [x, y] not in snake:
            return x, y
# 初始狀態
snake = []
food_x = 0
food_y = 0
score = 0
snake_speed_x = BLOCK
snake_speed_y = 0
game_speed = 10
game_start = False
game_over = False
reset_game()
running = True
while running:
    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # 開始畫面
            if not game_start:

                if event.key == pygame.K_RETURN:
                    game_start = True

            # GAME OVER
            elif game_over:

                if event.key == pygame.K_r:

                    reset_game()
            # 遊戲中控制
            else:

                if event.key == pygame.K_RIGHT:

                    if snake_speed_x == 0:
                        snake_speed_x = BLOCK
                        snake_speed_y = 0

                elif event.key == pygame.K_LEFT:

                    if snake_speed_x == 0:
                        snake_speed_x = -BLOCK
                        snake_speed_y = 0

                elif event.key == pygame.K_UP:

                    if snake_speed_y == 0:
                        snake_speed_x = 0
                        snake_speed_y = -BLOCK

                elif event.key == pygame.K_DOWN:

                    if snake_speed_y == 0:
                        snake_speed_x = 0
                        snake_speed_y = BLOCK
    # 開始畫面
    if not game_start:
        screen.fill((20,20,35))
        title = title_font.render(
            "SNAKE GAME",
            True,
            (0,255,150)
        )
        start = font.render(
            "Press ENTER to Start",
            True,
            (255,255,255)
        )
        info = small_font.render(
            "Arrow Keys : Move",
            True,
            (180,180,180)
        )
        screen.blit(title,(300,250))
        screen.blit(start,(330,400))
        screen.blit(info,(360,460))
        
        pygame.display.update()
        clock.tick(10)
        continue
    # GAME OVER 畫面
    if game_over:
        screen.fill((25,15,25))
        text = title_font.render(
            "GAME OVER",
            True,
            (255,70,70)
        )
        restart = font.render(
            "Press R Restart",
            True,
            (255,255,255)
        )
        score_text = font.render(
            f"Final Score : {score}",
            True,
            (255,220,0)
        )
        restart = font.render(
            "Press R Restart",
            True,
            (255,255,255)
        )
        score_text = font.render(
            f"Score: {score}",
            True,
            (255,255,255)
        )
        screen.blit(text,(380,350))
        screen.blit(restart,(350,420))
        screen.blit(score_text,(400,480))
        pygame.display.update()
        clock.tick(10)
        continue
    # 移動蛇
    new_head = [
        snake[0][0] + snake_speed_x,
        snake[0][1] + snake_speed_y
    ]
    snake.insert(0,new_head)
    # 撞牆
    if (
        snake[0][0] < 0 or
        snake[0][0] >= WIDTH or
        snake[0][1] < 0 or
        snake[0][1] >= HEIGHT
    ):
        game_over = True
    # 撞自己
    if snake[0] in snake[1:]:
        game_over = True
    # 吃食物
    ate = False
    if snake[0][0] == food_x and snake[0][1] == food_y:
        score += 1
        ate = True
        food_x, food_y = spawn_food()
        # 每三分增加速度
        if score % 3 == 0:
            game_speed += 1
    # 沒吃到就刪尾巴
    if not ate:
        snake.pop()
    # 畫面
    screen.fill((0,0,0))
    # 食物
    pygame.draw.circle(
    screen,
    (255,0,0),
    (food_x + BLOCK//2, food_y + BLOCK//2),
    BLOCK//2 - 2
    )
    pygame.draw.line(
    screen,
    (80,50,0),
    (food_x+10, food_y+4),
    (food_x+10, food_y-2),
    2
    )
    # 蛇
    for i, block in enumerate(snake): 
        if i == 0: 
            color = (0,255,100) # 蛇頭 
        else: color = (0,180,80) # 蛇身 
        pygame.draw.rect( 
            screen, color,
            ( block[0], block[1], BLOCK, BLOCK ), 
            border_radius=8 )

        if i == 0:

            pygame.draw.circle(screen,(255,255,255),(block[0]+6,block[1]+6),2)
            pygame.draw.circle(screen,(255,255,255),(block[0]+14,block[1]+6),2)
    # 分數
    score_text = font.render(
        f"Score: {score}",
        True,
        (255,255,255)
    )
    screen.blit(score_text,(20,20))
    pygame.display.update()
    clock.tick(game_speed)
pygame.quit()