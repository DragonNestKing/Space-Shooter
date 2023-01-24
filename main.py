import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups) # 1. we have to init the parent class

        self.image = pygame.image.load("./Space-Shooter/graphics/ship.png").convert_alpha() #2 We need a surface -> image

        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) # 3 We need a rect

        self.mask = pygame.mask.from_surface(self.image)
    
        # timer
        self.can_shoot = True
        self.shoot_time = None

        #sound
        self.laser_sound = pygame.mixer.Sound("./Space-Shooter/sounds/laser.ogg")

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 100:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):

        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Laser(self.rect.midtop, laser_group)
            self.laser_sound.play()

        
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.input_position()
        self.laser_shoot()
        self.laser_timer()

        self.meteor_collision()

# exercise
#Create a laser sprite
#Create a new clasee + a new group
# when the laser object is created you should be able to set it's position
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load("./Space-Shooter/graphics/laser.png").convert_alpha()

        self.rect = self.image.get_rect(midbottom = pos)

        self.mask = pygame.mask.from_surface(self.image)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()

    def update(self):
        #self.rect.y -= 1
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()
        self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("./Space-Shooter/graphics/meteor_new.png").convert_alpha()

        self.rect = self.image.get_rect(center = pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)
        
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()

class Score:
    def __init__(self):
        self.font = pygame.font.Font("./Space-Shooter/graphics/subatomic.ttf", 50)

    def display(self):

        score_text = f"Score:  {pygame.time.get_ticks() // 1000}"
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            display_surface,
            (255, 255, 255),
            text_rect.inflate(30,30),
            width = 8,
            border_radius = 5
        )

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load("./Space-Shooter/graphics/background_new.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)

# timer

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

score = Score()


# main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == meteor_timer:
            meteor_y_pos = randint(-150, -50)
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Meteor((meteor_x_pos, meteor_y_pos), groups = meteor_group)

    # delta time
    dt = clock.tick() / 1000

    # background
    display_surface.blit(background_surf, (0,0))

    #Update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    #score
    score.display()

    #graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    pygame.display.update()