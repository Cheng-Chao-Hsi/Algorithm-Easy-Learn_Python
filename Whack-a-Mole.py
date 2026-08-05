import pygame
import random
pygame.init()
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
clock = pygame.time.Clock()
font = pygame.font.Font(None,40)
MOLE_EVENT = pygame.USEREVENT + 1
mole_speed = 700
level = 1
pygame.time.set_timer(MOLE_EVENT, mole_speed)
holes = [
    (150,150),(300,150),(450,150),
    (150,300),(300,300),(450,300),
    (150,450),(300,450),(450,450)
]
mole = random.choice(holes)
mole_type = "normal"
mole_score = 1
miss = 0
score = 0
MAX_MISS = 10
time_left = 30
countdown = 3
countdown_time = pygame.time.get_ticks()
game_started = False
hit = False
hit_time = 0
high_score = 0
game_over = False
max_combo = 0
combo = 0
combo_effect = False
combo_time = 0
show_plus = False
plus_x = 0
plus_y = 0
plus_time = 0
# 打擊特效
effect = False
effect_x = 0
effect_y = 0
effect_start_time = 0
effect_type = ""
TIMER_EVENT = pygame.USEREVENT + 2
running = True
while running:
    for event in pygame.event.get():
        if not game_started:
            current_time = pygame.time.get_ticks()
            if current_time - countdown_time >= 1000:
                countdown -= 1
                countdown_time = current_time
                if countdown == 0:
                    game_started = True
                    pygame.time.set_timer(TIMER_EVENT,1000)
        
        if event.type == MOLE_EVENT and not game_over:
            mole = random.choice(holes)

    # 隨機決定地鼠種類
            chance = random.randint(1, 100)

            if chance <= 10:
        # 10%：獎勵地鼠
                mole_type = "bonus"
                mole_score = 3
        # 10%炸彈
            elif chance <= 20:
                mole_type = "bomb"
                mole_score = 0

            elif chance <= 30:
        # 20%：快速地鼠
                mole_type = "fast"
                mole_score = 2

            else:
        # 70%：普通地鼠
                mole_type = "normal"
                mole_score = 1
        elif event.type == TIMER_EVENT:
            if time_left > 0:
                time_left -= 1
            if time_left == 0:
                game_over = True
                combo = 0
                if score>high_score:
                    high_score = score
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and game_started:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            distance = (
            (mouse_x - mole[0]) ** 2 +
            (mouse_y - mole[1]) ** 2
            ) ** 0.5

            if distance <= 30:
                if mole_type == "bomb":
                    game_over = True
                    combo = 0
                    if score > high_score:
                        high_score = score
                else:
                    score += mole_score
                    effect = True
                    effect_x = mole[0]
                    effect_y = mole[1]
                    effect_start_time = pygame.time.get_ticks()
                    
                    if score % 5 == 0 and mole_speed >= 20:
                        mole_speed -= 100
                        level += 1
                        pygame.time.set_timer(MOLE_EVENT,mole_speed)
        # 飄字
            show_plus = True
            plus_x = mole[0]
            plus_y = mole[1] - 20
            plus_time = pygame.time.get_ticks()

        # Combo
            combo += 1

            if combo >= 5:
                    combo_effect = True
                    combo_time = pygame.time.get_ticks()

            if combo > max_combo:
                max_combo = combo

        # 地鼠被打中的表情
                hit = True
                hit_time = pygame.time.get_ticks()

        # 換下一隻地鼠
                mole = random.choice(holes)
            else:
                miss += 1
                combo = 0
                if miss >= MAX_MISS:
                   game_over = True
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                score = 0
                time_left = 30
                max_combo = 0
                miss = 0
                hit = False
                combo_effect = False
                show_plus = False
                game_over = False
                mole = random.choice(holes)
                mole_speed = 700
                level = 1
                pygame.time.set_timer(MOLE_EVENT,mole_speed)
        if event.type == pygame.QUIT:
            running = False
        if hit:
            if show_plus:
                plus_y -= 1
                if pygame.time.get_ticks() - plus_time > 500:
                    show_plus = False
            if combo_effect:
                if pygame.time.get_ticks() - combo_time > 500:
                    combo_effect = False
            if pygame.time.get_ticks() - hit_time > 200:
                hit = False
    screen.fill((180,220,180))
    for hole in holes:
        pygame.draw.circle(
            screen,
            (90,60,30),
            hole,
            45
        )
        score_text = font.render(
            f"Score:{score}",
            True,
            (255,255,255)
        )
        score_text2 = font.render(
            f"High Score:{high_score}",
            True,
            (255,255,200)
        )
        miss_text = font.render(
            f"Miss:{miss}",
            True,
            (255,255,150)
        )
        combo_text = font.render(
            f"Combo:{combo}",
            True,
            (255,150,50)
        )
        combo_final = font.render(
            f"Max Combo:{max_combo}",
            True,
            (255,200,0)
        )
        
    if hit:
        # 打擊特效
        if effect:
            effect_elapsed = pygame.time.get_ticks() - effect_start_time

            if effect_elapsed < 400:

                effect_radius = int(effect_elapsed / 2)

                if effect_type == "hit":
                    pygame.draw.circle(
                screen,
                (255, 255, 0),
                (effect_x, effect_y),
                effect_radius,
                5
            )
                elif effect_type == "bomb":
                    pygame.draw.circle(
                screen,
                (255, 80, 0),
                (effect_x, effect_y),
                effect_radius,
                8
            )

            pygame.draw.circle(
                screen,
                (255, 200, 0),
                (effect_x, effect_y),
                effect_radius // 2,
                4
            )

        else:
            effect = False
            pygame.draw.circle(
            screen,
            (120,80,40),
            mole,
            30
        )
    # 左眼 X
        pygame.draw.line(screen,(0,0,0),
            (mole[0]-14,mole[1]-12),
            (mole[0]-6,mole[1]-4),2)
        pygame.draw.line(screen,(0,0,0),
            (mole[0]-14,mole[1]-4),
            (mole[0]-6,mole[1]-12),2)
    # 右眼 X
        pygame.draw.line(screen,(0,0,0),
            (mole[0]+6,mole[1]-12),
            (mole[0]+14,mole[1]-4),2)
        pygame.draw.line(screen,(0,0,0),
            (mole[0]+6,mole[1]-4),
            (mole[0]+14,mole[1]-12),2)
    # 嘴巴
        pygame.draw.arc(
            screen,
            (0,0,0),
            (mole[0]-10,mole[1],20,10),
            3.14,
            6.28,
            2
        )
    elif game_started:
    # 原本活著的地鼠
        # 根據地鼠種類決定顏色
        if mole_type == "normal":
            mole_color = (120,80,40)

        elif mole_type == "fast":
            mole_color = (220,80,80)
        elif mole_type == "bonus":
            mole_color = (255,200,50)
        elif mole_type == "bomb":
            mole_color = (30,30,30)

        pygame.draw.circle(
            screen,
            mole_color,
            mole,
            30
        )
        if mole_type == "bomb":
            pygame.draw.line(
                screen,
                (255,0,0),
                (mole[0],mole[1]-25),
                (mole[0]+10,mole[1]-35),
                4
            )
            pygame.draw.line(
                screen,
                (255,0,0),
                (mole[0]-10,mole[1]-10),
                (mole[0]+10,mole[1]+10),
                3
            )
            pygame.draw.line(
                screen,
                (255,0,0),
                (mole[0]+10,mole[1]-10),
                (mole[0]-10,mole[1]+10),
                3
            )
        pygame.draw.circle(
            screen,
            (255,255,255),
            (mole[0]-10,mole[1]-8),
            5
        )
        pygame.draw.circle(
            screen,
            (0,0,0),
            (mole[0]-10,mole[1]-8),
            2
        )
        pygame.draw.circle(
        screen,
        (255,255,255),
        (mole[0]+10,mole[1]-8),
        5
    )
        pygame.draw.circle(
        screen,
        (0,0,0),
        (mole[0]+10,mole[1]-8),
        2
    )
        pygame.draw.circle(
        screen,
        (255,120,120),
        (mole[0],mole[1]+1),
        4
    )
    screen.blit(score_text,(20,20))
    screen.blit(score_text2,(20,60))
    total = score + miss

    if total > 0:
        accuracy = score / total * 100
    else:
        accuracy = 0
    accuracy_text = font.render(
    f"Accuracy: {accuracy:.1f}%",
    True,
    (150,255,150)
    )
    screen.blit(accuracy_text,(20,140))
    screen.blit(combo_text,(20,180))
    screen.blit(miss_text,(20,100))
    miss_limit_text = font.render(
    f"Miss Limit: {MAX_MISS}",
    True,
    (255,100,100)
    )
    screen.blit(miss_limit_text,(20,260))
    time_text = font.render(
        f"Time : {time_left}",
        True,
        (255,255,255)
        )
    screen.blit(time_text,(430,20))
    level_text = font.render(
        f"Level:{level}",
        True,
        (255,255,255)
    )
    screen.blit(level_text,(430,60))
    if game_over:
        over = font.render(
            "GAME OVER",
            True,
            (255,0,0)
        )
        final = font.render(
            f"Final Score : {score}",
            True,
            (255,255,255)
        )
        restart = font.render(
            "Press R to Restart",
            True,
            (255,255,0)
        )
        screen.blit(over,(180,240))
        screen.blit(final,(180,290))
        screen.blit(restart,(140,340))
    if combo_effect:
        combo_text = font.render(
            f"COMBO{combo}!",
            True,
            (255,215,0)
        )
        screen.blit(combo_text,(170,180))
        screen.blit(combo_final,(170,330))
        screen.blit(combo_final,(20,220))
    if show_plus:
        plus_text = font.render(
        f"+{mole_score}",
        True,
        (255,255,0)
        )
        screen.blit(plus_text, (plus_x, plus_y))
    if not game_started:
        if countdown > 0:
            countdown_text = font.render(
                str(countdown),
                True,
                (255,255,255)
            )
        else:
            countdown_text = font.render(
                "GO!",
                True,
                (255,255,0)
            )
        screen.blit(countdown_text,(280,260))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
