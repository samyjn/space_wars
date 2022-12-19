import pygame
import os
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720

WIN = pygame.display.set_mode((WIDTH,HEIGHT))     # Making screen/window


SPACE = pygame.image.load(os.path.join('assets_multiplayer','space.png'))

MAX_BULLETS = 3
VEL_BULLETS = 13

enemy_hit = pygame.USEREVENT + 1


SCORE_FONT = pygame.font.SysFont('comicsans', 25)
game_over_font = pygame.font.SysFont('comicsans', 100)
over_text = "WASTED"

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 67
PLAYER_VEL = 11

PLAYER_IMG = pygame.image.load(os.path.join('assets_singleplayer','player_singleplayer.png'))
PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH,PLAYER_HEIGHT)),90)

ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35
NUM_ENEMY = 8
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

def over(over_text):
    text = game_over_font.render(over_text, 1, (255,255,255))
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()

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
                pygame.event.post(pygame.event.Event(enemy_hit))
                enemy[i].x = random.randint(300,400)
                enemy[i].y = random.randint(0, 720)
                BULLETS.remove(bullet)

        if bullet.x < 0:
            BULLETS.remove(bullet)

def main_sing():
    score_value = 0
    player = pygame.Rect(980, 315, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy = []
    for i in range(NUM_ENEMY):
        enemy.append(pygame.Rect(random.randint(300,400), random.randint(0, 720), ENEMY_WIDTH, ENEMY_HEIGHT))

    BULLETS = []

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.x, player.y + (PLAYER_WIDTH)//2, 8, 5)
                    BULLETS.append(bullet)
            
            if event.type == enemy_hit:
                score_value += 1
        for i in range(NUM_ENEMY):
            if enemy[i].x >= 950:
                for j in range(NUM_ENEMY):
                    enemy[j].x = 2000
                over(over_text) 
                break 

        keys_pressed = pygame.key.get_pressed()  
        player_handle_movement(player, keys_pressed)
        enemy_handle_movement(enemy)
        handle_bullets_sing(BULLETS,enemy)
        
        draw_window_sing(player,enemy,BULLETS,score_value)

main_sing()