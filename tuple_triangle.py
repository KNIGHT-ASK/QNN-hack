# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 03:34:28 2025

@author: Owner
"""

def make_tups(n):
    # output_list = []
    # for x in range(1,n):
    #     inner_list = []
    #     inner_list.append((x, x+1))
    #     if x>2:
    #         inner_list.append((x+1,x+2))
    #     if x>4:
    #         inner_list.append((x+2, x+3))
    #     if x>6:
    #         inner_list.append((x+3,x+4))
            
    #     output_list.append(inner_list)
    output_list = []
    for x in range(1,n):
        inner_list = []
        if x%2 == 1:
            inner_list.append((1,2))
            if x>2:
                inner_list.append((3,4))
                if x>4:
                    inner_list.append((5,6))
                    if x>6:
                        inner_list.append((7,8))
        if x%2 == 0:
          inner_list.append((2,3))  
          if x>3:
              inner_list.append((4,5))
              if x>5:
                  inner_list.append((6,7))
        output_list.append(inner_list)
    for y in range(n-1,0, -1):
        inner_list = []
        if y%2 == 1:
            inner_list.append((1,2))
            if y>2:
                inner_list.append((3,4))
                if y>4:
                    inner_list.append((5,6))
        if y%2 == 0:
          inner_list.append((2,3))  
          if y>3:
              inner_list.append((4,5))
              if y>5:
                  inner_list.append((6,7))
        output_list.append(inner_list)
        
            
            
            
    
    return output_list
        
        
