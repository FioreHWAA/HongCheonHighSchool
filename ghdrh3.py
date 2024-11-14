import pygame
import random
import sys
import time
import platform

# 초기화
pygame.init()

# 화면 설정
screen_width = 648
screen_height = 635
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("내가 꼭 완성함")

# 이미지 로딩
background_image = pygame.image.load("background.jpg").convert()
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (60, 60))
obstacle_image = pygame.image.load("missile.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (80, 50))

# 플레이어 설정
player_width = 60
player_height = 60
player_x = 50
player_y = screen_height - player_height
player_y_velocity = 0
gravity = 1.0

# 장애물 설정
obstacle_width = 80
obstacle_height = 50
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height
obstacle_speed_range = range(7, 16)
obstacle_speed = 0

# 게임 상태 변수
game_over = False
boss_stage = False  # 보스 스테이지 여부

# 보스 및 레이저 설정
boss_x = screen_width - 80  # 보스의 x 위치
boss_y = 50  # 보스의 y 위치
leaser_width = screen_width  # 레이저 너비 (화면 전체 너비)
leaser_height = 20  # 레이저 높이
leaser_y = boss_y  # 레이저의 초기 y 위치
leaser_active = False  # 레이저가 발사 중인지 여부
show_trajectory = False  # 궤적이 표시 중인지 여부
boss_timer = 0  # 보스 타이머
trajectory_display_time = 60  # 궤적 표시 시간 (프레임 단위)
trajectory_color = (0, 0, 0)  # 궤적 색상 (검은색)

# 시작 대기 시간 설정 (3초)
start_delay = 4
start_time = time.time()
start_countdown = True

# 게임 루프
running = True
clock = pygame.time.Clock()
score = 0  # 점수 변수

# 한글 지원 폰트를 시스템에서 불러오기
if platform.system() == "Windows":
    korean_font = pygame.font.SysFont("malgungothic", 36)
elif platform.system() == "Darwin":
    korean_font = pygame.font.SysFont("AppleGothic", 36)
else:
    korean_font = pygame.font.Font(None, 36)

def check_collision(player_rect, obstacle_rect):
    return player_rect.colliderect(obstacle_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 특정 키를 눌렀을 때 프로그램 종료
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Q 키가 눌렸을 때
                running = False

        # 스페이스바로 점프
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over and not start_countdown:
            if player_y == screen_height - player_height:
                player_y_velocity = -20

        # 게임 오버 상태에서 아무 키나 누르면 다시 시작
        if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE and game_over:
            game_over = False
            player_y = screen_height - player_height
            obstacle_x = screen_width
            obstacle_y = screen_height - obstacle_height
            obstacle_speed = random.choice(obstacle_speed_range)
            score = 0
            start_time = time.time()
            start_countdown = True
            boss_stage = False  # 보스 스테이지 초기화
            leaser_active = False  # 레이저 초기화
            show_trajectory = False  # 궤적 초기화
            boss_timer = 0  # 보스 타이머 초기화

    if not game_over:
        # 플레이어 이동 및 점프
        player_y_velocity += gravity
        player_y += player_y_velocity
        if player_y >= screen_height - player_height:
            player_y = screen_height - player_height
            player_y_velocity = 0

        if not start_countdown:
            # 점수에 따라 보스 스테이지로 전환
            if score >= 20:
                boss_stage = True  # 보스 스테이지 활성화

            # 장애물 이동 (보스 스테이지가 아닐 때만)
            if not boss_stage:
                obstacle_x -= obstacle_speed
                if obstacle_x < 0:
                    obstacle_x = screen_width
                    obstacle_y = screen_height - obstacle_height
                    obstacle_speed = random.choice(obstacle_speed_range)
                    score += 1  # 점수 증가

            # 보스 스테이지에서 레이저 발사 패턴
            if boss_stage:
                boss_timer += 1

                # 레이저 궤적 표시 시작
                if boss_timer % 180 == 0:
                    leaser_y = player_y  # 현재 플레이어 위치에 맞춰 궤적 위치 설정
                    show_trajectory = True  # 궤적을 표시
                    leaser_active = False  # 레이저 비활성화 상태로 대기

                # 궤적을 일정 시간 동안 표시 후 레이저 발사
                if boss_timer % 180 == trajectory_display_time:
                    show_trajectory = False  # 궤적 숨기기
                    leaser_active = True  # 레이저 발사 시작

                # 레이저 발사 중일 때 충돌 감지
                if leaser_active:
                    leaser_rect = pygame.Rect(0, leaser_y, leaser_width, leaser_height)
                    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                    if check_collision(player_rect, leaser_rect):
                        game_over = True
                    if boss_timer % 180 >= trajectory_display_time + 60:  # 레이저 일정 시간 후 비활성화
                        leaser_active = False

            # 충돌 감지 (보스 스테이지가 아닐 때)
            if not boss_stage:
                player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
                obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
                if check_collision(player_rect, obstacle_rect):
                    game_over = True

    # 배경화면 그리기
    screen.blit(background_image, (0, 0))

    if start_countdown:
        current_time = time.time()
        if current_time - start_time >= start_delay:
            start_countdown = False
            obstacle_speed = random.choice(obstacle_speed_range)
            game_over = False
        else:
            font = pygame.font.Font(None, 72)
            countdown_text = font.render(str(int(start_delay - (current_time - start_time))), True, (255, 255, 255))
            screen.blit(countdown_text, (screen_width // 2 - 20, screen_height // 2 - 40))
    else:
        if not game_over:
            # 이미지 그리기
            screen.blit(player_image, (player_x, player_y))
            if not boss_stage:  # 보스 스테이지가 아닐 때만 장애물 표시
                screen.blit(obstacle_image, (obstacle_x, obstacle_y))
            else:
                # 보스 스테이지에서 레이저 궤적 및 레이저 표시
                if show_trajectory:
                    # 레이저 궤적 그리기
                    pygame.draw.rect(screen, trajectory_color, (0, leaser_y, leaser_width, leaser_height))
                elif leaser_active:
                    # 레이저 그리기
                    pygame.draw.rect(screen, (255, 0, 0), (0, leaser_y, leaser_width, leaser_height))

            # 점수 표시
            font = pygame.font.Font(None, 36)
            score_text = font.render("score: " + str(score), True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
        else:
            # 게임 오버 메시지
            game_over_text_1 = korean_font.render("죽었네요! 점수: " + str(score), "\n", True, (255, 255, 255))
            screen.blit(game_over_text_1, (screen_width // 2 - 220, screen_height // 2))

            font_small = pygame.font.SysFont("malgungothic", 20)
            game_over_text_2 = font_small.render("다시 시작하려면 아무 키를 입력하세요", "\n", True, (255, 255, 255))
            screen.blit(game_over_text_2, (screen_width // 2 - 220, screen_height // 2 + 42))

            game_over_text_3 = font_small.render("게임을 종료하려면 Q를 입력하세요", "\n", True, (255, 255, 255))
            screen.blit(game_over_text_3, (screen_width // 2 - 220, screen_height // 2 + 68))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
