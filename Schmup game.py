##---------------##
#) Scump         (#
#) Aiden Delaine (#
#) jan, 7/2026   (#
##---------------##


########### import ##########
import pygame
import random
from os import path

########### Setup ##########

# define file locations
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# define dementions and fps
WIDTH = 600
HEIGHT = 650
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scump!")
clock = pygame.time.Clock()

########## Functions ##########
# score
def score():
    global score
    score = 0


# draw text
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# spawn mob
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
# sheild bar
def draw_sheild_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 4)

########### Classes ##########
    
# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (46, 41))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.sheild = 100
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -10
        if keystate[pygame.K_d]:
            self.speedx = 10
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        
# mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        #pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3,15)
        self.speedx = random.randrange(-5, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
        
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
      
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
        
# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

########## import 2 ##########

# load all graphics
background = pygame.image.load(path.join(img_dir, "space.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playership.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "playerbullet.png")).convert()
meteor_images = []
meteor_list = ["bml.png", "bmm.png", "bmt.png", "gml.png", "gmm.png",
               "gmt.png"]
for img in meteor_list:
     meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
pygame.display.set_icon(player_img)
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['ma'] = []
for i in range (9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100, 100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (50, 50))
    explosion_anim['sm'].append(img_sm)
    img_ma = pygame.transform.scale(img, (200, 200))
    explosion_anim['ma'].append(img_ma)

# load all sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Boom.wav'))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'space scump.mp3'))
pygame.mixer.music.set_volume(1)


########## game ##########

# set sprite groups
all_sprites = pygame.sprite.Group()
player = Player()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)
for i in range(8):
        newmob()
score()

pygame.mixer.music.play(loops=-1)

# Game loop
running = True
while running:
    clock.tick(FPS)
    #player.shoot()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    
    
    # check for colliosions bullet <> mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 55 - hit.radius
        explosion_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
    
    # check for colliosions player <> mob
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.sheild -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.sheild <= 0:
            death_expl = Explosion(player.rect.center, 'ma')
            all_sprites.add(death_expl)
            player.kill()
            for i in range(45):
                Clock.tick(FPS)
                FPS =+ 1
                all_sprites.update()
                screen.fill(BLACK)
                screen.blit(background, background_rect)
                all_sprites.draw(screen)
                
                
    
    # if the player is dead and explosion is finish
    if not player.alive() and not death_expl.alive():
        running = False
            

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2 , 10)
    draw_sheild_bar(screen, 5, 5, player.sheild)
    pygame.display.flip()
  
# exit slip
print(score)
pygame.quit()