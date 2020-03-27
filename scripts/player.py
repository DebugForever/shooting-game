"""
玩家类，玩家控制的角色
class player
"""
from .entity import Entity
import pygame
from pygame.sprite import Group
from .bullet import Bullet
from math import atan2
from . import image_dict
from . import constants as c
from . import setting, dbgscreen


class Player(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        self.is_fire = False
        self.fire_control = ''
        """开火方式，键盘还是鼠标还是手柄"""
        self.fire_dir = 0.0
        """暂存的开火方向，在使用手柄时使用"""
        self.fire_cd = 0
        """距离下一次能开火的时间"""
        self.viewport = pygame.Rect(0, 0, 0, 0)
        """是外面的这个的引用(Game.viewport)，用于计算玩家在屏幕上的实际位置"""

        # combat stats
        self.hp = 100
        self.maxhp = 100
        self.atk = 10

    def fire(self, bullets: Group):
        """
        射出子弹，方向由操控方式决定，如果在CD则不发射
        :param bullets:子弹群组
        :return:None
        """

        if self.fire_cd > 0 or not self.is_fire:
            return
        direction = 0.0
        if self.fire_control == c.CONTROL_KEYBOARD:
            direction = self.direction
        elif self.fire_control == c.CONTROL_MOUSE:
            mx, my = pygame.mouse.get_pos()
            direction = atan2(my + self.viewport.y - self.y, mx + self.viewport.x - self.x)
        elif self.fire_control == c.CONTROL_JOYSTICK:
            direction = self.fire_dir

        bullet = Bullet(image_dict[c.PLAYER_BULLET_NAME])
        bullet.setup(self.x, self.y, self.atk)
        bullet.set_dir_v(direction, setting.bullet_speed_p)
        bullets.add(bullet)
        self.fire_cd = setting.player_fire_cd

    def update(self):
        super().update()
        self.fire_cd -= 1

    def draw(self, screen: pygame.Surface):
        super().draw(screen)  # 这段代码是复制过来的，因为不想再做一层继承
        hp_bar_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, setting.player_hpbar_height))
        pygame.draw.rect(screen, setting.player_hpbar_color_high, hp_bar_rect)  # 画血条
        pygame.draw.rect(screen, setting.player_hpbar_line_color, hp_bar_rect, setting.player_hpbar_line_width)  # 画边框
