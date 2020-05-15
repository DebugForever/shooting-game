"""
战利品表类，用于生成怪物掉落的战利品
"""
import random
from typing import Union, Tuple, List, Any


class Loot:
    """战利品类，保存一组*互斥的*物品以及其掉落权重"""

    def __init__(self, *loot_list: Tuple[Union[Any, None], float]):
        self.loot_class_list: List[Union[Any, None]] = []
        self.weight_list: List[float] = []
        for loot in loot_list:
            self.add(loot[0], loot[1])

    def add(self, item: Union[Any, None], weight: float):
        """
        增加一种掉落
        :param item:掉落物的类
        :param weight:权重
        :return:None
        """
        self.loot_class_list.append(item)
        self.weight_list.append(weight)

    def gen_loot(self):
        """
        根据掉落表生成一组掉落
        :return:生成的掉落物，不掉落返回None
        """
        wsum = sum(self.weight_list)
        r = random.uniform(0, wsum)
        # improve: 这个算法有些暴力
        # 使用二分查找会更优一些（但是我不会用py的二分查找）
        now_sum = 0.0
        for loot_class, weight in zip(self.loot_class_list, self.weight_list):
            now_sum += weight
            if r <= now_sum:
                if loot_class is None:
                    return None
                else:
                    return loot_class()
        return None


class LootTable:
    def __init__(self, *loot_list_list: Tuple[Tuple[Union[Any, None], float], ...]):
        self.loots: List[Loot] = []
        for loot_list in loot_list_list:
            self.add_loot(*loot_list)

    def gen_loot(self):
        """
        根据已有的掉落表生成一组掉落
        :return 生成的掉落列表，不包含None
        """
        loot_result = []
        for loot in self.loots:
            result = loot.gen_loot()
            if result is not None:
                loot_result.append(result)
        return loot_result

    def add_loot(self, *loot_list: Tuple[Union[Any, None], float]):
        self.loots.append(Loot(*loot_list))
