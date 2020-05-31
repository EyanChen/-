# coding:utf-8
import pygame
from pygame.locals import *
from pygame.math import Vector2
import time

background = pygame.image.load('../background_Moon.png')
image_plane = pygame.image.load('../plane1.png')


class Plane(object):
    def __init__(self, screen_temp, clock_temp, plane_pos_temp):
        # self.x = x
        # self.y = y
        self.clock = clock_temp
        self.pos = plane_pos_temp
        self.speed = 150
        self.key_direction = Vector2()  # 加速度与方向
        self.screen = screen_temp
        self.img = image_plane
        self.rotate_img = self.img
        self.event_left = 0  # 记录四个方向按键,状态默认不按时(0),按下为1
        self.event_right = 0
        self.event_up = 0
        self.event_down = 0

    def ready(self, screen_temp):
        self.move()
        # 转向后,要重新计算一下启始座标
        w, h = self.img.get_size()
        sprite_draw_pos = Vector2(self.pos.x - w / 2, self.pos.y - h / 2)
        screen_temp.blit(self.rotated(), sprite_draw_pos)

    def move(self):
        time_passed = self.clock.tick()
        time_passed_seconds = time_passed / 1000  # 每帧占多少秒
        # 拿key_direction更新位置,在这里直接计算key_direction
        self.key_direction = Vector2(self.event_left + self.event_right, self.event_down + self.event_up)
        self.pos += self.key_direction * self.speed * time_passed_seconds
        # 判断有无出边界
        if self.pos.x > 600:
            self.pos.x = 600
        elif self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > 450:
            self.pos.y = 450
        elif self.pos.y < 0:
            self.pos.y = 0

    # 根据当前方向转向
    def rotated(self):
        # 根据key_direction计算当前方向
        if self.key_direction.x == 0 and self.key_direction.y == 0:  # 不动时
            pass
        elif self.key_direction.x == 1 and self.key_direction.y == 0:  # 右
            self.rotate_img = pygame.transform.rotate(self.img, 270)
        elif self.key_direction.x == -1 and self.key_direction.y == 0:  # 左
            self.rotate_img = pygame.transform.rotate(self.img, 90)
        elif self.key_direction.x == 0 and self.key_direction.y == -1:  # 上
            self.rotate_img = self.img
        elif self.key_direction.x == 0 and self.key_direction.y == 1:  # 下
            self.rotate_img = pygame.transform.rotate(self.img, 180)
        elif self.key_direction.x == -1 and self.key_direction.y == -1:  # 左上
            self.rotate_img = pygame.transform.rotate(self.img, 45)
        elif self.key_direction.x == 1 and self.key_direction.y == -1:  # 右上
            self.rotate_img = pygame.transform.rotate(self.img, 315)
        elif self.key_direction.x == -1 and self.key_direction.y == 1:  # 左下
            self.rotate_img = pygame.transform.rotate(self.img, 135)
        elif self.key_direction.x == 1 and self.key_direction.y == 1:  # 右下
            self.rotate_img = pygame.transform.rotate(self.img, 225)
        else:
            print('当前向量不在判断范围.')
        return self.rotate_img


def key_control(sprite_plane):
    for event in pygame.event.get():
        if event.type == QUIT:  # 按X退出
            exit()
        # 判断是否是按下了键==========
        elif event.type == KEYDOWN:
            # 检测按键是否是a s d w 或者left,right,up,down
            if event.key == K_a or event.key == K_LEFT:
                print('left_down')
                sprite_plane.event_left = -1
            elif event.key == K_d or event.key == K_RIGHT:
                print('right_down')
                sprite_plane.event_right = 1
            elif event.key == K_w or event.key == K_UP:
                print('UP')
                sprite_plane.event_up = -1
            elif event.key == K_s or event.key == K_DOWN:
                print('DOWN')
                sprite_plane.event_down = 1
        # 判断是否是松开了键===========
        elif event.type == KEYUP:
            # 检测按键松开,分四个写,每个按键单独,方便多按键同按
            if event.key == K_a or event.key == K_LEFT:
                sprite_plane.event_left = 0
                # print(Vector2(sprite_plane.event_left + sprite_plane.event_right,  # 测试用
                #               sprite_plane.event_down + sprite_plane.event_up))
            elif event.key == K_d or event.key == K_RIGHT:
                sprite_plane.event_right = 0
                # print(Vector2(sprite_plane.event_left + sprite_plane.event_right,
                #               sprite_plane.event_down + sprite_plane.event_up))
            elif event.key == K_w or event.key == K_UP:
                sprite_plane.event_up = 0
                # print(Vector2(sprite_plane.event_left + sprite_plane.event_right,
                #               sprite_plane.event_down + sprite_plane.event_up))
            elif event.key == K_s or event.key == K_DOWN:
                sprite_plane.event_down = 0
                # print(Vector2(sprite_plane.event_left + sprite_plane.event_right,
                #               sprite_plane.event_down + sprite_plane.event_up))


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Moon')

clock = pygame.time.Clock()

# 速度(像素/秒)
speed = 200
plane_pos = Vector2(300, 300)  # 默认座标
sprite_plane = Plane(screen, clock, plane_pos)

while True:

    screen.blit(background, (0, 0))
    sprite_plane.ready(screen)  # 更新
    key_control(sprite_plane)
    pygame.display.update()
    time.sleep(0.01)
