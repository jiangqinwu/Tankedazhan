# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:02:51 2021

@author: jiangqinwu
"""

class GameStats:
    "跟踪游戏统计信息"
    def __init__(self,ai_game):
        "初始化"
        self.settings = ai_game.settings
        self.reset_stats()
        #游戏启动时的活动状态
        self.game_active = False
        #self.high_score = 0
        
    def reset_stats(self):
        "初始化在游戏运行期间可能变化的统计信息"
        self.ships_left = self.settings.ship_limit
        #self.score = 0
        self.level= 1
        #self.settings.ailensnum = 0
        
        