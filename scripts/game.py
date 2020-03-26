"""
游戏的主类，包含运行中的几乎所有信息
main class of game, contains almost data
"""
import pygame

from pygame.sprite import Group
from math import sin, cos, atan2
from . import setting, image_dict, dbgscreen
from .player import Player
from .enemy import Enemy
from . import constants as c
from .room import Room


class Game:
    """
    游戏的主类，包含运行中的几乎所有信息，负责处理所有游戏功能
    """
    # 类型提示，用于编译器自动补全和消除warning
    canvas: pygame.Surface
    screen: pygame.Surface
    player: Player
    enemies: Group
    bullets_p: Group
    bullets_e: Group
    viewport: pygame.Rect
    clock: pygame.time.Clock
    joystick: pygame.joystick.Joystick
    room: Room
    debug: bool

    def __init__(self):
        pygame.event.set_allowed(setting.event_allowed)
        self.setup()
        self.done = False

    def setup(self):
        self.canvas = pygame.Surface(setting.room_size)
        self.screen = pygame.display.set_mode(setting.screen_resolution)
        pygame.display.set_caption(setting.caption)
        self.debug = setting.debug_default
        self.clock = pygame.time.Clock()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.room = Room()
        self.viewport = pygame.rect.Rect(0, 0, *setting.screen_resolution)
        self.viewport.center = self.room.rect.center
        self.setup_entities()

    def setup_entities(self):
        self.player = Player(image_dict['player'])
        screen_rect = self.canvas.get_rect()  # 感觉这样搞破坏了封装性似乎有点不妥？
        self.player.x = screen_rect.centerx
        self.player.y = screen_rect.centery
        self.player.viewport = self.viewport

        self.enemies = Group()
        self.room.generate(self.enemies)

        self.bullets_p = Group()  # bullets shoot by player
        self.bullets_e = Group()  # bullets shoot by enemy

    def handle_events(self):
        """
        处理所有事件
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.handle_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.is_fire = True
                self.player.fire_control = c.CONTROL_MOUSE
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.is_fire = False
            elif event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joy_axis_events()

    def handle_joy_axis_events(self):
        # 这里有一个问题：手柄和键盘同时操作时，
        # 可能会出现不受控制状态，只需把手柄摇杆摇到中间即可解决，更改代码不好处理。

        # improve:这里应该可以分离处理的，但是我不知道怎么改，（可能通过event拿信息？）
        move_x = self.joystick.get_axis(setting.joystick_axis_move_x)
        move_y = self.joystick.get_axis(setting.joystick_axis_move_y)
        fire_x = self.joystick.get_axis(setting.joystick_axis_fire_x)
        fire_y = self.joystick.get_axis(setting.joystick_axis_fire_y)
        if abs(move_x) >= setting.joystick_min_motion:
            self.player.x_vel = setting.player_speed * move_x
        else:
            self.player.x_vel = 0.0
        if abs(move_y) >= setting.joystick_min_motion:
            self.player.y_vel = setting.player_speed * move_y
        else:
            self.player.y_vel = 0.0

        if abs(fire_x) >= setting.joystick_min_motion or abs(fire_y) >= setting.joystick_min_motion:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_JOYSTICK
            self.player.fire_dir = atan2(fire_y, fire_x)
        else:
            self.player.is_fire = False

    def handle_keydown_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.y_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.y_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.x_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.x_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_KEYBOARD
        elif event.key in keymap[c.CONTROL_DEBUG]:
            self.debug = not self.debug

    def handle_keyup_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.y_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.y_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.x_vel += setting.player_speed
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.x_vel -= setting.player_speed
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = False

    def check_collision_be(self):
        """
        检测子弹与敌人之间的碰撞，并处理这些碰撞
        :return:
        """
        collision = pygame.sprite.groupcollide(self.bullets_p, self.enemies, True, False)

    def check_everything(self):
        if self.player.is_fire:
            self.player.fire(self.bullets_p)
        self.scroll_screen()

    def scroll_screen(self):
        """
        当玩家处于屏幕边缘时滚动屏幕
        :return:
        """
        # 视点应向左移动的距离，下面的三段处理其他方向的代码逻辑和这个是一样的
        # improve:这几段代码有重复的地方（编译器提示），但是我不知道怎么合并起来
        dx_l = self.viewport.left + setting.scroll_dis_x - self.player.rect.left
        if dx_l > 0:
            self.viewport.left = max(0, self.viewport.left - dx_l)  # left必须大于0，否则就看到外面的黑框了

        dx_r = self.player.rect.right + setting.scroll_dis_x - self.viewport.right
        if dx_r > 0:
            self.viewport.right = min(self.room.rect.right, self.viewport.right + dx_r)

        dy_u = self.viewport.top + setting.scroll_dis_y - self.player.rect.top
        if dy_u > 0:
            self.viewport.top = max(0, self.viewport.top - dy_u)

        dy_d = self.player.rect.bottom + setting.scroll_dis_y - self.viewport.bottom
        if dy_d > 0:
            self.viewport.bottom = min(self.room.rect.bottom, self.viewport.bottom + dy_d)

    def update_everything(self):
        dbgscreen.set_fps(int(self.clock.get_fps()))
        self.player.update()
        self.bullets_p.update()
        self.enemies.update()

    def draw_everything(self):
        # 先执行的绘画会在最底下
        self.canvas.fill((220, 220, 220))
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        for bullet in self.bullets_p:
            bullet.draw(self.canvas)
        self.player.draw(self.canvas)
        self.screen.blit(self.canvas, (0, 0), self.viewport)
        if self.debug:
            dbgscreen.draw(self.screen)

    def run(self):
        while not self.done:
            self.handle_events()
            self.check_everything()
            self.update_everything()
            self.draw_everything()
            pygame.display.flip()
            self.clock.tick(setting.fps_limit)  # 限制帧数
        pygame.quit()
