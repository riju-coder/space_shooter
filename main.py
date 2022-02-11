import pygame
import random
from math import *
from pygame import mixer

pygame.init()
screen =pygame.display.set_mode((800,600))
run = True
mixer.music.load("background.wav")
mixer.music.play(-1)
pygame.display.set_caption('Space shooter')
# icon= pygame.image.load('icon.png') 
# Change icon.png it's 64 pixel of size.
background = pygame.image.load('background.png')
playerimg=pygame.image.load('spaceship.png')
playerx=338
playery=480
pchange = 0
enemyimg=[]
enemyx=[]
enemyy=[]
echangex=[]
echangey=[]
num_e = 5
b=7
for i in range (num_e):
	enemyimg.append(pygame.image.load('enemy.png'))
	enemyx.append(random.randint(0,735))
	enemyy.append(random.randint(0,50))
	echangex.append(b)
	echangey.append(40)

bulletimg = pygame.image.load('bullet.png')
bulletx = 338
bullety = 480
bchange = 15
b_state = 'wait'

score_value =0
font = pygame.font.Font('freesansbold.ttf',32)
textx = 10
texty= 10

over_font =pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(over_text,(200,250))

def score(x,y):
	scr = font.render("Score : " + str(score_value),True,(255,255,255))
	screen.blit(scr,(x,y))

def is_collision(bulletx,enemyx,bullety,enemyy):
	dist = sqrt(pow((bulletx-enemyx),2)+pow((bullety-enemyy),2))
	if dist <27:
		return True
	return False

def b_fire(x,y):
	global b_state
	b_state = 'fire'
	screen.blit(bulletimg,(x+16,y+10))

a = 6
def player(x,y):
	screen.blit(playerimg,(x,y))
	
def enemy(x,y,i):
	screen.blit(enemyimg[i],(x,y))

while run:
	screen.fill((0,0,0))
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pchange = -a
			if event.key == pygame.K_RIGHT:
				pchange = a
			if event.key == pygame.K_SPACE:
				if b_state == 'wait':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletx = playerx
					b_fire(bulletx,bullety)
		elif event.type == pygame.KEYUP:
			pchange = 0
	playerx += pchange
	if playerx <= 0:
		playerx = 0
	elif playerx >= 736:
		playerx = 736
	player(playerx,playery)
	for i in range(num_e):
		if (enemyy[i] > 440) :
				for j in range(num_e):
					enemyy[j] = 2000
				game_over_text()
				break
		if enemyx[i] <= 0:
			echangex[i] = b
			enemyy[i] += echangey[i]
		elif enemyx[i] >= 736:
			echangex[i] = -b
			enemyy[i] += echangey[i]
		enemyx[i] += echangex[i]
		enemy(enemyx[i],enemyy[i],i)
		collision = is_collision(bulletx,enemyx[i],bullety,enemyy[i])
		if collision:
			exp_sound = mixer.Sound('explosion.wav')
			exp_sound.play()
			enemyx[i]=random.randint(0,735)
			enemyy[i]=random.randint(0,50)
			b_state = 'wait'
			bullety = 480
			score_value += 1
	if bullety <= 0:
		bullety = playery
		b_state = 'wait'
		
	if b_state == 'fire':
		b_fire(bulletx,bullety)
		bullety -= bchange
	score(textx,texty)
	pygame.display.update()
