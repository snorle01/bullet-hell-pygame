from turtle import circle, window_height, window_width
from functions import *
import pygame
import math
import random
import json

#player images
playerimage = pygame.image.load('assets/player_ship.png')
playerimage_glow = pygame.image.load('assets/player_ship_glow.png')
playerbullet = pygame.image.load('assets/player_bullet.png')
playerbullet_blur = pygame.image.load('assets/player_bullet_blur.png')
playerarrow = pygame.image.load('assets/player_arrow.png')
playerarrow_blur = pygame.image.load('assets/player_arrow_blur.png')
playerhitboximage = pygame.image.load('assets/player_hitbox.png')
#enemy images
enemyimage_red = pygame.image.load('assets/enemy_red.png')
enemyimage_blue = pygame.image.load('assets/enemy_blue.png')
enemyimage_green = pygame.image.load('assets/enemy_green.png')
#enemy bullets
enemybullet_green = pygame.image.load('assets/enemy_bullet_green.png')
enemybullet_blue = pygame.image.load('assets/enemy_bullet_blue.png')
enemybullet_red = pygame.image.load('assets/enemy_bullet_red.png')
enemybullet_orange = pygame.image.load('assets/enemy_bullet_orange.png')
#item images
pointitemimage = pygame.image.load('assets/pointitem.png')
poweritemimage = pygame.image.load('assets/poweritem.png')
big_poweritemimage = pygame.image.load('assets/big_poweritem.png')
heart_image = pygame.image.load('assets/heart_object.png')
bomb_image = pygame.image.load('assets/bomb_object.png')
ghost_point_image = pygame.image.load('assets/ghost_point.png')
#animation
exsplotion_image = [pygame.image.load('assets/exsplotion1.png'), pygame.image.load('assets/exsplotion2.png'), pygame.image.load('assets/exsplotion3.png'), pygame.image.load('assets/exsplotion4.png')]

json_file_boss = json.load(open('boss.json'))

#main classes
class Classbase:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
    
    def getwidth(self):
        return self.image.get_width()

    def getheight(self):
        return self.image.get_height()

    def getcenter(self, return_what='both'):
        if return_what == 'both':
            return self.x+self.getwidth()/2, self.y+self.getheight()/2
        elif return_what == 'x':
            return self.x+self.getwidth()/2
        elif return_what == 'y':
            return self.y+self.getheight()/2
        else:
            print('ERROR: write either x, y or both')
    
    def collide(self, object):
        return collide(self, object)
    
    def outside_play_area(self, screen_height, screen_width):
        if self.x > screen_width or self.y > screen_height or self.x+self.getwidth() < 0 or self.y+self.getheight() < 0:
            return True
    
    def inside_play_area(self, screen_height, screen_width):
        if self.x+self.getwidth() <= screen_width and self.x >= 0 and self.y+self.getheight() <= screen_height and self.y >= 0:
            return True

class Shipclass(Classbase):
    def __init__(self, x, y):
        super().__init__(x,y)

    def cooldown_function(self):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

class Bulletclass(Classbase):
    def __init__(self, x, y, velocity, direction_x, direction_y, despawn=True):
        super().__init__(x,y)
        self.velocity = velocity
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.despawn_when_out_of_screen = despawn

    def close_to(self, target):#checks how far the entity is from the target
        lenght_x = self.getcenter('x') - target.getcenter('x')
        lenght_y = self.getcenter('y') - target.getcenter('y')
        return math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y)

class Itemclass(Classbase):
    collect_distance = 60
    pickup_distance = 10
    def __init__(self, x, y, worth):
        super().__init__(x,y)
        self.worth = worth
        self.velocity = 2
        self.direction_x = 0
        self.direction_y = 2
        self.is_going_to_player = False
    
    def close_to(self, target):#checks how far the entity is from the target
        lenght_x = self.getcenter('x') - target.getcenter('x')
        lenght_y = self.getcenter('y') - target.getcenter('y')
        return math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y)

    def go_to(self, target):#the entity wil now go twoards the target
        angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x'))
        self.velocity = 7
        self.is_going_to_player = True
        self.direction_x = math.cos(angle_in_radians)*self.velocity
        self.direction_y = math.sin(angle_in_radians)*self.velocity

#player classes
class Playerclass(Shipclass):
    bullet_static_cooldown = 5
    bomb_static_cooldown = 60
    player_glow_animation = [playerimage_glow, playerimage]
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        #base ship
        self.image = playerimage
        self.ship_velocity = 5
        self.hitboximage = playerhitboximage
        self.mask = pygame.mask.from_surface(self.hitboximage)
        self.score = 0
        self.lives = 3
        self.heart_pice = 0
        self.power = 0
        self.full_power_timer = 0
        self.can_move = True
        self.just_spawned = False
        self.can_get_hurt = True
        self.invulnerable_timer = 0
        self.god = False
        self.animaton_framerate = 5 #set framerate (can be changed to make animation faster or slower)
        self.current_animaton_frame = 0 #current frame of a animation
        self.animation_timer = 0 #counts the amount of frames has passed before a new frame
        #bullets
        self.bullets_on_screen = []
        self.bullet_velocity = 15
        self.bullet_cooldown_counter = 0
        #bomb
        self.bombs = 3
        self.bomb_pice = 0
        self.bomb_cooldown_counter = 0
        self.bomb_on = False
        self.bomb_current_size = 0
        self.bomb_max_size = 850
        self.bomb_grow_rate = 15
        self.death_bomb_counter = 0

    def shoot(self):
        if self.bullet_cooldown_counter == 0:
            self.bullet_cooldown_counter = self.bullet_static_cooldown
            bullet_velocity = self.bullet_velocity

            #normal bullets
            center_x = self.getcenter('x')-playerbullet.get_width()/2
            center_y = self.getcenter('y')-playerbullet.get_height()/2
            arrow_y = self.y+playerarrow.get_height()
            arrow_center_x = playerarrow.get_width()/2

            bullet = Playerbulletclass(center_x, center_y, 'playerbullet', bullet_velocity, 1)
            self.bullets_on_screen.append(bullet)

            #special bullets based on power
            if self.power == 400:
                self.bullets_on_screen.append(Playerbulletclass(center_x-self.getwidth()-arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x+self.getwidth()+arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x-self.getwidth()+arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x+self.getwidth()-arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
            elif self.power >= 300:
                self.bullets_on_screen.append(Playerbulletclass(center_x-self.getwidth()+arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x+self.getwidth()-arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
            elif self.power >= 200:
                self.bullets_on_screen.append(Playerbulletclass(center_x-self.getwidth()+arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
                self.bullets_on_screen.append(Playerbulletclass(center_x+self.getwidth()-arrow_center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))
            elif self.power >= 100:
                self.bullets_on_screen.append(Playerbulletclass(center_x, arrow_y, 'playerarrow', bullet_velocity, 0.1))

    def draw(self, window, screen_width, screen_height):
        #draw player bullets
        for bullet in self.bullets_on_screen:
            bullet.draw(window)
        if self.bomb_on == True and self.bomb_current_size > 0:
            #draws faded part of the bomb
            bomb_alpha = 255-255/(self.bomb_max_size/self.bomb_current_size)
            bomb_surface = pygame.Surface((screen_width,screen_height), pygame.SRCALPHA)
            pygame.draw.circle(bomb_surface, (255,255,255,bomb_alpha), [self.getcenter('x'), self.getcenter('y')], self.bomb_current_size, 0)
            window.blit(bomb_surface, (0,0))
            pygame.draw.circle(window, (255,255,255), [self.getcenter('x'), self.getcenter('y')], self.bomb_current_size, 3)
        #changes self.image
        if self.invulnerable_timer > 0:
            self.animation_timer += 1
            if self.animation_timer == self.animaton_framerate:
                self.animation_timer = 0
                if self.current_animaton_frame == len(self.player_glow_animation)-1:
                    self.current_animaton_frame = 0
                else:
                    self.current_animaton_frame += 1
            self.image = self.player_glow_animation[self.current_animaton_frame]
        else:
            self.image = playerimage
        window.blit(self.image, (self.x, self.y))
    
    def update(self, window_width, window_height, power_list):
        #bullet
        if self.bullet_cooldown_counter > 0:
            self.bullet_cooldown_counter -= 1
        #bomb
        if self.bomb_cooldown_counter > 0:
            self.bomb_cooldown_counter -= 1
        #invulnerable
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer == 0:
                self.can_get_hurt = True
        #death
        if self.death_bomb_counter > 0:
            self.death_bomb_counter -= 1
            if self.death_bomb_counter == 0:
                self.die(window_width, window_height, power_list)

    def activate_bomb(self):
        if self.bombs > 0 and self.bomb_cooldown_counter == 0:
            self.bomb_cooldown_counter = self.bomb_static_cooldown
            self.bomb_on = True
            self.bombs -= 1
            self.invulnerable(60)
            #death bomb
            if self.death_bomb_counter > 0:
                self.bomb_max_size = 120
                self.bomb_grow_rate = 5
                self.death_bomb_counter = 0
    
    def move_bomb(self, boss, enemy_list, item_list, other_lists):
        if self.bomb_on:
            #damedges the boss
            if boss != None and boss.invulnerable_timer == 0:
                lenght_x = self.getcenter('x') - boss.getcenter('x')
                lenght_y = self.getcenter('y') - boss.getcenter('y')
                if math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y) < self.bomb_current_size:
                    boss.health -= 1
            #damadegs the enemys in enemy list
            for enemy in enemy_list:
                lenght_x = self.getcenter('x') - enemy.getcenter('x')
                lenght_y = self.getcenter('y') - enemy.getcenter('y')
                if math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y) < self.bomb_current_size:
                    enemy.health -= 1
            #goes trough all objects in other lists and removes them
            for index in range(len(other_lists)):
                for object in other_lists[index]:
                    lenght_x = self.getcenter('x') - object.getcenter('x')
                    lenght_y = self.getcenter('y') - object.getcenter('y')
                    if math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y) < self.bomb_current_size:
                        other_lists[index].remove(object)
            #goes trough all items in item list and makes them go to the player
            for index in range(len(item_list)):
                for object in item_list[index]:
                    lenght_x = self.getcenter('x') - object.getcenter('x')
                    lenght_y = self.getcenter('y') - object.getcenter('y')
                    if math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y) < self.bomb_current_size:
                        object.go_to(self)
            #if bomb is at max size. reset bomb and turn it off
            self.bomb_current_size += self.bomb_grow_rate
            if self.bomb_current_size >= self.bomb_max_size:
                self.bomb_on = False
                self.bomb_current_size = 0
                self.bomb_max_size = 850
                self.bomb_grow_rate = 15

    def make_items_go_to_me(self, all_lists):
        for index in range(len(all_lists)):
            for item in all_lists[index]:
                item.go_to(self)
    
    def spawn(self, game_window_width, game_window_height):
        self.can_move = False
        self.y = game_window_height-1
        self.x = game_window_width/2-self.getwidth()/2
        self.just_spawned = True

    def invulnerable(self, timer=180):
        self.invulnerable_timer = timer
        self.can_get_hurt = False

    def collide_with_bullet_and_enemy(self, bullet_list, enemy_list):
        if self.can_get_hurt and self.death_bomb_counter == 0 and self.god == False:
            for bullet in bullet_list:
                if bullet.close_to(self) < bullet.hit_distance:
                    self.death_bomb_counter = 30
                    bullet_list.remove(bullet)
            for enemy in enemy_list:
                if self.collide(enemy):
                    self.death_bomb_counter = 30
                    enemy_list.remove(enemy)

    def die(self, game_window_width, game_window_height, power_list):
        self.lives -= 1
        self.full_power_timer = 0
        if self.bombs < 3:
            self.bombs = 3
        if self.power > 0:
            if self.power >= 100:
                power = 100
                isbig = True
            else:
                power = self.power
                isbig = False
            power_list.append(Powerclass(self.getcenter('x'),self.getcenter('y'),5,power,isbig))
        self.power = 0
        self.spawn(game_window_width, game_window_height)
        self.invulnerable()

    def move(self, game_window_width, game_window_height):
        if self.can_move == True:
            if self.death_bomb_counter == 0:
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    if self.y+self.ship_velocity > game_window_height-self.getheight():
                        self.y = game_window_height-self.getheight()
                    else:
                        self.y += self.ship_velocity
                if pygame.key.get_pressed()[pygame.K_UP]:
                    if self.y - self.ship_velocity < 0:
                        self.y = 0
                    else:
                        self.y -= self.ship_velocity
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if self.x + self.ship_velocity > game_window_width-self.getwidth():
                        self.x = game_window_width-self.getwidth()
                    else:
                        self.x += self.ship_velocity
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    if self.x - self.ship_velocity < 0:
                        self.x = 0
                    else:
                        self.x -= self.ship_velocity

                #if player holds shift make ship slow down
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    self.ship_velocity = 3
                else:
                    self.ship_velocity = 5
                #player shoot
                if pygame.key.get_pressed()[pygame.K_z]:
                    self.shoot()

            #player bomb
            if pygame.key.get_pressed()[pygame.K_x]:
                self.activate_bomb()

            #cheats
            if pygame.key.get_pressed()[pygame.K_F1]:
                self.god = True
            if pygame.key.get_pressed()[pygame.K_F2]:
                if self.lives < 8:
                    self.lives += 1
            if pygame.key.get_pressed()[pygame.K_F3]:
                if self.bombs < 8:
                    self.bombs += 1
            if pygame.key.get_pressed()[pygame.K_F4]:
                if self.power != 400:  
                    self.power += 1

        elif self.just_spawned == True:
            self.y -= 3
            if self.y < game_window_height-self.getheight()-40:
                self.just_spawned = False
                self.can_move = True

class Playerbulletclass(Bulletclass):
    images = {'playerbullet':(playerbullet, playerbullet_blur), 'playerarrow':(playerarrow, playerarrow_blur)}
    def __init__(self, x, y, image_choice, velocity, damage):
        super().__init__(x, y, velocity, 0, 0)
        self.image_string = image_choice
        self.image = self.images[self.image_string][0]
        self.damage = damage
        self.mask = pygame.mask.from_surface(self.image)
        self.dying = False
        self.dying_timer = 10

    def move(self, screen_height, bullet_list):
        self.y -= self.velocity
        if self.y > screen_height:
            bullet_list.remove(self)

    def die(self):
        self.image = self.images[self.image_string][1]
        self.dying = True
        self.velocity = 3

    def update(self, bullet_list):
        if self.dying:
            self.dying_timer -= 1
            if self.dying_timer == 0:
                bullet_list.remove(self)

#enemy classes
class Enemyclass(Shipclass):
    image_choise = {'red_spaceship':enemyimage_red, 'blue_spaceship':enemyimage_blue, 'green_spaceship':enemyimage_green}
    def __init__(self, x, y, health, ship_id, image, ship_velocity, cooldown, worth, amount_of_items_to_drop, amount_of_bullets_shoot, ammo, ammo_cooldown, angle_offset, angle_spread, path):
        super().__init__(x, y)
        #base ship
        self.image = self.image_choise[image]
        self.mask = pygame.mask.from_surface(self.image)
        self.health = health
        self.max_health = health
        self.worth = worth
        self.amount_of_item_to_drop = amount_of_items_to_drop
        self.respawn = False
        self.ship_id = ship_id
        self.item = None
        #movement
        self.origin_x = x
        self.origin_y = y
        self.path = path
        self.ship_velocity = ship_velocity
        self.goal_x = None
        self.goal_y = None
        self.direction_x = 0
        self.directoin_y = 0
        self.current_node = 0
        self.wait_move = 0
        self.ready_to_shoot = True
        self.done_moving = False
        #bullets
        self.bulletvelocity = 3
        self.cooldown = cooldown
        self.cooldown_counter = 0
        self.ammo_cooldown = ammo_cooldown
        self.amount_of_bullets_shoot = amount_of_bullets_shoot
        self.angle_offset = angle_offset
        self.angle_spread = angle_spread
        self.ammo_count = 0
        self.ammo = ammo

    def move(self, enemy_list, json):
        if self.wait_move > 0:
            self.wait_move -= 1
        elif self.done_moving == False:
            move_x_done = False
            move_y_done = False
            if self.x+self.ship_velocity > self.goal_x and self.x-self.ship_velocity < self.goal_x:
                self.x = self.goal_x
                move_x_done = True
            else:
                self.x += self.direction_x

            if self.y+self.ship_velocity > self.goal_y and self.y-self.ship_velocity < self.goal_y:
                self.y = self.goal_y
                move_y_done = True
            else:
                self.y += self.direction_y

            #when enemy has reached its goal 
            if move_x_done and move_y_done == True:
                self.current_node += 1
                if self.current_node < len(json['paths'][0][self.path]):
                    if 'die' in json['paths'][0][self.path][self.current_node]:
                        enemy_list.remove(self)
                    elif 'wait' in json['paths'][0][self.path][self.current_node]:
                        self.wait_move = json['paths'][0][self.path][self.current_node]['wait']
                    else:
                        if json['paths'][0][self.path][self.current_node]['x'] == 'relative':
                            self.goal_x = self.x
                        else:
                            self.goal_x = json['paths'][0][self.path][self.current_node]['x']

                        if json['paths'][0][self.path][self.current_node]['y'] == 'relative':
                            self.goal_y = self.y
                        else:
                            self.goal_y = json['paths'][0][self.path][self.current_node]['y']

                        angle_in_radians = math.atan2(self.goal_y-self.y, self.goal_x-self.x)
                        self.direction_x = math.cos(angle_in_radians)*self.ship_velocity
                        self.direction_y = math.sin(angle_in_radians)*self.ship_velocity
                    
                    if 'shoot' in json['paths'][0][self.path][self.current_node]:
                        self.ready_to_shoot = json['paths'][0][self.path][self.current_node]['shoot']
                else:
                    self.done_moving = True

    def collide_with_player_bullet(self, player_bullet):
        for bullet in player_bullet:
            if bullet.dying == False and self.collide(bullet):
                self.health -= bullet.damage
                bullet.die()

    def shoot(self, target, bullet_list):
        if self.cooldown_counter == 0 and self.ready_to_shoot:
            self.cooldown_counter = self.cooldown

            angle_offset = self.angle_offset
            for i in range(self.amount_of_bullets_shoot):
                angle_offset += self.angle_spread
                angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x')) + angle_offset
                direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2-enemybullet_red.get_width()/2, self.y+self.getheight()/2-enemybullet_red.get_height()/2, self.bulletvelocity, direction_x, direction_y))

            if self.ammo != False:
                self.ammo_count += 1
                if self.ammo_count == self.ammo:
                    self.cooldown_counter += self.ammo_cooldown
                    self.ammo_count = 0

    def die(self, enemy_list, particle_list, point_list, power_list, heart_list, bomb_list):
        particle_list.append(Exsplotionclass(self.getcenter('x'),self.getcenter('y'), self.getwidth()+5, 3))
        for i in range(self.amount_of_item_to_drop):
            point_list.append(Pointclass(random.randrange(int(self.x), int(self.x+self.getwidth())), random.randrange(int(self.y), int(self.y+self.getheight())), int(self.worth/self.amount_of_item_to_drop)))
            power_list.append(Powerclass(random.randrange(int(self.x), int(self.x+self.getwidth())), random.randrange(int(self.y), int(self.y+self.getheight())), int(self.worth/self.amount_of_item_to_drop)))
            if self.item == 'heart':
                heart_list.append(Heartclass(self.getcenter('x')-heart_image.get_width()/2,self.getcenter('y')-heart_image.get_height()/2,100))
            elif self.item == 'bomb':
                bomb_list.append(Bombclass(self.getcenter('x')-bomb_image.get_width()/2,self.getcenter('y')-bomb_image.get_height()/2,100))
        if self.respawn == True:
            self.x = self.origin_x
            self.y = self.origin_y
            self.health = self.max_health
            self.wait_move = 30
            self.done_moving = False
        else:
            enemy_list.remove(self)

