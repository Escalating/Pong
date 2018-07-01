import sys, math, random, functools
import pygame as pg
import pygame.gfxdraw
from pygame import *

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
LB = (0,255,255)
GRAY = (64,64,64)

x = 640
y = 480

class Scene():
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class GameScene(Scene):
    def __init__(self, level):
        super(GameScene, self).__init__()
        global speed, score1, score2
        self.w = 6
        self.h = 6
        self.x = x
        self.y = 240
        self.px = 0
        self.py = 0
        self.y2 = 240
        self.top = pg.draw.rect(screen, GRAY, ((0, 0, 640, 15)))
        self.bottom = pg.draw.rect(screen, GRAY, ((0, 465, 640, 15)))
        for qq in range(random.randrange(270, 370, 1)):
            self.px = qq
        for ww in range(random.randrange(50, 430, 1)):
            self.py = ww
        self.ball = Ball(self.px, self.py, speed)
        self.paddle1 = Paddle(20, 240, 15, 80)
        self.paddle2 = Paddle(615, 240, 15, 80)    

    def render(self, screen):
        global score1, score2
        screen.fill(BLACK)
        for y in range(3, 477, 9):
            pg.gfxdraw.box(screen, ((x/2), (y), self.w, self.h), GRAY)
        self.top = pg.draw.rect(screen, GRAY, ((0, 0, 640, 15)))
        self.bottom = pg.draw.rect(screen, GRAY, ((0, 465, 640, 15)))
        self.paddles = pg.sprite.Group()
        self.paddle1 = Paddle(20, self.y, 15, 80)
        self.paddle2 = Paddle(605, self.y2, 15, 80)
        self.paddles.add(self.paddle1, self.paddle2)
        self.paddles.draw(screen)
        self.ball.draw(screen)

        self.score1Text = font.render('%s' %(score1), True, WHITE)
        screen.blit(self.score1Text, (640/4, 30))
        self.score2Text = font.render('%s' %(score2), True, WHITE)
        screen.blit(self.score2Text, (640*6/8, 30))
        return
    
    def update(self):
        global speed, score1, score2
        if self.ball.rect.x < 0 or self.ball.rect.x > 640-15:
            speed[0] *= -1
        elif (self.ball.rect.y<0) or (self.ball.rect.y > 480-15):
            speed[1] *= -1
        if self.ball.rect.left <= 35 and self.paddle1.rect.top < self.ball.rect.top and self.paddle1.rect.bottom > self.ball.rect.bottom:
            speed[0] *= -1
        elif self.ball.rect.right >=605 and self.paddle2.rect.top < self.ball.rect.top and self.paddle2.rect.bottom > self.ball.rect.bottom:
            speed[0] *= -1
        if self.ball.rect.top <= self.top.bottom:
            speed[1] *= -1
        elif self.ball.rect.bottom >= self.bottom.top:
            speed[1] *= -1
            
        elif self.ball.rect.right >= 640:
            update_score1()
            pg.time.wait(75)
            self.ball.rect.x = random.randint(270, 370)
            self.ball.rect.y = random.randint(50, 430)
        elif self.ball.rect.left <= 0:
            update_score2()
            pg.time.wait(75)
            self.ball.rect.x = random.randint(270, 370)
            self.ball.rect.y = random.randint(50, 430)
        else:
            speed[0] *= 1
            
        global d
        if speed[0] == -5 or speed[0] == -6 or speed[0] == -7:
            if self.paddle2.rect.centery < 240:
                self.y2 += d
            elif self.paddle2.rect.centery > 240:
                self.y2 -= d
        elif speed[0] == 5 or speed[0] == 6 or speed[0] == 7:
            if self.paddle2.rect.centery < self.ball.rect.centery:
                self.y2 += d
            else:
                self.y2 -= d
           
        if score1 == 10:
            global p1W
            p1W = True
            self.manager.go_to(GameOverScene())
        elif score2 == 10:
            global p2W
            p2W = True
            self.manager.go_to(GameOverScene())
            
        self.ball.rect.x += speed[0]
        self.ball.rect.y += speed[1]
        
    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_t:
                    print('')
                if e.key == K_s and self.paddle1.rect.bottom < 480:
                    self.y += 35
                if e.key == K_w and self.paddle1.rect.top > 0:
                    self.y -= 35
                if e.key == K_p or e.key == K_ESCAPE:
                    self.manager.go_to(PauseScene())
            if e.type == MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                self.y = mouse_pos[1]-40
                pg.mouse.set_visible(False)
            else:
                pg.mouse.set_visible(True)
        return

