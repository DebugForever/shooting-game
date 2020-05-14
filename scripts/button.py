import pygame.font


class Button():
    """
    按钮基类
    """

    def __init__(self, image: pygame.Surface, msg, width, height):
        # button
        self.screen = image
        self.screen_rect = image.get_rect()

        self.width, self.height = width, height
        self.color = (150, 255, 150)
        self.text_color = (255, 240, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.msg = msg

    def set(self):
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(self.msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Menu():
    """
    菜单选项，用于弹出菜单，其中option用于描述众多选项
    option_continue:继续游戏
    option_restart:重新开始游戏
    option_quit:退出游戏

    """
    options: Button
    option_continue: Button
    option_restart: Button
    option_quit: Button
    menu: Button
    button: Button

    def __init__(self, image):
        """
        初始化
        """
        self.options = Button(image, "option", 150, 35)
        self.option_continue = Button(image, "continue", 150, 35)
        self.option_restart = Button(image, "restart", 150, 35)
        self.option_quit = Button(image, "quit", 150, 35)
        self.menu = Button(image, "menu", 150, 35)
        self.button = Button(image, "play", 200, 50)
        self.menu.set()
        self.options.set()
        self.option_continue.set()
        self.option_restart.set()
        self.option_quit.set()
        self.button.set()

        self.start_x, self.start_y = self.option_continue.rect.bottomleft
        self.start_y -= 3 * self.option_continue.height
        self.menu.rect = pygame.Rect(0, 0, self.menu.width, self.menu.height)
        self.menu.rect.centerx = self.option_continue.rect.centerx  # menu
        self.menu.rect.centery += 5
        self.options.rect = pygame.Rect(self.start_x, self.start_y, self.options.width, self.options.height)
        self.option_continue.rect = pygame.Rect(self.start_x, self.start_y + self.options.height,
                                                self.option_continue.width, self.option_continue.height)
        self.option_restart.rect = pygame.Rect(self.start_x,
                                               self.start_y + self.options.height + self.option_continue.height,
                                               self.option_restart.width, self.option_restart.height)
        self.option_quit.rect = pygame.Rect(self.start_x,
                                            self.start_y + 2 * self.option_continue.height + self.option_restart.height,
                                            self.option_quit.width, self.option_quit.height)
        self.options.prep_msg(self.options.msg)
        self.option_continue.prep_msg(self.option_continue.msg)
        self.option_quit.prep_msg(self.option_quit.msg)
        self.option_restart.prep_msg(self.option_restart.msg)
        self.menu.prep_msg(self.menu.msg)
        """
        解释一下上面代码的含义
        第一段是确定了button，menu，option三个选项的位置，但是初始化他们均在屏幕中间，其中button不需要修改位置，其他五个需要移动一下位置
        所以第二段是修改了他们的位置，将menu移动到最上面，option等根据start_x和start_y移动一下
        移动之后还需要移动一下对应的字符的位置
        """

    def draw_list(self):
        self.options.draw()
        self.option_continue.draw()
        self.option_quit.draw()
        self.option_restart.draw()

    def draw_button(self):
        self.button.draw()

    def draw_menu(self):
        self.menu.draw()
