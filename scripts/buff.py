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
        return self.tick_left <= 0

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
        self.duration = 5 * setting.fps_limit
        self.tick_left = self.duration
        self.name = 'burn'
        self.icon = image_dict['buff1']

    def on_update(self, target: 'creature.Creature'):
        target.take_damage(0.1)


class BuffRegen(Buff):
    def __init__(self):
        super().__init__()
        self.id = 2
        self.duration = 10 * setting.fps_limit
        self.tick_left = self.duration
        self.name = 'regen'
        self.icon = image_dict['buff2']

    def on_update(self, target: 'creature.Creature'):
        target.heal(0.1)


class BuffSlow_down(Buff):
    """
    减速buff，确实不好搞，因为会更改属性，所以要慎重考虑叠加的问题，所以决定每次就是从速度加减的方面考虑
    而不去考虑乘法
    """
    def __init__(self):
        super().__init__()
        self.id = 3
        self.duration = 10*setting.fps_limit
        self.tick_left = self.duration
        self.name = 'slow_down'
        self.icon = image_dict['buff3']

    def on_inflict(self, target: 'creature.Creature'):  # 使用前向声明并不导入具体的类来防止循环导入
        """上buff（应用buff）时调用的函数"""
        target.base_speed -= 2

    def on_fade(self, target: 'creature.Creature'):
        """buff自然消失（时间结束）时调用的函数"""
        target.base_speed += 2


class BuffShield(Buff):
    """
    盾牌 增加血量（因为没有防御力这一说）
    血量的增加使用了非常暴力的方式，通过对其maxhp*2来直接处理
    """
    def __init__(self):
        super().__init__()
        self.id = 4
        self.duration = 10*setting.fps_limit
        self.tick_left = self.duration
        self.name = 'Shield'
        self.icon = image_dict['shield']

    def on_inflict(self, target: 'creature.Creature'):  # 使用前向声明并不导入具体的类来防止循环导入
        """上buff（应用buff）时调用的函数"""
        target.hp += target.maxhp
        target.maxhp *= 2
        if target.hp > target.maxhp:
            target.hp = target.maxhp

    def on_fade(self, target: 'creature.Creature'):
        """buff自然消失（时间结束）时调用的函数"""
        tmp = target.maxhp // 2
        target.hp = target.hp//2
        if target.hp < 0:
            target.hp = 0


class BuffBow(Buff):
    """
    增加子弹速度的buff
    """
    def __init__(self):
        super().__init__()
        self.id = 5
        self.duration = 10*setting.fps_limit
        self.tick_left = self.duration
        self.name = 'Row'
        self.icon = image_dict['bow']

    def on_inflict(self, target: 'creature.Creature'):  # 使用前向声明并不导入具体的类来防止循环导入
        """上buff（应用buff）时调用的函数"""
        target.bullet_speed += 10

    def on_fade(self, target: 'creature.Creature'):
        """buff自然消失（时间结束）"""
        target.bullet_speed -= 10


class BuffSword(Buff):
    """
    增加自身攻击力的buff
    """
    def __init__(self):
        super().__init__()
        self.id = 6
        self.duration = 10*setting.fps_limit
        self.tick_left = self.duration
        self.name = 'Sword'
        self.icon = image_dict['sword']

    def on_inflict(self, target: 'creature.Creature'):  # 使用前向声明并不导入具体的类来防止循环导入
        """上buff（应用buff）时调用的函数"""
        target.atk += 10

    def on_fade(self, target: 'creature.Creature'):
        """buff自然消失（时间结束）时调用的函数"""
        target.atk -= 10