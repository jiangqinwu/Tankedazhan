# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 13:52:07 2021

@author: jiangqinwu
"""

import random
import pygame
from pygame.sprite import Sprite
from tankebullet import TankeBullet
from time import sleep

class Alien(Sprite):
    "表示单个外星人类"
    
    def __init__(self,ai_game):
        "初始化外星人并设置其初始位置"
        super().__init__()
        
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        self.sb = ai_game.sb
        #创建一个用于存储游戏统计信息的实例
        self.stats = ai_game.stats
        #加载外星人图像并设置其rect属性
        self.image = pygame.image.load("images/tanke.bmp")
        self.rect = self.image.get_rect()
        
        self.direction = [1,2,3,4]#1表示前，2表示右，3表示后，4表示左
        self.head = 1
        #每个外星人随机生成位置
        self.rect.x = self.rect.width + random.random()*(self.screen.get_rect().right - 2  * self.rect.width)
        self.rect.y = self.rect.height + random.random()*self.screen.get_rect().bottom/2
        
        #防止随机生成到我方坦克上
        if self.rect.left < self.ship.rect.right and self.rect.right > self.ship.rect.left:
            self.rect.x -= self.ship.rect.width
        if self.rect.top < self.ship.rect.bottom and self.rect.bottom > self.ship.rect.top:
            self.rect.y += self.ship.rect.height
        
            
        #防止随机生成到敌方坦克上
        self._change_rect_()
        #储存外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        #记录之前的方向前进的步数
        self.fgo = 0
        #self.f = 0
        #敌方坦克的子弹
        self.bullets = pygame.sprite.Group()
        
        #敌方坦克子弹速度
        self.tankebullet_speed = self.settings.tankebullet_speed 
        #敌方坦克子弹伤害
        self.harm = self.settings.alien_bullet_harm
        
        #敌方坦克血量
        self.blood = self.settings.alien_blood
        
        #攻击频率
        self.bullet_num = 0
        #是否跳过转向
        self.whether_direction = True
        #是否跳过移动
        self._whether_pass_update = False
        
        
    def _change_rect_(self):
        for alien in self.ai_game.aliens.sprites():
            if self.rect.left < alien.rect.right and self.rect.right > alien.rect.left:
                self.rect.x -= 2 * alien.rect.width
                if self.rect.left < 0:
                    self.rect.left = 0
            if self.rect.top < alien.rect.bottom and self.rect.bottom > alien.rect.top:
                self.rect.y += 2 * alien.rect.height
                
    
    def check_edges(self):
        "如果撞到了屏幕，则返回true"
        #screen_rect = self.screen.get_rect()
        if self.rect.right > self.screen.get_rect().right  or self.rect.left < 0  \
        or self.rect.top < 0 or self.rect.bottom > self.screen.get_rect().bottom :
            
            return True
        
    def update(self):
        "随机移动"
        #敌方坦克碰撞
        #self._check_alien_alien_collisions()
        
        self.fgo += 1
        self._fire_move()
        if self._whether_pass_update == True and self.fgo >= 500:
            self._whether_pass_update = False
        else:
            #飞船的开火和移动'
            #self._fire_move()
                
            #记录之前的方向
            lhead = self.head
            
            if self.ai_game.stats.level == 1:
                #每个坦克会在固定一个方向上前进500步，同时转向
                if self.fgo >= 500:
                    self.head =  random.choice(self.direction)
                    self.image = pygame.transform.rotate(self.image,(lhead - self.head)*90)
                    self.fgo = 0
                    #self.f = 10
                    
            elif self.ai_game.stats.level == 2: #第二关增加的难度
                
                self.whether_direction = True
                if self.whether_fire():
                    self.whether_direction = False
                
                #每个坦克会在固定一个方向上前进500步，同时转向
                if self.fgo >= 500 and self.whether_direction:
                    self.head =  random.choice(self.direction)
                    self.image = pygame.transform.rotate(self.image,(lhead - self.head)*90)
                    self.fgo = 0
                    #self.f = 10
                    
            elif self.ai_game.stats.level == 3: #第三关增加的难度
                self.whether_direction = True
                if self.whether_fire():
                    self.whether_direction = False
        
                #每个坦克会在固定一个方向上前进500步，同时转向
                if self.fgo >= 500 and self.whether_direction :
                    if self.ship.rect.x >= self.rect.x and self.ship.rect.y >= self.rect.y:
                        self.head =  random.choice([2,3]) 
                    elif self.ship.rect.x >= self.rect.x and self.ship.rect.y < self.rect.y:
                        self.head =  random.choice([2,1])
                    elif self.ship.rect.x < self.rect.x and self.ship.rect.y >= self.rect.y:
                        self.head =  random.choice([4,3])
                    elif self.ship.rect.x < self.rect.x and self.ship.rect.y < self.rect.y:
                        self.head =  random.choice([4,1])
                    self.image = pygame.transform.rotate(self.image,(lhead - self.head)*90)
                    self.fgo = 0
                    #self.f = 10
                
    def _alien_edges(self):
        if self.head > 2:
            self.head -= 2
        else:
            self.head += 2
        self.image = pygame.transform.rotate(self.image,180)
        if self._whether_pass_update == False:
            self.fgo = 0
            
            
    def _fire_move(self):
        '''飞船的开火和移动'''
        self.bullet_num += 1
        if self.bullet_num == self.settings.alien_bullet_frequency:
            self.fire()
            self.bullet_num = 0
        self._update_bullets()
        if self.head == 1 or self.head == 3:
            self.y -= (self.settings.alien_speed*(2 - self.head))
        elif self.head == 2 or self.head == 4:
            self.x += (self.settings.alien_speed*(3 - self.head))
        # self.x += (self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x = self.x
        self.rect.y = self.y
            
            
        
    def _check_alien_alien_collisions(self):
        '''检测敌方坦克的碰撞'''
        collisions = pygame.sprite.spritecollide(
            self,self.ai_game.aliens,False)#true表示发生碰撞的精灵会自动移除
        #collisons为一个字典，键是精灵组1中发生碰撞的精灵，值是精灵组2中与该精灵发生碰撞的精灵的列表。
        #发生冲突的精灵会作为一个列表返回
        if collisions and self.fgo  > 200:
            for alien in collisions:
                '''  cjac'''
                if self is not alien:
                    self.image = pygame.transform.rotate(self.image,180)
                    if self.head > 2:
                        self.head -= 2
                    else:
                        self.head += 2
                    self.fgo = 0#固定方向
                    alien.image = pygame.transform.rotate(alien.image,180)
                    if alien.head > 2:
                        alien.head -= 2
                    else:
                        alien.head += 2
                    alien.fgo = 0
    
    def whether_fire(self):
        if self.head == 1 and self.ship.rect.right > self.rect.left and  \
        self.ship.rect.left < self.rect.right and self.rect.y > self.ship.rect.y:
            return True
        elif self.head == 2 and self.ship.rect.top < self.rect.bottom and  \
        self.ship.rect.bottom > self.rect.top and  self.rect.x < self.ship.rect.x:
            return True
        elif self.head == 3 and self.ship.rect.right > self.rect.left and \
        self.ship.rect.left < self.rect.right and self.rect.y < self.ship.rect.y:
            return True
        elif self.head == 4 and self.ship.rect.top < self.rect.bottom and  \
        self.ship.rect.bottom > self.rect.top and self.rect.x > self.ship.rect.x:
            return True
        else:
            return False
            
    def fire(self):
        '''开火'''
        #ship 表示我方坦克，rect表示敌方坦克
        if self.head == 1 and self.ship.rect.right > self.rect.left and  \
        self.ship.rect.left < self.rect.right and self.rect.y > self.ship.rect.y:
            bullet = TankeBullet(self)
            self.bullets.add(bullet)
            return True
        elif self.head == 2 and self.ship.rect.top < self.rect.bottom and  \
        self.ship.rect.bottom > self.rect.top and  self.rect.x < self.ship.rect.x:
            bullet = TankeBullet(self)
            self.bullets.add(bullet)
            return True
        elif self.head == 3 and self.ship.rect.right > self.rect.left and \
        self.ship.rect.left < self.rect.right and self.rect.y < self.ship.rect.y:
            bullet = TankeBullet(self)
            self.bullets.add(bullet)
            return True
        elif self.head == 4 and self.ship.rect.top < self.rect.bottom and  \
        self.ship.rect.bottom > self.rect.top and self.rect.x > self.ship.rect.x:
            bullet = TankeBullet(self)
            self.bullets.add(bullet)
            return True
        else :
            return False
        
    def _update_bullets(self):
        "更新子弹的位置并删除消失的子弹"
        self.bullets.update()#为bullets编组中的每颗子弹调用bullet.update()
        for bullet in self.bullets.copy():#删除消失的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen.get_rect().height or \
            bullet.rect.right <= 0 or bullet.rect.left >= self.screen.get_rect().width:
                #查看是否从屏幕顶部消失
                self.bullets.remove(bullet)
                del bullet
        self._check_bullet_ship_collisions()
        
    def _check_bullet_ship_collisions(self):
        "检查是否有子弹集中了我方坦克，如果有则扣除我方坦克的血量或结束游戏"
        collisions = pygame.sprite.spritecollide(
            self.ship,self.bullets,True)#true表示发生碰撞的精灵会自动移除
        #collisons为一个字典，键是精灵组1中发生碰撞的精灵，值是精灵组2中与该精灵发生碰撞的精灵的列表。
        #发生冲突的精灵会作为一个列表返回
        if collisions:
            for bullet in collisions:
                '''  cjac'''
                self.ship.blood -= self.settings.alien_bullet_harm
                if self.ship.blood <= 0:
                    self.ai_game._ship_hit()
            self.sb.prep_blood()
            self.sb.draw_blood()
    
    def blitme(self):
        self.screen.blit(self.image,self.rect)
        for bullet in self.bullets.sprites():
            bullet.blitme()
       
