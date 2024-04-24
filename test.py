import pygame
import random

# Khai báo các màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Khai báo kích thước của cửa sổ trò chơi
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

# Khai báo kích thước của thanh và quả bóng
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20

# Khai báo tốc độ di chuyển của thanh và quả bóng
PADDLE_SPEED = 5
BALL_INITIAL_SPEED_X = 5
BALL_INITIAL_SPEED_Y = 5

pygame.init()

# Tạo cửa sổ trò chơi
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()

# Hàm vẽ thanh
def draw_paddle(paddle):
    pygame.draw.rect(window, WHITE, paddle)

# Hàm vẽ quả bóng
def draw_ball(ball):
    pygame.draw.circle(window, WHITE, (ball[0], ball[1]), BALL_SIZE)

# Hàm di chuyển thanh
def move_paddle(paddle, direction):
    if direction == "up" and paddle.top > 0:
        paddle.y -= PADDLE_SPEED
    elif direction == "down" and paddle.bottom < WINDOW_HEIGHT:
        paddle.y += PADDLE_SPEED

# Hàm xử lý va chạm với tường
def check_wall_collision(ball):
    if ball[1] <= 0 or ball[1] >= WINDOW_HEIGHT - BALL_SIZE:
        return True
    return False

# Hàm xử lý va chạm với thanh
def check_paddle_collision(ball, paddle):
    if ball.colliderect(paddle):
        return True
    return False

# Biến lưu trữ mức độ hiện tại của trò chơi

ball_speed = [0,0]
current_level = 1
# Hàm reset trạng thái ban đầu của trò chơi và tăng mức độ khó
def reset_game():
    global current_level
    ball[0] = WINDOW_WIDTH // 2
    ball[1] = WINDOW_HEIGHT // 2
    ball_speed[0] = random.choice([-1, 1]) * (BALL_INITIAL_SPEED_X + current_level)  # Điều chỉnh tốc độ dựa trên mức độ khó
    ball_speed[1] = random.choice([-1, 1]) * (BALL_INITIAL_SPEED_Y + current_level)  # Điều chỉnh tốc độ dựa trên mức độ khó
    player_paddle.y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 3
    bot_paddle.y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 3

# Khởi tạo vị trí ban đầu của thanh và quả bóng
player_paddle = pygame.Rect(50, (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
bot_paddle = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, random.choice([-1, 1]) * BALL_INITIAL_SPEED_X, random.choice([-1, 1]) * BALL_INITIAL_SPEED_Y]

player_score = 0
bot_score = 0

level_results = {}
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_paddle(player_paddle, "up")
    if keys[pygame.K_s]:
        move_paddle(player_paddle, "down")

    # Di chuyển thanh bot để hứng quả bóng
    if ball[1] < bot_paddle.centery:
        move_paddle(bot_paddle, "up")
    elif ball[1] > bot_paddle.centery:
        move_paddle(bot_paddle, "down")

    # Di chuyển quả bóng
    ball[0] += ball[2]
    ball[1] += ball[3]

    # Xử lý va chạm với tường
    if check_wall_collision(ball):
        ball[3] *= -1

    # Xử lý va chạm với thanh
    if check_paddle_collision(pygame.Rect(ball[0], ball[1], BALL_SIZE, BALL_SIZE), player_paddle):
        ball[2] *= -1
        ball_speed[0] *= -1
        ball_speed[0] += 1  # Tăng tốc độ của quả bóng khi va chạm với thanh của người chơi
    elif check_paddle_collision(pygame.Rect(ball[0], ball[1], BALL_SIZE, BALL_SIZE), bot_paddle):
        ball_speed[0] *= -1
        ball[2] *= -1

    # Kiểm tra điều kiện thắng thua và reset trò chơi nếu cần
    if ball[0] <= 0:
        bot_score += 1
        level_results[current_level] = "Bot wins"
        reset_game()
    elif ball[0] >= WINDOW_WIDTH - BALL_SIZE:
        player_score += 1
        level_results[current_level] = "Player wins"
        reset_game()

    if player_score >= 3 or bot_score >= 3:
        level_results_text = font.render("Level Results: " "Level " + str(current_level), True, WHITE)
        result_text = font.render(level_results[current_level], True, WHITE)
        next_level_text = font.render("Press SPACE to continue to next level", True, WHITE)

        window.fill(BLACK)
        window.blit(level_results_text, (WINDOW_WIDTH // 2 - 100, 200))
        window.blit(result_text, (WINDOW_WIDTH // 2 - 100, 300))
        window.blit(next_level_text, (WINDOW_WIDTH // 2 - 200, 350))

        pygame.display.update()

        # Chờ người chơi nhấn SPACE để tiếp tục
        waiting_for_space = True
        while waiting_for_space:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_space = False

        # Tăng mức độ và chuẩn bị cho level mới
        current_level += 1
        player_score = 0
        bot_score = 0
        reset_game()

    # Xóa màn hình và vẽ lại đối tượng
    window.fill(BLACK)
    draw_paddle(player_paddle)
    draw_paddle(bot_paddle)
    draw_ball(ball)

    # Vẽ điểm số
    font = pygame.font.Font(None, 36)
    player_text = font.render("Player: " + str(player_score), True, WHITE)
    bot_text = font.render("Bot: " + str(bot_score), True, WHITE)
    window.blit(player_text, (20, 20))
    window.blit(bot_text, (WINDOW_WIDTH - 120, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
