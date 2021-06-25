# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:25:45 2021

@author: jiangqinwu
"""
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from  scoreboard import Scoreboard
from prop import Prop

class AlienInvasion:
    def __init__(self):
        pygame.init()  #初始化背景设置
        self.settings = Settings()
        
        
        #创建一个显示窗口，指定游戏窗口的尺寸，返回surface对象，此时surface对象为游戏窗口
        if self.settings.whetherfull:
            #是否需要全屏pygame.FULLSCREEN表示全屏
            self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            #将设置settings中的宽改变
            self.settings.screen_width = self.screen.get_rect().width
            #将设置settings中的高改变
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))           
        
        pygame.display.set_caption("坦克大战") #设置当前的窗口的标题
        
        #创建一个ship实例
        self.ship = Ship(self)
        #创建一个编组是 pygame.sprite.Group类的一个实例
        self.bullets = pygame.sprite.Group()
        #创建一个外星人编组
        self.aliens = pygame.sprite.Group()
        #self._create_fleet()
        #创建一个开始play键
        self.play_button = Button(self,"GAME PLAY !!!")
        self.over_button = Button(self,"GAME OVER !!!")
        self.pass_button = Button(self,"Congratulations, customs clearance!!!")
        #设置背景色
        self.bg_color = self.settings.bg_color
        #方向响应按钮
        self.candirection = True
        #创建一个用于存储游戏统计信息的实例5
        self.stats = GameStats(self)
        self.sb =Scoreboard(self) #分数
        #开始
        self.first = 0
        #道具
        self.props = pygame.sprite.Group()
        #道具是否使用
        self.can_prop = False
        #道具是否产生
        self.can_create_prop = True
        #道具是否被获得
        self.get_prop = False
        
        
    def _check_events(self):
        #监视键盘和鼠标事件，pygame.event.get()返回包含它上一次被调用前
        #的发生的所有时事件的列表，pygame.QUIT表示单击游戏窗口关闭键
        for event in pygame.event.get():  #事件循环
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #当按键按下的时候响应KEYDOWN事件(按下键盘)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #当按键按下的时候响应KEYUP事件(释放键盘)
            elif event.type == pygame.KEYUP:
                self._check_ketup_events(event)
            #当玩家单击play按钮
            elif event.type == pygame.MOUSEBUTTONDOWN: 
            #pygame.MOUSEBUTTONDOWN表示点击屏幕
                #pygame.mouse.get_pos()返回一个元组，包含玩家单击时鼠标的x，y的值
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                    
    def _check_keydown_events(self,event):
        #当按键按下的时候响应KEYDOWN事件(按下键盘)
        '''
        if event.key == pygame.K_d and self.candirection:
            self.ship.moving_right = True
            self.candirection = False
        if event.key == pygame.K_a and self.candirection:
            self.ship.moving_left = True
            self.candirection = False
        if event.key == pygame.K_w and self.candirection:
            self.ship.moving_up = True
            self.candirection = False
        if event.key == pygame.K_s and self.candirection:
            self.ship.moving_down = True
            self.candirection = False
        '''
        if event.key == pygame.K_d :
            self.ship.moving_right = True
        if event.key == pygame.K_a:
            self.ship.moving_left = True
        if event.key == pygame.K_w :
            self.ship.moving_up = True
        if event.key == pygame.K_s:
            self.ship.moving_down = True
            
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_ketup_events(self,event):
        #当按键按下的时候响应KEYUP事件(释放键盘)
        if event.key == pygame.K_d and self.ship.moving_right == True:
            self.ship.moving_right = False
            self.candirection = True
        if event.key == pygame.K_a and self.ship.moving_left == True:
            self.ship.moving_left = False
            self.candirection = True
        if event.key == pygame.K_w and self.ship.moving_up == True:
            self.ship.moving_up = False
            self.candirection = True
        if event.key == pygame.K_s and self.ship.moving_down == True:
            self.ship.moving_down = False
            self.candirection = True
        
     
  
    '''
    敌方坦克
    '''      
    def _create_fleet(self):
        "随机生成敌方坦克"
        #创建一个外星人
        #alien = Alien(self)
        #屏幕上最多只能右12个，不过每一关最多只有50个
        
        while len(self.aliens) < self.settings.alien_oncenum and  self.settings.aliennum < self.settings.aliensmaxnum:
            self._create_alien()
            self.settings.aliennum += 1
            
    def _create_alien(self):
        "创建一个外星人并将其加入当前行"
        alien = Alien(self)
        self.aliens.add(alien)
        
    
    def _check_fleet_edges(self):
        "敌方坦克到达边缘时采取的措施"
        for alien in self.aliens.sprites():
            if alien.check_edges(): #对外星人群体中每个外星人调用check_edges()函数
                #改变敌方坦克的方向
                alien._alien_edges()
                alien._whether_pass_update = True
                break
        
        '''
    def _check_alien_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.aliens,self.aliens,False,False)
        if collisions:
            for aliens in collisions.values():
                for alien in  aliens:
                    alien.head += 1
                    alien.head = alien.head % 4     
                    alien.image = pygame.transform.rotate(alien.image,180)
        '''
        
        
    def _update_aliens(self):
        "敌方坦克行动"
        
        #self._check_alien_alien_collisions()#敌方坦克相撞时采取的措施
        self._check_fleet_edges()#敌方坦克到达边缘时采取的措施
        self.aliens.update()#自动调用每个alien的update（）方法
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
         
    def _ship_hit(self):
        "相应我方坦克被敌方坦克撞到即我方坦克死后的处理方法"
        #将ships_left减1,即飞船数减1
        if self.stats.ships_left > 1:
            #将ships_left减一并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        
            #清空余下的外星人和子弹，清空aliens和bullets
            #self.aliens.empty()5
            self.bullets.empty()
            self.ship.blood = self.settings.ship_blood
            for prop in self.props.sprites():
                if prop.whether_get:
                    prop.Disappearance()
                    self.props.remove()
            
            #随机生成敌方坦克，并将我方坦克放到屏幕底部正中央
            self._create_fleet()
            self.ship.center_ship()
        
            #暂停
            sleep(0.5)
        else:
            #游戏状态为停止
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.stats.game_active = False
            #屏幕上的游戏区间的鼠标的光标重新显现
            pygame.mouse.set_visible(True)
        
        
        
        '''
        子弹
        '''
    def _fire_bullet(self):
        "创建一颗子弹，并将其加入编组bullets中"
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        "更新子弹的位置并删除消失的子弹"
        self.bullets.update()#为bullets编组中的每颗子弹调用bullet.update()
        for bullet in self.bullets.copy():#删除消失的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen.get_rect().height or \
            bullet.rect.right <= 0 or bullet.rect.left >= self.screen.get_rect().width:
                #查看是否从屏幕顶部消失
                self.bullets.remove(bullet)
                del bullet
        self._check_bullet_alien_collisions()
                
    def _check_bullet_alien_collisions(self):
        "检查是否有子弹集中了敌方坦克，如果有则扣除敌方坦克的血量或删去敌方坦克"
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,False)#true表示发生碰撞的精灵会自动移除
        #collisons为一个字典，键是精灵组1中发生碰撞的精灵，值是精灵组2中与该精灵发生碰撞的精灵的列表。
        #返回的值是发生碰撞的外星人
        if collisions:
            for aliens in collisions.values():
                '''  cjac'''
                for alien in  aliens:
                    alien.blood -= self.settings.bullet_harm
                    if alien.blood <= 0:
                        self.aliens.remove(alien)
                        self.settings.fire_aliennum += 1 #击杀的坦克数量
                       
        self._level_increse()
    
    
    
        '''
        道具
        '''
    def _prop_create_disappear(self):
        '''道具的创建和消失'''
        if  self.can_create_prop and (self.settings.fire_aliennum == 5 or self.settings.fire_aliennum == 10):
            prop = Prop(self)
            self.props.add(prop)
            self.can_prop = True
            self.can_create_prop = False
        if self.settings.fire_aliennum == 9 or self.settings.fire_aliennum == 14:
            for prop in self.props.sprites():
                if prop.whether_get:
                    prop.Disappearance()
            self.props.empty()
            self.can_prop = False
            self.can_create_prop = True
            
    def _prop_ship_collisions(self):
        '''获取道具'''
        if self.can_prop:
            collisions = pygame.sprite.spritecollide(self.ship,self.props,False)
            #发生冲突的精灵会作为一个列表返回
            if collisions:
                for prop in collisions:
                    prop.whether_get = True
                    prop.update()
                    self.can_prop = False
        
        
    def _level_increse(self):
        #增加难度
        if not self.aliens :
            #删除现有的子弹并新建一群外星人
            self.stats.level += 1
            for prop in self.props.sprites():
                if prop.whether_get:
                    prop.Disappearance()
            self.props.empty()
            self.bullets.empty()
            self.settings.aliennum = 0
            self.settings.fire_aliennum = 0
            if self.stats.level > 3:
                
                self.stats.game_active = False
                #屏幕上的游戏区间的鼠标的光标重新显现
                pygame.mouse.set_visible(True)
                return 
            self._create_fleet()
            self.sb.prep_level()
            self.settings.increase_level()#提高等级
            
    
    def _check_play_button(self,mouse_pos):
        "开始游戏"
        #防止即使play键消失但单击该地方仍有效
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #检测mouse_pos点是否在rect中
        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息
            self.first = 1
            self.settings.initialize_dynamic_settings()
            self.ship.blood = self.settings.ship_blood 
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_blood()
            #道具是否使用
            self.can_prop = False
            #道具是否产生
            self.can_create_prop = True
            
            #清空余下的外星人和子弹
            for prop in self.props.sprites():
                if prop.whether_get:
                    prop.Disappearance()
            self.props.empty()
            self.aliens.empty()
            self.bullets.empty()
            
            
            #随机生成敌方坦克，并生成我方坦克
            self._create_fleet()
            self.ship.center_ship()
            
            #隐藏鼠标光标,在游戏开始后将光标隐藏
            pygame.mouse.set_visible(False)
        
    def _update_screen(self):
        "每次循环时都重绘屏幕"
        self.screen.fill(self.settings.bg_color)
        #将飞船绘制到屏幕上
        for bullet in self.bullets.sprites():
            bullet.blitme()
        #将编组中的每一个元素绘制到属性rect指定的位置
        for alien in self.aliens.sprites():
            alien.blitme()
        #绘制道具
        for prop in self.props.sprites():
            if not prop.whether_get:
                prop.blitme()
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动的状态，则绘制play按钮
        if not self.stats.game_active:
            if self.stats.level > 3:
                self.pass_button.draw_buttonpass()
            self.play_button.draw_button()
            if self.first == 1 and self.stats.level <= 3:
                self.over_button.draw_buttonup()
        else:
            self.ship.blitme()
        #让最近绘制的屏幕可见，绘制一个空屏幕，并擦除旧屏幕
        pygame.display.flip()
        
    def run_game(self):
        #开始游戏的主循环
        while True:
            self._check_events() #键盘事件
            #判断游戏是否继续运行
            if  self.stats.game_active:
                self.ship.update() #飞船的移动d
                self._create_fleet()#敌方坦克的创建
                self._update_aliens() #敌方坦克的移动及射击
                self._update_bullets() #我方子弹的移动
                self._prop_create_disappear()#道具的创建和消失
                self._prop_ship_collisions()#检测道具的获取
                
            self._update_screen() #屏幕显示
            
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
  
