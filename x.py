# 222222222222222222222
from pygame import *

clock = time.Clock()
DONE = False
screen = display.set_mode((1024,768))
class Thing():
    def __init__(self,x,y,w,h,s,c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.s = s
        self.sur = Surface((64,48))
        draw.rect(self.sur,c,(self.x,self.y,w,h),1)
        self.sur.fill(c)
    def draw(self):
        screen.blit(self.sur,(self.x,self.y))
    def move(self,x,r):
        if key.get_pressed()[K_w] or key.get_pressed()[K_UP]:
            if x == 1:
                self.y -= self.s
            else:
                self.y = (r.y + r.h) + self.s
        if key.get_pressed()[K_s] or key.get_pressed()[K_DOWN]:
            if x == 1:
                self.y += self.s
            else:
                self.y = (r.y - r.h) - self.s
        if key.get_pressed()[K_a] or key.get_pressed()[K_LEFT]:
            if x == 1:
                self.x -= self.s
            else:
                self.x = (r.x + r.w) + self.s
        if key.get_pressed()[K_d] or key.get_pressed()[K_RIGHT]:
            if x == 1:
                self.x += self.s
            else:
                self.x = (r.x - r.w) - self.s
    def warp(self):
        if self.y < -48:
             self.y = 768
        if self.y > 768 + 48:
             self.y = 0
        if self.x < -64:
             self.x = 1024 + 64
        if self.x > 1024 + 64:
             self.x = -64
r1 = Thing(0,0,64,48,1,(0,255,0))
r2 = Thing(6*64,6*48,64,48,1,(255,0,0))

while not DONE:
    screen.fill((0,0,0))
    r2.draw()
    r1.draw()
    if not ((((r1.x + r1.w) >= r2.x) and r1.x <= ((r2.x + r2.w))) and (((r1.y + r1.h) >= r2.y) and (r1.y <= (r2.y + r2.h)))):
        r1.move(1,r2)
    r1.warp()
    if key.get_pressed()[K_ESCAPE]:
        DONE = True
    for ev in event.get():
        if ev.type == QUIT:
            DONE = True
    display.flip()
quit()
