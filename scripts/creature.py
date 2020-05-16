"""
生物类，是Entity类之上抽象的一层类，
是有血条，攻击力，buff等战斗数值的实体，目前包括Player和Enemy
"""
from typing import List

import pygame

from . import buff
from . import item
from . import setting
from .entity import Entity


class Creature(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        # 战斗有关的属性，以下为默认值，没有什么用（还不是因为python没有变量声明），需要要覆盖这些值
        # 这里写上这些值主要是为了方便IDE提示
        self.maxhp = 1
        self.hp = 1
        self.atk = 1
        self.gold = 1
        self.base_speed = 1.0
        """基础移速"""
        self.speed = self.base_speed
        """当前移速"""
        self.bullet_speed = 1

        self.buffs: List['buff.Buff'] = []
        """当前附加的buff"""

    def update(self):
        for buff_ in self.buffs:
            buff_.update()
            buff_.on_update(self)
            if buff_.is_faded():
                buff_.on_fade(self)

        self.buffs: List['buff.Buff'] = list(filter(lambda b: not b.is_faded(), self.buffs))  # 去除所有到期的buff

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

        # 画buff图标 buff个数过多怎么办？暂时可以不用管，但是还是要考虑
        if self.buffs:
            buff_icon_top = hp_bar_rect.bottom + setting.distance_tiny
            buff_icon_left = hp_bar_rect.left
            buff_icon_rect = pygame.Rect(buff_icon_left, buff_icon_top, setting.buff_icon_width,
                                         setting.buff_icon_width)
            for buff_ in self.buffs:
                if buff_.icon is None:
                    continue  # 没有图标就不画了
                screen.blit(buff_.icon, buff_icon_rect)
                buff_icon_rect.left += buff_icon_rect.width + setting.distance_tiny

    def add_buff(self, buff_: 'buff.Buff'):
        self.buffs.append(buff_)
        buff_.on_inflict(self)

    def pick_item(self, item_: 'item.Item'):
        item_.on_pick(self)

    def take_damage(self, damage: float):
        self.hp -= damage

    def heal(self, heal_hp: float):
        self.hp += heal_hp
        if self.hp > self.maxhp:
            self.hp = self.maxhp