class GameScene2(Scene):
    def __init__(self, level):
        super(GameScene2, self).__init__()
        global score1, score2
        self.w = 6
        self.h = 6
        self.x = x
        self.y = 240
        self.px = 0
        self.py = 0
        self.speed = [4,4]
        self.y2 = 240
        self.top = pg.draw.rect(screen, GRAY, ((0, 0, 640, 15)))
        self.bottom = pg.draw.rect(screen, GRAY, ((0, 465, 640, 15)))
        for qq in range(random.randrange(270, 370, 1)):
            self.px = qq
        for ww in range(random.randrange(50, 430, 1)):
            self.py = ww
        self.ball = Ball(self.px, self.py, self.speed)
        self.paddle1 = Paddle(20, 240, 15, 80)
        self.paddle2 = Paddle(615, 240, 15, 80)
        

    def render(self, screen):
        global score1, score2
        screen.fill(BLACK)
        for y in range(3, 477, 9):
            pg.gfxdraw.box(screen, ((x/2), (y), self.w, self.h), GRAY)
        self.top = pg.draw.rect(screen, GRAY, ((0, 0, 640, 15)))
        self.bottom = pg.draw.rect(screen, GRAY, ((0, 465, 640, 15)))
        self.paddles = pg.sprite.Group()
        self.paddle1 = Paddle(20, self.y, 15, 80)
        self.paddle2 = Paddle(605, self.y2, 15, 80)
        self.paddles.add(self.paddle1, self.paddle2)
        self.paddles.draw(screen)
        self.ball.draw(screen)

        self.score1Text = font.render('%s' %(score1), True, WHITE)
        screen.blit(self.score1Text, (640/4, 30))
        self.score2Text = font.render('%s' %(score2), True, WHITE)
        screen.blit(self.score2Text, (640*6/8, 30))
        return
    
    def update(self):
        global score1, score2
        if self.ball.rect.x < 0 or self.ball.rect.x > 640-15:
            self.speed[0] *= -1
        elif (self.ball.rect.y<0) or (self.ball.rect.y > 480-15):
            self.speed[1] *= -1
        if self.ball.rect.left <= 35 and self.paddle1.rect.top < self.ball.rect.top and self.paddle1.rect.bottom > self.ball.rect.bottom:
            self.speed[0] *= -1
            print('hit')
        elif self.ball.rect.right >=605 and self.paddle2.rect.top < self.ball.rect.top and self.paddle2.rect.bottom > self.ball.rect.bottom:
            self.speed[0] *= -1
            print('hit 2')
        if self.ball.rect.top <= self.top.bottom:
            self.speed[1] *= -1
        elif self.ball.rect.bottom >= self.bottom.top:
            self.speed[1] *= -1
        elif self.ball.rect.right >= 640:
            update_score1()
            pg.time.wait(75)
            self.ball.rect.x = random.randint(270, 370)
            self.ball.rect.y = random.randint(50, 430)
        elif self.ball.rect.left <= 0:
            update_score2()
            pg.time.wait(75)
            self.ball.rect.x = random.randint(270, 370)
            self.ball.rect.y = random.randint(50, 430)
        else:
            self.speed[0] *= 1
            
        if score1 == 10:
            global p1W
            p1W = True
            self.manager.go_to(GameOverScene2())
        elif score2 == 10:
            global p2W
            p2W = True
            self.manager.go_to(GameOverScene2())

        self.ball.rect.x += self.speed[0]
        self.ball.rect.y += self.speed[1]
        
        return
    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_t:
                    print('')
                if e.key == K_s and self.paddle1.rect.bottom < 480:
                    self.y += 35
                if e.key == K_w and self.paddle1.rect.top > 0:
                    self.y -= 35
                if e.key == K_DOWN and self.paddle2.rect.bottom < 480:
                    self.y2 += 35
                if e.key == K_UP and self.paddle2.rect.top > 0:
                    self.y2 -= 35
                if e.key == K_p or e.key == K_ESCAPE:
                    self.manager.go_to(PauseScene())
        return

