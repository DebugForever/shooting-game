"""
增益和减益
buffs and debuffs
"""
from typing import Optional

import pygame
from . import creature, dbgscreen, setting, image_dict


class Buff:
    """所有buff的基类,或许应该叫buff_abc或者buff_base？"""

    def __init__(self):
        self.id = 0
        self.duration = 0
        """初始持续时间"""
        self.tick_left = 0
        """剩余时间"""
        self.name = ''
        """buff显示的名字"""
        self.icon: Optional[pygame.Surface] = None
        """没有icon（图标）的buff不会显示"""

    def is_faded(self):
        return self.tick_left > 0

    def update(self):
        self.tick_left -= 1

    def on_inflict(self, target: 'creature.Creature'):  # 使用前向声明并不导入具体的类来防止循环导入
        """上buff（应用buff）时调用的函数，需要子类覆盖"""
        pass

    def on_fade(self, target: 'creature.Creature'):
        """buff自然消失（时间结束）时调用的函数，需要子类覆盖"""
        pass

    def on_update(self, target: 'creature.Creature'):
        """每帧更新的时候，buff对目标有什么影响，比如中毒"""
        pass


class BuffBurn(Buff):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.duration = 30 * setting.fps_limit
        self.tick_left = self.duration
        self.name = 'burn'
        self.icon = image_dict['buff1']

    def on_update(self, target: 'creature.Creature'):
        target.hp -= 0.1
        dbgscreen.print(target.hp)
