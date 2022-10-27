from cgi import print_directory
import pygame as pg
from settings import HITBOX_OFFSET, CONTROLKEYS
from support import import_folder

class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        self.image = pg.image.load('../graphs/playerdefault/0.png')
        
        self.rect = self.image.get_rect(topleft=pos)
        
        self.hitbox = self.rect.inflate(HITBOX_OFFSET['playerY'], HITBOX_OFFSET['playerX'])
        
        self.direction = pg.math.Vector2() 
        
        self.speed = 20 # velocidade do player
        
        self.attackspeed = 1
        
        self.status = 'down'
        
        self.attacktime= 0
        
        self.obstacle_sprites = obstacle_sprites
        
        self.isanimated = False
        #importanto as animações
        self.import_player_assets()

    def import_player_assets(self):
        assets_path = '../graphs/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'left_idle': [], 'right_idle': [
        ], 'up_idle': [], 'down_idle': [], 'left_attack': [], 'right_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = assets_path + animation
            self.animations[animation] = import_folder(full_path)
            
        
    def input(self):
        
        keys = pg.key.get_pressed()
        
        if keys[CONTROLKEYS['up']]:
            self.direction.y = -1
            self.status = 'up'
            self.image = pg.image.load('../graphs/player/up/up_0.png')
            
        elif keys[CONTROLKEYS['down']]:
            self.direction.y = 1
            self.status = 'down'
            self.image = pg.image.load('../graphs/player/down/down_0.png')
            
        else:
            self.direction.y = 0
            
        if keys[CONTROLKEYS['right']]:
            self.direction.x = 1
            self.status = 'right'
            self.image = pg.image.load('../graphs/player/right/right_0.png')
            
        elif keys[CONTROLKEYS['left']]:
            self.direction.x = -1
            self.status = 'left'
            self.image = pg.image.load('../graphs/player/left/left_0.png')
            
        else:
            self.direction.x = 0
        if keys[CONTROLKEYS['attack']] and int(pg.time.get_ticks()) - self.attacktime >= (1000/self.attackspeed):
                print('atacou')
                self.attacktime = pg.time.get_ticks()
        if keys[CONTROLKEYS['magic']]:
            #imagino q vamos usar mais de um spell entao tem q chegar na conclusao de como q vai funcionar para calcular o cd
            print('magica')
            pass
        if keys[CONTROLKEYS['interact']]:
            print('interagiu')
        if keys[CONTROLKEYS['inventory']]:
            print('inventario')
    
    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y == 0 and not 'idle' in self.status:
            self.status = self.status + '_idle'
            
        
    
    
    def move(self,speed): 
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        
        self.collision('horizontal')
        
        self.hitbox.y += self.direction.y * speed
        
        self.collision('vertical')
        
        self.rect.center = self.hitbox.center
        
    def collision(self,direction):
        
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: 
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: 
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom        
        
    def playertp(self):
        
        keys = pg.key.get_pressed()
        
        if keys[pg.K_F2]: #Não vamos definir no settings porque é só debug
            print('tp')
            X = int(input('X:'))
            Y = int(input('Y:'))
            self.hitbox.x = X
            self.hitbox.y = Y
            
            
    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
        #self.playertp()