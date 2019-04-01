'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Katie Chiu
Asteroids
Version 1.0
Last updated 27 March 2019
Shoot as many asteroids as you can with 3 lives. Each asteroid is 100 points. Each asteroid not hit is -100 points. Each potion that passes by is an extra life. Use arrows to move left and right. Use spacebar to shoot lasers.
'''
import pygame, random, time,sys

pygame.init()
pygame.font.init()

window_width = 1000
window_height = 504
screen = pygame.display.set_mode((window_width, window_height))

global points, speed, shipy, total, scores, x, done, need, begin,lifecount
begin = 0
need = 150
scores = []
points = 0
speed = 2
entity_color = (255, 64, 64)
lives = 3
total = 0
count = 0
lifecount=0
x = 0
done = False


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Player(Entity):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)
        self.ship = pygame.image.load('spaceship.png')
        self.image = pygame.transform.scale(self.ship, (175, 70))

        # How many pixels the Player spaceship should move on a given frame.
        self.y_change = 0
        self.move=window_height/2
        # How many pixels the spaceship should move each frame a key is pressed.

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change = -4
        elif (key == pygame.K_DOWN):
            self.y_change = 4

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change =0
        elif (key == pygame.K_DOWN):
            self.y_change =0

    def update(self):
        self.rect.move_ip(0, self.y_change)

        # If the spaceship moves off the screen, put it back on.
        if self.rect.y<0:
            self.rect.y = 0
        elif self.rect.y>424:
            self.rect.y = 424
        # Moves it relative to its current location.

class Laser(Entity):

    def __init__(self, x, y, width, height):
        super(Laser, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 1
        self.y_direction = 0
        self.speed = 6

    def update(self):
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)


class Asteroid(Entity):
    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)
        self.asteroid = pygame.image.load("asteroid2.png")
        self.image = pygame.transform.scale(self.asteroid, (80, 69))
        self.y_direction = 0

    def update(self):
        global speed, done
        if done == False:
            self.x_direction = -1
        self.rect.move_ip(speed * self.x_direction, speed * self.y_direction)

class Potion(Entity):
    def __init__(self, x, y, width, height):
        super(Potion, self).__init__(x, y, width, height)
        self.potion = pygame.image.load("potion.png")
        self.image = pygame.transform.scale(self.potion, (80, 69))
        self.y_direction = 0
    def update(self):
        global speed, done
        if done == False:
            self.x_direction = -1
        self.rect.move_ip(speed * self.x_direction, speed * self.y_direction)

def objcollide(astlist, laslist):
    global points, need
    for asteroid in astlist:
        for laser in laslist:
            if asteroid.rect.colliderect(laser.rect):
                asteroid.remove(all_sprites_list)
                astlist.remove(asteroid)
                laser.remove(all_sprites_list)
                laslist.remove(laser)
                points = points + 100
                if need > 25:
                    need = need - 1


def collision(astlist):
    global lives
    for asteroid in astlist:
        if player.rect.colliderect(asteroid.rect):
            asteroid.remove(all_sprites_list)
            astlist.remove(asteroid)
            lives = lives - 1
            if lives != 0:
                soundObj2.play()

def collide2(potionlist):
    global lives
    for potion in potionlist:
        if player.rect.colliderect(potion.rect):
            potion.remove(all_sprites_list)
            potionlist.remove(potion)
            lives=lives+1

def restart(astlist, laslist, all_sprites_list):
    global points, total, x, done, lives,need,shipy,begin
    total = 0
    begin=0
    need = 150
    shipy=window_height/2
    points = 0
    x = 0
    lives = 3
    done = False
    for asteroid in astlist:
        asteroid.remove(all_sprites_list)
    for laser in laslist:
        laser.remove(all_sprites_list)
    astlist = []
    laslist = []
    potionlist=[]
    all_sprites_list = []
    change = random.randrange(0, 350)
    player = Player(-5, shipy, 175, 75)
    laser = Laser(160, player.rect.y + 40, 20, 3)
    asteroid = Asteroid(1010, change, 70, 60)
    potion = Potion(1010, change, 70, 60)
    potionlist.append(potion)
    time.sleep(1)
    astlist.append(asteroid)
    laslist.append(laser)
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(player)

pygame.display.set_caption("Asteroid Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background = Background('space2.png', [0, 0])
shipy = window_height / 2
astlist = []
laslist = []
potionlist=[]
change = random.randrange(0, 350)
soundObj = pygame.mixer.Sound("lasersound.wav")
soundObj2 = pygame.mixer.Sound("crash.wav")
lose = pygame.mixer.Sound("fail.wav")
music = pygame.mixer.music.load("spacesound.wav")
font = pygame.font.SysFont('arial', 18)
bigfont = pygame.font.SysFont('arial', 24)
titlefont = pygame.font.SysFont('arial', 40)

pygame.mixer.music.play(-1, 0.0)

spaceship = pygame.image.load("spaceship.png")

player = Player(-5, shipy, 160, 75)
laser = Laser(160, player.rect.y + 40, 20, 3)
asteroid = Asteroid(1010, change, 70, 60)
potion = Potion(1010, change, 70, 60)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.stop()
                pygame.quit()
                sys.exit()
    # Event processing here
    count = count + 1
    lifecount=lifecount+1
    if begin == 0:
        title = titlefont.render(str("ASTEROIDS GAME"), True, WHITE)
        titlerect = title.get_rect()
        titlerect.center = (505, 50)
        start = bigfont.render("Press S to Start", True, WHITE)
        startrect = start.get_rect()
        startrect.center = (500, 125)
        how = bigfont.render("Press I for Instructions", True, WHITE)
        howrect = how.get_rect()
        howrect.center = (500, 175)
        
        screen.fill(BLACK)
        screen.blit(title, titlerect)
        screen.blit(start, startrect)
        screen.blit(how, howrect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                begin = 3
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                begin = 2


    if begin == 2:
        textsurface = bigfont.render(str("INSTRUCTIONS"), True, WHITE)
        textrect = textsurface.get_rect()
        textrect.center = (500, 50)
        instruct1=font.render(str("Shoot as many asteroids as you can with 3 lives."),True,WHITE)
        instruct2=font.render(str("Each asteroid is 100 points. Each asteroid not hit is -100 points."),True,WHITE)
        instruct3=font.render(str("Each potion that your spaceship touches is an extra life."),True,WHITE)
        instruct4=font.render(str("Use arrows to move left and right. Use spacebar to shoot lasers."),True,WHITE)
        instruct5=font.render(str("PRESS H TO RETURN TO HOME SCREEN"),True,WHITE)

        instructbox1=instruct1.get_rect()
        instructbox2=instruct2.get_rect()
        instructbox3=instruct3.get_rect()
        instructbox4=instruct4.get_rect()
        instructbox5=instruct5.get_rect()
        instructbox1.center=(500,100)
        instructbox2.center=(500,125)
        instructbox3.center=(500,150)
        instructbox4.center=(500,200)
        instructbox5.center=(500,250)
        screen.fill(BLACK)
        screen.blit(textsurface, textrect)
        screen.blit(instruct1,instructbox1)
        screen.blit(instruct2,instructbox2)
        screen.blit(instruct3,instructbox3)
        screen.blit(instruct4,instructbox4)
        screen.blit(instruct5,instructbox5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_h:
                done = False
                begin = 0
                
    if begin == 3:
        if done == False:
            if count >= need:
                change = random.randrange(0, 350)
                asteroid = Asteroid(1010, change, 70, 60)
                astlist.append(asteroid)
                all_sprites_list.add(asteroid)
                count = 0
            if lifecount>=2000:
                change=random.randrange(0,350)
                potion=Potion(1010,change,70,60)
                potionlist.append(potion)
                lifecount=0
                all_sprites_list.add(potion)

            objcollide(astlist, laslist)
            collision(astlist)
            collide2(potionlist)

            for ent in all_sprites_list:
                ent.update()

            for asteroid in astlist:
                if asteroid.rect.x <= -100:
                    asteroid.remove(all_sprites_list)
                    astlist.remove(asteroid)
                    points = points - 100
            for laser in laslist:
                if laser.rect.x > 1000:
                    laser.remove(all_sprites_list)
                    laslist.remove(laser)
                    
            screen.blit(background.image, background.rect)

            all_sprites_list.draw(screen)

            textSurfaceObj = font.render(str("Points: " + str(points)), True, WHITE)  # text
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (60, 15)  # places text
            screen.blit(textSurfaceObj, textRectObj)

            textSurfaceObj2 = font.render(str("Lives: " + str(lives)), True, WHITE)  # text
            textRectObj2 = textSurfaceObj.get_rect()
            textRectObj2.center = (60, 40)  # places text
            screen.blit(textSurfaceObj2, textRectObj2)

            if lives == 0:
                done = True
                lose.play()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if lives > 0:
                        laser = Laser(160, player.rect.y + 40, 20, 3)
                        laslist.append(laser)
                        all_sprites_list.add(laser)
                        soundObj.play()
                elif event.type == pygame.KEYDOWN:
                    player.MoveKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    player.MoveKeyUp(event.key)

    while done:
        screen.fill(BLACK)
        total = points
        score = font.render(str("Points: " + str(points)), True, WHITE)
        scorerect = score.get_rect()
        scorerect.center = (500, 25)
        screen.blit(score, scorerect)
        textsurface = font.render(str("You are out of lives!"), True, WHITE)
        textrect = textsurface.get_rect()
        textrect.center = (500, 50)
        screen.blit(textsurface, textrect)

        file = open("asteroidscore.txt", "r")
        y = file.readline()
        scores = []
        while y:
            if int(points) > int(y) and x == 0:
                scores.append(points)
                scores.append("\n")
                x = 1
                y = file.readline()
            else:
                scores.append(y)
                y = file.readline()
        file.close()
        files = open("asteroidscore.txt", "w")
        for z in scores:
            files.write(str(z))
        files.close()

        if x == 1:
            new = font.render(str("NEW HIGHSCORE!"), True, WHITE)
            newbox = new.get_rect()
            newbox.center = (500, 75)
            screen.blit(new, newbox)
        file = open("asteroidscore.txt", "r")
        label = "HIGHSCORES"
        line = file.readlines()
        leave = "PRESS H TO RETURN TO HOME SCREEN"
        file.close()
        positions = [(500, 150), (500, 175), (500, 200), (500, 225), (500, 250), (500, 275),
                     (500, 300), (500, 325), (500, 350), (500, 375), (500, 425)]

        textsurface1 = font.render(label, True, WHITE)
        textrect1 = textsurface1.get_rect()
        textrect1.center = (500, 125)

        line = [SCORE.replace('\n', '') for SCORE in line]

        textsurface2 = font.render(str("1. " + line[0]), True, WHITE)
        textrect2 = textsurface2.get_rect()
        textrect2.center = positions[0]

        textsurface3 = font.render(str("2. " + line[1]), True, WHITE)
        textrect3 = textsurface3.get_rect()
        textrect3.center = positions[1]

        textsurface4 = font.render(str("3. " + line[2]), True, WHITE)
        textrect4 = textsurface4.get_rect()
        textrect4.center = positions[2]

        textsurface5 = font.render(str("4. " + line[3]), True, WHITE)
        textrect5 = textsurface5.get_rect()
        textrect5.center = positions[3]

        textsurface6 = font.render(str("5. " + line[4]), True, WHITE)
        textrect6 = textsurface6.get_rect()
        textrect6.center = positions[4]

        textsurface7 = font.render(str("6. " + line[5]), True, WHITE)
        textrect7 = textsurface7.get_rect()
        textrect7.center = positions[5]

        textsurface8 = font.render(str("7. " + line[6]), True, WHITE)
        textrect8 = textsurface8.get_rect()
        textrect8.center = positions[6]

        textsurface9 = font.render(str("8. " + line[7]), True, WHITE)
        textrect9 = textsurface9.get_rect()
        textrect9.center = positions[7]

        textsurface10 = font.render(str("9. " + line[8]), True, WHITE)
        textrect10 = textsurface10.get_rect()
        textrect10.center = positions[8]

        textsurface11 = font.render(str("10. " + line[9]), True, WHITE)
        textrect11 = textsurface11.get_rect()
        textrect11.center = positions[9]

        textsurface12 = font.render(leave, True, WHITE)
        textrect12 = textsurface12.get_rect()
        textrect12.center = positions[10]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h and lives <= 0:
                done = False
                begin = 0
                restart(astlist, laslist, all_sprites_list)

        screen.blit(textsurface1, textrect1)
        screen.blit(textsurface2, textrect2)
        screen.blit(textsurface3, textrect3)
        screen.blit(textsurface4, textrect4)
        screen.blit(textsurface5, textrect5)
        screen.blit(textsurface6, textrect6)
        screen.blit(textsurface7, textrect7)
        screen.blit(textsurface8, textrect8)
        screen.blit(textsurface9, textrect9)
        screen.blit(textsurface10, textrect10)
        screen.blit(textsurface11, textrect11)
        screen.blit(textsurface12, textrect12)
        pygame.display.flip()

    pygame.display.flip()
