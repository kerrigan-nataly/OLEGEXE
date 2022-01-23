import pygame
from random import randint


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, sheet, columns, rows, x, y):
        super().__init__(group)
        
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.collide_frame = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.alive:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        
class Charecter:
    def __init__(self, game):
        self.game = game
        self.loc = game.locations[1]
        self.animations = {}
        self.icon = 0
        
        # КООРИДНАТЫ
        self.x = 0
        self.y = 0
        self.h = 0
        self.coords = (self.x, self.y - self.h)

        # ХАРАКТЕРИСТИКИ ПЕРСОНАЖА
        self.alive = True
        self.health = 100
        self.speed = 10
        self.damage = 10
        
        self.health_bar_coord = 150

        self.death_screen = 'fail'

    def show_health(self, screen):
        screen.blit(self.loc.icon, (50, self.health_bar_coord - 5))
        screen.blit(self.icon, (20, self.health_bar_coord - 5))
        pygame.draw.rect(screen, (10, 255, 5), (80, self.health_bar_coord, self.health, 10))
        pygame.draw.rect(screen, (255, 255, 255), (80, self.health_bar_coord, 100, 10), 1)
        
    def set_coords(self, x, y):
        self.x= x
        self.y = y
        self.coords = (self.x, self.y - self.h)

    def update(self):
        self.current_anim.update()

    def move(self, axle, direction):
        fps = self.game.fps
        game = self.game
        
        vx = vy = 0
        if axle == 'y':
            if direction == '-':
                if game.current_location.y < self.y - (self.speed / fps) < game.current_location.h:
                    vy = -self.speed
                self.current_anim = self.animations['go_up']
                self.current_state = self.animations['stand_up']
                
            elif direction == '+':
                if game.current_location.y < self.y + (self.speed / fps) < game.current_location.h:
                    vy = self.speed
                self.current_anim = self.animations['go_down']
                self.current_state = self.animations['stand_down']
                
        elif axle == 'x':
            if direction == '-':
                if game.current_location.x < self.x - self.speed / fps < game.current_location.w:
                    vx = -self.speed
                self.current_anim = self.animations['go_left']
                self.current_state = self.animations['stand_left']
                
            elif direction == '+':
                if game.current_location.x < self.x + self.speed / fps < game.current_location.w:
                    vx = self.speed
                self.current_anim = self.animations['go_right']
                self.current_state = self.animations['stand_right']
                

        self.set_coords(self.x + round(vx / fps, 0), self.y + round(vy / fps, 0))

        if self.x > self.game.current_location.w - 2:
            e = pygame.event.Event(self.game.LOCATION_CHANGE_CODE, direction=1)
            pygame.event.post(e)
            
        if self.x < self.game.current_location.x + 2:
            e = pygame.event.Event(self.game.LOCATION_CHANGE_CODE, direction=-1)
            pygame.event.post(e)
        

    def hit(self, damage):
        self.health -= damage
        print(self, 'потерял 10 здоровья')
        if self.health <= 0:
            self.game.in_game = False
            self.game.current_screen = self.game.state_screens[self.death_screen]
            print(self, 'УМЕР!')

    def attack(self, char):
        #print('x', self.x - self.attack_radius, char.x, self.x + self.attack_radius)
        #print('y', self.y - self.attack_radius, char.y, self.y + self.attack_radius)
        if self.loc == char.loc and \
           self.x - self.attack_radius < char.x < self.x + self.attack_radius and \
           self.y - self.attack_radius - self.h < char.y < self.y + self.attack_radius - self.h:
            
            char.hit(self.damage)

            
