import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 350
PLAYER_SPEED = 5
OBSTACLE_SPEED = 5
GRAVITY = 0.7
JUMP_STRENGTH = -10

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Witch Game")

# Load and resize images
background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("witch.png"), (64, 64))
heart_img = pygame.transform.scale(pygame.image.load("heart.png"), (20, 20))
obstacle_img = pygame.transform.scale(pygame.image.load("cloud.png"), (50, 50))

# Player variables
player_x = 100
player_y = (HEIGHT - player_img.get_height()) / 2  # Start vertically centered
player_dy = 0
lives = 3
score = 0
game_running = True

# Font
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# Obstacles
obstacles = []

# Clock
clock = pygame.time.Clock()

def draw_lives():
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 30, 10))

def spawn_obstacle():
    y = random.randint(50, HEIGHT - 100)
    x = WIDTH
    obstacles.append(pygame.Rect(x, y, 60, 60))

def draw_obstacles():
    for obs in obstacles:
        screen.blit(obstacle_img, obs.topleft)

def move_obstacles():
    global score
    for obs in obstacles[:]:
        obs.x -= OBSTACLE_SPEED
        if obs.right < 0:
            obstacles.remove(obs)
            score += 1

def check_collision(player_rect):
    global lives, game_running
    for obs in obstacles[:]:
        if player_rect.colliderect(obs):
            obstacles.remove(obs)
            lives -= 1
            if lives <= 0:
                game_running = False

def show_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def main():
    global player_y, player_dy, game_running

    spawn_timer = 0

    # Define floor at middle of screen vertically
    floor_y = (HEIGHT - player_img.get_height()) / 2

    while True:
        clock.tick(60)
        screen.blit(background, (0, 0))  # Clear screen each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_running and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_dy = JUMP_STRENGTH

        if game_running:
            # Apply gravity and update player vertical position
            player_dy += GRAVITY
            player_y += player_dy

            # Prevent player going above top
            if player_y < 0:
                player_y = 0
                player_dy = 0
            # Prevent player falling below floor (middle line)
            if player_y > floor_y:
                player_y = floor_y
                player_dy = 0

            player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())

            # Spawn obstacles every ~2 seconds
            spawn_timer += clock.get_time()
            if spawn_timer > 2000:
                spawn_obstacle()
                spawn_timer = 0

            move_obstacles()
            draw_obstacles()
            check_collision(player_rect)
            screen.blit(player_img, (player_x, player_y))
            draw_lives()
            show_text(f"Score: {score}", font, (255, 255, 255), WIDTH - 150, 10)

        else:
            show_text("Game Over", big_font, (255, 0, 0), WIDTH // 2 - 100, HEIGHT // 2 - 24)
            show_text(f"Final Score: {score}", font, (255, 255, 255), WIDTH // 2 - 70, HEIGHT // 2 + 30)
            show_text("Press ESC to Quit", font, (255, 255, 255), WIDTH // 2 - 80, HEIGHT // 2 + 70)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()
