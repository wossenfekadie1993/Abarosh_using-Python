import math
import random
import pygame

# Set up the screen
SCREEN_WIDTH = 940
SCREEN_HEIGHT = 680
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Abarosh")

# Set up the clock
clock = pygame.time.Clock()

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

standing = pygame.image.load('./images/runner/standing.PNG')
player_speed = 5

# Set up the restart button
font = pygame.font.SysFont(None, 48)
restart_text = font.render("Restart", True, WHITE)
restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

# Set up the chaser images
chaser_image = pygame.image.load('./images/runner/standing.PNG')
chaser_speed = random.randint(1, 2)


# Load and Size Images
stationary = pygame.image.load('./images/runner/standing.PNG')
right = [None]*10
for picIndex in range(1,9):
    right[picIndex-1] = pygame.image.load(f"images/runner/r{str(picIndex)}.png")
    picIndex+=1
    
left = [None]*10
for picIndex in range(1,9):
    left[picIndex-1] = pygame.image.load(f"images/runner/l{str(picIndex)}.png")
    picIndex+=1
    
up = [None]*10
for picIndex in range(1,9):
    up[picIndex-1] = pygame.image.load(f"images/runner/b{str(picIndex)}.png")
    picIndex+=1
    
down = [None]*10
for picIndex in range(1,9):
    down[picIndex-1] = pygame.image.load(f"images/runner/f{str(picIndex)}.png")
    picIndex+=1
    
#chaser position
right_chaser = [None]*10
for picIndex in range(1,9):
    right_chaser[picIndex-1] = pygame.image.load(f"images/runner/r{str(picIndex)}.png")
    picIndex+=1

left_chaser = [None]*10
for picIndex in range(1,9):
    left_chaser[picIndex-1] = pygame.image.load(f"images/runner/l{str(picIndex)}.png")
    picIndex+=1
    
up_chaser = [None]*10
for picIndex in range(1,9):
    up_chaser[picIndex-1] = pygame.image.load(f"images/runner/b{str(picIndex)}.png")
    picIndex+=1
    
down_chaser = [None]*10
for picIndex in range(1,9):
    down_chaser[picIndex-1] = pygame.image.load(f"images/runner/f{str(picIndex)}.png")

# Set up the game over flag and message
font = pygame.font.SysFont(None, 50)
game_over = False
game_over_msg = font.render("Game Over", True, RED)
game_over_rect = game_over_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Set up the score text and rectangle
score = 0
font = pygame.font.SysFont(None, 30)
score_text = font.render("Score: {}".format(score), True, WHITE)
score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 10))

# Set up the player and chaser classes
class Hero:
    def __init__(self):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.face_right = True
        self.face_left = False
        self.face_up = False
        self.face_down = False
        self.stepIndex = 0
        self.image = standing
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def update(self):
        if self.face_right:
            self.image = self.right[self.stepIndex//14]
        elif self.face_left:
            self.image = self.left[self.stepIndex//14]
        elif self.face_up:
            self.image = self.up[self.stepIndex//14]
        elif self.face_down:
            self.image = self.down[self.stepIndex//14]

        self.stepIndex += 1
        if self.stepIndex >= 99:
            self.stepIndex = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Chaser:
    def __init__(self):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.face_right = True
        self.face_left = False
        self.face_up = False
        self.face_down = False
        self.stepIndex = 0
        self.image = standing
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def update(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist != 0:
            self.rect.x += chaser_speed * dx / dist
            self.rect.y += chaser_speed * dy / dist

        if dx <= -1 and dx > dy:
            self.face_left = True
            self.face_right = False
            self.face_up = False
            self.face_down = False
        elif dx >= 1 and dx > dy:
            self.face_right = True
            self.face_left = False
            self.face_up = False
            self.face_down = False
        if dy < -1 and dx < dy:
            self.face_right = False
            self.face_left = False
            self.face_up = True
            self.face_down = False
        elif dy > 1 and dx < dy:
            self.face_right = False
            self.face_left = False
            self.face_down = True
            self.face_up = False
        if self.face_right:
            self.image = self.right[self.stepIndex//14]
        elif self.face_left:
            self.image = self.left[self.stepIndex//14]
        elif self.face_up:
            self.image = self.up[self.stepIndex//14]
        elif self.face_down:
            self.image = self.down[self.stepIndex//14]

        self.stepIndex += 1
        if self.stepIndex >= 99:
            self.stepIndex = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Set up the player and chaser objects
player = Hero()
chaser = Chaser()

run = True
# Set up the game loop
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    if not game_over:
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.rect.x <= SCREEN_WIDTH - 62:
            player.rect.x += player_speed
            player.face_right = True
            player.face_left = False
            player.face_up = False
            player.face_down = False
        elif keys[pygame.K_LEFT] and player.rect.x >= 0:
            player.rect.x -= player_speed
            player.face_right = False
            player.face_left = True
            player.face_up = False
            player.face_down = False
        elif keys[pygame.K_DOWN] and player.rect.y <= SCREEN_HEIGHT - 62:
            player.rect.y += player_speed
            player.face_right = False
            player.face_left = False
            player.face_up = False
            player.face_down = True
        elif keys[pygame.K_UP] and player.rect.y >= 0:
            player.rect.y -= player_speed
            player.face_right = False
            player.face_left = False
            player.face_up = True
            player.face_down = False
        else:
            player.stepIndex = 0

        # Update the player and chaser
        player.update()
        chaser.update(player.rect)

        # Check for collisions
        if player.rect.colliderect(chaser.rect):
            game_over = True

        # Draw the screen
        screen.fill(BLACK)
        player.draw(screen)
        chaser.draw(screen)
        screen.blit(score_text, score_rect)


        # Check for game over
        if game_over:
            screen.blit(game_over_msg, game_over_rect)
            screen.blit(restart_text, restart_rect)

        # Update the score
        score += 1
        score_text = font.render("Score: {}".format(score), True, WHITE)
        
    # Update the display
    pygame.display.flip()

    # Set the game's FPS
    clock.tick(60)

# Quit the game
pygame.quit()