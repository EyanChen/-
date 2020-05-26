import pygame
from pygame.locals import *


pygame.init()
# 建窗口
screen = pygame.display.set_mode((480, 810), 0, 32)
# 建背景图片
background = pygame.image.load('../plane_img/background.png')

while True:
    for event in pygame.event.get():
        print('=========')
        if event.type == QUIT:
            exit()
        # 判断是否是按下了键
        elif event.type == KEYDOWN:
            # 检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
            # 检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_LEFT:
                print('left_UP')
    screen.blit(background, (0, 0))  # 填充背景
    pygame.display.update()