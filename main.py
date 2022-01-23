import pygame

import location

import charecter
# Player 
# Yebaka
# Owner
# Потом поменяем


class Game:
    def __init__(self, fps, in_game):
        self.all_sprites = pygame.sprite.Group()
        self.fps = fps
        self.in_game = in_game

        # Пытаюс
        self.LOCATION_CHANGE_CODE = pygame.USEREVENT + 1
        self.LOCATION_CHANGE = pygame.event.Event(self.LOCATION_CHANGE_CODE, direction=1)
        
        # Заставки??
        self.state_screens = {'first': pygame.image.load('screens_/first.png'),
                              'win': pygame.image.load('screens_/win.png'),
                              'fail': pygame.image.load('screens_/fail.png')}
        self.current_screen = self.state_screens['first']

        # Локация
        self.locations = [location.Location(pygame.image.load('icons_/bathroom.png'), pygame.image.load('locations_/bathroom.png'), 370, 300, 120, 150),
                          location.Location(pygame.image.load('icons_/room.png'), pygame.image.load('locations_/room.png'), 400, 400, 60, 230),
                          location.Location(pygame.image.load('icons_/kitchen.png'), pygame.image.load('locations_/kitchen.png'), 400, 370, 60, 230),
                          location.Location(pygame.image.load('icons_/start.png'), pygame.image.load('locations_/start.png'), 370, 400, 60, 200)]
        
        self.current_location = self.locations[-1]
        
        self.location_num = 0

    def new_game(self):
        for loc in self.locations:
            loc.set_char([])
            
        self.player = charecter.Player(self, self.all_sprites) # игрок
        self.oleg = charecter.Oleg(self, self.all_sprites) # ебака
        self.owner = charecter.Owner(self, self.all_sprites)   # хозяйка

        self.chars = [self.owner, self.oleg, self.player]

        self.player.set_coords(self.current_location.x + 10, self.current_location.y + 10)
        self.oleg.set_coords(self.current_location.x + 30, self.current_location.y + 30)
        self.owner.set_coords(self.current_location.x + 70, self.current_location.y + 70)

        self.locations[1].set_char([self.oleg, self.owner])
        self.current_location.add_char(self.player)
        
        self.owner.owner_place = self.owner.loc.start_coords
        

    def render(self, screen):
        self.current_location.chars.sort(key= lambda x: x.y)
        if self.in_game:
            self.current_location.render(screen)
            for char in self.current_location.chars:
                screen.blit(char.current_anim.image, char.coords)
            for char in self.chars:
                char.show_health(screen)
        else:
            screen.blit(self.current_screen, (0, 0))


if __name__ == '__main__':
    pygame.init()
    
    size = width, height = 500, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('OLEGEXE')

    all_sprites = pygame.sprite.Group()
    FPS = 30
    GAME = Game(FPS, False)

    clock = pygame.time.Clock()
    time = 0
    
    running = True
    
    
    while running:
        if GAME.in_game:
            ### КАДР
            if time % 5 == 0:
                for char in GAME.current_location.chars:
                    char.update()

            ### ДВИЖЕНИЕ
            for char in GAME.chars:
                char.go(time, pygame.key.get_pressed())

            # АТАКА ОЛЕГА
            if time % 100 == 0:
                GAME.oleg.current_anim = GAME.oleg.animations['stand_right']
                GAME.oleg.attack(GAME.owner)
                GAME.oleg.attack(GAME.player)
             
        ### ВЗАИМОДЕЙСТВИЕ  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False

            if GAME.in_game:
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if GAME.oleg in GAME.current_location.chars and keys[pygame.K_e]:  # Удар
                        GAME.player.attack(GAME.oleg)

                    if keys[pygame.K_f]: # Позвать
                        GAME.player.call(GAME.owner, GAME.current_location)
                        GAME.owner.loc = GAME.current_location

                    if keys[pygame.K_q] and keys[pygame.K_w] and keys[pygame.K_e]:  # читкод
                        GAME.player.health = 5
                        GAME.oleg.health = 5
                        
                if event.type == GAME.LOCATION_CHANGE_CODE:
                    
                    GAME.current_location.remove_char(GAME.player)
                    GAME.current_location = GAME.locations[(GAME.location_num + event.direction) % (len(GAME.locations) - 1)]
                    GAME.location_num += event.direction
                    GAME.current_location.add_char(GAME.player)
                    GAME.player.set_coords(*GAME.current_location.start_coords)
            else:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    GAME.in_game = True
                    GAME.new_game()


        GAME.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
        time += 1
        
    pygame.quit()
