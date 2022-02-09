#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 19:17:02 2019

@author: Tristan Brunet-Cote, David Cote
"""
import pygame
from pygame.locals import *

import time
from Parametres import MAX_X,MAX_Y

class ChoseQuiBouge(pygame.sprite.Sprite):
    def __init__(self,position,image1,image2=None):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.image=image1
       self.images=[]
       self.image_index=0
       self.rect = image1.get_rect()
       self.rect.x = position[0]
       self.rect.y = position[1]
       self.carre_noir=pygame.Surface([self.rect.w,self.rect.h])
       self.carre_noir.fill(Color('black'))
       self.cn_rect=self.carre_noir.get_rect()
       self.cn_rect.x = position[0]
       self.cn_rect.y = position[1]
       self.vitesse=[0,0]
       self.touche_sol=False
       self.redessine=True
       return

    def switch_image(self):
        if self.images:
            iTmp=self.images[self.image_index]
            if isinstance(iTmp,str):
                self.image = pygame.image.load(iTmp).convert()
            else:
                self.image=iTmp
                
            if (self.image_index+1) < len(self.images):
                self.image_index+=1
            else:
                self.image_index=0
        return

   
    def get_position(self):
        return self.rect.x,self.rect.y

    def get_vitesse(self):
        return math.sqrt(self.vitesse[0]**2 + self.vitesse[1]**2)
    
    def bouge_x(self,limit_to_frame=False):
        dx=self.vitesse[0]
        if limit_to_frame:
            if self.rect.right+dx<5 or self.rect.left+dx>(MAX_X-5):
                return
        self.rect.x += dx
        return
        
    def bouge_y(self,limit_to_frame=False):
        dy=self.vitesse[1]
        if limit_to_frame:
            if self.rect.bottom+dy<20 or self.rect.top-dy > MAX_Y:
                return
        self.rect.y += dy
        return

    def bouge(self,limit_to_frame=False):
        self.bouge_x(limit_to_frame)
        self.bouge_y(limit_to_frame)
        return
    
    def dessine_basic(self,list_sprites):
        list_sprites.add(Carre('black',self.cn_rect.x,self.cn_rect.y,self.cn_rect.w,self.cn_rect.h))
        #list_sprites.add(Carre('transparent',self.cn_rect.x,self.cn_rect.y,self.cn_rect.w,self.cn_rect.h))
        list_sprites.add(self)

        self.cn_rect.x = self.rect.x
        self.cn_rect.y = self.rect.y
        return

    def dessine(self,list_sprites):
        return self.dessine_basic(list_sprites)
    
    def efface(self,list_sprites):
        image=pygame.Surface([self.rect.w,self.rect.h])
        image.fill(Color('black'))
        rect=image.get_rect()
        rect.x=self.rect.x
        rect.y=self.rect.y
        self.image=image
        self.rect=rect
        self.dessine(list_sprites)
        return

    def somme_des_forces_basic(self,obstacles,sensible_a_gravite=True):
        if sensible_a_gravite:
            self.vitesse[1]+=1

        #collision avec obstacles?
        self.touche_sol=False
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(obstacle,self):
                diff_x = self.diff_gd(obstacle)
                diff_y = self.diff_hb(obstacle)

                if diff_x and self.vitesse[0]:
                    self.rect.x+=diff_x
                    self.vitesse[0]=0
                    obstacle.redessine=True

                elif diff_y and self.vitesse[1]:
                    self.rect.y-=diff_y
                    self.vitesse[1]=0
                    obstacle.redessine=True

            elif self.almost_collide_y(obstacle):
                self.touche_sol=True
                if self.vitesse[1]>0:
                    self.vitesse[1]=0

        return

    def somme_des_forces(self,obstacles,sensible_a_gravite=True):
        return self.somme_des_forces_basic(obstacles,sensible_a_gravite)

    def diff_gd(self,obstacle):
        #est-ce que la collision est par la gauche ou la droite?
        if (self.rect.right >= obstacle.rect.left) and (self.rect.left < obstacle.rect.left):
            return obstacle.rect.left - self.rect.right #self est a gauche (diff<0)

        if (self.rect.left <= obstacle.rect.right) and (self.rect.right > obstacle.rect.right):
            return obstacle.rect.right - self.rect.left #self est a droite (diff >0)

        return 0

    def diff_hb(self,obstacle):
        #est-ce que la collision est par le haut ou le bas?
        if (self.rect.top <= obstacle.rect.bottom) and (self.rect.top > obstacle.rect.top):
            return self.rect.top - obstacle.rect.bottom -1 #self est en bas (diff<0)

        if (self.rect.bottom >= obstacle.rect.top) and (self.rect.bottom < obstacle.rect.bottom):
            return self.rect.bottom - obstacle.rect.top +1 #self est en haut (diff>0)

        return 0


    def almost_collide_y(self,obstacle):
        #fonction speciale pour dealer avec la gravite
        if (obstacle.rect.top - self.rect.bottom) !=1: 
            return False
        if self.rect.right<=obstacle.rect.left:
            return False
        if self.rect.left>=obstacle.rect.right:
            return False
        return True


class Carre(ChoseQuiBouge):
    def __init__(self,color,posX,posY,largeur,hauteur):
        image = pygame.Surface([largeur, hauteur])
        if color=="transparent":
            image.set_colorkey((0,0,0))
        else:
            image.fill(Color(color))
        ChoseQuiBouge.__init__(self,[posX,posY],image)
        return
   

class Goomba(ChoseQuiBouge):
    def __init__(self,posX,posY):
       image1=pygame.image.load("/Users/dcote/Tristan/Mario/images/gomba_gauche.gif").convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image1)
       self.images.append("/Users/dcote/Tristan/Mario/images/gomba_gauche.gif")
       self.images.append("/Users/dcote/Tristan/Mario/images/gomba_droite.gif")
       self.t1=0
       return

    def attaque(self,hero):
        #bouge vers le hero
        if self.rect.x<hero.rect.x:
            self.vitesse[0]=1
        else:
            self.vitesse[0]=-1
                
        if pygame.sprite.collide_rect(self,hero):
            return 10
        return 0

    def dessine(self,list_sprites):
        if time.time()-self.t1 >0.5:
            self.t1=time.time()
            self.switch_image()

        self.dessine_basic(list_sprites)
        return

class Radio(ChoseQuiBouge):
    def __init__(self,posX,posY):
       image1=pygame.image.load("/Users/dcote/Tristan/Mario/images/radioenrage1.gif").convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image1)
       self.images.append("/Users/dcote/Tristan/Mario/images/radioenrage1.gif")
       self.images.append("/Users/dcote/Tristan/Mario/images/radioenrage2.gif")
       self.t1=0
       return

    def attaque(self,hero):
        #bouge vers le hero
        if self.rect.x<hero.rect.x:
            self.vitesse[0]=1
        else:
            self.vitesse[0]=-1
                
        if pygame.sprite.collide_rect(self,hero):
            return 10
        return 0

    def dessine(self,list_sprites):
        if time.time()-self.t1 >0.5:
            self.t1=time.time()
            self.switch_image()

        self.dessine_basic(list_sprites)
        return


class JoueurPrincipal(ChoseQuiBouge):
    def __init__(self,posX,posY):
       #image=pygame.image.load("/Users/dcote/Tristan/Mario/images/alien1.gif")
       image=pygame.image.load("/Users/dcote/Tristan/Mario/images/max1_petit.gif").convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image)
       self.projectiles=[]
       self.t_jump=0
       self.t_run=0
       self.images_droite=[]
       self.images_droite.append("/Users/dcote/Tristan/Mario/images/max1_petit.gif")
       self.images_droite.append("/Users/dcote/Tristan/Mario/images/max2_petit.gif")
       self.images_gauche=[]
       self.images_gauche.append("/Users/dcote/Tristan/Mario/images/max1_petit_gauche.gif")
       self.images_gauche.append("/Users/dcote/Tristan/Mario/images/max2_petit_gauche.gif")
       self.images=self.images_droite
       return


    def somme_des_forces(self,obstacles,sensible_a_gravite=True):
        keystate = pygame.key.get_pressed()
        #run
        dx=(keystate[K_RIGHT]-keystate[K_LEFT])
        if dx:
            if dx>0:
                self.images=self.images_droite
            else:
                self.images=self.images_gauche

            if self.t_run<18:
                self.vitesse[0]+=dx
            self.t_run+=1
            if self.t_run%10==0:
                self.switch_image()

        else:
            self.vitesse[0]=0

        #jump
        if keystate[K_SPACE]: 
            if self.t_jump<11:
                self.vitesse[1]-=2
            self.t_jump+=1

        return self.somme_des_forces_basic(obstacles,sensible_a_gravite)

        
    def shoot(self):
        laser=Carre('turquoise',self.cn_rect.x,self.cn_rect.y+self.cn_rect.h/2.0,50,2)
        keystate = pygame.key.get_pressed()
        dx=(keystate[K_RIGHT]-keystate[K_LEFT])*20
        dy=(keystate[K_UP]-keystate[K_DOWN])*20

        if dx or dy:
            laser.vitesse[0]=dx
            laser.vitesse[1]=-dy
        else:
            laser.vitesse[0]=20
        self.projectiles.append(laser)
        return

    def attaque(self,ennemis,sprites):
        for obj in self.projectiles:
            obj.bouge()
            for enn in ennemis:
                if pygame.sprite.collide_rect(enn,obj):
                    obj.efface(sprites)
                    self.projectiles.remove(obj)
                    enn.efface(sprites)
                    ennemis.remove(enn)

        return

    def jump(self):
        if self.touche_sol:
            self.t_jump=0
            self.vitesse[1]= -6
        return

    def run(self):
        self.t_run=0
        self.switch_image()
        return

    def dessine(self,list_sprites):
        self.dessine_basic(list_sprites)
        for obj in self.projectiles:
            obj.dessine(list_sprites)
            if (obj.rect.left > MAX_X) or (obj.rect.top > MAX_Y) or (obj.rect.right < 0) or (obj.rect.bottom < 0):
                self.projectiles.remove(obj)

        return
