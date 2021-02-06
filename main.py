import pygame
import os
import math
import time
from pygame.locals import *

#constant colors
WHITE = (255,255,255)
BLACK = (0,0,0)

#create game and screen
pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Pong')

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 0, 0).inflate(10, 70)
    def move(self, change):
        self.y += change
        self.rect = pygame.Rect(self.x, self.y, 0, 0).inflate(10, 70)

class Ball:
    VEL = 8;
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
    def move(self):
        self.x += self.VEL * math.cos(self.dir)
        self.y += self.VEL * math.sin(self.dir)

def draw(rect1, rect2, ball, score1, score2):
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (400, 0), (400, 600))
    pygame.draw.rect(screen, WHITE, rect1)
    pygame.draw.rect(screen, WHITE, rect2)
    pygame.draw.circle(screen, WHITE, [ball.x, ball.y], 5)
    font = pygame.font.Font('freesansbold.ttf', 32)
    score1_font = font.render(str(score1), True, WHITE)
    score2_font = font.render(str(score2), True, WHITE)
    screen.blit(score1_font, (350, 20))
    screen.blit(score2_font, (432, 20))

def collision(ball, paddle):
    return paddle.rect.collidepoint(ball.x, ball.y)

clock = pygame.time.Clock()

def main():
    #create players and ball
    p1 = Paddle(50, 300)
    p1Change = 0
    score1 = 0

    p2 = Paddle(740, 300)
    p2Change = 0
    score2 = 0

    ball = Ball(400, 300, 0)

    #game loop  
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p2Change = -5
                if event.key == pygame.K_DOWN:
                    p2Change = 5
                if event.key == pygame.K_w:
                    p1Change = -5
                if event.key == pygame.K_s:
                    p1Change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p2Change = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    p1Change = 0

        #check if paddle is off the board
        if p1.y <= 35:
            p1.y = 36
            p1Chagne = 0
        if p1.y >= 565:
            p1.y = 564
            p1Change = 0
        if p2.y <= 35:
            p2.y = 36
            p2Change = 0
        if p2.y >= 565:
            p2.y = 564
            p2Change = 0

        #make player 1 a bot
        """ if ball.y > p1.y + 35:
            p1Change = 5
        if ball.y < p1.y - 35:
            p1Change = -5 """

        #move everything
        p1.move(p1Change)
        p2.move(p2Change)
        ball.move()

        #check if ball hits paddle or hits top/bottom
        if (collision(ball, p2)):
            ball.dir = math.pi - ((ball.y - p2.y)/35.0) * (math.pi/4)
        if (collision(ball, p1)):
            ball.dir = ((ball.y - p1.y)/35.0) * (math.pi/4)
        if (ball.y <= 0 or ball.y >= 600):
            if (ball.y <= 0):
                ball.y = 1
            else:
                ball.y = 599
            ball.dir = 2*math.pi - ball.dir
        ball.dir %= 2*math.pi

        #check if ball goes off screen
        if ball.x <= 0 or ball.x >= 800:
            if ball.x <= 0:
                ball = Ball(400, 300, 0)
                score2 += 1
            if ball.x >= 800:
                ball = Ball(400, 300, math.pi)
                score1 += 1
            p1 = Paddle(50, 300)
            p1Change = 0
            p2 = Paddle(740, 300)
            p2Change = 0

        #redraw screen
        draw(p1.rect, p2.rect, ball, score1, score2)
        pygame.display.update()

main()
        
