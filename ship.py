# -*- coding: utf-8 -*-
"""
Created on Fri May 14 09:10:29 2021

@author: jiangqinwu
"""

import pygame 
from pygame.sprite import Sprite
import random


"管理飞船的类"
class Ship(Sprite):
    "初始化飞船并设置其初始位置"
    def __init__(self,ai_game):  #ai_game是alien_invasion文件的AlienInvasion实例
        super().__init__()
        self.screen = ai_game.screen  #将屏幕赋给ship的一个属性
        self.settings = ai_game.settings #给ship类添加属性settings以便能够在update()中使用它
        self.screen_rect = ai_game.screen.get_rect() #使用get_rect()方法访问屏幕rect属性
                                       #返回值包含矩形的居中属性
                     
        #加载飞船图像并获取其外接矩形
        #pygame.image.load()加载图片，返回一个表示飞船的surface对象
        self.image = pygame.image.load("images/me.bmp")
        self.rect = self.image.get_rect() # 使用get_rect()获取相应的surface的属性rect
                                            #以便确定后面能够使用它来指定飞船的位置
        
        #对于每一艘新的飞船。都将其放在屏幕底部的正中央
        self.rect.midbottom = self.screen_rect.midbottom
        
        #在飞船的属性x中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        #坦克的方向
        self.direction = [1,2,3,4]#1表示前，2表示右，3表示后，4表示左
        self.head = 1
        
        #坦克得血量
        self.blood = self.settings.ship_blood
        
    def update(self):
        "根据移动标志来调整飞船的位置"
        #根据移动标志来判断是否移动,更新的是飞船的位置而不是rect对象的x值
        #并限制飞船的位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.image = pygame.transform.rotate(self.image,(self.head - 2)*90)
            self.head = 2
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.image = pygame.transform.rotate(self.image,(self.head - 4)*90)
            self.head = 4
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.image = pygame.transform.rotate(self.image,(self.head - 1)*90)
            self.head = 1
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <  self.screen_rect.bottom:
            self.image = pygame.transform.rotate(self.image,(self.head - 3)*90)
            self.head = 3
            self.y += self.settings.ship_speed
        #根据飞船的位置来更新你rect对象的值
        self.rect.x = self.x
        self.rect.y = self.y
        
    def blitme(self):
        "在指定位置绘制飞船"
        self.screen.blit(self.image,self.rect)
       
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.image = pygame.transform.rotate(self.image,(self.head - 1)*90)
        self.head = 1
        
        