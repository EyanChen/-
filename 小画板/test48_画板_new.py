# coding:utf-8
import pygame
from pygame.locals import *
from math import sqrt


class Brush(object):
    def __init__(self, screen):
        self.screen = screen
        self.color = (0x00, 0xff, 0x00)
        self.size = 5
        self.drawing = False
        self.last_pos = None
        self.style = False  # False是铅笔，True是画刷
        self.brush = pygame.image.load('../painter/brush.png').convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (5, 5))

    def start_down(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def get_brush_style(self):
        return self.style

    def set_brush_style(self, style):
        self.style = style
        if style:
            print('当前画笔为：画刷')
        else:
            print('当前画笔为：铅笔')

    def get_current_brush(self):
        return self.brush_now

    def get_color(self):
        return self.color

    def set_color(self, color_temp):
        self.color = color_temp
        print(self.color)
        # 改变画刷时，把brush的单个像素值也变色
        for i in range(0, self.brush.get_width()):
            for j in range(0, self.brush.get_height()):
                self.brush.set_at((i, j), color_temp + (self.brush.get_at((i, j)).a, ))

    def set_size(self, size):
        if size < 1:
            self.size = 1
        elif size > 31:
            self.size = 31
        else:
            self.size = size
        print('笔当前的大小：', end='')
        print(self.size)
        self.brush_now = self.brush.subsurface((0, 0), (size * 2, size * 2))

    def get_size(self):
        return self.size

    def draw(self, pos):
        if self.drawing:
            for p in self.get_points(pos):
                if not self.style:
                    pygame.draw.circle(self.screen, self.color, p, self.size)
                else:
                    self.screen.blit(self.brush_now, p)
            self.last_pos = pos

    def get_points(self, pos):
        """拿到当前点与上一点之间，所有的点"""
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = sqrt(len_x ** 2 + len_y ** 2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(0, int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))


class Menu(object):
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        # self.rect = (position,(width, high))
        self.font = pygame.font.SysFont('arial', 18)
        self.tip = self.font.render('[Esc_Clear]', True, (0xc0, 0xc0, 0xc0))
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80)
        ]
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 294 + i // 2 * 32, 32, 32)
            self.colors_rect.append(rect)
        self.pens = [
            pygame.image.load('../painter/pen1.png'),
            pygame.image.load('../painter/pen2.png')
        ]
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)
        self.size = [
            pygame.image.load('../painter/big.png'),
            pygame.image.load('../painter/small.png')
        ]
        self.size_rect = []
        for (i, surface) in enumerate(self.size):
            rect = pygame.Rect(10 + i % 2 * 32, 148, 32, 32)
            self.size_rect.append(rect)

    def set_brush(self, brush):
        self.brush = brush

    def click_button(self, pos):
        # 当是按切换画笔时
        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))  # 0是铅笔，1是刷子
                return True
        # 是改变画笔大小时
        for (i, rect) in enumerate(self.size_rect):
            if rect.collidepoint(pos):
                if i == 0:  # 加大
                    self.brush.set_size(self.brush.get_size() + 1)
                else:
                    self.brush.set_size(self.brush.get_size() - 1)
                return True
        # 是选颜色时
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        return False

    def draw(self):
        # 画两个画笔按钮
        for (i, surface) in enumerate(self.pens):
            self.screen.blit(surface, self.pens_rect[i].topleft, )
        # 画加和减的按钮
        for (i, surface) in enumerate(self.size):
            self.screen.blit(surface, self.size_rect[i].topleft)
        # 画彩色块、
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])
        # 画当前画笔和画刷
        self.screen.fill((255, 255, 255), (10, 200, 64, 64))  # 中间白色块
        pygame.draw.rect(self.screen, (0, 0, 0), (12, 200, 59, 64), 2)  # 黑色边框
        # 画个大框把工具栏框起来
        pygame.draw.rect(self.screen, (122, 82, 90), (10, 10, 64, 541), 3)

        size = self.brush.get_size()
        x = 10 + 32
        y = 200 + 32
        if self.brush.get_brush_style():
            x -= size
            y -= size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), size)
        # 写字
        self.screen.blit(self.tip, (5, 555))


class Painter(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Painter（画板）')
        self.clock = pygame.time.Clock()
        self.frame = 0
        self.sum = 0
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)

    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            time_passed = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    # 按‘Esc’清屏
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    # 看点在哪个区域,x<74,是点功能键
                    if event.pos[0] < 74 and self.menu.click_button(event.pos):
                        pass
                    else:
                        self.brush.start_down(event.pos)
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            # self.screen.blit(, (0, 0))

            self.menu.draw()

            pygame.display.update()
            # 记录帧率
            self.sum += time_passed
            self.frame += 1
            if self.sum > 1000:
                # print('当前帧率：', end='')
                # print(self.frame)
                self.sum = 0
                self.frame = 0


if __name__ == '__main__':
    app = Painter()
    app.run()
