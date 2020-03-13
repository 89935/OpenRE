# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 11:21:27 2020

@author: thinkpad
"""

class EntityPair:
    """
    实体对
    Attributes:
        entity1：WordUnit，实体1的词单元
        entity2：WordUnit，实体2的此单元
    """
    def __init__(self,entity1,entity2):
        self.entity1 = entity1
        self.entity2 = entity2
    
    def get_entity1(self):
        return self.entity1
    
    def set_entity1(self,entity1):
        self.entity1 = entity1
    
    def get_entity2(self):
        return self.entity2
    
    def set_entity2(self,entity2):
        self.entity2 = entity2
    