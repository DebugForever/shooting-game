"""
道具类
这个道具指的是在地上的道具
"""
import pygame

from . import creature, image_dict, buff
from .entity import Entity


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


class ItemExit(Item):
    """房间出口，用于切换关卡"""

    def __init__(self, next_room_class=None):
        """指定下一个房间，不指定则随机"""
        super().__init__(image_dict['roomexit'])
        self.next_room_class = next_room_class


class ItemHpRegen(Item):
    def __init__(self):
        super().__init__(image_dict['item1'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffRegen())


class ItemSlowDown(Item):
    def __init__(self):
        super().__init__(image_dict['slow'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffSlowDown())


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


class ItemHpPotion(Item):
    def __init__(self):
        super().__init__(image_dict['hp_potion'])

    def on_pick(self, target: 'creature.Creature'):
        target.add_buff(buff.BuffHeal())