class Enemybulletclass(Bulletclass):
    image_choise = {'red':(enemybullet_red, 8), 'blue':(enemybullet_blue, 8), 'green':(enemybullet_green, 8), 'orange':(enemybullet_orange, 15)}
    def __init__(self, x, y, velocity, direction_x, direction_y, color='red', bullet_type=None, despawn=True, origin_x=None, origin_y=None):
        super().__init__(x, y, velocity, direction_x, direction_y, despawn)
        self.image, self.hit_distance = self.image_choise[color]
        self.bullet_type = bullet_type
        self.origin_x = origin_x
        self.origin_y = origin_y

    def move(self, bullet_list, screen_height, screen_width):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.bullet_type == 'bounce':
            lenght_x = self.getcenter('x') - self.origin_x
            lenght_y = self.getcenter('y') - self.origin_y
            lenght = math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y)
            if lenght > 700:
                self.direction_x = self.direction_x*-1
                self.direction_y = self.direction_y*-1
        
        if self.despawn_when_out_of_screen and self.outside_play_area(screen_height, screen_width):
            bullet_list.remove(self)

    def turn_into_ghost(self, ghostitem_list):
        ghostitem_list.append(Ghostpointclass(self.getcenter('x')-ghost_point_image.get_width()/2,self.getcenter('y')-ghost_point_image.get_height()/2))

