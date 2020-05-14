"""
生物类，是Entity类之上抽象的一层类，
是有血条，攻击力，buff等战斗数值的实体，目前包括Player和Enemy
"""
from typing import List

from . import buff
from .entity import Entity
from . import setting
import pygame


class Creature(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        # 战斗有关的属性，以下为默认值，没有什么用（还不是因为python没有变量声明），需要要覆盖这些值
        # 这里写上这些值主要是为了方便IDE提示
        self.maxhp = 1
        self.hp = 1
        self.atk = 1
        self.gold = 1
        self.basespeed = 1.0
        """基础移速"""
        self.speed = self.basespeed
        """当前移速"""
        self.bullet_speed = 1

        self.buffs: List['buff.Buff'] = []
        """当前附加的buff"""

    def update(self):
        for buff_ in self.buffs:
            buff_.update()
            buff_.on_update(self)

        self.buffs = list(filter(lambda b: b.is_faded(), self.buffs))  # 去除所有到期的buff

        self.velocity = self.speed  # 先同步速度属性，这样可以处理加减速的buff效果
        super().update()  # 其他代码不变

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        hp_bar_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, setting.hpbar_height))
        hp_rect = hp_bar_rect.copy()
        hp_ratio = self.hp / self.maxhp
        hp_rect.width *= hp_ratio
        hp_rect.left = hp_bar_rect.left
        if hp_rect.right < hp_rect.left:  # 处理负血条
            hp_rect.width = 0
        pygame.draw.rect(screen, setting.hpbar_color, hp_rect)  # 画血条
        pygame.draw.rect(screen, setting.hpbar_line_color, hp_bar_rect, setting.hpbar_line_width)  # 画边框

        # 画buff图标
        if self.buffs:
            buff_icon_top = hp_bar_rect.bottom + setting.distance_tiny
            buff_icon_left = hp_bar_rect.left
            buff_icon_rect = pygame.Rect(buff_icon_left, buff_icon_top, setting.buff_icon_width,
                                         setting.buff_icon_width)
            for buff in self.buffs:
                if buff.icon is None:
                    continue  # 没有图标就不画了
                screen.blit(buff.icon, buff_icon_rect)
                buff_icon_rect.left += buff_icon_rect.width + setting.distance_tiny