class Player(Charecter):
    def __init__(self, game, group):
        super().__init__(game)

        self.loc = game.locations[-1]
        
        self.animations['go_left'] = Sprite(group, pygame.image.load('player_/go_left.png'), 2, 1, self.x, self.y)
        self.animations['go_right'] = Sprite(group, pygame.image.load('player_/go_right.png'), 2, 1, self.x, self.y)
        self.animations['go_down'] = Sprite(group, pygame.image.load('player_/go_down.png'), 2, 1, self.x, self.y)
        self.animations['go_up'] = Sprite(group, pygame.image.load('player_/go_up.png'), 2, 1, self.x, self.y)
        self.animations['stand_left'] = Sprite(group, pygame.image.load('player_/stand_left.png'), 1, 1, self.x, self.y)
        self.animations['stand_right'] = Sprite(group, pygame.image.load('player_/stand_right.png'), 1, 1, self.x, self.y)
        self.animations['stand_up'] = Sprite(group, pygame.image.load('player_/stand_up.png'), 1, 1, self.x, self.y)
        self.animations['stand_down'] = Sprite(group, pygame.image.load('player_/stand_down.png'), 1, 1, self.x, self.y)
        self.animations['hit_right'] = Sprite(group, pygame.image.load('player_/hit_right.png'), 1, 1, self.x, self.y)
        self.animations['hit_left'] = Sprite(group, pygame.image.load('player_/hit_left.png'), 1, 1, self.x, self.y)

        self.current_anim = self.animations['go_left']
        self.current_state = self.animations['stand_left']

        self.icon = pygame.image.load('icons_/player.png')

        self.speed = 80
        self.attack_radius = 30
        self.damage = 5
        self.h = 40

        self.health_bar_coord = 500

    def go(self, time, keys):
        if keys[pygame.K_UP]:
            self.move('y', '-')
            
        elif keys[pygame.K_DOWN]:
            self.move('y', '+')
            
        if keys[pygame.K_LEFT]:
            self.move('x', '-')
            
        elif keys[pygame.K_RIGHT]:
            self.move('x', '+')

        if not any((keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT])):
            
            self.current_anim = self.current_state

    def call(self, owner, loc):
        if owner.speed > 0:
            owner.speed -= 5

        if owner.loc != loc:
            owner.loc.remove_char(owner)
            loc.add_char(owner)
            owner.set_coords(*loc.start_coords)
  
        owner.owner_place = int(self.x), int(self.y)


class Owner(Charecter):
    def __init__(self, game, group):
        super().__init__(game)

        self.h = 135
        
        self.animations['go_left'] = Sprite(group, pygame.image.load('owner_/left.png'), 1, 1, self.x, self.y)
        self.animations['go_right'] = Sprite(group, pygame.image.load('owner_/right.png'), 1, 1, self.x, self.y)
        self.animations['go_down'] = Sprite(group, pygame.image.load('owner_/down.png'), 1, 1, self.x, self.y)
        self.animations['go_up'] = Sprite(group, pygame.image.load('owner_/up.png'), 1, 1, self.x, self.y)
        self.animations['stand_left'] = Sprite(group, pygame.image.load('owner_/left.png'), 1, 1, self.x, self.y)
        self.animations['stand_right'] = Sprite(group, pygame.image.load('owner_/right.png'), 1, 1, self.x, self.y)
        self.animations['stand_up'] = Sprite(group, pygame.image.load('owner_/down.png'), 1, 1, self.x, self.y)
        self.animations['stand_down'] = Sprite(group, pygame.image.load('owner_/up.png'), 1, 1, self.x, self.y)
        
        self.current_anim = self.animations['stand_left']

        self.icon = pygame.image.load('icons_/owner.png')

        self.speed = 100    
        self.owner_place = self.coords

        self.health_bar_coord = 520

    def go(self, time, keys):
        x, y = self.owner_place
        axle = ''
        direction = ''
        
        if self.x not in range(x - 5, x + 5):
            axle = 'x'
            if self.x > x:
                direction = '-'
            else:
                direction = '+'
        self.move(axle, direction)
            
        if self.y not in range(y - 5, y + 5):
            axle = 'y'  
            if self.y > y:
                direction = '-'
            else:
                direction = '+'
        self.move(axle, direction)


class Oleg(Charecter):
    def __init__(self, game, group):
        super().__init__(game)
        
        self.animations['stand_right'] = Sprite(group, pygame.image.load('oleg_/stand_right.png'), 3, 1, self.x, self.y)
        self.animations['hit'] = Sprite(group, pygame.image.load('oleg_/hit.png'), 1, 1, self.x, self.y)

        self.current_anim = self.animations['stand_right']
        self.icon = pygame.image.load('icons_/oleg.png')

        self.attack_radius = 60
        self.speed = 20
        self.chance_teleport = 2

        self.health_bar_coord = 540

        self.death_screen = 'win'

    def go(self, time, keys, to_owner=True):
        if time % 100 == 0:
            
            game = self.game
            
            tp = 1 == randint(0, self.chance_teleport)
            
            if not tp or not to_owner:
                w, h = game.current_location.x + game.current_location.w, game.current_location.y + game.current_location.y
                rad = self.attack_radius * 2
                if to_owner:
                    x, y = game.owner.x, game.owner.y  
                else:
                    x, y = game.current_location.w - game.owner.x, game.current_location.h - game.owner.y
                
                new_x, new_y = (randint(x - rad, x + rad), randint(y - rad, y + rad))
        
                new_x = max((0, min((new_x, w))))
                new_y = max((0, min((new_y, y))))
                            
                self.set_coords(new_x, new_y)
            else:
                new = randint(0, len(self.game.locations) - 1)
                self.loc.remove_char(self)
                self.game.locations[new].add_char(self)
            
    def hit(self, damage):
        super().hit(damage)
        self.current_anim = self.animations['hit']
        self.go(100, [], to_owner=False)





