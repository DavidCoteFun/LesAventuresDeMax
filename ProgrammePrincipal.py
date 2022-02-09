#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov 21st 2019
Les aventures de Max 0.2.0
@author: Tristan Brunet-Cote, David Cote
"""
import pygame
from pygame.locals import *
import random, math, time

from Parametres import MAX_X,MAX_Y
from maps import dico_tableaux,ImageGenerique,MarioMap
from personnages import Goomba,JoueurPrincipal,Radio

class App:
    def __init__(self):
        self._running = True
        self.t=0
        self.timer=0
        self.newLevel=False
        return        

    def on_init(self,tableau):
        self._display_surf = pygame.display.set_mode((MAX_X,MAX_Y))
        pygame.display.set_caption('Les Aventures de Max')
        self._running = True
        self.hero=JoueurPrincipal(MAX_X/2,MAX_Y/2)
        self.ennemis=[]
        if isinstance(tableau,MarioMap):
            self.map=tableau
        else:
            self.map=tableau()
        self.obstacles=self.map.obstacles
        self.backgrounds=self.map.backgrounds
        return

    def bouge_ecran(self,x,y):
        return

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                self.hero.run()
            elif event.key == pygame.K_SPACE:
                self.hero.jump()
            elif event.key == pygame.K_s:
                self.hero.shoot()
            elif event.key == pygame.K_UP:
                prochain_tableau=self.map.ouvre_une_porte(self.hero)
                if prochain_tableau:
                    self.nouveau_tableau(prochain_tableau)
            elif event.key == pygame.K_z:
                self.nouveau_tableau('tableau2')
            elif event.key == pygame.K_q:
                self._running = False
        elif event.type == pygame.QUIT:
            self._running = False
        return

    
    def on_loop(self):
        self.sprites = pygame.sprite.RenderUpdates()
                
        #Calcule hero
        self.hero.somme_des_forces(self.obstacles)
        self.hero.bouge(limit_to_frame=True)
        self.hero.attaque(self.ennemis,self.sprites)

        #Calcule ennemis
        if len(self.ennemis)<1:
            newEnnemy=self.spawn(self.map.ennemi_type)
            if newEnnemy:
                self.ennemis.append(newEnnemy)
        for ennemi in self.ennemis:
            ennemi.somme_des_forces(self.obstacles,sensible_a_gravite=True)
            ennemi.bouge()
            if ennemi.attaque(self.hero)>0:
                self.game_over()
            if ennemi.rect.top > MAX_Y:
                ennemi.efface(self.sprites)
                self.ennemis.remove(ennemi)


        #Calcule map et obstacles
        if self.hero.vitesse[0]:
            if (self.hero.rect.x < MAX_X*0.25) or (self.hero.rect.x > MAX_X*0.6):
                dxEcran=self.hero.vitesse[0]
                self.map.bouge_ecran(dxEcran,0)
                self.hero.rect.x-=dxEcran
                for enn in self.ennemis:
                    enn.rect.x-=dxEcran
        
        if self.hero.vitesse[1]:
            if (self.hero.rect.y <MAX_Y*0.1) or (self.hero.rect.bottom>MAX_Y)*0.9:
                dyEcran=self.hero.vitesse[1]
                self.map.bouge_ecran(0,dyEcran)
                self.hero.rect.y-=dyEcran
                for enn in self.ennemis:
                    enn.rect.y-=dyEcran
                
        xMap,yMap=self.map.ecran_to_map(self.hero.rect.x,self.hero.rect.top)
        if yMap > MAX_Y:
            print(self.hero.rect.top)
            print(self.hero.rect.bottom)
            print(self.hero.vitesse[1])
            print(yMap)
            self.game_over()
        

        #Dessine tout
        for back in self.backgrounds:
            if back.redessine:
                back.dessine(self.sprites)
                back.redessine=False
        self.hero.dessine(self.sprites)
        for ennemi in self.ennemis:
            ennemi.dessine(self.sprites)
        for obstacle in self.obstacles:
            if obstacle.redessine:
                obstacle.dessine(self.sprites)
                obstacle.redessine=False


        #mesure performance de l'ordi
        if self.timer%100==0:
            tmp=time.time()
            #print("t: %.2f"%(tmp-self.t))
            self.t=tmp
        self.timer+=1
        return
    
    def nouveau_tableau(self,prochain_tableau):
        print("Nouveau tableau: %s"%prochain_tableau)
        self.newLevel=prochain_tableau
        self._running=False
        return

    def game_over(self):
        print("\nGame Over\n")
        self._running = False
        goSurf=pygame.image.load("/Users/dcote/Tristan/Mario/images/game_over_petit.gif")
        goIma=ImageGenerique(0,0,"/Users/dcote/Tristan/Mario/images/game_over_petit.gif")
        self._display_surf.blit(goSurf,((MAX_X-goIma.rect.w)/2,(MAX_Y-goIma.rect.h)/2))
        return

    def spawn(self,sorte):
        if sorte is None:
            return
        #cree le personnage ennemi
        tmpX=random.random()*MAX_X        
        tmpY=random.random()*MAX_Y/2
        perso=None
        if sorte=="Goomba":
            perso=Goomba(tmpX,tmpY)
        elif sorte=="Radio":
            perso=Radio(tmpX,tmpY)

        #empeche de spawner a un endroit chiant(David)
        #C'est vrai maudit goomba de $#%&%*(Tristan)
        if perso.rect.left<self.hero.rect.right and perso.rect.right>self.hero.rect.left:
            return self.spawn(sorte)
        for obstacle in self.obstacles:
            if pygame.sprite.collide_rect(obstacle,perso):
                return self.spawn(sorte)
        return perso
    
    def on_render(self):
        rects = self.sprites.draw(self._display_surf)
        pygame.display.update(rects)
        return

    def on_cleanup(self,nextLevel):
        self.newLevel=False
        if nextLevel:
            time.sleep(1)
            theApp.on_init(dico_tableaux[nextLevel])
            theApp.on_execute()
        else:
            pygame.quit()
        return
 
    def on_execute(self):
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup(self.newLevel)
        return

if __name__ == "__main__" :
    theApp = App()
    theApp.on_init(dico_tableaux['debut'])
    theApp.on_execute()
    time.sleep(3)
    exit()

