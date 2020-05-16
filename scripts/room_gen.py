"""
生成随机房间
"""
from .loot_table import Loot
from .room import BattleRoom, BattleRoom2, BattleRoom3, BattleRoom4, Room

# 这里偷懒直接用了Loot类，虽然名字有点不对劲，但是功能是一样的
random_room = Loot(
    (BattleRoom, 1),
    (BattleRoom2, 1),
    (BattleRoom3, 1),
    (BattleRoom4, 1),
)


def get_random_room() -> Room:
    """

    :rtype: object
    """
    return random_room.gen_loot()
