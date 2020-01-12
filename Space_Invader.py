import pygame
import random
import math

# Initialize Pygame
pygame.init()

# player class
class player:
        image = pygame.image.load('player.png')
        x_coord = 370
        y_coord = 480
        delta_x = 0

# enemy class
class enemy:
        image = pygame.image.load('ufo.png')
        x_coord = 0
        y_coord = 0
        delta_x = 6
        delta_y = 40

        def __init__ (self, x_value, y_value):
            self.x_coord = x_value
            self.y_coord = y_value

        # bullet class
class bullet:
        image = pygame.image.load('bullet.png')
        x_coord = 0
        y_coord = 480
        delta_x = 0
        delta_y = 50
        state = "ready"

# -- SET_UP THE GAME --

# Window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")

# Score
score_value = 0
score_text_x = 10
score_text_y = 10

# font (Score)
font = pygame.font.Font('freesansbold.ttf', 32)

# font (Game Over)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function which render the score text
def render_show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit (score, (x, y))

# Function which render the Game Over text
def render_game_over_text():
    gg_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gg_text, (200, 250))

# Creating player object
player_Obj= player()

# Creating bullet object
bullet_Obj = bullet()

# Creating enemy objects
# TODO: Adjust the number of enemies depending on level of difficulty
num_of_enemies = 6
# Array of enemy objects
enemy_objs = []
for i in range (0, num_of_enemies):
    enemy_objs.append (enemy(random.randint(0, 800), random.randint(50, 150)))

# Function that render the player image
def render_player (x, y):
    screen.blit(player_Obj.image, (x, y))

# Function that render the enemy image
def render_enemy (x, y, i):
    screen.blit(enemy_objs[i].image, (x, y))

# Function that render the bullet image
def render_bullet (x, y):
    # global bullet_Obj.state
    bullet_Obj.state = "fire"
    screen.blit(bullet_Obj.image, (x + 16, y + 10))

# Collision engines b/w bullet & enemy
def isCollision (enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False

# Declare control parameters for the game while loops
running = False
intro = True

# Initialize color RGB values for easy passing
dark_green = (0, 255, 0)
dark_red = (255, 0, 0)
bright_green = (0, 200, 0)
bright_red = (200, 0, 0)

# -- RUNNING CODE --
# INTRO Screen

# Provide functionalities to the buttons
def button_func (button_msg, x_pos, y_pos, width, height, inactive, active, function):
    # TODO: Add button texts on the buttons
    # Definition of mouse position
    mouse = pygame.mouse.get_pos()
    # Definition of mouse click
    click = pygame.mouse.get_pressed()

    # Getting the position of the mouse
    mouse = pygame.mouse.get_pos()
    # If statement to see if the mouse position is with the rectangles
    if x_pos + width > mouse[0] > x_pos and y_pos + height > mouse[1] > y_pos:
        pygame.draw.rect(screen, active, (x_pos, y_pos, width, height))

        if click[0] == 1 and function != None:
            if function is "Start_the_game":
                global running
                running = True
                global intro
                intro = False
            else:
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, inactive, (x_pos, y_pos, width, height))

# Executing intro screen
while intro:
    #TODO: Better intro screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
    screen.fill((0, 0, 0))
    # Displaying the title of the game
    start_screen_font = pygame.font.Font('freesansbold.ttf', 64)
    intro_text = start_screen_font.render("Space Invader", True, (255, 255, 255))
    screen.blit(intro_text, (200, 250))

    # Making the buttons (rectangles)
    # Green - Play the game
    pygame.draw.rect(screen, (0, 200, 0), (150, 450, 100, 50))
    # Red - Quit the game
    pygame.draw.rect(screen, (200, 0, 0), (550, 450, 100, 50))

    # Adding functionality to the buttons
    button_func("Start", 150, 450, 100, 50, dark_green, bright_green, "Start_the_game")
    button_func("Quit", 550, 450, 100, 50, dark_red, bright_red, "Quit_the_game")
    pygame.display.update()

# Game window, run continuously
while running:
    screen.fill((0, 0, 0))

    # Check if the user is closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic when a key is pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_Obj.delta_x = -20
        if event.key == pygame.K_RIGHT:
            player_Obj.delta_x = 20
        if event.key == pygame.K_SPACE:
            if bullet_Obj.state is "ready":
                # Ensure when the bullet is fired, it is not following movement of the player
                bullet_Obj.x_coord = player_Obj.x_coord
                render_bullet (player_Obj.x_coord, bullet_Obj.y_coord)

    # Logic when a key is released
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            player_Obj.delta_x = 0

    # Player Movement Calculation
    player_Obj.x_coord += player_Obj.delta_x

    # State 1: Make sure the spaceship does not go out of bounds
    if player_Obj.x_coord <= 0:
        player_Obj.x_coord = 0
    elif player_Obj.x_coord >= 736: #800 - 64 (64x64 image)
        player_Obj.x_coord = 736

    # Enemy Movement (Automatic)
    for i in range (0, num_of_enemies):
        # State 1: When an enemy reaches y_coord > 240, touching the player
        if enemy_objs[i].y_coord > 240:
            for j in range (0, num_of_enemies):
                enemy_objs[j].y_coord = 20000
                render_game_over_text()
                break

        # Making enemies move
        enemy_objs[i].x_coord += enemy_objs[i].delta_x

        # State 2: When the enemy touches the border, bounce back
        if enemy_objs[i].x_coord <= 0:
            enemy_objs[i].delta_x *= -1
            enemy_objs[i].y_coord += enemy_objs[i].delta_y
        elif enemy_objs[i].x_coord >= 736: # 800 - 64 (64 x 64 image)
            enemy_objs[i].delta_x *= -1
            enemy_objs[i].y_coord += enemy_objs[i].delta_y

        # State 3: When the enemy collide with the bullet
        collision = isCollision(enemy_objs[i].x_coord, enemy_objs[i].y_coord, bullet_Obj.x_coord, bullet_Obj.y_coord)
        if collision:
            bullet_Obj.y_coord = 480
            bullet_Obj.state = "ready"
            score_value += 1
            # If the enemy collided with the bullet, the position changes
            enemy_objs[i].x_coord = random.randint(0, 800)
            enemy_objs[i].y_coord = random.randint(50, 150)

        render_enemy(enemy_objs[i].x_coord, enemy_objs[i].y_coord, i)

    # Bullet Movement
    # Returning to original position, ready to shoot
    if bullet_Obj.y_coord <= 0:
        bullet_Obj.y_coord = 480
        bullet_Obj.state = "ready"
    # When spacebar is hit
    if bullet_Obj.state is "fire":
        render_bullet (bullet_Obj.x_coord, bullet_Obj.y_coord)
        bullet_Obj.y_coord -= bullet_Obj.delta_y

    render_player(player_Obj.x_coord, player_Obj.y_coord)
    render_show_score(score_text_x, score_text_y)
    pygame.display.update()





