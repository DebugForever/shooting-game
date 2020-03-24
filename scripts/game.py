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

    def __init__(self):
        pygame.init()
        self.setup()
        self.done = False

    def setup(self):
        self.screen = pygame.display.set_mode(setting.screen_resolution)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(setting.caption)
        self.clock = pygame.time.Clock()
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
        # todo 添加手柄支持
        keymap = setting.keymap
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == keymap['up']:
                    self.player.y_vel -= setting.player_speed
                elif event.key == keymap['down']:
                    self.player.y_vel += setting.player_speed
                elif event.key == keymap['left']:
                    self.player.x_vel -= setting.player_speed
                elif event.key == keymap['right']:
                    self.player.x_vel += setting.player_speed
                elif event.key == keymap['fire']:
                    self.player.is_fire = True
                    self.player.fire_control = c.CONTROL_KEYBOARD
            elif event.type == pygame.KEYUP:
                if event.key == keymap['up']:
                    self.player.y_vel += setting.player_speed
                elif event.key == keymap['down']:
                    self.player.y_vel -= setting.player_speed
                elif event.key == keymap['left']:
                    self.player.x_vel += setting.player_speed
                elif event.key == keymap['right']:
                    self.player.x_vel -= setting.player_speed
                elif event.key == keymap['fire']:
                    self.player.is_fire = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.is_fire = True
                self.player.fire_control = c.CONTROL_MOUSE
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.is_fire = False
            elif event.type == pygame.QUIT:
                self.done = True

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
