import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Falling Ball")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
paddle_color = (0, 255, 0)

# Ball setup
ball_radius = 20
ball_x = random.randint(ball_radius, width - ball_radius)
ball_y = 0
ball_speed = 5

# Paddle setup
paddle_width = 100
paddle_height = 15
paddle_x = (width - paddle_width) // 2
paddle_y = height - 50
paddle_speed = 10

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Award text
def get_award(score):
    if score >= 50:
        return "🏅 Ultimate Award!"
    elif score >= 20:
        return "🎖 Silver Award!"
    elif score >= 10:
        return "🥉 Bronze Award!"
    return ""

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill(black)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed

    # Ball falling
    ball_y += ball_speed

    # Check catch
    if ball_y + ball_radius >= paddle_y:
        if paddle_x < ball_x < paddle_x + paddle_width:
            score += 1
            ball_y = 0
            ball_x = random.randint(ball_radius, width - ball_radius)
        elif ball_y > height:
            score = 0
            ball_y = 0
            ball_x = random.randint(ball_radius, width - ball_radius)

    # === Determine shape and color based on score milestone ===
    if score < 10:
        ball_shape = "circle"
        current_color = (255, 0, 0)         # Red
    elif score < 20:
        ball_shape = "square"
        current_color = (0, 0, 255)         # Blue
    elif score < 50:
        ball_shape = "triangle"
        current_color = (255, 255, 0)       # Yellow
    else:
        ball_shape = "star"
        current_color = (255, 105, 180)     # Pink

    # === Draw ball shape ===
    if ball_shape == "circle":
        pygame.draw.circle(screen, current_color, (ball_x, ball_y), ball_radius)
    elif ball_shape == "square":
        pygame.draw.rect(screen, current_color, (ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2))
    elif ball_shape == "triangle":
        point1 = (ball_x, ball_y - ball_radius)
        point2 = (ball_x - ball_radius, ball_y + ball_radius)
        point3 = (ball_x + ball_radius, ball_y + ball_radius)
        pygame.draw.polygon(screen, current_color, [point1, point2, point3])
    elif ball_shape == "star":
        points = []
        for i in range(10):
            angle = math.pi / 5 * i
            r = ball_radius if i % 2 == 0 else ball_radius // 2
            x = ball_x + int(r * math.cos(angle))
            y = ball_y + int(r * math.sin(angle))
            points.append((x, y))
        pygame.draw.polygon(screen, current_color, points)

    # Draw paddle
    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Draw score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Draw award text
    award = get_award(score)
    if award:
        award_text = font.render(award, True, white)
        screen.blit(award_text, (width - 300, 10))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
