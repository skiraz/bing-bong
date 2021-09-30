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




     def hit_left(self):
         if self.pong.colliderect(self.bar) and self.bar.left<self.pongx<self.bar.centerx:
             return 1
         else:return 0







     def move(self,action):
         keys = pygame.key.get_pressed()
         if np.array_equal(action, [1 ,0, 0]):
             self.direction="Left"

         elif np.array_equal(action, [0 ,0, 1]):
             self.direction = "Right"
         else:
             self.direction=" "


         if self.bar.right>=self.w:
             self.plocx=self.plocx-2
         if self.bar.left <=0:
             self.plocx = self.plocx + 2

         if self.direction=="Left":
             self.plocx-=1.5
         if self.direction == "Right":
             self.plocx+=1.5
         if self.direction==" ":
             pass
         #print(self.direction)

     def reset(self):
         self.stopwatch1 = pygame.time.get_ticks()
         self.loopbounce=0
         self.direction=" "
         self.Bounces = 0
         self.plocx = 350
         self.frames = 0
         self.plocy = 600
         self.pongx =random.randint(10,self.w-10)
         self.pongy = 100
         self.pdy = 1
         self.pdx = 1
         self.barsize = (200, 10)
         self.bar = pygame.draw.rect(self.display, (0, 0, 255),
                                     pygame.Rect(self.plocx, self.plocy, self.barsize[0], self.barsize[1]))



         self.pong = pygame.draw.circle(self.display, (255, 0, 0), (self.pongx, self.pongy), 8)






     def Pong(self):
         self.pongy+=2. *self.pdy
         self.pongx+=0.027*self.pdx
         collx=0

         if self.bar.colliderect(self.pong):
             self.Bounces += 1

             pygame.mixer.music.play(loops=0, start=0.2)
             collx=self.bar.centerx-self.pong.x


             self.pdx=-collx
             self.pdy=-1
         if self.pongy<=0:
             self.pdy=self.pdy*-1
             pygame.mixer.music.play(loops=0, start=0.2)
         if self.pongx>=self.w:
             self.pdx=self.pdx*-1
             pygame.mixer.music.play(loops=0, start=0.2)
         if self.pongx<=0:
             self.pdx=self.pdx*-1
             pygame.mixer.music.play(loops=0, start=0.2)
         if self.pongy>=self.h:
             self.display.fill((0,0,0))
             text = font.render("Game Over !" , True, (255,0,0))
             self.display.blit(text, [self.h-450, self.w-600])




     def update(self):
            self.stopwatch2 = pygame.time.get_ticks()
            self.display.fill((0,0,0))
            self.bar = pygame.draw.rect(self.display, (0, 0, 255),
                                        pygame.Rect(self.plocx, self.plocy, self.barsize[0], self.barsize[1]))
            font1 = pygame.font.Font('arial.ttf', 20)
            text = font1.render(f"Bounces : {int(self.Bounces/3)}", True, (255, 255, 255))

            self.display.blit(text, [0, 0])
            self.seconds=int((self.stopwatch2 - self.stopwatch1)/1000 % 60)




            text = font1.render(f"seconds : {self.seconds}", True, (255, 255, 255))

            self.display.blit(text, [self.w-150, 0])


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
         if  self.pongy>=self.h:
             game_over=1
             reward=-90
             return reward,game_over
         if  self.bar.left+10 <=self.pongx<=self.bar.right-10:
             reward=10


         if self.bar.colliderect(self.pong):
             reward=30


         # loop check :
         if self.bar.colliderect(self.pong)  and (self.pong.centerx-self.bar.centerx==8) :
             self.loopbounce+=1

         elif self.pong.colliderect(self.bar) and (self.pong.centerx-self.bar.centerx!=8) :
             self.loopbounce=0

         if self.loopbounce== 9:
             self.reset()









         self.update()



         return reward, game_over












game=bb_game()