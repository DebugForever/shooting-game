from .setting import Setting
from .tools import load_all_images
import os
import pygame

setting = Setting()
pygame.display.set_mode(setting.screen_resolution)  # 必须set_mode之后才能载入图片
image_dict = load_all_images(os.path.join('resources', 'images'))
