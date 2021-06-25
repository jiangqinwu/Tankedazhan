# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 09:55:19 2021

@author: jiangqinwu
"""
import random
import pygame
from pygame.sprite import Sprite

class Prop(Sprite):
    "管理飞船所发射子弹的类"
    
    def __init__(self,ai_game):
        #ai_game当前AlienInvasion类的实例
        "在飞船当前位置创建一个子弹对象"
        super().__init__()
        #
        self.dic = {1:"images2/b.bmp",2:"images2/s.bmp",3:"images2/bloodincrease.bmp"}
        self.prop_kind = random.choice([1,2,3])
        self.image = pygame.image.load(self.dic[self.prop_kind])
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        
        
        #获取道具的rect
        self.rect = self.image.get_rect()
        #是否被获取
        self.whether_get = False
        
        #随机生成道具
        self.rect.x = random.random()*(self.screen.get_rect().right - self.rect.width)
        self.rect.y = self.rect.width + random.random()*self.screen.get_rect().bottom/2
        
        
    def Disappearance(self):
        if self.prop_kind == 1:
            self.settings.bullet_harm -= self.settings.bullet_increase_harm
        elif self.prop_kind == 2:
            self.settings.ship_speed -= self.settings.increase_speed
        
        
    def update(self):
        '''产生作用'''
        if self.prop_kind == 1:
            self.settings.bullet_harm += self.settings.bullet_increase_harm
        elif self.prop_kind == 2:
            self.settings.ship_speed += self.settings.increase_speed
        elif self.prop_kind == 3:
            self.ship.blood += self.settings.increase_blood 
            if self.ship.blood > 400:
                self.ship.blood = 400
            
        
    
    def blitme(self):
        "在指定位置绘制飞船"
        self.screen.blit(self.image,self.rect)
