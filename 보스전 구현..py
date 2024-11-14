import pygame
import random
import sys
import time

# 초기화
pygame.init()

# 화면 설정
screen_width = 648
screen_height = 635
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("보스전 구현")

# 이미지 로딩
background_image = pygame.image.load("image/background.jpg").convert()  # 원하는 배경 이미지 파일명
player_image = pygame.image.load("image/player.jpg").convert_alpha()  # 플레이어 이미지 파일명
player_image = pygame.transform.scale(player_image, (60, 60))  # 이미지 크기 조정

# 플레이어 설정
player_width = 60
player_height = 60
player_x = 50
player_y = screen_height - player_height
player_y_velocity = 0
gravity = 1.5

# 장애물 설정
obstacle_width = 30
obstacle_height = 40
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height
obstacle_speed_range = range(4, 20)  # 장애물 속도 범위 (4부터 19까지)
obstacle_speed = 0  # 시작 전에 속도를 0으로 설정

boss_width = 30
boss_height = 40
boss_x = 618
boss_y = 50
boss_y_velocity = 0
pattern_progress = False
boss_timer = 0

leaser_width = screen_width
leaser_height = 50
leaser_x = 0
leaser_y = boss_y

# 게임 오버 여부 
game_over = False

boss_stage = False
leaser_start = False
leaser_hit = False

# 시작 대기 시간 설정 (3초)
start_delay = 4
start_time = time.time()
start_countdown = True

# 게임 루프
running = True
clock = pygame.time.Clock()
timer = 0
def check_collision_ob(player_rect, obstacle_rect):
    return player_rect.colliderect(obstacle_rect)
def check_collision_le(player_rect, leaser_rect):
    return player_rect.colliderect(leaser_rect)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over and not start_countdown:
            if player_y == screen_height - player_height:
                player_y_velocity = -30

        # 게임 오버 상태에서 아무 키나 누르면 다시 시작
        if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE and game_over:
            #변수 초기화
            game_over = False
            player_y = screen_height - player_height
            obstacle_x = screen_width
            obstacle_y = screen_height - obstacle_height
            obstacle_speed = random.choice(obstacle_speed_range)
            boss_stage = False
            leaser_start = False
            timer = 0
            boss_timer = 0


            
    if not game_over:
        # 플레이어 이동 및 점프
        player_y_velocity += gravity
        player_y += player_y_velocity
        if player_y >= screen_height - player_height:
            player_y = screen_height - player_height
            player_y_velocity = 0

        if not start_countdown :
            if not boss_stage:# 장애물 이동
                obstacle_x -= obstacle_speed
                if obstacle_x < 0:
                    obstacle_x = screen_width
                    obstacle_y = screen_height - obstacle_height
                    obstacle_speed = random.choice(obstacle_speed_range)  # 새로운 속도 선택
            # 충돌 감지
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
            leaser_rect = pygame.Rect(leaser_x, leaser_y, leaser_width, leaser_height)
            if check_collision_ob(player_rect, obstacle_rect):
                print("Game Over!")
                #game_over = True
            elif check_collision_le(player_rect, leaser_rect) and leaser_hit:
                print("Game Over!")
                #game_over = True
        if timer//60 == 5 and boss_stage == False :
            boss_stage = True
            leaser_start = True

        if boss_stage:
            obstacle_x = screen_width
            obstacle_y = screen_height - obstacle_height
            if boss_timer/60 > 1: #위치 고정
                print(boss_timer)
                if (boss_timer/60 < 2.5) and (boss_timer/60 > 1.5): #발사
                    leaser_hit = True
                    print("1.5")
                    boss_timer += 1
                elif (boss_timer/60 >= 2.5) and (boss_timer/60 < 3): #발사 정지
                    leaser_hit =  False
                    leaser_start = False
                    print(" , 2.5")
                    boss_timer += 1
                elif boss_timer/60 >= 3: #다시 추적
                    leaser_start = True
                    boss_timer = 0
                    print(" , 3")
                    boss_timer += 1
                else:
                    boss_timer += 1
            else: #추적 움직임
                leaser_y = boss_y
                boss_timer += 1
                boss_y = player_y

    # 배경화면 그리기
    screen.blit(background_image, (0, 0))

    if start_countdown:
        current_time = time.time()
        if current_time - start_time >= start_delay:
            start_countdown = False
            obstacle_speed = random.choice(obstacle_speed_range)  # 시작 후에 장애물 속도 설정
            game_over = False  # 게임 시작 후에 game_over 초기화
            timer = 0
        else:
            font = pygame.font.Font(None, 72)
            countdown_text = font.render(str(int(start_delay - (current_time - start_time))), True, (255, 255, 255))
            screen.blit(countdown_text, (screen_width // 2 - 20, screen_height // 2 - 40))
    else:
        if not game_over:
            # 이미지 그리기          
            if boss_stage:
                pygame.draw.rect(screen, (255, 0, 0), (boss_x, boss_y, boss_width, boss_height))
                if leaser_start:
                    pygame.draw.rect(screen, (boss_timer*1.5, boss_timer*1.5, boss_timer*1.5), (leaser_x, leaser_y, leaser_width, leaser_height))
                    if leaser_hit:
                        pygame.draw.rect(screen, (boss_timer*1.5, 0, 0), (leaser_x, leaser_y, leaser_width, leaser_height))
            pygame.draw.rect(screen, (0, 0, 255), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            screen.blit(player_image, (player_x, player_y))
        else:
            # 게임 오버 메시지 표시
            font = pygame.font.Font(None, 36)
            game_over_text = font.render("Game Over - Press any key to restart", True, (255, 255, 255))
            screen.blit(game_over_text, (screen_width // 2 - 220, screen_height // 2))

    pygame.display.flip()

    clock.tick(60)
    timer += 1

pygame.quit()
sys.exit()
