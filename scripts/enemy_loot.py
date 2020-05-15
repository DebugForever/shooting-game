"""
存放一些预设的敌人掉落种类
"""
from . import item
from .loot_table import LootTable

loot_hp_regen = LootTable(
    ((item.ItemHpRegen, 1.0), (None, 1.0)),
)
