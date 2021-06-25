# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 05:38:20 2021

@author: jiangqinwu
"""

import pygame
from pygame.sprite import Sprite


class TankeBullet(Sprite):
    "管理敌方坦克所发射子弹的类"
    
    def __init__(self,alien):
        #ai_game当前AlienInvasion类的实例
        "在飞船当前位置创建一个子弹对象"
        super().__init__()
        self.alien = alien
        #子弹的方向
        self.head = alien.head #1表示前，2表示右，3表示后，4表示左
        dic = {1:"images2/MU.bmp",2:"images2/MR.bmp",3:"images2/MD.bmp",4:"images2/ML.bmp"}
        #print(dic[2])
        #self.image = pygame.image.load("images2/MR.bmp")
        self.image = pygame.image.load(dic[self.head])
        self.rect  = self.image.get_rect()
        self.screen = self.alien.screen
        #self.settings = ai_game.settings
        #self.ship = ai_game.ship
        
        #在（0，0）处创建一个表示子弹的矩形，在设置正确的位置
        
        #转移到正确的位置
        #self.rect.midtop = ai_game.ship.rect.midtop
        if self.head == 1 :
            self.rect.midtop = self.alien.rect.midtop
        elif self.head == 2:
            self.rect.midright = self.alien.rect.midright
        elif self.head == 3 :
            self.rect.midbottom = self.alien.rect.midbottom
        elif self.head == 4:
            self.rect.midleft = self.alien.rect.midleft
        
        
        #存储用小数表示的子弹的位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
    def update(self):
        "子弹发射"
        #更新表示子弹位置的小数值
        if self.head == 1:
            self.y -= self.alien.tankebullet_speed
        elif self.head == 2:
            self.x += self.alien.tankebullet_speed
        elif self.head == 3:
            self.y += self.alien.tankebullet_speed
        elif self.head == 4:
            self.x -= self.alien.tankebullet_speed
        
        #更新表示子弹的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y
    
    def blitme(self):
        "在指定位置绘制飞船"
        self.screen.blit(self.image,self.rect)