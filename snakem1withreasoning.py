# Date: 2021-09-26

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
fps = 60

def main():
    # Directions: up, right, down, left
    directions = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    
    snake_speed = 15
    snake_positions = [(200, 200), (220, 200), (240, 200)]
    direction = 'right'
    food_position = get_random_food_position(snake_positions)
    score = 0

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'

        head = snake_positions[-1]
        new_head_position = (head[0] + directions[direction][0]*snake_speed, 
                            head[1] + directions[direction][1]*snake_speed)

        # Check for collision with food
        if new_head_position == food_position:
            score += 1
            food_position = get_random_food_position()
        else:
            snake_positions.pop(0)
        
        # Add new head position to the snake
        snake_positions.append(new_head_position)

        # Collision with wall or self
        if (new_head_position[0] < 0 or 
            new_head_position[0] > SCREEN_WIDTH - 10 or 
            new_head_position[1] < 0 or 
            new_head_position[1] > SCREEN_HEIGHT - 10 or 
            new_head_position in snake_positions[:-1]):
            print(f"Game Over! Your score: {score}")
            pygame.quit()
            sys.exit()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        for pos in snake_positions:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, RED, (food_position[0], food_position[1], 10, 10))
        pygame.display.flip()

def get_random_food_position(snake_positions):
    while True:
        x = random.randint(0, SCREEN_WIDTH - 10) // 10 * 10
        y = random.randint(0, SCREEN_HEIGHT - 10) // 10 * 10
        if (x, y) not in snake_positions:
            return (x, y)

if __name__ == "__main__":
    main()
 # 


