import pygame
pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # 視窗設定
pygame.display.set_caption("Pomodoro Timer")
clock = pygame.time.Clock()
title_font = pygame.font.Font(None,55)  # 字型
timer_font = pygame.font.Font(None,110)
info_font = pygame.font.Font(None,35)
START_TIME = 25*60  # 時間設定
time_left = START_TIME
running = False
finished = False
TIMER_EVENT = pygame.USEREVENT + 1  # 每秒事件
pygame.time.set_timer(TIMER_EVENT,1000)
game = True
work_mode = True
pomodoro_count = 0
START_TIME = 25*60
time_left = START_TIME
running = False
finished = False
work_mode = True
pomodoro_count = 0
TOTAL_TIME = START_TIME
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            print("KEY:", event.key)
            if event.key == pygame.K_RETURN and not finished:
                running = not running
            elif event.key == pygame.K_r:
                time_left = START_TIME
                running = False
                finished = False
        elif event.type == TIMER_EVENT:
            if running:
                time_left -= 1
                if time_left <= 0:
                    if work_mode:
                        pomodoro_count += 1
                        START_TIME = 5*60
                        TOTAL_TIME = START_TIME
                        work_mode = False
                    else:
                        START_TIME = 25*60
                        TOTAL_TIME = START_TIME
                        work_mode = True
                    time_left = START_TIME
    screen.fill((35,40,55))  # 畫面
    title = title_font.render(
        "Pomodoro Timer",
        True,
        (255,255,255)
    )
    if work_mode:
            mode = "WORK"
            color = (255,120,120)
    else:
            mode = "BREAK"
            color = (120,120,255)
    mode_text = info_font.render(
            f"Mode:{mode}",
            True,
            color
        )
    screen.blit(mode_text,(160,250))
    screen.blit(title,(100,40))
    minutes = time_left // 60
    seconds = time_left % 60
    if time_left <= 60:
        timer_color = (255,80,80)
    else:
        timer_color = (255,220,80)
    pygame.draw.circle(
        screen,
        (220,220,220),
        (450,50),
        20,
        2
    )
    pygame.draw.line(
        screen,
        (220,220,220),
        (450,50),
        (450,40),
        2
    )
    pygame.draw.line(
        screen,
        (220,220,220),
        (450,50),
        (460,50),
        2
    )
    # 番茄葉子
    pygame.draw.polygon(
        screen,
        (40,180,60),
        [
            (250,290),
            (240,305),
            (250,300),
            (260,305),
            (250,290),
            (235,295),
            (265,295)
        ]
    )
# 番茄蒂
    pygame.draw.line(
        screen,
        (80,50,20),
        (250,285),
        (250,270),
        4
    )
    pygame.draw.rect(
        screen,
        (55,60,80),
        (70,90,360,120),
        border_radius=20
    )
    pygame.draw.circle(
        screen,
        (230,60,60),
        (250,340),
        45
    )
    pygame.draw.polygon(
        screen,
        (30,180,80),
        [
            (250,285),
            (235,305),
            (245,300),
            (255,300),
            (265,305)
        ]
    )
    pygame.draw.rect(
        screen,
        (80,80,80),
        (100,390,300,20),
        border_radius=10
    )
    fill = int(300*(TOTAL_TIME-time_left)/TOTAL_TIME)
    pygame.draw.rect(
        screen,
        (0,220,120),
        (100,390,fill,20),
        border_radius=10
    )
    pygame.display.set_caption(
         f"{minutes:02}:{seconds:02}|Pomodoro Timer"
    )
    timer = timer_font.render(
        f"{minutes:02}:{seconds:02}",
        True,
        timer_color
    )
    screen.blit(timer,(115,120))
    if finished:
        text = info_font.render(
            "Time's Up!",
            True,
            (0,255,120)
        )
    elif running:
        text = info_font.render(
            "ENTER = Pause",
            True,
            (220,220,220)
        )
    else:
        text = info_font.render(
            "ENTER = Start  R = Reset",
            True,
            (220,220,220)
        )
    count_text = info_font.render(
        f"Pomodoros:{pomodoro_count}",
        True,
        (255,255,255)
    )
    screen.blit(count_text,(120,430))
    
    screen.blit(text,(90,280))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()