class TitleScene(Scene):
    def __init__(self):
        super(TitleScene, self).__init__()
        global score1, score2
        score1 = 0
        score2 = 0
        self.active = True
        self.p1c = False
        self.p2c = False
        self.htpc = False
        self.quitc = False
        self.v = pg.mouse.set_visible(True)
        
    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pg.mouse.get_pos()
        
        self.titleText = bfont.render('P O N G', True, WHITE)
        screen.blit(self.titleText, ((x/2)-148, (y*1/20)+16))

        self.onePlayerText = font.render('1 Player', True, WHITE)
        self.onePlayerRect = pg.draw.rect(screen, BLACK, ((x/2)-200, y*4/10, 103, 32))
        if self.onePlayerRect.collidepoint(self.mouse):
            self.onePlayerText = font.render('1 Player', True, LB)
            self.p1c = True
        else:
            self.p1c = False
        screen.blit(self.onePlayerText, ((x/2)-200 , (y*4/10)))

        self.twoPlayersText = font.render('2 Players', True, WHITE)
        self.twoPlayersRect = pg.draw.rect(screen, BLACK, ((x/2)-200, y*5/10, 116, 32))
        if self.twoPlayersRect.collidepoint(self.mouse):
            self.twoPlayersText = font.render('2 Players', True, LB)
            self.p2c = True
        else:
            self.p2c = False
        screen.blit(self.twoPlayersText, ((x/2)-200, (y*5/10)))

        self.htpText = font.render('How to Play', True, WHITE)
        self.htpRect = pg.draw.rect(screen, BLACK, ((x/2)-200, y*6/10, 149, 32))
        if self.htpRect.collidepoint(self.mouse):
            self.htpText = font.render('How to Play', True, LB)
            self.htpc = True
        else:
            self.htpc = False
        screen.blit(self.htpText, ((x/2)-200, (y*6/10)))

        self.quitText = font.render('Quit', True, WHITE)
        self.quitRect = pg.draw.rect(screen, BLACK, ((x/2)-200, y*7/10, 53, 32))
        if self.quitRect.collidepoint(self.mouse):
            self.quitText = font.render('Quit', True, LB)
            self.quitc = True
        else:
            self.quitc = False
        screen.blit(self.quitText, ((x/2)-200, (y*7/10)))
        return

    def update(self):
        if  self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == K_t:
                    print(self.onePlayerRect, ' and ', self.twoPlayersRect, ' and ', self.htpRect, ' and ', self.quitRect)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.p1c == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(DifficultyScene())
                elif self.p2c == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene2(0))
                elif self.htpc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(HTPScene())
                elif self.quitc == True and pg.MOUSEBUTTONDOWN:
                    pg.quit()
                    break
        return

class HTPScene(Scene):
    def __init__(self):
        super(HTPScene, self).__init__()
        global score1, score2
        score1 = 0
        score2 = 0
        self.v = pg.mouse.set_visible(True)

    def render(self, screen):
        screen.fill(BLACK)

        self.titleText = bfont.render('How to Play', True, WHITE)
        self.titleRect = self.titleText.get_rect()
        screen.blit(self.titleText, ((x/2)-222, (y*1/20)+16))

        self.p1htp = font.render('1 Player:', True, WHITE)
        screen.blit(self.p1htp, (10, (y*3/10)))
        self.p1htp2 = sfont.render('Use the W or S keys to move your paddle up or down.', True, WHITE)
        screen.blit(self.p1htp2, (25, (y*3/10) + 35))
        self.p1htp3 = sfont.render('You can also use your mouse to control the paddle.', True, WHITE)
        screen.blit(self.p1htp3, (25, (y*3/10) + 60))

        
        self.p2htp = font.render('2 Players:', True, WHITE)
        screen.blit(self.p2htp, (10, (y*5/10)))
        self.p2htp2 = sfont.render('Player 1 uses the W and S keys to control his or her paddle.', True, WHITE)
        screen.blit(self.p2htp2, (25, (y*5/10) + 35))
        self.p2htp3 = sfont.render('Player 2 uses the Up and Down arrow keys to control his or her', True, WHITE)
        screen.blit(self.p2htp3, (25, (y*5/10) + 60))
        self.blah = sfont.render('paddle.', True, WHITE)
        screen.blit(self.blah, (25, (y*5/10) + 85))

        self.goback = sfont.render('Press Escape to return to the Title Screen', True, WHITE)
        screen.blit(self.goback, (0, (y - 25)))
        return
    
    def update(self):
        if  self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_t:
                 print(self.titleRect)
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                 self.manager.go_to(TitleScene())
        return