class Bossclass(Shipclass):
    def __init__(self, midstage_boss):
        super().__init__(x=0, y=0)
        self.max_health = 100
        self.health = 100
        self.goal_x = None
        self.goal_y = None
        self.ship_velocity = 3
        self.ready_to_shoot = False
        self.stop_moving = False
        self.attack_count = 0
        self.midstage_boss = midstage_boss
        self.special_attack = False
        self.invulnerable_timer = 0
        #bullets
        self.cooldown_counter = 0
        self.second_cooldown_counter = 0
        self.bulletvelocity = 0

    def spawn(self, window_width):
        self.x = window_width/2-self.getcenter('x')
        self.goal_x = self.x
        self.goal_y = 200

    def update(self):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
        if self.second_cooldown_counter > 0:
            self.second_cooldown_counter -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def move(self):
        if self.stop_moving == False:
            reached_goal_x = False
            reached_goal_y = False
            angle_in_radians = math.atan2(self.goal_y-self.y, self.goal_x-self.x)
            direction_x = math.cos(angle_in_radians)*self.ship_velocity
            direction_y = math.sin(angle_in_radians)*self.ship_velocity
            if self.x+self.ship_velocity > self.goal_x and self.x-self.ship_velocity < self.goal_x:
                self.x = self.goal_x
                reached_goal_x = True
            else:
                self.x += direction_x

            if self.y+self.ship_velocity > self.goal_y and self.y-self.ship_velocity < self.goal_y:
                self.y = self.goal_y
                reached_goal_y = True
            else:
                self.y += direction_y

            if reached_goal_y and reached_goal_x:
                self.stop_moving = True
                self.ready_to_shoot = True

    def collide_with_player_bullets(self, player_bullets):
        for bullet in player_bullets:
            if bullet.dying == False and self.collide(bullet):
                if self.invulnerable_timer == 0:
                    self.health -= bullet.damage
                bullet.die()

    def die(self, enemy_bullets, point_list, power_list, ghost_list, particle_list):
        if self.midstage_boss == False:
            for bullet in enemy_bullets:
                bullet.turn_into_ghost(ghost_list)
            enemy_bullets.clear()
        if self.midstage_boss == False and self.attack_count != self.max_attacks:
            self.attack_count += 1
            self.special_attack = json_file_boss['boss00'][0]['boss'][self.attack_count]['special']
            self.max_health = json_file_boss['boss00'][0]['boss'][self.attack_count]['health']
            self.health = self.max_health
            self.bulletvelocity = json_file_boss['boss00'][0]['boss'][self.attack_count]['bulletvelocity']
            self.invulnerable_timer = 120
            self.cooldown_counter = 30
        else:
            for i in range(30):
                point_list.append(Pointclass(random.randrange(int(self.x), int(self.x+self.getwidth())), random.randrange(int(self.y), int(self.y+self.getwidth())), 5))
            power_list.append(Powerclass(self.getcenter('x')-big_poweritemimage.get_width()/2,self.getcenter('y')-big_poweritemimage.get_height()/2,50,50,True))
            if self.midstage_boss == False and self.attack_count == self.max_attacks:
                particle_list.append(Exsplotionclass(self.getcenter('x'), self.getcenter('y'), 850, 10))
            return True

