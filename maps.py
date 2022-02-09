#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 19:15:15 2019

@author: Tristan Brunet-Cote, David Cote
"""

import pygame
from pygame import Color
from Parametres import MAX_X,MAX_Y
from personnages import ChoseQuiBouge,Carre
import time

dico_tableaux={}  #voir plus bas pour remplir le dictionnaire

class MarioMap:
    def __init__(self,nom,ennemi_type=None):
        self.nom=nom
        self.obstacles=[]
        self.backgrounds=[]
        self.coord_ecran=[0,0]
        self.ennemi_type=ennemi_type
        self.portes=[]
        return
    
    def reset(self):
        self.coord_ecran=[0,0]
        for obs in self.obstacles:
            obs.redessine=True
        for back in self.backgrounds:
            back.redessine=True
        return
    
    def bouge_ecran(self,dx,dy):
        if dx==0 and dy==0:
            return
        self.coord_ecran[0]+=dx
        self.coord_ecran[1]+=dy
        for obj in self.obstacles:
            obj.rect.x-=dx
            obj.rect.y-=dy
            obj.redessine=True
        for back in self.backgrounds:
            back.rect.x-=dx
            back.rect.y-=dy
            back.redessine=True
        return
    
    def ajoute_obstacle(self,obstacle):
        #ordonne en position x
        self.obstacles.append(obstacle)
        return

    def ajoute_background(self,image_de_fond):
        #ordonne en position x
        self.backgrounds.append(image_de_fond)
        return

    def map_to_ecran(self,x,y):
        return x-self.coord_ecran[0],y-self.coord_ecran[1]

    def ecran_to_map(self,x,y):
        return x+self.coord_ecran[0],y+self.coord_ecran[1]
    
    def ouvre_une_porte(self,hero):
        for porte in self.portes:
            if pygame.sprite.collide_rect(porte,hero):
                return porte.prochain_tableau
        return False


class Gazon(ChoseQuiBouge):
    def __init__(self,posX,posY):
       image=pygame.image.load("/Users/dcote/Tristan/Mario/images/herbemario_petit.png").convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image)
       return

class Poutre(ChoseQuiBouge):
    def __init__(self,posX,posY):
       image=pygame.image.load("/Users/dcote/Tristan/Mario/images/bloc_pour_poutre_petit.png").convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image)
       return

class ImageGenerique(ChoseQuiBouge):
    def __init__(self,posX,posY,nom_fichier):
       image=pygame.image.load(nom_fichier).convert()
       ChoseQuiBouge.__init__(self,[posX,posY],image)
       return

class Texte(ChoseQuiBouge):
    def __init__(self,texte,couleur,posX,posY):
        font = pygame.font.Font('freesansbold.ttf', 32)
        ChoseQuiBouge.__init__(self,[posX,posY],font.render(texte,True,couleur))
        return


hPout=Poutre(0,0).rect.h
hPlat=ImageGenerique(0,0,"/Users/dcote/Tristan/Mario/images/plateforme_petit.png").rect.h
hGazon=Gazon(0,0).rect.h
wGazon=Gazon(0,0).rect.w
hPierre=ImageGenerique(0,0,"/Users/dcote/Tristan/Mario/images/Pierre.gif").rect.h
wPierre=ImageGenerique(0,0,"/Users/dcote/Tristan/Mario/images/Pierre.gif").rect.w


# INTRO screen
intro=MarioMap("intro")
porte0=Carre('black',0,0,MAX_X,MAX_Y)
porte0.prochain_tableau='tableau1'
intro.portes.append(porte0)
tt=Texte("Les Aventures de Max!!!",Color('yellow'),0,0)
tt.rect.center=(MAX_X/2.0,MAX_Y/3.5)
intro.ajoute_background(tt)
tt2=Texte("Fleche UP pour commencer",Color('yellow'),0,0)
tt2.rect.center=(MAX_X/2.0,MAX_Y/2.5)
intro.ajoute_background(tt2)
intro.ajoute_obstacle(Gazon((MAX_X-wGazon)*0.5,MAX_Y-hGazon))
intro.ajoute_background(ImageGenerique(100,100,"/Users/dcote/Tristan/Mario/images/RelaxMax.gif"))


# MAP 1
def get_map1():
    map1=MarioMap("Map1",ennemi_type="Radio")
    
    #c1=Carre('green',0,MAX_Y-40,MAX_X,40)
    g1=Gazon(0,MAX_Y-hGazon)
    map1.ajoute_obstacle(g1)
    map1.ajoute_obstacle(Carre('green',0,MAX_Y,g1.rect.width*2,100))
    
    b1=Poutre(200,g1.rect.top-hPout)
    map1.ajoute_obstacle(b1)
    
    b2=Poutre(200,b1.rect.top-hPout)
    map1.ajoute_obstacle(b2)
    
    b3=Poutre(200,b2.rect.top-hPout)
    map1.ajoute_obstacle(b3)
    
    b4=Poutre(350,g1.rect.top-hPout)
    map1.ajoute_obstacle(b4)
    
    b5=Poutre(350,b4.rect.top-hPout)
    map1.ajoute_obstacle(b5)
    
    b6=Poutre(350,b5.rect.top-hPout)
    map1.ajoute_obstacle(b6)
    
    b7=Poutre(100, -20)
    map1.ajoute_obstacle(b7)
    
    map1.ajoute_obstacle(Carre('transparent',200,220,50,50))
    
    #map1.ajoute_obstacle(ImageGenerique(200,-300,"/Users/dcote/Tristan/Mario/images/tuyau_petit.gif"))
    tuy=ImageGenerique(450,-300,"/Users/dcote/Tristan/Mario/images/tuyau_petit.gif")
    porte1=Carre('transparent',tuy.rect.x,tuy.rect.y-80,tuy.rect.w,80)
    porte1.prochain_tableau='shortcut1'
    map1.portes.append(porte1)
    map1.ajoute_background(porte1)
    
    map1.ajoute_obstacle(tuy)
    bri=ImageGenerique(450,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif")
    map1.ajoute_obstacle(bri)
    map1.ajoute_obstacle(ImageGenerique(bri.rect.x-2*bri.rect.w,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif"))
    map1.ajoute_obstacle(ImageGenerique(bri.rect.x-bri.rect.w,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif"))
    map1.ajoute_obstacle(ImageGenerique(bri.rect.x+bri.rect.w,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif"))
    map1.ajoute_obstacle(ImageGenerique(bri.rect.x+2*bri.rect.w,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif"))
    map1.ajoute_obstacle(ImageGenerique(bri.rect.x+3*bri.rect.w,tuy.rect.y+tuy.rect.h,"/Users/dcote/Tristan/Mario/images/brique_petit.gif"))
    
    p7=ImageGenerique(100,b6.rect.top-hPlat,"/Users/dcote/Tristan/Mario/images/plateforme_petit.png")
    map1.ajoute_obstacle(p7)
    
    g2=Gazon(g1.rect.right,g1.rect.top)
    map1.ajoute_obstacle(g2)
    
    p8=ImageGenerique(g2.rect.right,p7.rect.top,"/Users/dcote/Tristan/Mario/images/plateforme_petit.png")
    map1.ajoute_obstacle(p8)
    
    p9=ImageGenerique(p8.rect.right,p8.rect.top-200,"/Users/dcote/Tristan/Mario/images/plateforme_petit.png")
    map1.ajoute_obstacle(p9)
    
    g3=Gazon(p9.rect.right+100,g1.rect.top)
    map1.ajoute_obstacle(g3)
    
    tmp=ImageGenerique(g3.rect.right-100,b6.rect.top,"/Users/dcote/Tristan/Mario/images/Pierre.gif")
    map1.ajoute_obstacle(tmp)
    porte2=Carre('yellow',tmp.rect.x,tmp.rect.y-80,tmp.rect.w,80)
    porte2.prochain_tableau='tableau2'
    map1.portes.append(porte2)
    map1.ajoute_background(porte2)
    print("porte1 %i %i"%(porte1.rect.x,porte1.rect.y))
    print("porte2 %i %i"%(porte2.rect.x,porte2.rect.y))
    return map1

def get_map1b():
    myMap=get_map1()
    myMap.bouge_ecran(2000,0)
    return myMap
    
# MAP 2
map2=MarioMap("Map2",ennemi_type="Goomba")
map2.ajoute_obstacle(Gazon(0,MAX_Y-hGazon))
map2.ajoute_obstacle(Poutre(200,MAX_Y-hGazon-3*hPout))
map2.ajoute_obstacle(Poutre(350,MAX_Y-hGazon-3*hPout))
map2.ajoute_obstacle(Poutre(100,MAX_Y-hGazon-7*hPout))
map2.ajoute_obstacle(Poutre(200,MAX_Y-hGazon-11*hPout))
map2.ajoute_obstacle(Poutre(0,MAX_Y-hGazon-13*hPout))
map2.ajoute_obstacle(Poutre(300,MAX_Y-hGazon-15*hPout))
map2.ajoute_obstacle(Poutre(500,MAX_Y-hGazon-17*hPout))
for i in range(-4,0):
    map2.ajoute_obstacle(ImageGenerique(300+i*wPierre,MAX_Y-hGazon-20*hPout,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))
for i in range(-8,-4):
    map2.ajoute_obstacle(ImageGenerique(300+i*wPierre,MAX_Y-hGazon-19*hPout,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))
map2.ajoute_background(Carre('red',300-8*wPierre,MAX_Y-hGazon-20*hPout,4*wPierre,50))

for i in range(0,40):
    map2.ajoute_obstacle(ImageGenerique(wGazon-wPierre,MAX_Y-hGazon-i*hPierre,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))


map2.ajoute_obstacle(Carre('blue',wGazon+50,MAX_Y-hGazon-3*hPout,50,50))
porte2=Carre('yellow',wGazon+50,MAX_Y-hGazon-3*hPout-100,50,100)
porte2.prochain_tableau='Fin'
map2.portes.append(porte2)
map2.ajoute_background(porte2)


# OUTRO screen
outro=MarioMap("Fin")
tt3=Texte("Bravo!!!",Color('yellow'),0,0)
tt3.rect.center=(MAX_X/2.0,MAX_Y/3.5)
outro.ajoute_background(tt3)
outro.ajoute_obstacle(Gazon((MAX_X-wGazon)*0.5,MAX_Y-hGazon))
outro.portes.append(porte0)

#shortcut1
shortcut1=MarioMap("shortcut1")
for i in range(-10,10):
    shortcut1.ajoute_obstacle(ImageGenerique(MAX_X/2+i*wPierre,MAX_Y-hPierre,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))
for i in range(12,16):
    shortcut1.ajoute_obstacle(ImageGenerique(MAX_X/2+i*wPierre,MAX_Y-4*hPierre,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))
for i in range(18,22):
    shortcut1.ajoute_obstacle(ImageGenerique(MAX_X/2+i*wPierre,MAX_Y-8*hPierre,"/Users/dcote/Tristan/Mario/images/Pierre.gif"))    
tuy=ImageGenerique(MAX_X/2+24*wPierre,MAX_Y-10*hPierre,"/Users/dcote/Tristan/Mario/images/tuyau_petit.gif")
porte3=Carre('transparent',tuy.rect.x,tuy.rect.y-80,tuy.rect.w,80)
porte3.prochain_tableau='tableau1b'
shortcut1.portes.append(porte3)
shortcut1.ajoute_background(porte3)
shortcut1.ajoute_obstacle(tuy)

#Dictionnaire
dico_tableaux['debut']=map2
#dico_tableaux['debut']=intro
dico_tableaux['tableau1']=get_map1
dico_tableaux['tableau1b']=get_map1b
dico_tableaux['tableau2']=map2
dico_tableaux['Fin']=outro
dico_tableaux['shortcut1']=shortcut1




