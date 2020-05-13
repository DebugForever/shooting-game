"""
实体类，是游戏所有实体的基类
contains entity base class, and other entity-like objects
"""

from pygame.sprite import Sprite
import pygame
from math import sqrt, atan2, sin, cos


class Entity(Sprite):
    """
    实体类，是游戏所有实体的基类，包含xy和xy速度的属性
    """
    _dir: float

    @property
    def velocity(self):
        """虚拟属性：速度（标量）"""
        return sqrt(self._x_vel ** 2 + self._y_vel ** 2)

    @velocity.setter
    def velocity(self, new_vel):
        self.set_dir_v(self.direction, new_vel)

    @property
    def direction(self):
        """虚拟属性：面朝角度"""
        if self._x_vel == 0 and self._y_vel == 0:  # 没有速度默认为0角度，否则atan2会报错
            return self._dir
        self._dir = atan2(self._y_vel, self._x_vel)
        return self._dir

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x: float):
        """把xy实现成虚拟属性是为了方便，因为xy坐标应始终与物体的碰撞箱同步，否则容易出bug"""
        self._x = new_x
        self.rect.centerx = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y: float):
        self._y = new_y
        self.rect.centery = self._y

    @property
    def x_vel(self):
        """
        为了解决停止时无法保存方向的问题，把x_vel和y_vel也写成了虚拟属性
        """
        return self._x_vel

    @x_vel.setter
    def x_vel(self, new_val):
        self._x_vel = new_val
        if self._x_vel != 0 or self._y_vel != 0:
            self._dir = atan2(self._y_vel, self._x_vel)

    @property
    def y_vel(self):
        return self._y_vel

    @y_vel.setter
    def y_vel(self, new_val):
        self._y_vel = new_val
        if self._x_vel != 0 or self._y_vel != 0:
            self._dir = atan2(self._y_vel, self._x_vel)

    def __init__(self, image: pygame.Surface):
        super().__init__()

        self._x = 0.0
        self._y = 0.0
        self._dir = 0.0
        """面朝方向，仅当速度为0时生效"""
        self._x_vel = 0.0
        """x轴分速度  velocity in x axis"""
        self._y_vel = 0.0
        """y轴分速度  velocity in y axis"""

        self.image = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.sync_rect_xy()

    def set_dir_v(self, direction: float, velocity: float):
        """
        同时设置角度和速度，这是一个妥协，因为只设置角度无法在速度为0时生效
        :param direction: 新的面朝角度
        :param velocity: 新的速度
        """
        self._x_vel = velocity * cos(direction)
        self._y_vel = velocity * sin(direction)
        self._dir = direction

    def set_xy(self, x: float, y: float):
        self.x = x
        self.y = y

    def sync_rect_xy(self):
        """
        将自身的矩形位置和xy同步，绘图的时候不会用到xy
        :return:None
        """
        self.rect.centerx = int(self._x)
        self.rect.centery = int(self._y)

    def sync_xy_rect(self):
        """
        将自身的xy和矩形位置同步，只更改矩形位置的时候需要用到
        improve:一个更好的方法是，实现rect的所有虚拟属性，并在修改后同步（但是实在是太多了）
        :return:None
        """
        self._x = self.rect.centerx
        self._y = self.rect.centery

    def update(self):
        self._x += self._x_vel
        self._y += self._y_vel
        self.sync_rect_xy()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def make_in_bound(self, rect: pygame.Rect):
        self.rect.left = max(self.rect.left, rect.left)
        self.rect.top = max(self.rect.top, rect.top)
        self.rect.right = min(self.rect.right, rect.right)
        self.rect.bottom = min(self.rect.bottom, rect.bottom)
        self._x, self._y = self.rect.center
