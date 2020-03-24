"""
包含游戏的一些设置，这些设置不会在运行时改变，所以使用全局变量，方便使用
contains game static settings
"""
import pygame.constants as pgc
from . import constants as c


class Setting:
    def __init__(self):
        self.screen_resolution = (800, 600)  # 分辨率
        self.caption = 'shooting game'  # 游戏标题

        ''' 需要锁帧率。因为攻击间隔等效果的实现都依赖帧率，
        不锁帧会导致游戏的速度在不同的机器上有不同的表现'''
        self.fps_limit = 60

        self.keymap = {
            c.CONTROL_UP: [pgc.K_UP, pgc.K_w],
            c.CONTROL_DOWN: [pgc.K_DOWN, pgc.K_s],
            c.CONTROL_LEFT: [pgc.K_LEFT, pgc.K_a],
            c.CONTROL_RIGHT: [pgc.K_RIGHT, pgc.K_d],
            c.CONTROL_FIRE: [pgc.K_SPACE, pgc.K_j],
            c.CONTROL_FPS: [pgc.K_BACKSPACE, ]
        }

        self.event_allowed = [pgc.JOYAXISMOTION, pgc.MOUSEBUTTONDOWN, pgc.MOUSEBUTTONUP, pgc.KEYDOWN, pgc.KEYUP]

        # bullet
        self.bullet_speed_p = 8.0  # 玩家射出子弹的初始速度
        self.bullet_speed_e = 2.0  # 敌人射出子弹的初始速度

        # player
        self.player_fire_cd = 10  # 单位是帧，其他类似的也是一样
        self.player_speed = 4.0

        # joystick
        self.joystick_min_motion = 0.2
        self.joystick_axis_move_x = 0
        self.joystick_axis_move_y = 1
        self.joystick_axis_fire_x = 4
        self.joystick_axis_fire_y = 3
