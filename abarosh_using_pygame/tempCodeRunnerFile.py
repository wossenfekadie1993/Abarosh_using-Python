 # Set up the game over flag and message
    font = pygame.font.SysFont(None, 50)
    game_over_msg = font.render("Game Over", True, red)
    game_over_rect = game_over_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))