"""
游戏的入口点
entry point
"""
from pygame import quit
from scripts.game import Game

game = Game()
game.run()
quit()