class PauseScene(Scene):
    def __init__(self):
        super(PauseScene, self).__init__()
        self.resumec = False
        self.htpc = False
        self.rtmc = False
        self.v = pg.mouse.set_visible(True)

    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pg.mouse.get_pos()

        self.titleText = bfont.render('Paused', True, WHITE)
        self.tt = self.titleText.get_rect()
        screen.blit(self.titleText, ((x/2)-133, (y*1/20)+16))
        
        self.resumeText = font.render('Resume', True, WHITE)
        self.rt = self.resumeText.get_rect()
        self.resumeRect = pg.draw.rect(screen, BLACK, ((x/2)-45, y*4/10, 99, 32))
        if self.resumeRect.collidepoint(self.mouse):
            self.resumeText = font.render('Resume', True, LB)
            self.resumec = True
        else:
            self.resumec = False
        screen.blit(self.resumeText, ((x/2)-45, (y*4/10)))

        self.htpText = font.render('How to Play', True, WHITE)
        self.ht = self.htpText.get_rect()
        self.htpRect = pg.draw.rect(screen, BLACK, ((x/2)-79, y*6/10, 148, 32))
        if self.htpRect.collidepoint(self.mouse):
            self.htpText = font.render('How to Play', True, LB)
            self.htpc = True
        else:
            self.htpc = False
        screen.blit(self.htpText, ((x/2)-79, (y*6/10)))

        self.rtmcText = font.render('Go back to Title', True, WHITE)
        self.rt2 = self.rtmcText.get_rect()
        self.rtmcRect = pg.draw.rect(screen, BLACK, ((x/2)-98.5, y*8/10, 197, 32))
        if self.rtmcRect.collidepoint(self.mouse):
            self.rtmcText = font.render('Go back to Title', True, LB)
            self.rtmc = True
        else:
            self.rtmc = False
        screen.blit(self.rtmcText, ((x/2)-98.5, (y*8/10)))
        return

    def update(self):
        if self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == K_t:
                    print(self.tt, ' and ', self.rt, ' and ', self.ht, ' and ', self.rt2)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.resumec == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                elif self.htpc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(HTPScene())
                elif self.rtmc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(TitleScene())
        return

class GameOverScene(Scene):
    def __init__(self):
        super(GameOverScene, self).__init__()
        global score1, score2
        score1 = 0
        score2 = 0
        self.pat = False
        self.rtmc = False
        self.v = pg.mouse.set_visible(True)

    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pg.mouse.get_pos()

        if p1W == True:
            self.winnerText = font.render('The Player Won', True, WHITE)
            self.wt = self.winnerText.get_rect()
            screen.blit(self.winnerText, ((x/2-98), (y*7/20)))
        elif p2W == True:
            self.winnerText = font.render('The Computer Won', True, WHITE)
            self.wt = self.winnerText.get_rect()
            screen.blit(self.winnerText, ((x/2-121.5), (y*7/20)))

        self.titleText = bfont.render('Game Over', True, WHITE)
        self.tt = self.titleText.get_rect()
        screen.blit(self.titleText, ((x/2-213), (y*1/20)+16))

        self.paText = font.render('Play Again', True, WHITE)
        self.pa = self.paText.get_rect()
        self.paRect = pg.draw.rect(screen, BLACK, ((x/2)-75, y*6/10, 130, 32))
        if self.paRect.collidepoint(self.mouse):
            self.paText = font.render('Play Again', True, LB)
            self.pat = True
        else:
            self.pat = False
        screen.blit(self.paText, ((x/2)-75, (y*6/10)))

        self.rtmcText = font.render('Go back to Title', True, WHITE)
        self.rt2 = self.rtmcText.get_rect()
        self.rtmcRect = pg.draw.rect(screen, BLACK, ((x/2)-98.5, y*8/10, 197, 32))
        if self.rtmcRect.collidepoint(self.mouse):
            self.rtmcText = font.render('Go back to Title', True, LB)
            self.rtmc = True
        else:
            self.rtmc = False
        screen.blit(self.rtmcText, ((x/2)-98.5, (y*8/10)))
        return

    def update(self):
        if self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == K_t:
                    print(self.tt, ' and ', self.wt, ' and ', self.pa, ' and ', self.rt2)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.pat == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                elif self.rtmc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(TitleScene())
        return

