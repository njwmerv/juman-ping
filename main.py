import pygame
import os # used to define path to assets
pygame.font.init()
pygame.mixer.init() # sound

# Making a window/main surface
# PYGAME Coordinate System -> origin is top left corner
# images will be drawn starting from top left
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
FPS = 60 # how many times game updates per second
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, 500)
PAUSE_TIME = 2500

#COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#SPACESHIP
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SHIP_VEL = 5

#BULLET
BULLET_VEL = 7.5
MAX_BULLETS = 3

#FONTS
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("arial", 150)

#SOUNDS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("First Pygame Game","Assets","Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("First Pygame Game","Assets","Gun+Silencer.mp3"))

#USER EVENTS
YELLOW_HIT = pygame.USEREVENT + 1 # code number for userevents
RED_HIT = pygame.USEREVENT + 2

#IMAGES
SPACE_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("First Pygame Game","Assets","space.png")), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("First Pygame Game","Assets","spaceship_yellow.png")) #could be a string but separator of path is inconsistent
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # North is 0

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("First Pygame Game","Assets","spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    #WIN.fill(WHITE) # just this alone deosnt work. need to update display
    WIN.blit(SPACE_BACKGROUND_IMAGE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER) # rect(surface, colour, rect)
    # order matters, if fill is last, covers whole screen

    red_hp_text = HEALTH_FONT.render("Health: "+str(red_hp), 1, WHITE) # creating text objects
    yellow_hp_text = HEALTH_FONT.render("Health: "+str(yellow_hp), 1, WHITE)
    WIN.blit(red_hp_text, (WIDTH - red_hp_text.get_width() - 10, 10))
    WIN.blit(yellow_hp_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # drawing a surface onto screen --> what the ship sprites are
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() # actually updates it to change colour

def yellow_handle_movement(keys_pressed, ship):
    if keys_pressed[pygame.K_a] and ship.x - SHIP_VEL > 0: #LEFT
        ship.x -= SHIP_VEL
    if keys_pressed[pygame.K_d] and ship.x + SHIP_VEL + ship.width < BORDER.x: #right
        ship.x += SHIP_VEL
    if keys_pressed[pygame.K_w] and ship.y - SHIP_VEL > 0: #UP
        ship.y -= SHIP_VEL
    if keys_pressed[pygame.K_s] and ship.y + SHIP_VEL + ship.height < HEIGHT - 10: #DOWN
        ship.y += SHIP_VEL

def red_handle_movement(keys_pressed, ship):
    if keys_pressed[pygame.K_LEFT] and ship.x - SHIP_VEL > BORDER.x + BORDER.width: #LEFT
        ship.x -= SHIP_VEL
    if keys_pressed[pygame.K_RIGHT] and ship.x + SHIP_VEL < WIDTH - ship.width: #right
        ship.x += SHIP_VEL
    if keys_pressed[pygame.K_UP] and ship.y - SHIP_VEL > 0: #UP
        ship.y -= SHIP_VEL
    if keys_pressed[pygame.K_DOWN] and ship.y + SHIP_VEL + ship.height < HEIGHT - 10: #DOWN
        ship.y += SHIP_VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) # posting an event then check for it in main()
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # posting an event then check for it in main()
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(PAUSE_TIME)

def main(): #main game loop
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_hp = 10
    red_bullets = []
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_hp = 10
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
  
    while run:
        clock.tick(FPS) # caps frame rate
        for event in pygame.event.get(): # list of all events and we're looping through them
            if event.type == pygame.QUIT: # when X button top right is clicked
                run = False
                pygame.quit() # since later one is commented out
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_hp -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_hp -= 1
                BULLET_HIT_SOUND.play()

        # yellow.x += 1 # 60 pixels/s
        # WASD for yellow, Arrows for red
        # this method allows multiple button presses at once
        keys_pressed = pygame.key.get_pressed() # gets what keys are being pressed down
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # BULLETS
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # UPDATE SCREEN
        draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)

        # WINNER?
        winner_text = ""
        if red_hp <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_hp <= 0:
            winner_text = "RED WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

    #pygame.quit()
    main() # restart game when over

if __name__ == "__main__": # only run this code if run through this file, not if imported # if name of file is main
    main()
