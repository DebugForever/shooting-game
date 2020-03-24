"""
游戏的主类，包含运行中的几乎所有信息
main class of game, contains almost data
"""
import pygame

from pygame.sprite import Group
from math import sin, cos, atan2
from . import setting, image_dict
from .player import Player
from .enemy import Enemy
from . import constants as c


class Game:
    """
    游戏的主类，包含运行中的几乎所有信息，负责处理所有游戏功能
    """
    # 类型提示，用于编译器自动补全和消除warning
    screen: pygame.Surface
    player: Player
    screen_rect: pygame.Rect
    enemies: Group
    bullets_p: Group
    bullets_e: Group
    clock: pygame.time.Clock
    joystick: pygame.joystick.Joystick

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        pygame.event.set_allowed(setting.event_allowed)
        self.setup()
        self.done = False

    def setup(self):
        self.screen = pygame.display.set_mode(setting.screen_resolution)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(setting.caption)

        self.clock = pygame.time.Clock()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.setup_entities()

    def setup_entities(self):
        self.player = Player(image_dict['player'])
        self.player.x = self.screen_rect.centerx
        self.player.y = self.screen_rect.centery

        self.enemies = Group()
        enemy1 = Enemy(image_dict['enemy1'])
        enemy1.x = 100
        enemy1.y = 100
        self.enemies.add(enemy1)

        self.bullets_p = Group()  # bullets shoot by player
        self.bullets_e = Group()  # bullets shoot by enemy

    def run(self):
        while not self.done:
            self.handle_events()
            self.check_everything()
            self.update_everything()
            self.draw_everything()
            pygame.display.flip()
            self.clock.tick(setting.fps_limit)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.handle_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.is_fire = True
                self.player.fire_control = c.CONTROL_MOUSE
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.is_fire = False
            elif event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joy_axis_events()

    def handle_joy_axis_events(self):
        # 这里有一个问题：手柄和键盘同时操作时，
        # 可能会出现不受控制状态，只需把手柄摇杆摇到中间即可解决，更改代码不好处理。

        # improve:这里应该可以分离处理的，但是我不知道怎么改，（可能通过event拿信息？）
        move_x = self.joystick.get_axis(setting.joystick_axis_move_x)
        move_y = self.joystick.get_axis(setting.joystick_axis_move_y)
        fire_x = self.joystick.get_axis(setting.joystick_axis_fire_x)
        fire_y = self.joystick.get_axis(setting.joystick_axis_fire_y)
        if abs(move_x) >= setting.joystick_min_motion:
            self.player.x_vel = setting.player_speed * move_x
        else:
            self.player.x_vel = 0.0
        if abs(move_y) >= setting.joystick_min_motion:
            self.player.y_vel = setting.player_speed * move_y
        else:
            self.player.y_vel = 0.0

        if abs(fire_x) >= setting.joystick_min_motion or abs(fire_y) >= setting.joystick_min_motion:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_JOYSTICK
            self.player.fire_dir = atan2(fire_y, fire_x)
        else:
            self.player.is_fire = False

    def handle_keydown_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.y_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.y_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.x_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.x_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_KEYBOARD

    def handle_keyup_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.y_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.y_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.x_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.x_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = False

    def check_everything(self):
        if self.player.is_fire:
            self.player.fire(self.bullets_p)

    def update_everything(self):
        self.player.update()
        self.bullets_p.update()
        self.enemies.update()

    def draw_everything(self):
        self.screen.fill((220, 220, 220))
        self.enemies.draw(self.screen)
        self.bullets_p.draw(self.screen)
        self.player.draw(self.screen)
