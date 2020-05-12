import pygame.font

class Button():
    def __init__(self,image:pygame.Surface,msg):
        #button
        self.screen = image
        self.screen_rect = image.get_rect()
        
        self.button_width,self.button_height = 200,50
        self.button_color= (0,255,0);
        self.button_text_color = (255,255,255)
        self.button_font = pygame.font.SysFont(None,48)
        
        self.rect = pygame.Rect(0,0,self.button_width,self.button_height)
        self.rect.center = self.screen_rect.center
        
        self.prep_msg(msg)
    
    def prep_msg(self,msg):
        self.msg_image = self.button_font.render(msg,True,self.button_text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)