class GameOverScene2(Scene):
    def __init__(self):
        super(GameOverScene2, self).__init__()
        global score1, score2
        score1 = 0
        score2 = 0
        self.pat = False
        self.rtmc = False
        self.v = pg.mouse.set_visible(True)

    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pg.mouse.get_pos()

        self.winner = None
        if p1W == True:
            self.winner = 1
        elif p2W == True:
            self.winner = 2

        self.titleText = bfont.render('Game Over', True, WHITE)
        self.tt = self.titleText.get_rect()
        screen.blit(self.titleText, ((x/2-213), (y*1/20)+16))
        
        self.winnerText = font.render('Player %s Won' %(self.winner), True, WHITE)
        self.wt = self.winnerText.get_rect()
        screen.blit(self.winnerText, ((x/2-83), (y*7/20)))

        self.paText = font.render('Play Again', True, WHITE)
        self.pa = self.paText.get_rect()
        self.paRect = pg.draw.rect(screen, BLACK, ((x/2)-75, y*6/10, 130, 32))
        if self.paRect.collidepoint(self.mouse):
            self.paText = font.render('Play Again', True, LB)
            self.pat = True
        else:
            self.pat = False
        screen.blit(self.paText, ((x/2)-75, (y*6/10)))

        self.rtmcText = font.render('Go back to Title', True, WHITE)
        self.rt2 = self.rtmcText.get_rect()
        self.rtmcRect = pg.draw.rect(screen, BLACK, ((x/2)-98.5, y*8/10, 197, 32))
        if self.rtmcRect.collidepoint(self.mouse):
            self.rtmcText = font.render('Go back to Title', True, LB)
            self.rtmc = True
        else:
            self.rtmc = False
        screen.blit(self.rtmcText, ((x/2)-98.5, (y*8/10)))
        return

    def update(self):
        if self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == K_t:
                    print(self.tt, ' and ', self.wt, ' and ', self.pa, ' and ', self.rt2)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.pat == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene2(0))
                elif self.rtmc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(TitleScene())
        return

