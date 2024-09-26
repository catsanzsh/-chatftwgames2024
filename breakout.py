import pygame
import random
import numpy as np

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game settings
BALL_SPEED = 5
PADDLE_SPEED = 10
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_PADDING = 10

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout')

# Sound generation using numpy
def generate_sound(frequency=440, duration=0.1, volume=1.0):
    sample_rate = 44100
    samples = np.sin(2 * np.pi * np.arange(sample_rate * duration) * frequency / sample_rate).astype(np.float32)
    sound = np.zeros((samples.shape[0], 2), dtype=np.float32)
    sound[:, 0] = samples * volume  # left channel
    sound[:, 1] = samples * volume  # right channel

    sound_array = (sound * 32767).astype(np.int16)
    sound_obj = pygame.sndarray.make_sound(sound_array)
    sound_obj.play()

# Define the ball
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, 20, 20)
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
            generate_sound(frequency=500, duration=0.05)  # Wall bounce sound

        if self.rect.top <= 0:
            self.dy = -self.dy
            generate_sound(frequency=500, duration=0.05)  # Ceiling bounce sound

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Define the paddle
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, 100, 10)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

# Define the bricks
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Function to create the bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
            y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING
            bricks.append(Brick(x, y))
    return bricks

# Game loop
def main():
    ball = Ball()
    paddle = Paddle()
    bricks = create_bricks()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move paddle with keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_RIGHT]:
            paddle.move(PADDLE_SPEED)

        # Move ball
        ball.move()

        # Ball collision with paddle
        if ball.rect.colliderect(paddle.rect):
            ball.dy = -ball.dy
            generate_sound(frequency=700, duration=0.1)  # Paddle hit sound

        # Ball collision with bricks
        for brick in bricks:
            if ball.rect.colliderect(brick.rect):
                ball.dy = -ball.dy
                bricks.remove(brick)
                generate_sound(frequency=300, duration=0.1)  # Brick hit sound
                break

        # Check if ball hits the bottom of the screen
        if ball.rect.bottom >= SCREEN_HEIGHT:
            print("Game Over!")
            running = False

        # Draw objects
        ball.draw(screen)
        paddle.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
