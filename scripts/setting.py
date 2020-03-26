"""
包含游戏的一些设置，这些设置不会在运行时改变，所以使用全局变量，方便使用
contains game static settings
"""
import pygame.constants as pgc
from . import constants as c
import pygame


class Setting:
    def __init__(self):
        # display
        self.screen_width = 800
        self.screen_height = 600
        self.screen_resolution = (self.screen_width, self.screen_height)  # 分辨率
        self.caption = 'shooting game'  # 游戏标题
        ''' 需要锁帧率。因为攻击间隔等效果的实现都依赖帧率，
        不锁帧会导致游戏的速度在不同的机器上有不同的表现'''
        self.fps_limit = 60
        self.scroll_dis_x = self.screen_width / 6  # 离边缘多少距离开始滚屏
        self.scroll_dis_y = self.screen_height / 6

        # key
        self.keymap = {
            c.CONTROL_UP: [pgc.K_UP, pgc.K_w],
            c.CONTROL_DOWN: [pgc.K_DOWN, pgc.K_s],
            c.CONTROL_LEFT: [pgc.K_LEFT, pgc.K_a],
            c.CONTROL_RIGHT: [pgc.K_RIGHT, pgc.K_d],
            c.CONTROL_FIRE: [pgc.K_SPACE, pgc.K_j],
            c.CONTROL_DEBUG: [pgc.K_BACKSPACE, ]
        }

        # event
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

        # room
        self.room_size = (1200, 800)

        # debug
        self.dbgscreen_font_face = 'YaHei Consolas Hybrid'
        self.dbgscreen_font_size = 18
        self.dbgscreen_font_color = pygame.Color('black')
        self.dbgscreen_line_height = 20
        self.dbgscreen_main_x = int(self.screen_width * 0.1)
        self.dbgscreen_main_top = int(self.screen_height * 0.3)
        self.dbgscreen_main_bottom = int(self.screen_height * 0.9)
        self.dbgscreen_fps_x = self.dbgscreen_main_x
        self.dbgscreen_fps_y = int(self.screen_height * 0.03)
