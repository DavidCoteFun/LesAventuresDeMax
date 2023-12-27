#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 19:32:28 2019

@author: Tristan Brunet-Cote, David Cote
"""
import pygame
pygame.init()

#where the files are
baseDir="/Users/stod/Codage/LesAventuresDeMax/"

#size of the game display
MAX_X=1000
MAX_Y=750

#on_execute() loop speed. The larger the faster. Zero for max possible speed.
exec_loop_speed=25

#display_surf=pygame.display.set_mode((MAX_X,MAX_Y), pygame.HWSURFACE | pygame.DOUBLEBUF)
display_surf=pygame.display.set_mode((MAX_X,MAX_Y))
