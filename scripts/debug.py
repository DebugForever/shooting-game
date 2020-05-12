"""
放置一些便于debug的工具和类
debug tools
"""
import pygame
from . import setting
from typing import Union, Any


class DebugScreen:
    """
    显示，绘制debug屏幕，接收发来的debug信息，并显现在屏幕上
    todo:给每个实体加上id，并且在debug模式下显示id
    """

    def __init__(self):
        self.screen = pygame.Surface(setting.screen_resolution, pygame.SRCALPHA)
        self.font = pygame.font.SysFont(setting.dbgscreen_font_face, setting.dbgscreen_font_size)
        """字体类，用于渲染文字"""
        self.line_height = setting.dbgscreen_line_height
        """行高，每一行字体所占的高度"""
        self.color = setting.dbgscreen_font_color

        self.fps = 0
        """暂存fps，用于打印"""
        self.fps_pos = (setting.dbgscreen_fps_x, setting.dbgscreen_fps_y)

        self.msg_x = setting.dbgscreen_main_left
        self.msg_y1 = setting.dbgscreen_main_top
        self.msg_y2 = setting.dbgscreen_main_bottom
        self.msg = []
        """存储要显示的debug信息，每条一行，此消息会滚动。"""
        self.max_msg = int((self.msg_y2 - self.msg_y1) / self.line_height)
        """最多能同时显示的信息行数"""

        # 这里采用不同的命名是因为如果是左上角，可以直接用来画，右上角需要计算（其实就是我懒得改了）
        self.hint_right = setting.dbgscreen_hint_right
        self.hint_top = setting.dbgscreen_hint_top
        self.hint = []
        """
        存储要显示的debug信息，每条一行。此消息会一直留在这里，不会滚动，每次绘制都会清空此消息，
        所以，如果存储每帧都打印的消息的话，就会一直留在此处。
        """

    def set_fps(self, fps: Union[int, float]):
        self.fps = fps

    def prep_fps(self):
        text_bitmap = self.font.render('fps:' + str(self.fps), True, self.color)
        self.screen.blit(text_bitmap, self.fps_pos)

    def print(self, *args: Any):
        arglen = len(args)
        msg = ''
        if arglen > 1:  # 这样写，使之更像python的print
            msg = str(args)
        elif arglen == 1:
            msg = str(args[0])

        self.msg.append(msg)

        if len(self.msg) > self.max_msg:
            self.msg.pop(0)

    def show(self, *args: Any):
        arglen = len(args)
        msg = ''
        if arglen > 1:
            msg = str(args)
        elif arglen == 1:
            msg = str(args[0])

        self.hint.append(msg)

    def prep_main(self):
        """
        main指主消息区，主消息区的消息是滚动的
        :return:
        """
        x = self.msg_x
        y = self.msg_y1
        for msg in self.msg:
            text_bitmap = self.font.render(msg, True, self.color)
            self.screen.blit(text_bitmap, (x, y))
            y += self.line_height

    def prep_hint(self):
        """
        hint指常驻消息区，此消息不会滚动
        :return:
        """
        right = self.hint_right
        top = self.hint_top
        for msg in self.hint:
            text_bitmap = self.font.render(msg, True, self.color)
            text_rect: pygame.Rect = text_bitmap.get_rect()
            text_rect.right = right
            text_rect.top = top
            top += self.line_height
            self.screen.blit(text_bitmap, text_rect)

        self.hint.clear()

    def draw(self, screen: pygame.Surface):
        self.screen.fill(pygame.SRCALPHA)
        self.prep_fps()
        self.prep_hint()
        self.prep_main()
        screen.blit(self.screen, (0, 0))