#item classes
class Pointclass(Itemclass):
    def __init__(self, x, y, worth):
        super().__init__(x, y, worth)
        self.image = pointitemimage
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, player, screen_height, item_list, text_list):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.y > screen_height:
            item_list.remove(self)
        elif self.is_going_to_player:
            self.go_to(player)

        distance_to_player = self.close_to(player)
        if distance_to_player < self.pickup_distance: #player picks up item and item gets deleted
            player.score += self.worth
            text_list.append(Textclass(player, self.worth))
            item_list.remove(self)
        elif distance_to_player < self.collect_distance:
            self.is_going_to_player = True
                

class Powerclass(Itemclass):
    def __init__(self, x, y, worth, power_worth=1, big=False):
        super().__init__(x, y, worth)
        if big == False:
            self.image = poweritemimage
        else:
            self.image = big_poweritemimage
        self.mask = pygame.mask.from_surface(self.image)
        self.power_worth = power_worth

    def move(self, player, screen_height, item_list, text_list):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.y > screen_height:
            item_list.remove(self)
        elif self.is_going_to_player:
            self.go_to(player)

        distance_to_player = self.close_to(player)
        if distance_to_player < self.collect_distance:
            self.is_going_to_player = True
            if distance_to_player < self.pickup_distance: #player picks up item
                if player.power == 400:
                    player.score += self.worth
                    text_list.append(Textclass(player, self.worth))
                elif player.power+self.power_worth > 400:
                    player.power = 400
                else:
                    player.power += self.power_worth
                item_list.remove(self)

