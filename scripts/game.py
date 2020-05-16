"""
游戏的主类，包含运行中的几乎所有信息
main class of game, contains almost data
"""
from math import atan2
from typing import Optional

import pygame
from pygame.sprite import Group

from . import constants as c
from . import item
from . import setting, image_dict, dbgscreen
from .button import Menu
from .item import ItemExit
from .music import Music
from .player import Player
from .room import DebugRoom
from .room import Room
from .room_gen import get_random_room
from .tools import fix_entity_collision


class Game:
    """
    游戏的主类，包含运行中的几乎所有信息，负责处理所有游戏功能
    """
    # 类型提示，用于编译器自动补全和消除warning
    canvas: pygame.Surface
    screen: pygame.Surface
    screen_rect: pygame.Rect
    player: Player
    enemies: Group
    bullets_p: Group
    bullets_e: Group
    obstacles: Group
    items: Group
    viewport: pygame.Rect
    clock: pygame.time.Clock
    joystick: pygame.joystick.Joystick
    room: Room
    debug: bool
    active: str
    """关于游戏活动状态，对应的状态设置在了constants"""
    play_list: Menu
    """一个集成了所有菜单的类，包括play按钮，menu，list功能"""
    game_music: Music
    room_passed: int

    def __init__(self):
        pygame.event.set_allowed(setting.event_allowed)
        self.setup()
        self.done = False
        self.active = c.ACTIVE_START  # 初始时游戏状态为actice_start

    def setup(self):
        self.canvas = pygame.Surface(setting.room_size)
        self.screen = pygame.display.set_mode(setting.screen_resolution)
        pygame.display.set_caption(setting.caption)
        self.debug = setting.debug_default
        self.clock = pygame.time.Clock()
        self.room_passed = 0

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.room = DebugRoom()
        self.viewport = pygame.rect.Rect(0, 0, *setting.screen_resolution)
        self.viewport.center = self.room.rect.center
        self.setup_entities()

        self.play_list = Menu(self.screen)
        self.active = c.ACTIVE_START
        self.game_music = Music()

    def setup_entities(self):
        self.player = Player(image_dict['player'])
        self.screen_rect = self.canvas.get_rect()
        self.player.x = self.screen_rect.centerx
        self.player.y = self.screen_rect.centery
        self.player.viewport = self.viewport  # 感觉这样搞破坏了封装性似乎有点不妥？

        self.enemies = Group()
        """所有敌人的群组"""
        self.bullets_p = Group()
        """玩家射出的子弹"""
        self.bullets_e = Group()
        """敌人射出的子弹"""
        self.obstacles = Group()
        """障碍物"""
        self.items = Group()
        """地上的道具"""

        # 注册room内的这些东西，这么写感觉很抠脚，有没有改进方法呢？
        self.room = DebugRoom()
        self.room.setup(self.enemies, self.bullets_p, self.bullets_e, self.obstacles, self.items, self.player)
        self.room.generate()

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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_check_play_button(mouse_x, mouse_y)
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
        状态       按钮   ->   转移状态
        start and button ->   play
        play  and menu   ->   list
        list  and continue->  play
        list  and quit   ->   quit
        list  and restart->   play
        """
        if self.active == c.ACTIVE_START and self.play_list.button.rect.collidepoint(mouse_x, mouse_y):
            self.active = c.ACTIVE_PLAY
            return

        if self.active == c.ACTIVE_PLAY and self.play_list.menu.rect.collidepoint(mouse_x, mouse_y):
            self.active = c.ACTIVE_LIST
            return

        if self.active == c.ACTIVE_LIST and self.play_list.option_continue.rect.collidepoint(mouse_x, mouse_y):
            self.active = c.ACTIVE_PLAY
            return
        elif self.active == c.ACTIVE_LIST and self.play_list.option_quit.rect.collidepoint(mouse_x, mouse_y):
            self.active = c.ACTIVE_QUIT
            self.done = True
            return
        elif self.active == c.ACTIVE_LIST and self.play_list.option_restart.rect.collidepoint(mouse_x, mouse_y):
            self.active = c.ACTIVE_START
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
                enemy.take_damage(bullet.damage)

    def check_collision_bp(self):
        """
        检测子弹与玩家之间的碰撞，并处理这些碰撞
        bp:bullet and player
        :return:
        """
        collision = pygame.sprite.spritecollide(self.player, self.bullets_e, True)
        for bullet in collision:
            self.player.take_damage(bullet.damage)

    def check_collision_ip(self):
        """
        检查地上物品与玩家的碰撞，并处理
        ip:item and player
        """
        switch_room = False
        next_room: Optional[Room] = None
        collision = pygame.sprite.spritecollide(self.player, self.items, True)
        for item_ in collision:
            item_.on_pick(self.player)
            if isinstance(item_, item.ItemExit):  # 碰到了下一关道具
                if item_.next_room_class is not None:
                    next_room = item_.next_room_class()
                else:
                    next_room = get_random_room()
        # 处理完所有道具的拾取再切换
        if next_room is not None:
            next_room.inherit(self.room)
            self.room = next_room
            self.room.clear()
            self.room.generate()
            self.room_passed += 1

    def check_room_finish(self):
        if len(self.room.enemies) == 0 and not self.room.done:  # 打完了生成一个下一关道具
            self.room.done = True  # 防止多次生成
            self.room.spawn_item(ItemExit(), self.player.x + setting.distance_big, self.player.y)
            self.room.spawn_item(ItemExit(), self.player.x - setting.distance_big, self.player.y)

    def check_everything(self):
        if self.player.is_fire:
            self.player.fire(self.bullets_p)
            self.game_music.play_player_shoot()
        self.check_collision_be()
        self.check_collision_bp()
        self.check_collision_ip()
        self.check_room_finish()
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
        for item_ in self.items:
            item_.draw(self.canvas)
        self.player.draw(self.canvas)
        self.screen.blit(self.canvas, (0, 0), self.viewport)
        if self.debug:
            dbgscreen.draw(self.screen)
        # 下列函数的功能 分不同的状态绘制不同的图像
        if self.active == c.ACTIVE_START:
            self.play_list.button.draw()
        if self.active == c.ACTIVE_PLAY:
            self.play_list.menu.draw()
        if self.active == c.ACTIVE_LIST:
            self.play_list.draw_list()

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
            fix_entity_collision(self.player, collision[0])  # 同时有多个碰撞无法处理，所以只处理一个

    def game_restart(self):
        """
        游戏重新启动:包括步骤：清空之前所有的群组
        重新放入数组，room的放置只是暂时的方法，之后添加更换房间功能
        """
        self.room.clear()

        self.player.x = self.screen_rect.centerx
        self.player.y = self.screen_rect.centery
        self.player.hp = self.player.maxhp
        self.player.hp = 100
        self.player.maxhp = 100 # 这里是一个妥协，因为添加了可以更改maxhp的buff
        self.player.hp = self.player.maxhp
        self.player.atk = 10
        self.player.base_speed = 4.0
        self.player.speed = self.player.base_speed
        self.player.bullet_speed = 8.0
        self.player.buffs.clear() # buff清零，这是死亡时的状态，所以包括道具在内一切道具清零

        # self.room.setup(self.enemies, self.bullets_p, self.bullets_e, self.obstacles, self.player)
        self.room.generate()
        self.game_music.end_background_music()
        self.game_music.play_background_music()  # 当游戏重新启动时，背景音乐什么的也要重新启动


    def check_player_hp(self):
        """
        用于检查玩家的hp是否清零，如果清零的话就处理
        :return:
        """
        if self.player.hp <= 0:
            self.active = c.ACTIVE_START
            self.game_restart()

    def check_enemy_hp(self):
        """
        用于检查敌人的hp是否清零，如果清零的话就处理
        :return:
        """
        for enemy in self.enemies:
            if enemy.hp <= 0:
                loots = enemy.loot_table.gen_loot()
                for loot in loots:
                    self.room.spawn_item(loot, enemy.x, enemy.y)
                enemy.kill()

    def run(self):
        self.game_music.play_background_music()  # 在游戏刚开始启动时载入
        while not self.done:
            dbgscreen.show('(debug)bullet_count:{}'.format(len(self.bullets_p) + len(self.bullets_e)))
            dbgscreen.show(f'enemy_count:{len(self.enemies)}')
            self.handle_events()
            if self.active == c.ACTIVE_PLAY:
                # 只有当游戏启动时敌人才会移动
                # 数组才会更新
                # 才需要检查血量
                self.check_everything()
                self.enemy_ai()
                self.update_everything()
                self.fix_block_entity_collision()
                self.check_player_hp()  # 添加的检查血量的函数
                self.check_enemy_hp()
            self.draw_everything()
            pygame.display.flip()
            self.clock.tick(setting.fps_limit)  # 限制帧数。同时，只有用了tick，pygame内置的fps()才能使用

        pygame.quit()
