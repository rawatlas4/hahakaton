from pygame import *
import os
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.direction = "right"
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
    def load_animation(self):
        sheet_right = image.load("images/player2.png").convert_alpha()
        frame_width = 24
        frame_height = 24
        self.frames_right = [
            transform.scale(sheet_right.subsurface((i * frame_width, 0, frame_width,frame_height)),(112,112))
            for i in range(4)
        ]
        self.frames_left = [transform.flip(f,True,True)for f in self.frames_right]
        self.animation_frames = self.frames_right

    def update_animation(self):
        self.frame_index +=0.2
        if self.frame_index>= len(self.animation_frames):
            self.frame_index = 0
        self.image = self.animation_frames[int(self.frame_index)]

    def update(self, barriers):
        if self.x_speed > 0:
            self.direction = "right"
            self.direction_frames = self.frames_right
        elif self.x_speed < 0:
            self.direction = "left"
            self.animation_frames = self.frames_left
        self.update_animation()
        if self.rect.x <= win_width-80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        if self.rect.y <= win_height-80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top) 
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) 

    def fire(self):
        bullet = Bullet('images/arrow1.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2

    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2

    def update(self):
        if self.rect.y <= self.y1: 
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()
def fade(screen,width,height):
    fade_surface = Surface((width,height))
    fade_surface.fill((0,0,0))
    for alpha in range(0,255,5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface,(0,0))
        display.update()
        time.delay(30)
def save_progres(amout):
    with open("save.txt","w") as f:
        f.write(str(amout))
def load_progres():
    if os.path.exists("save.txt"):
        with open("save.txt") as f:
            return int(f.read())
    return 0 


win_width = 1200
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")

back_m = transform.scale(image.load("images/fon.jpg"), (win_width, win_height))
start_but = GameSprite("images/start.png",1000,10,200,80)
exit_but = GameSprite("images/exit.png",0,10,200,80)
mus_but = GameSprite("images/musicb.png", 1000, 600, 80, 80)

mixer.init()
mixer.music.load("sounds/music.wav")
mixer.music.set_volume(0.3)
mixer.music.play(-1)
lose = mixer.Sound("sounds/lose.mp3")
win = mixer.Sound("sounds/win.mp3")
total_amout = load_progres()
#-------------------------------1lvl----------------------------
amount = 0

font.init()
text = font.SysFont(None, 36).render("Coins: " + str(amount), True, (255, 255, 0))

back = transform.scale(image.load("images/fon.jpg"), (win_width, win_height))
bullets = sprite.Group()
barriers = sprite.Group()
monsters = sprite.Group()
coins = sprite.Group()

w1 = GameSprite('images/wall2.png',0, 200, 300, 50)
w2 = GameSprite('images/wall1.png', 250, 200, 50, 400)
barriers.add(w1)
barriers.add(w2)

hero = Player('images/player.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('images/next.png', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy_v('images/eneme.png', 1000, 200, 80, 80, 5, 200, 420)
monster2 = Enemy_h('images/eneme.png', 0, 90, 80, 80, 5, 0, 200)
monsters.add(monster1)
monsters.add(monster2)

coin1 = GameSprite('images/coin.png', 400, 200, 80, 80)
coin2 = GameSprite('images/coin.png', 200, 600, 80, 80)
coins.add(coin1)
coins.add(coin2)

#-------------------------------2lvl----------------------------
amount_2 = 0

back_2 = transform.scale(image.load("images/fon_2.jpg"), (win_width, win_height))
barriers_2 = sprite.Group()
monsters_2 = sprite.Group()
coins_2 = sprite.Group()

w1_2 = GameSprite('images/wall2.png',400, 200, 300, 50)
w2_2= GameSprite('images/wall1.png', 750, 200, 50, 400)
barriers_2.add(w1_2)
barriers_2.add(w2_2)

hero_2 = Player('images/player.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite_2 = GameSprite('images/next.png', win_width - 85, win_height - 100, 80, 80)

monster1_2 = Enemy_v('images/eneme.png', 1000, 200, 80, 80, 5, 200, 420)
monster2_2 = Enemy_h('images/eneme.png', 0, 90, 80, 80, 5, 0, 200)
monsters_2.add(monster1_2)
monsters_2.add(monster2_2)

coin1_2 = GameSprite('images/coin.png', 200, 300, 80, 80)
coin2_2 = GameSprite('images/coin.png', 300, 100, 80, 80)
coins_2.add(coin1_2)
coins_2.add(coin2_2)
#-------------------------------3lvl---------------------------------------------------------------------------------------
amount_3 = 0

back_3 = transform.scale(image.load("images/fon_3.jpg"), (win_width, win_height))
barriers_3 = sprite.Group()
monsters_3 = sprite.Group()
coins_3 = sprite.Group()

hero_3 = Player('images/player.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite_3 = GameSprite('images/tresure.png', win_width - 85, win_height - 400, 80, 80)

monster1_3 = Enemy_v('images/eneme.png', 1000, 200, 80, 80, 5, 200, 420)
monster2_3 = Enemy_v('images/eneme.png', 1000, 300, 80, 80, 5, 200, 420)
monster3_3 = Enemy_v('images/eneme.png', 1000, 400, 80, 80, 5, 200, 420)
monster4_3 = Enemy_v('images/eneme.png', 1000, 500, 80, 80, 5, 200, 420)
monster5_3 = Enemy_v('images/eneme.png', 1100, 600, 80, 80, 5, 200, 420)
monster6_3 = Enemy_v('images/eneme.png', 1200, 700, 80, 80, 5, 200, 420)
monsters_3.add(monster1_3)
monsters_3.add(monster1_3)
monsters_3.add(monster2_3)
monsters_3.add(monster3_3)
monsters_3.add(monster4_3)
monsters_3.add(monster5_3)
monsters_3.add(monster6_3)

coin1_3 = GameSprite('images/coin.png', 1000, 300, 80, 80)
coin2_3 = GameSprite('images/coin.png', 300, 100, 80, 80)
coins_3.add(coin1_3)
coins_3.add(coin2_3)
#--------------------------ігровий цикл-------------------------------------------------------------------------------------------------------------------------
finish = False
run = True
a = "menu"
music = "on"
while run:
    if a == "menu":
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN:
                if exit_but.rect.collidepoint(e.pos):
                    run = False
                if mus_but.rect.collidepoint(e.pos):
                    if music == "on":
                        mixer.music.pause()
                        music = "off"
                    else:
                        mixer.music.unpause()
                        music = "on"
                if start_but.rect.collidepoint(e.pos):
                    mixer_music.stop()
                    fade(window,win_width,win_height)
                    a = "lvl1"
        window.blit(back_m,(0,0))
        start_but.reset()
        exit_but.reset()
        mouse_pos = mouse.get_pos()
    elif a == "lvl1":
            
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero.x_speed = -8
                if e.key == K_RIGHT:
                    hero.x_speed = 8
                if e.key == K_UP:
                    hero.y_speed = -8
                if e.key == K_DOWN:
                    hero.y_speed = 8
                if e.key == K_SPACE:
                    hero.fire()

            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    hero.x_speed = 0
                if e.key == K_RIGHT:
                    hero.x_speed = 0 
                if e.key == K_UP:
                    hero.y_speed = 0
                if e.key == K_DOWN:
                    hero.y_speed = 0

        if not finish:
            window.blit(back, (0, 0))
            window.blit(text, (270, 0))

            hero.update(barriers)
            hero.reset()
            bullets.draw(window)
            bullets.update()

            barriers.draw(window)
            final_sprite.reset()

            sprite.groupcollide(monsters, bullets, True, True)
            monsters.update()
            monsters.draw(window)
            sprite.groupcollide(bullets, barriers, True, False)

            coins.draw(window)
            if sprite.spritecollide(hero, coins, True):
                amount += 1
                total_amout+=1
                save_progres(total_amout)
            text = font.SysFont(None, 36).render("Coins: " + str(amount), True, (255, 255, 0))

            if sprite.spritecollide(hero, monsters, False):
                finish = True
                lose.play()
                mixer.music.stop()
                img = image.load('images/game_over.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            if sprite.collide_rect(hero,final_sprite):
                fade(window,win_width,win_height)
                a = "lvl2"
    elif a == "lvl2":
            
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero_2.x_speed = -8
                if e.key == K_RIGHT:
                    hero_2.x_speed = 8
                if e.key == K_UP:
                    hero_2.y_speed = -8
                if e.key == K_DOWN:
                    hero_2.y_speed = 8
                if e.key == K_SPACE:
                    hero_2.fire()

            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    hero_2.x_speed = 0
                if e.key == K_RIGHT:
                    hero_2.x_speed = 0 
                if e.key == K_UP:
                    hero_2.y_speed = 0
                if e.key == K_DOWN:
                    hero_2.y_speed = 0

        if not finish:
            window.blit(back_2, (0, 0))
            window.blit(text, (270, 0))

            hero_2.update(barriers_2)
            hero_2.reset()
            bullets.draw(window)
            bullets.update()

            barriers_2.draw(window)
            final_sprite_2.reset()

            sprite.groupcollide(monsters_2, bullets, True, True)
            monsters_2.update()
            monsters_2.draw(window)
            sprite.groupcollide(bullets, barriers_2, True, False)

            coins_2.draw(window)
            if sprite.spritecollide(hero_2, coins_2, True):
                amount_2 += 1
                total_amout+=1
                save_progres(total_amout)
            text = font.SysFont(None, 36).render("Coins: " + str(amount_2), True, (255, 255, 0))

            if sprite.spritecollide(hero_2, monsters_2, False):
                finish = True
                lose.play()
                mixer.music.stop()
                img = image.load('images/game_over.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))        
            if sprite.collide_rect(hero_2,final_sprite):
                fade(window,win_width,win_height)
                a = "lvl3"
    elif a == "lvl3":
            
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero_3.x_speed = -8
                if e.key == K_RIGHT:
                    hero_3.x_speed = 8
                if e.key == K_UP:
                    hero_3.y_speed = -8
                if e.key == K_DOWN:
                    hero_3.y_speed = 8
                if e.key == K_SPACE:
                    hero_3.fire()

            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    hero_3.x_speed = 0
                if e.key == K_RIGHT:
                    hero_3.x_speed = 0 
                if e.key == K_UP:
                    hero_3.y_speed = 0
                if e.key == K_DOWN:
                    hero_3.y_speed = 0

        if not finish:
            window.blit(back_3, (0, 0))
            window.blit(text, (270, 0))

            hero_3.update(barriers_3)
            hero_3.reset()
            bullets.draw(window)
            bullets.update()

            barriers_3.draw(window)
            final_sprite_3.reset()

            sprite.groupcollide(monsters_3, bullets, True, True)
            monsters_3.update()
            monsters_3.draw(window)
            sprite.groupcollide(bullets, barriers_3, True, False)

            coins_3.draw(window)
            if sprite.spritecollide(hero_3, coins_3, True):
                amount_3 += 1
                total_amout+=1
                save_progres(total_amout)
            text = font.SysFont(None, 36).render("Coins: " + str(amount_3), True, (255, 255, 0))

            if sprite.spritecollide(hero_3, monsters_3, False):
                finish = True
                lose.play()
                mixer.music.stop()
                img = image.load('images/game_over.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))        







            
            
            
            
            if sprite.collide_rect(hero_3, final_sprite_3):
                finish = True
                win.play()
                mixer.music.stop()
                img = image.load('images/winner.png')
                window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        
    time.delay(50)
    display.update()