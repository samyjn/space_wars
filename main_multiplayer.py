import pygame
import os

pygame.init()
WIDTH = 1280
HEIGHT =720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('multiplayer')

BORDER = pygame.Rect(635, 0, 10, 720)

VEL = 10     #velocity of spaceships

MAX_BULLETS = 10
VEL_BULLETS = 12


RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2


HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

SPACESHIP_WIDTH = 80
SPACESHIP_HEIGHT = 87

SPACE = pygame.image.load(os.path.join('assets_multiplayer','space.png'))

RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BLUE_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def draw_window_mult(red,blue,red_bullets,blue_bullets,red_health,blue_health):
    WIN.blit(SPACE, (0,0))
    
    red_health_text = HEALTH_FONT.render('Health: '+ str(red_health),1,(255,255,255))
    blue_health_text = HEALTH_FONT.render('Health: '+ str(blue_health),1,(255,255,255))
    WIN.blit(red_health_text, (10,10))
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width()-10,10))
    
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    WIN.blit(RED_SPACESHIP, (red.x,red.y))
    WIN.blit(BLUE_SPACESHIP,(blue.x,blue.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, ((255,0,0)), bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(WIN, ((0,0,255)), bullet)

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < (BORDER.x-SPACESHIP_HEIGHT):
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + SPACESHIP_WIDTH + VEL < HEIGHT:
        red.y += VEL

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > BORDER.x + 10:
        blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x +SPACESHIP_HEIGHT + VEL < 1280:
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0:
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + SPACESHIP_WIDTH + VEL < 720:
        blue.y += VEL

def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += VEL_BULLETS
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
            
    for bullet in blue_bullets:
        bullet.x -= VEL_BULLETS
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

def draw_winner(winner_text):
    winner_text = WINNER_FONT.render(winner_text, 1, (255,255,255))
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(20, 315, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Rectange of red spaceship
    blue = pygame.Rect(1170, 315, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Rectange of blue spaceship

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    winner_text = ''

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + SPACESHIP_HEIGHT, red.y + (SPACESHIP_WIDTH)//2, 8, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + (SPACESHIP_WIDTH)//2, 8, 5)
                    blue_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == BLUE_HIT:
                blue_health -= 1
        

        if red_health <= 0:
            winner_text = 'BLUE WINS!'
        if blue_health <=0:
            winner_text = 'RED WINS!'
        if winner_text != '':
            draw_winner(winner_text)  
            break

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        blue_handle_movement(keys_pressed, blue)
        handle_bullets(red_bullets, blue_bullets, red, blue)
        
        draw_window_mult(red, blue, red_bullets, blue_bullets,red_health,blue_health)

    main()
    
main()