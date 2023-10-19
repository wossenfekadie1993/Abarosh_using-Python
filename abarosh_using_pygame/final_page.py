import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the clock
clock = pygame.time.Clock()

# Set up the screen
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 690
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("አባሮሽ")


# Load the pause and resume images
pause_image = pygame.image.load("./images/pause.png")
resume_image = pygame.image.load("./images/resume.png")
button_size = (50, 50)
pause_image = pygame.transform.scale(pause_image, button_size)
resume_image = pygame.transform.scale(resume_image, button_size)

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up the score text and rectangle
score = 0
font = pygame.font.SysFont(None, 30)
score_text = font.render("Score: {}".format(score), True, white)
score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 10))

standing = pygame.image.load('./images/runner/standing.PNG')
player_speed = 5

# Set up the score text and rectangle
score = 0

# Set up the pause/resume button
pause_rect = pause_image.get_rect(center=(SCREEN_WIDTH// 2, SCREEN_HEIGHT // 2 + 100))

# Set up the chaser images
chaser_image = pygame.image.load('./images/runner/standing.PNG')
chaser_speed = 3
pygame.mixer.music.load('home.mp3')
pygame.mixer.music.play()
# Load and Size Images
stationary = pygame.image.load('./images/runner/standing.PNG')
right = [None]*6
for picIndex in range(1,5):
    right[picIndex-1] = pygame.image.load(f"images/runner/r{str(picIndex)}.png")
    picIndex+=1
    
left = [None]*6
for picIndex in range(1,5):
    left[picIndex-1] = pygame.image.load(f"images/runner/l{str(picIndex)}.png")
    picIndex+=1
    
up = [None]*6
for picIndex in range(1,5):
    up[picIndex-1] = pygame.image.load(f"images/runner/b{str(picIndex)}.png")
    picIndex+=1
    
down = [None]*6
for picIndex in range(1,5):
    down[picIndex-1] = pygame.image.load(f"images/runner/f{str(picIndex)}.png")
    picIndex+=1
    
#chaser position
right_chaser = [None]*6
for picIndex in range(1,5):
    right_chaser[picIndex-1] = pygame.image.load(f"images/chaser/r{str(picIndex)}.png")
    picIndex+=1

left_chaser = [None]*6
for picIndex in range(1,5):
    left_chaser[picIndex-1] = pygame.image.load(f"images/chaser/l{str(picIndex)}.png")
    picIndex+=1
        
up_chaser = [None]*6
for picIndex in range(1,5):
    up_chaser[picIndex-1] = pygame.image.load(f"images/chaser/b{str(picIndex)}.png")
    picIndex+=1
    
down_chaser = [None]*6
for picIndex in range(1,5):
    down_chaser[picIndex-1] = pygame.image.load(f"images/chaser/f{str(picIndex)}.png")

# Load the background image
background_image = pygame.image.load("./images/start.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image1 = pygame.image.load('./images/boy.png')
background_image1 = pygame.transform.scale(background_image1,(SCREEN_WIDTH//2,SCREEN_HEIGHT/1.5))
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
background_image2 = pygame.image.load("gameover.jpg")
background_image2 = pygame.transform.scale(background_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game variables
game_running = False
game_paused = False

# Display the home page
def home_page():
    welcome = True

    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_game() 
                elif quit_button.collidepoint(event.pos):
                    welcome = False

        # Draw the background image
        screen.blit(background_image, (0, 0))
        screen.blit(background_image1,(-60,220))

        # Draw the start button
        start_button_rect = pygame.Rect(SCREEN_WIDTH/ 2 - 75, SCREEN_HEIGHT / 2 + 100, 150, 50)
        border_radius = 10
        pygame.draw.rect(screen, green, start_button_rect, border_radius=border_radius)
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render("Start", True, black)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # Draw the quit button
        quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 200, 150, 50)
        pygame.draw.rect(screen, red, quit_button, border_radius=border_radius)
        stop_font = pygame.font.Font(None, 36)
        stop_text = stop_font.render("Quit", True, black)
        stop_text_rect = stop_text.get_rect(center=quit_button.center)
        screen.blit(stop_text, stop_text_rect)

        # Update the display
        pygame.display.update()
        
def start_game():
    global game_running, game_paused
    pygame.mixer.music.stop()
    game_running = True
    game_paused = False

    game_over = False
    
    # Set up the player classes
    class Player:
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
            self.rect = self.image.get_rect().inflate(-10,-10)
            self.rect = self.rect.inflate(-10, -10)
            self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            self.score = 0

        def update(self):
            if self.face_right:            
                for i in range(4):
                    self.image = self.right[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0

            elif self.face_left:
                for i in range(4):
                    self.image = self.left[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0
            elif self.face_up:
                for i in range(4):
                    self.image = self.up[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0
            elif self.face_down:
                for i in range(4):
                    self.image = self.down[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0

            self.stepIndex += 1
            if self.stepIndex >= 100:
                self.stepIndex = 0

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    # Set up the chaser classes
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
            self.rect = self.image.get_rect().inflate(-10,-10)
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

            # updating the image
            if self.face_right:
                for i in range(4):
                    self.image = self.right[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0
            elif self.face_left:
                for i in range(4):
                    self.image = self.left[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0
            elif self.face_up:
                for i in range(4):
                    self.image = self.up[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0
            elif self.face_down:
                for i in range(4):
                    self.image = self.down[self.stepIndex//25]
                    self.stepIndex += 1
                    if self.stepIndex >= 100:
                        self.stepIndex = 0

            self.stepIndex += 1
            if self.stepIndex >= 100:
                self.stepIndex = 0

        def draw(self, surface):
            surface.blit(self.image, self.rect)


    # Set up the player and chaser objects
    player = Player()
    chaser = Chaser()


    # Set up the game loop
    while game_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    game_running = False  # Exit the game loop
                    home_page() 
                # if back_button_rect.collidepoint(event.pos):
                #     game_running = False
                #     return
                # if start_button_rect.collidepoint(event.pos):  
                #     start_game() 
                # elif quit_button.collidepoint(event.pos):
                #     welcome = False
                elif pause_rect.collidepoint(event.pos):
                    game_paused = not game_paused  # Pause/resume the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    start_game()  # Restart the game 
                    
        if game_running and not game_paused:
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
                    # Update the score
                player.score += 1
                score_text = font.render("Score: {}".format(player.score), True, white)

                # Update the player and chaser
                player.update()
                chaser.update(player.rect)

                

                # Check for collisions
                if player.rect.colliderect(chaser.rect):
                    game_over = True

                # Draw the screen
                screen.blit(background,(0,0))
                player.draw(screen)
                chaser.draw(screen)
                screen.blit(score_text, score_rect)
        
        if game_over:
            game_over_screen(player.score)
           
            # # Hide the pause/resume button when game is over
            # pause_rect.center = (-100, -100)  # Move the button off the screen

        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        game_paused = not game_paused  # Toggle the game_paused variable

            if game_paused:
                # Draw the Resume button
                screen.blit(resume_image, pause_rect)
            else:
                # Draw the Pause button
                screen.blit(pause_image, pause_rect)
        

         # Draw the Back button
        border_radius = 10
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 200, 150, 50)
        pygame.draw.rect(screen, red, back_button_rect, border_radius=border_radius)
        stop_font = pygame.font.Font(None, 36)
        stop_text = stop_font.render("Back", True, black)
        stop_text_rect = stop_text.get_rect(center=back_button_rect.center)
        screen.blit(stop_text, stop_text_rect)
        
        if game_paused:
            screen.blit(resume_image, pause_rect)
        else:
            screen.blit(pause_image, pause_rect)

        # Update the screen
        pygame.display.update()
        # Set the game's FPS
        clock.tick(60)
        # Quit the game
    pygame.quit()

def game_over_screen(score):
    global game_running
    game_over = True
    pygame.mixer.music.load('gameover.mp3')
    pygame.mixer.music.play()
    # Set up the game over flag and message
    font = pygame.font.SysFont(None, 50)
    game_over_msg = font.render("", True, red)
    game_over_rect = game_over_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Set up the restart button
    restart_button_rect = pygame.Rect(SCREEN_WIDTH/ 2 - 75, SCREEN_HEIGHT / 2 + 100, 150, 50)
    border_radius = 10
    pygame.draw.rect(screen, green, restart_button_rect, border_radius=border_radius)
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Restart", True, black)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)
   

    # Set up the score text and rectangle
    score_text = font.render("Score: {}".format(score), True, white)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
    

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    game_running = True
                    start_game()

        screen.blit(background_image2, (0, 0))
        screen.blit(background_image1, (20, 180))
        screen.blit(game_over_msg, game_over_rect)
        screen.blit(restart_text, restart_button_rect)
        screen.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(60)


# Call the function to display the welcome page
home_page()
