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
        self.screen_resolution = (self.screen_width, self.screen_height)
        """分辨率，宽*高"""
        self.caption = 'shooting game'
        """游戏标题"""

        self.fps_limit = 60
        '''
        帧率上限。
        需要锁帧率。因为攻击间隔等效果的实现都依赖帧率，
        不锁帧会导致游戏的速度在不同的机器上有不同的表现。
        '''

        # 物体之间的距离常量，方便使用和管理
        self.distance_tiny = 5
        self.distance_small = 20
        self.distance_mid = 50
        self.distance_big = 200
        self.distance_huge = 400

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

        # player
        self.player_fire_cd = 10
        """单位是帧，其他类似的也是一样"""

        # hp_bar 血条
        self.hpbar_height = 10
        self.hpbar_color = (0, 220, 0)
        self.hpbar_line_color = (255, 255, 255)
        self.hpbar_line_width = 1

        # joystick
        self.joystick_min_motion = 0.2
        """检测有效移动的阈值"""
        self.joystick_axis_move_x = 0
        """控制移动的摇杆对应的编号，下同"""
        self.joystick_axis_move_y = 1
        self.joystick_axis_fire_x = 4
        self.joystick_axis_fire_y = 3

        # room
        self.room_size = (1200, 800)

        # debug
        self.debug_default = True
        self.dbgscreen_font_face = 'YaHei Consolas Hybrid'
        self.dbgscreen_font_size = 18
        self.dbgscreen_font_color = pygame.Color('black')
        self.dbgscreen_line_height = 20
        self.dbgscreen_main_left = int(self.screen_width * 0.1)
        self.dbgscreen_main_top = int(self.screen_height * 0.3)
        self.dbgscreen_main_bottom = int(self.screen_height * 0.9)
        self.dbgscreen_fps_x = self.dbgscreen_main_left
        self.dbgscreen_fps_y = int(self.screen_height * 0.03)
        self.dbgscreen_hint_right = int(self.screen_width * 0.9)
        self.dbgscreen_hint_top = self.dbgscreen_fps_y

        # buff
        self.buff_icon_width = 30
        self.buff_icon_height = 30
