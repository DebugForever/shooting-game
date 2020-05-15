import pygame
import os
from typing import Dict

class Music():
    """
    关于音乐的类
    """
    all_music: dict() # 全部音乐的字典,但是不知道里面填什么(sound不是类名)，就暂时这样放着
    background_music: pygame.mixer.Sound
    player_shoot: pygame.mixer.Sound
    player_hit: pygame.mixer.Sound

    def __init__(self):
        pygame.mixer.init()
        self.all_music = dict()
        self.load_all_music(os.path.join('resources', 'cd'))
        self.player_shoot = self.all_music["play_shoot"]
        self.player_shoot.set_volume(0.1)
        self.background_music = self.all_music['bgm']
        self.background_music.set_volume(0.5)

    def load_all_music(self, directory: str, accept_suffixs: tuple = ('.ogg', '.wav') ) :
        """
        :param directory:要读取的路径
        :param accept_suffixs要读取的格式
        """
        all_music = dict()
        for music in os.listdir(directory):
            name, suffix = os.path.splitext(music)
            if suffix.lower() in accept_suffixs:
                music_path = os.path.join(directory, music)
                self.all_music[name] = pygame.mixer.Sound(music_path)

    def play_background_music(self):
        self.background_music.stop()
        self.background_music.play(-1)

    def play_player_shoot(self):
        self.player_shoot.stop()
        self.player_shoot.play()

    def end_background_music(self):
        self.background_music.stop()