# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 19:35:07 2021

@author: jiangqinwu
"""

import pygame.font
from ship import Ship

class Scoreboard:
    "显示得分的类"
    
    def __init__(self,ai_game):
        "初始化显示得分涉及的属性"
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ship = ai_game.ship
        
        #显示得分时的字体设置
        self.text_color = (225,38,0)
        self.font = pygame.font.SysFont(None,60)
        self.dic = {1:"first level",2:"second level",3:"third level"}
        
        #显示血量时的设置
        self.blood_width,self.blood_height = 30,30
        self.blood_color = (225,38,0)
        
        #准备初始得分的图像
        self.prep_blood()
        #self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
        
    def prep_ships(self):
        "显示剩余的飞船数"
        #创建一个飞船编组
        self.ships  = pygame.sprite.Group()
        
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            #依次设置飞船的x轴位置
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            
        
    def prep_level(self):
        "将关卡转换为一副渲染的图像"
        level_str = self.dic[self.stats.level]
        self.level_image = self.font.render(level_str,True,self.text_color,
                                           self.settings.bg_color)
        #将等级放在等分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.screen_rect.top + 30
        
    def prep_blood(self):
        "将血量转换为一副渲染的图像"
        blood_str = "Blood:"
        self.blood_image = self.font.render(blood_str,True,self.text_color,
                                           self.settings.bg_color)
        #将等级放在等分下方
        self.blood_rect = self.blood_image.get_rect()
        self.blood_rect.right = self.screen_rect.width/2 -  self.blood_width - 10
        self.blood_rect.top = self.screen_rect.top + 25
    
    def draw_blood(self):
        '''显示剩余血量'''
        for i in range(int(self.ship.blood / 100)):
            pygame.draw.rect(self.screen, self.blood_color, \
            (self.screen_rect.width/2 + (i-1) * (self.blood_width + 5) ,30,self.blood_width,self.blood_height), 0)

    def show_score(self):
        "在屏幕上显示得分、等级和余下的飞船"
        self.screen.blit(self.blood_image,self.blood_rect)
        self.draw_blood()
        self.screen.blit(self.level_image,self.level_rect)
        for ship in self.ships:
            ship.blitme()
   
        '''
    def prep_high_score(self):
        "将最高分转换为一副渲染的图像"
        #将high.score的值摄入到最近的10的整数倍
        high_score = round(self.stats.high_score,-1)
        #将数值转换为字符串并在其中插入，
        high_score_str = "{:,}".format(high_score)
        #再将转换后的字符串传递给创建图像的render()
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,
                                           self.settings.bg_color)
        
        #在屏幕顶部正中央显示最高分
        #让其向左延申
        self.high_score_rect = self.high_score_image.get_rect()
        #让其右边缘与屏幕右边缘相距20像素
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def prep_score(self):
        "将得分转换为一副渲染的图像"
        #将stats.score的值摄入到最近的10的整数倍
        rounded_score = round(self.stats.score,-1)
        #将数值转换为字符串并在其中插入，
        score_str = "{:,}".format(rounded_score)
        #将数值self.stats.score转换为字符串
        #score_str = str(self.stats.score)
        #再将转换后的字符串传递给创建图像的render()
        self.score_image = self.font.render(score_str,True,self.text_color,
                                           self.settings.bg_color)
        
        #在屏幕右上角显示得分
        #让其向左延申
        self.score_rect = self.score_image.get_rect()
        #让其右边缘与屏幕右边缘相距20像素
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def check_high_score(self):
        "检查是否产生了最高分"
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
     '''   
    
        

        