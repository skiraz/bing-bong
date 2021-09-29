import random
import numpy as np
import pygame
pygame.init()
pygame.mixer.music.load('Dodgeball_sound_effect_(getmp3.pro).mp3')

font = pygame.font.Font('arial.ttf', 100)

class bb_game:
     def __init__(self,width=860,height=640):
         self.h=height
         self.w=width
         self.display=pygame.display.set_mode((self.w,self.h))
         pygame.display.set_caption("Bing Bong")
         self.clock=pygame.time.Clock()
         self.reset()







     def move(self,action):
         keys = pygame.key.get_pressed()
         if np.array_equal(action, [1, 0]):
             self.direction="Left"

         elif np.array_equal(action, [0, 1]):
             self.direction = "Right"


         if self.bar.right>=self.w:
             self.plocx=self.plocx-1
         if self.bar.left <=0:
             self.plocx = self.plocx + 1

         if self.direction=="Left":
             self.plocx-=1
         if self.direction == "Right":
             self.plocx+=1.

     def reset(self):
         self.alr=[10,750]
         a=random.randint(0,1)
         self.direction="Right"
         self.plocx = 350
         self.frames = 0
         self.plocy = 600
         self.pongx = self.alr[1]
         self.pongy = 100
         self.pdy = 1
         self.pdx = 1
         self.barsize = (200, 10)
         self.bar = pygame.draw.rect(self.display, (0, 0, 255),
                                     pygame.Rect(self.plocx, self.plocy, self.barsize[0], self.barsize[1]))

         self.pong = pygame.draw.circle(self.display, (255, 0, 0), (self.pongx, self.pongy), 8)




     def Pong(self):
         self.pongy+=1.8 *self.pdy
         self.pongx+=0.007*self.pdx
         collx=0

         if self.bar.colliderect(self.pong):
             pygame.mixer.music.play(loops=0, start=0.2)
             collx=self.bar.centerx-self.pong.x
             self.pdx=-collx
             self.pdy=-1
         if self.pongy<=0:
             self.pdy=self.pdy*-1
         if self.pongx>=self.w:
             self.pdx=self.pdx*-1
         if self.pongx<=0:
             self.pdx=self.pdx*-1
         if self.pongy>self.h:
             self.display.fill((0,0,0))
             text = font.render("Game Over !" , True, (255,0,0))
             self.display.blit(text, [self.h-450, self.w-600])




     def update(self):
            self.display.fill((0,0,0))
            self.bar = pygame.draw.rect(self.display, (0, 0, 255),
                                        pygame.Rect(self.plocx, self.plocy, self.barsize[0], self.barsize[1]))

            self.pong = pygame.draw.circle(self.display, (255, 0, 0), (self.pongx, self.pongy), 8)
            self.Pong()
            pygame.display.flip()

     def play_step(self,action):
         self.frames+=1
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 quit()
         self.move(action)
         reward=0
         game_over=0
         if  self.pongy>self.h:
             game_over=1
             reward=-20
             return reward,game_over
         if self.bar.colliderect(self.pong):
             reward=20


         self.update()

         return reward, game_over












game=bb_game()