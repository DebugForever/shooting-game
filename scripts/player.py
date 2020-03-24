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
from . import setting


class Player(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        self.is_fire = False
        self.fire_control = ''  # 开火方式，键盘还是鼠标还是手柄
        self.fire_cd = 0  # 距离下一次能开火的时间

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
            x, y = pygame.mouse.get_pos()
            direction = atan2(y - self.y, x - self.x)
        elif self.fire_control == c.CONTROL_JOYSTICK:
            direction = 0.0  # todo joystick support

        bullet = Bullet(image_dict[c.PLAYER_BULLET_NAME])
        bullet.x = self.x
        bullet.y = self.y
        bullet.set_dir_v(direction, setting.bullet_speed_p)
        bullets.add(bullet)
        self.fire_cd = setting.player_fire_cd

    def update(self):
        super().update()
        self.fire_cd -= 1
