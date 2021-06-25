# -*- coding: utf-8 -*-
"""
Created on Fri May 14 08:45:26 2021

@author: jiangqinwu
"""

            
class Settings:
    #"存储游戏《外星人入侵》中所有设置的类",将所有设置储存在一个地方
    def __init__(self):
        #"初始化游戏设置"
        
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)
        self.whetherfull  = False
        
            
        #我方坦克设置
        self.ship_limit = 3#飞船数量
        #我方坦克血量
        self.ship_blood = 300
        
        #我方坦克设置
        if self.whetherfull:
            self.bullet_speed = 2
            self.ship_speed = 0.6
            self.increase_speed = 0.3#道具增加的速度s道具
        else:
            self.bullet_speed = 0.8
            self.ship_speed = 0.3
            self.increase_speed = 0.15#道具增加的速度s道具
            
        #self.bullet_color = (60,60,60)
        self.bullets_allowed = 50
        #我方子弹的伤害
        self.bullet_harm = 100
        #道具增加的伤害b道具
        self.bullet_increase_harm = 100
        #血量增加道具
        self.increase_blood = 100
        
    
        #敌方坦克子弹速度
        if self.whetherfull:
            self.tankebullet_speed = 2
            self.alien_speed = 0.5
        else:
            self.tankebullet_speed = 0.5
            self.alien_speed = 0.15
       
        #敌方坦克血量
        self.alien_blood = 200
        #敌方坦克子弹伤害
        self.alien_bullet_harm = 100
        #敌方坦克攻击频率
        self.alien_bullet_frequency = 200
        #敌方坦克
        self.alien_oncenum = 8
        
        #通关所需打击的坦克数量的数量
        self.fire_aliennum = 0 #击杀的坦克数量
        self.aliennum = 0 #已经产生的坦克数量
        self.aliensmaxnum = 1
        #游戏节奏加快的速度
        self.speedup_scale = 1.2
        #外星人分数提高的速度
        #self.score_scale = 1.5
        #初始化随游戏进行而变化的属性
        self.initialize_dynamic_settings()
        
        
        #任何情况下都不应重置最高得分
        #self.high_score = 0
        
        
    def initialize_dynamic_settings(self):
        "初始化随游戏进行而变化的设置"
        if self.whetherfull:
            self.ship_speed = 0.6
        else:
            self.ship_speed = 0.3 # 我方坦克的移动速度
        
        if self.whetherfull:
            self.bullet_speed = 2
        else:
            self.bullet_speed = 0.8
        if self.whetherfull:
            self.tankebullet_speed = 2
        else:
            self.tankebullet_speed = 0.5
        if self.whetherfull:
            self.alien_speed = 0.5
        else:
            self.alien_speed = 0.15
            
        self.fire_aliennum = 0 #击杀的坦克数量
        self.aliennum = 0#当前敌方坦克的数量
         #敌方坦克血量
        self.alien_blood = 200
        #敌方坦克子弹伤害
        self.alien_bullet_harm = 100
         #我方子弹的伤害
        self.bullet_harm = 100
        #我方坦克血量
        self.ship_blood = 400
        #self.fleet_direction为1表示右移，-1表示左移
        #self.fleet_direction = 1
        #记分
        #self.alien_points = 50
        
    def increase_level(self):
        "提高速度设置"
        #self.ship_speed *= self.speedup_scale
        self.alien_blood += 100
        if self.whetherfull:
            self.ship_speed += 0.2
            self.alien_speed += 0.1
        else:
            self.ship_speed += 0.1
            self.alien_speed += 0.05
        
        