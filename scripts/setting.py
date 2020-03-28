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
        self.bullet_speed_p = 8.0
        """玩家射出子弹的初始速度"""

        # player
        self.player_fire_cd = 10
        """单位是帧，其他类似的也是一样"""
        self.player_speed = 4.0
        """玩家的移动速度，如果移速可变的话，玩家移动的代码要重写"""
        self.player_hpbar_height = 10
        self.player_hpbar_color_high = (0, 220, 0)
        self.player_hpbar_color_mid = (220, 220, 0)
        self.player_hpbar_color_low = (220, 0, 0)
        self.player_hpbar_line_color = (255, 255, 255)
        self.player_hpbar_line_width = 1

        # enemy
        self.enemy_hpbar_height = 10
        self.enemy_hpbar_color = (0, 220, 0)
        self.enemy_hpbar_line_color = (255, 255, 255)
        self.enemy_hpbar_line_width = 1

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
