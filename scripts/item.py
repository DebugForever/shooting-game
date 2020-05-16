"""
道具类
这个道具指的是在地上的道具
"""
import pygame

from .entity import Entity
from . import creature, image_dict, buff


class Item(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)

    def on_pick(self, target: 'creature.Creature'):
        """
        拾取时触发的函数，需要子类覆盖。
        需要注意的是：有一些特殊的道具，拾取后不仅仅能影响自身的状态，
        比如下一关的出口等。
        """
        pass


class ItemHpRegen(Item):
    def __init__(self):
        super().__init__(image_dict['item1'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffRegen())


class ItemSlowDown(Item):
    def __init__(self):
        super().__init__(image_dict['item3'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffSlow_down())


class ItemShield(Item):
    def __init__(self):
        super().__init__(image_dict['shield'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffShield())


class ItemBow(Item):
    def __init__(self):
        super().__init__(image_dict['bow'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffBow())


class ItemSword(Item):
    def __init__(self):
        super().__init__(image_dict['sword'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffSword())