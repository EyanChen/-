# coding : utf-8

import pygame
from pygame.locals import *
from pygame.math import Vector2
import time
from random import randint


class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.fill((215, 255, 255))
        # 画个巢穴
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, NEST_SIZE)

    # 每添加一个entity,就赋值一个id,
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    # 通过id 找entity
    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def process(self, time_passed_temp):
        time_passed_second = time_passed_temp / 1000
        for entity in list(self.entities.values()):
            entity.process(time_passed_second)

    # 判断当前location周围有没有靠近的其它entity,靠近范围close_range默认100
    def get_close_entity(self, name, location, close_range=100):
        location = Vector2(*location)  # *表示展开当前元素 *(x,y) = x, y
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.distance_to(entity.location)
                if distance < close_range:
                    return entity
        return None


class GameEntity(object):
    def __init__(self, world_temp, name, image):
        self.world = world_temp
        self.name = name
        self.image = image
        self.location = Vector2()
        self.destination = Vector2()
        self.speed = 0
        self.brain = StateMachine()
        self.id = 0

    def render(self, surface):
        x, y = self.location
        weigh, high = self.image.get_size()
        surface.blit(self.image, (x - weigh / 2, y - high / 2))

    def process(self, time_passed_temp):
        # 处理每一个entity的运动
        self.brain.think()
        if self.speed > 0 and self.location != self.destination:
            vec = self.destination - self.location
            distance_to_destination = vec.length()  # 当前与目的地的距离
            heading = vec.normalize()
            travel_dis = min(distance_to_destination, time_passed_temp * self.speed)  # 单位速度
            self.location += travel_dis * heading


class Leaf(GameEntity):
    def __init__(self, world_temp, image):
        GameEntity.__init__(self, world_temp, 'leaf', image)


class Spider(GameEntity):
    def __init__(self, world_temp, image):
        GameEntity.__init__(self, world_temp, 'spider', image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.speed = 50 + randint(-20, 20)
        self.health = 25

    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0
            self.image = self.dead_image
        self.speed = 160

    # 多画一个蜘蛛血条
    def render(self, surface):
        GameEntity.render(self, surface)
        x, y = self.location
        wide, high = self.image.get_size()
        bar_x = x - 12
        bar_y = y + high / 2
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))  # 底槽
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))  # 血量

    #  蜘蛛爬出界，就删除掉
    def process(self, time_passed_temp):
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        GameEntity.process(self, time_passed_temp)


class Ant(GameEntity):
    def __init__(self, world_temp, image):
        GameEntity.__init__(self, world_temp, 'ant', image)
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)
        self.carry_img = None

    # 携带东西，放图片
    def carry(self, image_temp):
        self.carry_img = image_temp
        pass

    # 放下东西，放图片
    def drop(self, surface):
        if self.carry_img:
            x, y = self.location
            wide, high = self.carry_img.get_size()
            surface.blit(self.carry_img, (x - wide, y - high / 2))
            self.carry_img = None

    def render(self, surface):
        GameEntity.render(self, surface)
        if self.carry_img:
            x, y = self.location
            wide, high = self.carry_img.get_size()
            surface.blit(self.carry_img, (x - wide - 8, y - high / 2))


# ===========================================================================================
# 各种状态类，用state工厂模式
# ===========================================================================================

class State(object):
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_states = None

    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if self.active_states is None:
            return
        self.active_states.do_actions()
        new_state_name = self.active_states.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
            # print('当前状态：', end='')
            # print(new_state_name)

    def set_state(self, new_state_name):
        if self.active_states is not None:
            self.active_states.exit_actions()
        self.active_states = self.states[new_state_name]
        self.active_states.entry_actions()


# 探索状态
class AntStateExploring(State):
    def __init__(self, ant_temp):
        State.__init__(self, 'exploring')
        self.ant = ant_temp

    def random_destination(self):
        weight, high = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, weight), randint(0, high))

    def do_actions(self):
        if randint(1, 200) == 1:
            self.random_destination()

    def check_conditions(self):
        # 检测是否发现树叶
        find_leaf = self.ant.world.get_close_entity('leaf', self.ant.location)
        if find_leaf is not None:
            # 找到附近有树叶，就把ant的carry_img加上树叶,并把活动状态改成 seeking
            self.ant.Leaf_id = find_leaf.id
            # print('找到树叶,变成寻址状态')
            return 'seeking'

        # 检测是否攻击蜘蛛
        find_spider = self.ant.world.get_close_entity('spider', self.ant.location)
        if find_spider is not None:
            self.ant.spider_id = find_spider.id
            return 'hunting'
        return None

    def entry_actions(self):
        self.ant.speed = 100 + randint(-30, 30)
        self.random_destination()


