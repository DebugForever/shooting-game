"""
放置一些便于debug的工具和类
debug tools
"""
import pygame
from . import setting


class DebugScreen:
    """
    显示，绘制debug屏幕，接收发来的debug信息，并显现在屏幕上
    """

    def __init__(self):
        self.screen = pygame.Surface(setting.screen_resolution, pygame.SRCALPHA)
        self.font = pygame.font.Font(None, setting.dbgscreen_font_size)
        self.line_height = setting.dbgscreen_line_height  # 行高，每一行字体所占的高度
        self.color = setting.dbgscreen_font_color
        self.fps_pos = (setting.dbgscreen_fps_x, setting.dbgscreen_fps_y)
        self.msg_x = setting.dbgscreen_main_x
        self.msg_y1 = setting.dbgscreen_main_top
        self.msg_y2 = setting.dbgscreen_main_bottom
        self.msg = []  # 存储要显示的debug信息，每条一行
        self.max_msg = int((self.msg_y2 - self.msg_y1) / self.line_height)  # 最多能同时显示的信息行数
        self.fps = 0  # 暂存fps，用于打印

    def set_fps(self, fps: int):
        self.fps = fps

    def prep_fps(self):
        text_bitmap = self.font.render('fps:' + str(self.fps), True, self.color)
        self.screen.blit(text_bitmap, self.fps_pos)

    def print(self, *args):
        arglen = len(args)
        if arglen > 1:  # 这样写，使之更像python的print
            self.msg.append(str(args))
        elif arglen == 1:
            self.msg.append(str(args[0]))
        else:
            pass
        if len(self.msg) > self.max_msg:
            self.msg.pop(0)

    def prep_main(self):  # maim指主消息区
        x = self.msg_x
        y = self.msg_y1
        for msg in self.msg:
            text_bitmap = self.font.render(msg, True, self.color)
            self.screen.blit(text_bitmap, (x, y))
            y += self.line_height

    def draw(self, screen: pygame.Surface):
        self.screen.fill(pygame.SRCALPHA)
        self.prep_fps()
        self.prep_main()
        screen.blit(self.screen, (0, 0))