class Heartclass(Itemclass):
    def __init__(self, x, y, worth):
        super().__init__(x, y, worth)
        self.image = heart_image

    def move(self, player, screen_height, item_list, text_list):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.y > screen_height:
            item_list.remove(self)
        elif self.is_going_to_player:
            self.go_to(player)

        distance_to_player = self.close_to(player)
        if distance_to_player < self.pickup_distance: #player picks up item and item gets removed
            if player.lives == 8:
                player.score += self.worth
                text_list.append(Textclass(player, self.worth))
            else:
                if player.heart_pice == 2:
                    player.heart_pice = 0
                    player.lives += 1
                else:
                    player.heart_pice += 1
            item_list.remove(self)

        elif distance_to_player < self.collect_distance:
            self.is_going_to_player = True

class Bombclass(Itemclass):
    def __init__(self, x, y, worth):
        super().__init__(x, y, worth)
        self.image = bomb_image

    def move(self, player, screen_height, item_list, text_list):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.y > screen_height:
            item_list.remove(self)
        elif self.is_going_to_player:
            self.go_to(player)

        distance_to_player = self.close_to(player)
        if distance_to_player < self.pickup_distance: #item gets picked up and removed
            if player.bombs == 8:
                player.score += self.worth
                text_list.append(Textclass(player, self.worth))
            else:
                if player.bomb_pice == 2:
                    player.bomb_pice = 0
                    player.bombs += 1
                else:
                    player.bomb_pice += 1
            item_list.remove(self)
        elif distance_to_player < self.collect_distance: #item begins to go towards player 
            self.is_going_to_player = True

