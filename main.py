import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation_state(self):
        if self.rect.bottom == 210:
            self.animation_index += 0.3
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000) 
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.1)
background_music.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title = score_font.render('Pixel Runner', False, (111, 196, 169))
title_rect = title.get_rect(center = (400, 80))

instructions = score_font.render('Press SPACE to run', False, (111, 196, 169))
instructions_rect = instructions.get_rect(center = (400, 325))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:        
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))         
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()  

    if game_active:     
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        
        score = display_score()
          
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
       
        game_active = collision_sprite()        
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
        player_gravity = 0

        score_message = score_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 325))
        screen.blit(title, title_rect)

        if score == 0: screen.blit(instructions, instructions_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update() 
    clock.tick(60)