class DifficultyScene(Scene):
    def __init__(self):
        super(DifficultyScene, self).__init__()
        global score1, score2
        score1 = 0
        score2 = 0
        self.difficulty = 0
        self.d1r = False
        self.d2tt = False
        self.d3tt = False
        self.d4tt = False
        self.v = pg.mouse.set_visible(True)

    def render(self, screen):
        screen.fill(BLACK)
        self.mouse = pg.mouse.get_pos()

        self.difText = dfont.render('Select a Difficulty', True, WHITE)
        self.difT = self.difText.get_rect()
        screen.blit(self.difText, ((x/2-287), (y*1/20)+16))
        
        self.d1Text = font.render('Easy', True, WHITE)
        self.d1T = self.d1Text.get_rect()
        self.d1R = pg.draw.rect(screen, BLACK, ((x/2)-29.5, y*4/10, 59, 32))
        if self.d1R.collidepoint(self.mouse):
            self.d1Text = font.render('Easy', True, LB)
            self.d1r = True
        else:
            self.d1r = False
        screen.blit(self.d1Text, ((x/2)-29.5, (y*4/10)))

        self.d2Text = font.render('Normal', True, WHITE)
        self.d2T = self.d2Text.get_rect()
        self.d2R = pg.draw.rect(screen, BLACK, ((x/2)-45.5, y*5/10, 91, 32))
        if self.d2R.collidepoint(self.mouse):
            self.d2Text = font.render('Normal', True, LB)
            self.d2tt = True
        else:
            self.d2tt = False
        screen.blit(self.d2Text, ((x/2)-45.5, (y*5/10)))

        self.d3Text = font.render('Hard', True, WHITE)
        self.d3T = self.d3Text.get_rect()
        self.d3R = pg.draw.rect(screen, BLACK, ((x/2)-30.5, y*6/10, 61, 32))
        if self.d3R.collidepoint(self.mouse):
            self.d3Text = font.render('Hard', True, LB)
            self.d3tt = True
        else:
            self.d3tt = False
        screen.blit(self.d3Text, ((x/2)-30.5, (y*6/10)))

        self.d4Text = font.render('Impossible', True, WHITE)
        self.d4T = self.d4Text.get_rect()
        self.d4R = pg.draw.rect(screen, BLACK, ((x/2)-68.5, y*7/10, 137, 32))
        if self.d4R.collidepoint(self.mouse):
            self.d4Text = font.render('Impossible', True, LB)
            self.d4tt = True
        else:
            self.d4tt = False
        screen.blit(self.d4Text, ((x/2)-68.5, (y*7/10)))


        self.rtmcText = font.render('Go back to Title', True, WHITE)
        self.rt2 = self.rtmcText.get_rect()
        self.rtmcRect = pg.draw.rect(screen, BLACK, ((x/2)-98.5, y*8/10, 197, 32))
        if self.rtmcRect.collidepoint(self.mouse):
            self.rtmcText = font.render('Go back to Title', True, LB)
            self.rtmc = True
        else:
            self.rtmc = False
        screen.blit(self.rtmcText, ((x/2)-98.5, (y*8/10)))
        return

    def update(self):
        if self.v == False:
             pg.mouse.set_visible(True)
        return

    def handle_events(self, events):
        global d, speed
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == K_t:
                    print(self.difT, ' and ', self.d1T, ' and ', self.d2T, ' and ', self.d3T, ' and ', self.d4T, ' and ', self.rt2)
            elif e.type == pg.MOUSEBUTTONDOWN:
                if self.d1r == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                    speed = [5,5]
                    d = 3
                elif self.d2tt == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                    speed = [5,5]
                    d = 4
                elif self.d3tt == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                    speed = [6,6]
                    d = 5.53
                elif self.d4tt == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(GameScene(0))
                    speed = [7,7]
                    d = 6.8
                elif self.rtmc == True and pg.MOUSEBUTTONDOWN:
                    self.manager.go_to(TitleScene())
        return

class SceneManager():
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class Paddle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([w, h])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pg.sprite.Sprite):
    def __init__(self, px, py, speed, image="circle.png"):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (15, 15))
        self.speed = speed
        self.rect = self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def update_score1():
    global score1
    if score1 != 10:
        score1 += 1
    print(score1)
    
def update_score2():
    global score2
    if score2 != 10:
        score2 += 1
    print(score2)
    
def main():
    global font, bfont, sfont, screen, speed, p1W, p2W, d, dfont, score1, score2
    pg.init()
    screen = pg.display.set_mode((x, y))
    pg.display.set_caption("Pong")
    FPS = pg.time.Clock()
    sfont = pg.font.SysFont("Verdana", 18)
    font = pg.font.SysFont("Verdana", 25)
    bfont = pg.font.SysFont("Verdana", 75)
    dfont = pg.font.SysFont("Verdana", 65)
    running = True
    speed = [5,5]
    p1W = False
    p2W = False
    score1 = 0
    score2 = 0
    d = 0

    manager = SceneManager()

    while running:
        FPS.tick(60)
        if pg.event.get(QUIT):
            running = False
            pg.quit()
            return

        manager.scene.handle_events(pg.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pg.display.flip()
if __name__ == '__main__':
    main()
