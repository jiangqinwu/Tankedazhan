# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:38:29 2021

@author: jiangqinwu
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    "管理飞船所发射子弹的类"
    
    def __init__(self,ai_game):
        #ai_game当前AlienInvasion类的实例
        "在飞船当前位置创建一个子弹对象"
        super().__init__()
        #子弹的方向
        self.head = ai_game.ship.head #1表示前，2表示右，3表示后，4表示左
        dic = {1:"images2/MU.bmp",2:"images2/MR.bmp",3:"images2/MD.bmp",4:"images2/ML.bmp"}
        #print(dic[2])
        #self.image = pygame.image.load("images2/MR.bmp")
        self.image = pygame.image.load(dic[self.head])
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        #伤害
        self.harm = self.settings.bullet_harm +100
        
        #在（0，0）处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = self.image.get_rect()
        
        
        #转移到正确的位置
        #self.rect.midtop = ai_game.ship.rect.midtop
        if self.head == 1 :
            self.rect.midtop = ai_game.ship.rect.midtop
        elif self.head == 2:
            self.rect.midright = ai_game.ship.rect.midright
        elif self.head == 3 :
            self.rect.midbottom = ai_game.ship.rect.midbottom
        elif self.head == 4:
            self.rect.midleft = ai_game.ship.rect.midleft
        
        
        #存储用小数表示的子弹的位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
    def update(self):
        "移动子弹"
        #更新表示子弹位置的小数值
        if self.head == 1:
            self.y -= self.settings.bullet_speed
        elif self.head == 2:
            self.x += self.settings.bullet_speed
        elif self.head == 3:
            self.y += self.settings.bullet_speed
        elif self.head == 4:
            self.x -= self.settings.bullet_speed
        
        #更新表示子弹的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y
    
    def blitme(self):
        "在指定位置绘制飞船"
        self.screen.blit(self.image,self.rect)
