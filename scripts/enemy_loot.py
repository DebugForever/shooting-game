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
    # 例子：这个loot_table表示必定掉落1个回血道具，同时有67%的概率追加一个
    ((item.ItemHpRegen, 2.0), (None, 1.0)),
    ((item.ItemHpRegen, 1.0),)
)

loot_hp_regen = LootTable(
    ((item.ItemHpRegen, 1.0), (None, 1.0)),
)

loot_enemy_normal = LootTable(
    ((item.ItemHpPotion, 1.0), (item.ItemSword, 1.0), (None, 3.0)),
)
"""普通怪掉落"""

loot_enemy_elite = LootTable(
    ((item.ItemHpRegen, 1.0),),
    ((item.ItemHpRegen, 1.0), (None, 4.0)),
    ((item.ItemSword, 1.0), (item.ItemShield, 1.0), (item.ItemBow, 1.0), (None, 2.0)),
)
"""精英怪掉落"""

loot_treasure_box = LootTable(
    ((item.ItemHpPotion, 1.0),),
    ((item.ItemSword, 1.0), (item.ItemShield, 1.0)),
    ((item.ItemHpRegen, 1.0), (item.ItemSlowDown, 1.0), (item.ItemBow, 1.0)),
)
"""给宝箱制作的掉落物"""
