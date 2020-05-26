# coding : utf-8
import pygame
from pygame.locals import *


class Animal(object):
    def __init__(self, screen, image_name='../plane_img/enemy0.png'):
        self.x = 200
        self.y = 300
        self.screen = screen
        self.img = pygame.image.load(image_name)
        self.event_left = 0  # 记录四个方向按键,状态默认不按时(0),按下为1
        self.event_right = 0
        self.event_up = 0
        self.event_down = 0

    def display(self):
        self.screen.blit(self.img, (self.x, self.y))

    def move_left(self):
        self.x -= 2
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += 2
        if self.x > 450:
            self.x = 450

    def move_up(self):
        self.y -= 2
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += 2
        if self.y > 775:
            self.y = 775


def main():
    # 建窗口
    screen = pygame.display.set_mode((480, 810), 0, 32)
    print(screen)
    # 设置标题
    pygame.display.set_caption('飞机移动')
    # 建背景图片
    background = pygame.image.load('../plane_img/background.png')
    # 建个飞机
    animal = Animal(screen)

    # 显示图片
    while True:
        screen.blit(background, (0, 0))  # 填充背景
        for event in pygame.event.get():
            if event.type == QUIT:  # 按X退出
                exit()
            # 判断是否是按下了键==========
            elif event.type == KEYDOWN:
                # 检测按键是否是a s d w 或者left,right,up,down
                if event.key == K_a or event.key == K_LEFT:
                    print('left_down')
                    animal.event_left = 1

                elif event.key == K_d or event.key == K_RIGHT:
                    print('right_down')
                    animal.event_right = 1
                elif event.key == K_w or event.key == K_UP:
                    print('UP')
                    animal.event_up = 1
                elif event.key == K_s or event.key == K_DOWN:
                    print('DOWN')
                    animal.event_down = 1
            # 判断是否是松开了键===========
            elif event.type == KEYUP:
                # 检测按键松开,分四个写,每个按键单独,方便多按键同按
                if event.key == K_a or event.key == K_LEFT:
                    animal.event_left = 0
                elif event.key == K_d or event.key == K_RIGHT:
                    animal.event_right = 0
                elif event.key == K_w or event.key == K_UP:
                    animal.event_up = 0
                elif event.key == K_s or event.key == K_DOWN:
                    animal.event_down = 0
        # 判断状态来移动
        if animal.event_left == 1:
            animal.move_left()
        if animal.event_right == 1:
            animal.move_right()
        if animal.event_up == 1:
            animal.move_up()
        if animal.event_down == 1:
            animal.move_down()

        animal.display()
        pygame.display.update()


if __name__ == '__main__':
    main()
