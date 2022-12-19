import pygame
import os
import random
import math
import sys
from pygame import mixer

pygame.init()
pygame.mixer.init()

WIDTH = 1280
HEIGHT =720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Space Wars')

SPACE = pygame.image.load(os.path.join('assets_multiplayer','space.png'))
MAIN_BG = pygame.image.load('main_bg.jpg')
logo_img = pygame.image.load('logo.png')
logo = pygame.transform.scale(logo_img, (450,325))

clock = pygame.time.Clock()

# Main menu buttons

font = pygame.font.SysFont('georgia', 30)
pause_font = pygame.font.SysFont('georgia', 50, bold=True)
surf1 = font.render('SINGLEPLAYER', 1, (255,255,255))
surf2 = font.render('MULTIPLAYER', 1, (255,255,255))
surf3 = font.render('QUIT', 1, (255,255,255))
button1 = pygame.Rect(WIDTH/2 - surf1.get_width()/2, 370, surf1.get_width()+10, surf1.get_height()+10)
button2 = pygame.Rect(WIDTH/2 - surf2.get_width()/2, 450, surf2.get_width()+10, surf2.get_height()+10)
button3 = pygame.Rect(WIDTH/2 - surf3.get_width()/2, 530, surf3.get_width()+10, surf3.get_height()+10)


# Pause menu buttons

surf4 = font.render('RESUME', 1, (255,255,255))
surf5 = font.render('MAIN MENU', 1, (255,255,255))
surf6 = font.render('QUIT', 1, (255,255,255))
button4 = pygame.Rect(200, 300, surf4.get_width()+10, surf4.get_height()+10)
button5 = pygame.Rect(200, 400, surf5.get_width()+10, surf5.get_height()+10)
button6 = pygame.Rect(200, 500, surf6.get_width()+10, surf6.get_height()+10)

bullet_fire_sound = pygame.mixer.Sound(os.path.join('assets_singleplayer','laser.wav'))
mixer.music.load(os.path.join('assets_singleplayer','background.wav'))
mixer.music.play(-1)

def draw_window_uni():
    WIN.blit(MAIN_BG, (0,0))
    WIN.blit(logo, (WIDTH/2 - 225, 20))
    
    a,b = pygame.mouse.get_pos()

    if button1.x <= a <= button1.x + surf1.get_width()+10 and button1.y <= b <= button1.y + surf1.get_height()+10:
        pygame.draw.rect(WIN, (180,180,180), button1)
    else:
        pygame.draw.rect(WIN, (110,110,110), button1)
    
    if button2.x <= a <= button2.x + surf2.get_width()+10 and button2.y <= b <= button2.y + surf2.get_height()+10:
        pygame.draw.rect(WIN, (180,180,180), button2)
    else:
        pygame.draw.rect(WIN, (110,110,110), button2)
    
    if button3.x <= a <= button3.x + surf3.get_width()+10 and button3.y <= b <= button3.y + surf3.get_height()+10:
        pygame.draw.rect(WIN, (180,180,180), button3)
    else:
        pygame.draw.rect(WIN, (110,110,110), button3)

    
    
    WIN.blit(surf1, (button1.x+5,button1.y+5))
    WIN.blit(surf2, (button2.x+5,button2.y+5))
    WIN.blit(surf3, (button3.x+5,button3.y+5))

    pygame.display.update()

def pause():
    transparent_bg_org = pygame.image.load('transparent_bg.png')
    transparent_bg = pygame.transform.scale(transparent_bg_org, (1280,720))
    WIN.blit(transparent_bg, (0,0))
    a,b = pygame.mouse.get_pos()
    clock.tick(60)
    paused = True
    while paused:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button4.collidepoint(event.pos):
                    paused = False
                if button5.collidepoint(event.pos):
                    main_game_uni()
                if button6.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        
    
        if button4.x <= a <= button4.x + surf4.get_width()+10 and button4.y <= b <= button4.y + surf4.get_height()+10:
            pygame.draw.rect(WIN, (180,180,180), button4)
        else:
            pygame.draw.rect(WIN, (110,110,110), button4)

        if button5.x <= a <= button5.x + surf5.get_width()+10 and button5.y <= b <= button5.y + surf5.get_height()+10:
            pygame.draw.rect(WIN, (180,180,180), button5)
        else:
            pygame.draw.rect(WIN, (110,110,110), button5)

        if button6.x <= a <= button6.x + surf6.get_width()+10 and button6.y <= b <= button6.y + surf6.get_height()+10:
            pygame.draw.rect(WIN, (180,180,180), button6)
        else:
            pygame.draw.rect(WIN, (110,110,110), button6)  

        pause_text = pause_font.render('PAUSE MENU:', 1, (255,255,255)) 
        WIN.blit(pause_text, (200,200))
        WIN.blit(surf4, (button4.x+5,button4.y+5))
        WIN.blit(surf5, (button5.x+5,button5.y+5))
        WIN.blit(surf6, (button6.x+5,button6.y+5))

        pygame.display.update()


# MULTIPLAYER VARIABLES AND DEFINATIONS-    

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


RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BLUE_SPACESHIP_IMG = pygame.image.load(os.path.join('assets_multiplayer','spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


def draw_window_mult(red,blue,red_bullets,blue_bullets,red_health,blue_health):
    SPACE = pygame.image.load(os.path.join('assets_multiplayer','mult_bg.jpg'))
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
        pygame.draw.rect(WIN, ((255,255,255)), bullet)

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
    main_game_uni()

def main_mult():
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
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + (SPACESHIP_WIDTH)//2, 8, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_p:
                    pause()

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




# SINGLEPLAYER VARIABLES AND DEFINATIONS

MAX_BULLETS = 3
VEL_BULLETS = 16

enemy_hit = pygame.USEREVENT + 3


SCORE_FONT = pygame.font.SysFont('comicsans', 25)
game_over_font = pygame.font.SysFont('comicsans', 100)
over_text = "WASTED"


PLAYER_WIDTH = 60
PLAYER_HEIGHT = 67
PLAYER_VEL = 12

PLAYER_IMG = pygame.image.load(os.path.join('assets_singleplayer','player_singleplayer.png'))
PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH,PLAYER_HEIGHT)),90)

ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35
NUM_ENEMY = 6
ENEMY_IMG = pygame.image.load(os.path.join('assets_singleplayer','enemy_singleplayer.png'))
ENEMY = []
ENEMY_Y_CHANGE = []
for i in range(NUM_ENEMY):
    ENEMY.append(pygame.transform.rotate(pygame.transform.scale(ENEMY_IMG, (ENEMY_WIDTH,ENEMY_HEIGHT)),90))
    ENEMY_Y_CHANGE.append(7)

BULLET_IMG = pygame.image.load(os.path.join('assets_singleplayer',"bullet_singleplayer.png"))


def draw_window_sing(player,enemy,BULLETS,score_value):
    WIN.blit(SPACE, (0,0))

    score_text = SCORE_FONT.render('Score: ' + str(score_value), 1, (255,255,255))
    WIN.blit(score_text, (10,10))
    WIN.blit(PLAYER, (player.x, player.y))
    for i in range(NUM_ENEMY):
        WIN.blit(ENEMY[i], (enemy[i].x,enemy[i].y))
    
    for bullet in BULLETS:
        pygame.draw.rect(WIN, ((255,255,255)), bullet)

    pygame.display.update()

def over(over_text,score_value):
    over_text1 = "YOU SCORED: " + str(score_value)
    text = game_over_font.render(over_text, 1, (255,255,255))
    text1 = SCORE_FONT.render(over_text1, 1, (0,255,0))
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    WIN.blit(text1,(WIDTH/2 - text1.get_width()/2, HEIGHT/2 - text.get_height()/2+200))
    pygame.display.update()
    pygame.time.delay(3000)
    main_game_uni()

def player_handle_movement(player,keys_pressed):
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VEL > 0:
        player.y -= PLAYER_VEL
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_WIDTH + PLAYER_VEL< HEIGHT:
        player.y += PLAYER_VEL
    
def enemy_handle_movement(enemy):
    for i in range(NUM_ENEMY):
        enemy[i].y -= ENEMY_Y_CHANGE[i]
        if enemy[i].y < 0:
            ENEMY_Y_CHANGE[i] = -7
            enemy[i].x += 120
        elif enemy[i].y + ENEMY_WIDTH > HEIGHT:
            ENEMY_Y_CHANGE[i] = +7
            enemy[i].x += 120

def handle_bullets_sing(BULLETS,enemy):
    for bullet in BULLETS:
        bullet.x -= VEL_BULLETS
        for i in range(NUM_ENEMY):
            if enemy[i].colliderect(bullet):
                BULLETS.remove(bullet)
                pygame.event.post(pygame.event.Event(enemy_hit))
                enemy[i].x = random.randint(300,350)
                enemy[i].y = random.randint(0, 720)
                

        if bullet.x < 0:
            BULLETS.remove(bullet)



def main_sing():
    score_value = 0
    player = pygame.Rect(980, 315, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy = []
    for i in range(NUM_ENEMY):
        enemy.append(pygame.Rect(random.randint(300,350), random.randint(0, 720), ENEMY_WIDTH, ENEMY_HEIGHT))

    BULLETS = []

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.x, player.y + (PLAYER_WIDTH)//2, 8, 5)
                    BULLETS.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_p:
                    pause()
            
            if event.type == enemy_hit:
                score_value += 1


        for i in range(NUM_ENEMY):
            if enemy[i].x >= 950:
                for j in range(NUM_ENEMY):
                    enemy[j].x = 2000
                over(over_text,score_value)
                break 

        keys_pressed = pygame.key.get_pressed()  
        player_handle_movement(player, keys_pressed)
        enemy_handle_movement(enemy)
        handle_bullets_sing(BULLETS,enemy)
        
        draw_window_sing(player,enemy,BULLETS,score_value)


def main_game_uni():
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    main_sing()
                if button2.collidepoint(event.pos):
                    main_mult()
                if button3.collidepoint(event.pos):
                    exit()
                
            
        draw_window_uni()
    
main_game_uni()