class Ghostpointclass(Itemclass):
    def __init__(self, x, y):
        super().__init__(x, y, worth=1)
        self.velocity = 7
        self.image = ghost_point_image

    def move(self, player, ghost_list):
        angle_in_radians = math.atan2(player.getcenter('y')-self.getcenter('y'), player.getcenter('x')-self.getcenter('x'))
        self.direction_x = math.cos(angle_in_radians)*self.velocity
        self.direction_y = math.sin(angle_in_radians)*self.velocity
        self.x += self.direction_x
        self.y += self.direction_y

        if self.close_to(player) < self.pickup_distance: #player picks up item and item gets deleted 
            player.score += self.worth
            ghost_list.remove(self)

class Textclass(Classbase):
    def __init__(self, player, text):
        self.text_label = pygame.font.SysFont(None, 20).render(str(text),1,(255,255,255))
        super().__init__(player.getcenter('x')-self.text_label.get_width()/2, player.getcenter('y')-self.text_label.get_height()/2)
        self.life = 60


    def draw(self, window):
        window.blit(self.text_label, (self.x, self.y))

    def move(self):
        self.y -= 1

    def update(self, text_list):
        self.life -= 1
        if self.life == 0:
            text_list.remove(self)

class Particleclass(Classbase):
    frames_until_next_texture = 3
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite_sheet = exsplotion_image
        self.image = self.sprite_sheet[0]
        self.timer = 0
        self.current_image_index = 0
        self.origin_x = x
        self.origin_y = y

    def update(self, particle_list):
        self.timer += 1
        if self.timer == self.frames_until_next_texture:
            self.timer = 0
            self.current_image_index += 1
            if self.current_image_index >= len(self.sprite_sheet):
                particle_list.remove(self)
            else:
                self.image = self.sprite_sheet[self.current_image_index]

class Exsplotionclass(Classbase):

    def __init__(self, x, y, max_size, groth):
        super().__init__(x, y)
        self.max_size = max_size
        self.groth = groth
        self.size = 0

    def draw(self, window):
        #for some reason it keeps trying to divide 0
        if self.max_size != 0 and self.size != 0:
            alpha_prosent = (self.max_size/self.size)
            if alpha_prosent != 0:
                exsplotion_alpha = 255-255/alpha_prosent
                exsplotion_surface = pygame.Surface((self.max_size*2,self.max_size*2), pygame.SRCALPHA)
                pygame.draw.circle(exsplotion_surface, (255,255,255,exsplotion_alpha), [self.max_size,self.max_size], self.size, 0)
                window.blit(exsplotion_surface, (self.x-self.max_size, self.y-self.max_size))
        pygame.draw.circle(window, (255,255,255), [self.x, self.y], self.size, 3)

    def update(self, particle_list):
        self.size += self.groth
        if self.size > self.max_size:
            particle_list.remove(self)