# 寻址状态（找到目标，往目标前进）
class AntStateSeeking(State):
    def __init__(self, ant_temp):
        State.__init__(self, 'seeking')
        self.ant = ant_temp
        self.Leaf_id = None

    def check_conditions(self):
        find_leaf = self.ant.world.get(self.ant.Leaf_id)
        if find_leaf is None:
            return 'exploring'
        if self.ant.location.distance_to(find_leaf.location) < 5:
            self.ant.carry(find_leaf.image)
            self.ant.world.remove_entity(find_leaf)
            return 'delivering'
        return None

    def entry_actions(self):
        find_leaf = self.ant.world.get(self.ant.Leaf_id)
        if find_leaf is not None:
            self.ant.destination = find_leaf.location
            self.ant.speed = 140 + randint(-20, 20)


# 运输状态
class AntStateDelivering(State):
    def __init__(self, ant_temp):
        State.__init__(self, 'delivering')
        self.ant = ant_temp

    def check_conditions(self):
        # 在巢穴范围时，放下携带东西
        if Vector2(*NEST_POSITION).distance_to(self.ant.location) < NEST_SIZE:
            if randint(1, 100) == 1:
                self.ant.drop(self.ant.world.background)
                # print('放下树叶了`')
                return 'exploring'
        return None

    def entry_actions(self):
        self.ant.speed = 60
        random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*NEST_POSITION) + random_offset


# 攻击状态
class AntStateHunting(State):
    def __init__(self, ant_temp):
        State.__init__(self, 'hunting')
        self.ant = ant_temp
        self.got_kill = False

    def do_actions(self):
        find_spider = self.ant.world.get(self.ant.spider_id)
        if find_spider is None:
            return
        if self.ant.location.distance_to(find_spider.location) < 5:
            if randint(1, 50) == 1:
                find_spider.bitten()
                if find_spider.health <= 0:
                    self.ant.carry(find_spider.image)
                    self.ant.world.remove_entity(find_spider)
                    self.got_kill = True

    def check_conditions(self):
        if self.got_kill:
            return 'delivering'
        find_spider = self.ant.world.get(self.ant.spider_id)
        if find_spider is None:
            return 'exploring'
        # 蜘蛛位置远离了巢穴，不追了
        if find_spider.location.distance_to(NEST_POSITION) > NEST_SIZE * 3:
            return 'exploring'
        # 蜘蛛离蚂蚁远了，也不追了
        if self.ant.location.distance_to(find_spider.location) > 100:
            return 'exploring'
        return None

    def entry_actions(self):
        find_spider = self.ant.world.get(self.ant.spider_id)
        self.ant.speed = 140 + randint(-20, 20)
        self.ant.destination = find_spider.location

    def exit_actions(self):
        self.got_kill = False


SCREEN_SIZE = (640, 480)
NEST_POSITION = (320, 240)
ANT_COUNT = 15
NEST_SIZE = 80

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
ant_image = pygame.image.load("../ant.png").convert_alpha()
leaf_image = pygame.image.load("../leaf.png").convert_alpha()
spider_image = pygame.image.load("../spider.png").convert_alpha()
w, h = SCREEN_SIZE
clock = pygame.time.Clock()

world = World()
# 添加蚂蚁
for ant_no in range(0, ANT_COUNT):
    ant = Ant(world, ant_image)
    ant.location = Vector2(randint(10, w), randint(10, h))
    ant.brain.set_state("exploring")
    world.add_entity(ant)

# 记录帧数
the_frame = 0
sum_f = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    time_passed = clock.tick()

    # 随机树叶
    if randint(1, 300) == 1:
        leaf = Leaf(world, leaf_image)
        leaf.location = Vector2(randint(0, w), randint(0, h))
        world.add_entity(leaf)
    # 随机蜘蛛
    if randint(1, 1000) == 1:
        spider = Spider(world, spider_image)
        spider.location = Vector2(+10, randint(0, h))
        spider.destination = Vector2(w + 30, randint(0, h))
        world.add_entity(spider)

    world.render(screen)
    world.process(time_passed)
    pygame.display.update()

    # 记录一下帧数
    sum_f += time_passed
    the_frame += 1

    if sum_f > 1000:
        print('当前帧数：', end='')
        print(the_frame)
        sum_f = 0
        the_frame = 0
    time.sleep(0.001)
