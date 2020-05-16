"""
存放一些预设的敌人掉落种类
LootTable的构造用法：
LootTable(
    ((掉落物1的类名，权重),...), # 每一个元组（一行）表示一组互斥的掉落，类名使用None表示不掉落
    ...
)
具体可以看下面的例子
"""
from . import item
from .loot_table import LootTable

loot_example = LootTable(
    # 例子：这个loot_table表示必定掉落1个回血道具，同时有50%的概率追加一个
    ((item.ItemHpRegen, 1.0), (None, 1.0)),
    ((item.ItemHpRegen, 1.0),)
)

loot_hp_regen = LootTable(
    ((item.ItemHpRegen, 1.0), (None, 1.0)),
)
