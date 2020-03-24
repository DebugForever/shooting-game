"""
包含游戏的一些设置，这些设置不会在运行时改变，所以使用全局变量，方便使用
contains game static settings
"""
import pygame.constants as pgc


class Setting:
    def __init__(self):
        self.screen_resolution = (800, 600)  # 分辨率
        self.caption = 'shooting game'  # 游戏标题

        ''' 需要锁帧率。因为攻击间隔等效果的实现都依赖帧率，
        不锁帧会导致游戏的速度在不同的机器上有不同的表现'''
        self.fps_limit = 60

        self.keymap = {'up': pgc.K_UP, 'down': pgc.K_DOWN, 'left': pgc.K_LEFT, 'right': pgc.K_RIGHT,
                       'fire': pgc.K_SPACE}

        # bullet
        self.bullet_speed_p = 8.0  # 玩家射出子弹的初始速度
        self.bullet_speed_e = 2.0  # 敌人射出子弹的初始速度

        # player
        self.player_fire_cd = 10  # 单位是帧，其他类似的也是一样
        self.player_speed = 4.0
