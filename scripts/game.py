"""
游戏的主类，包含运行中的几乎所有信息
main class of game, contains almost data
"""
import pygame

from pygame.sprite import Group
from math import sin, cos, atan2
from . import setting, image_dict, dbgscreen
from . import buff
from .entity import Entity
from .player import Player
from .enemy import Enemy
from . import constants as c
from .room import Room, BattleRoom
from .tools import fix_entity_collision

from .room import Room
from .button import Button


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
    obstacles: Group
    viewport: pygame.Rect
    clock: pygame.time.Clock
    joystick: pygame.joystick.Joystick
    room: Room
    debug: bool
    active: bool  # 关于游戏活动状态与否
    play_button: Button

    def __init__(self):
        pygame.event.set_allowed(setting.event_allowed)
        self.setup()
        self.done = False
        self.active = False  # 初始时游戏状态为False

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
        """
        按钮的设置
        """
        self.play_button = Button(self.screen, "Play")

    def setup_entities(self):
        self.player = Player(image_dict['player'])
        screen_rect = self.canvas.get_rect()
        self.player.x = screen_rect.centerx
        self.player.y = screen_rect.centery
        self.player.viewport = self.viewport  # 感觉这样搞破坏了封装性似乎有点不妥？

        self.enemies = Group()
        """所有敌人的群组"""
        self.bullets_p = Group()
        """玩家射出的子弹"""
        self.bullets_e = Group()
        """敌人射出的子弹"""
        self.obstacles = Group()
        """障碍物"""
        # 注册room内的这些东西，这么写感觉很抠脚，有没有改进方法呢？
        self.room.setup(self.enemies, self.bullets_p, self.bullets_e, self.obstacles, self.player)
        self.room.generate()

    def handle_events(self):
        """
        处理所有事件
        :return:
        """
        for event in pygame.event.get():
            if not self.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.handle_check_play_button(mouse_x, mouse_y)
                elif event.type == pygame.QUIT:
                    self.done = True
                else:
                    continue
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

    def handle_check_play_button(self, mouse_x, mouse_y):
        """
        检查鼠标按键是否点击了botton
        """
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self.active = True
        if self.active:
            self.game_restart()

    def handle_joy_axis_events(self):
        """
        这里有一个问题：手柄和键盘同时操作时，
        可能会出现不受控制状态，只需把手柄摇杆摇到中间即可解决，更改代码不好处理。

        improve:这里应该可以分离处理的，但是我不知道怎么改，（可能通过event拿信息？）
        """
        move_x = self.joystick.get_axis(setting.joystick_axis_move_x)
        move_y = self.joystick.get_axis(setting.joystick_axis_move_y)
        fire_x = self.joystick.get_axis(setting.joystick_axis_fire_x)
        fire_y = self.joystick.get_axis(setting.joystick_axis_fire_y)
        if abs(move_x) >= setting.joystick_min_motion:
            self.player.control_factor_x = move_x
        else:
            self.player.control_factor_x = 0.0
        if abs(move_y) >= setting.joystick_min_motion:
            self.player.control_factor_y = move_y
        else:
            self.player.control_factor_y = 0.0

        if abs(fire_x) >= setting.joystick_min_motion or abs(fire_y) >= setting.joystick_min_motion:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_JOYSTICK
            self.player.fire_dir = atan2(fire_y, fire_x)
        else:
            self.player.is_fire = False

    def handle_keydown_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.control_factor_y -= 1.0
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.control_factor_y += 1.0
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.control_factor_x -= 1.0
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.control_factor_x += 1.0
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = True
            self.player.fire_control = c.CONTROL_KEYBOARD
        elif event.key in keymap[c.CONTROL_DEBUG]:
            self.debug = not self.debug

    def handle_keyup_events(self, event: pygame.event.Event):
        keymap = setting.keymap
        if event.key in keymap[c.CONTROL_UP]:
            self.player.control_factor_y += 1.0
        elif event.key in keymap[c.CONTROL_DOWN]:
            self.player.control_factor_y -= 1.0
        elif event.key in keymap[c.CONTROL_LEFT]:
            self.player.control_factor_x += 1.0
        elif event.key in keymap[c.CONTROL_RIGHT]:
            self.player.control_factor_x -= 1.0
        elif event.key in keymap[c.CONTROL_FIRE]:
            self.player.is_fire = False

    def check_collision_be(self):
        """
        检测子弹与敌人之间的碰撞，并处理这些碰撞
        be:bullet and enemy
        :return:
        """
        collision = pygame.sprite.groupcollide(self.enemies, self.bullets_p, False, True)
        for enemy, bullets in collision.items():
            for bullet in bullets:
                enemy.hp -= bullet.damage
            if enemy.hp <= 0:
                enemy.kill()  # kill函数会把它从所有群组里移除（pygame提供）

    def check_collision_bp(self):
        """
        检测子弹与玩家之间的碰撞，并处理这些碰撞
        bp:bullet and player
        :return:
        """
        collision = pygame.sprite.spritecollide(self.player, self.bullets_e, True)
        for bullet in collision:
            self.player.hp -= bullet.damage
        if self.player.hp <= 0:
            self.active = False

    def check_everything(self):
        if self.player.is_fire:
            self.player.fire(self.bullets_p)
        self.check_collision_be()
        self.check_collision_bp()
        self.scroll_screen()

    def scroll_screen(self):
        """
        当玩家处于屏幕边缘时滚动屏幕
        improve:这几段代码有重复的地方（编译器提示），但是我不知道怎么合并起来
        :return:
        """
        dx_l = self.viewport.left + setting.scroll_dis_x - self.player.rect.left
        """视点应向左移动的距离，下面的三段处理其他方向的代码逻辑和这个是一样的"""
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

    def remove_outbound_bullets(self):
        for bullets in (self.bullets_p, self.bullets_e):
            for bullet in bullets:
                if not self.room.rect.colliderect(bullet.rect):  # 如果两个矩形没有交点
                    bullet.kill()  # 那么子弹出界，删除掉

    def make_all_in_bound(self):  # but remove outbound bullets
        """
        当有非子弹实体将要移动出边界时，将它移回边界内
        子弹实体出边界会销毁
        :return:
        """
        self.player.make_in_bound(self.room.rect)
        for enemy in self.enemies:
            enemy.make_in_bound(self.room.rect)
        self.remove_outbound_bullets()

    def update_everything(self):
        dbgscreen.set_fps(int(self.clock.get_fps()))
        self.player.update()
        self.bullets_p.update()
        self.bullets_e.update()
        self.enemies.update()
        self.make_all_in_bound()

    def draw_everything(self):
        # 先执行的绘画会在最底下
        self.canvas.fill((220, 220, 220))
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        for bullet in self.bullets_p:
            bullet.draw(self.canvas)
        for bullet in self.bullets_e:
            bullet.draw(self.canvas)
        for obstacle in self.obstacles:
            obstacle.draw(self.canvas)
        self.player.draw(self.canvas)
        self.screen.blit(self.canvas, (0, 0), self.viewport)
        if self.debug:
            dbgscreen.draw(self.screen)

        if not self.active:
            self.play_button.draw()

    def enemy_ai(self):
        """
        总感觉这个名字取得不是很好。
        调用所有敌人的ai()函数，处理它们的所有行动
        :return:
        """
        for enemy in self.enemies:
            enemy.ai()

    def fix_block_entity_collision(self):
        """
        处理实体与障碍物之间的碰撞（重叠）。
        对于子弹：销毁
        对于其他实体：移动至范围外面
        """

        # 清除碰撞的子弹
        for group in self.bullets_e, self.bullets_p:
            pygame.sprite.groupcollide(group, self.obstacles, True, False)

        collision = pygame.sprite.groupcollide(self.obstacles, self.enemies, False, False)
        for block, collided_enemys in collision.items():
            for enemy in collided_enemys:
                fix_entity_collision(enemy, block)

        collision = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if collision:
            fix_entity_collision(self.player, collision[0])

    def game_restart(self):
        """
        游戏重新启动:包括步骤：清空之前所有的数组
        重新放入数组
        """
        self.enemies.empty()
        self.bullets_e.empty()
        self.bullets_p.empty()
        self.setup_entities()

    def run(self):
        while not self.done:
            dbgscreen.show('(debug)bullet_count:{}'.format(len(self.bullets_p) + len(self.bullets_e)))
            dbgscreen.show(f'enemy_count:{len(self.enemies)}')
            self.handle_events()
            if self.active:
                # 只有当游戏启动时敌人才会移动
                # 数组才会更新
                self.check_everything()
                self.enemy_ai()
                self.update_everything()
                self.fix_block_entity_collision()
            self.draw_everything()
            pygame.display.flip()
            self.clock.tick(setting.fps_limit)  # 限制帧数。同时，只有用了tick，pygame内置的fps()才能使用

        pygame.quit()
