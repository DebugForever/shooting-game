from .setting import Setting
from .tools import load_all_images
import os
import pygame

pygame.init()
pygame.joystick.init()

setting = Setting()
pygame.display.set_mode(setting.screen_resolution)  # 必须set_mode之后才能载入图片
image_dict = load_all_images(os.path.join('resources', 'images'))

from . import debug

dbgscreen = debug.DebugScreen()  # 把这个设为全局变量是因为你在代码的每一个地方都有可能要dbg_print
