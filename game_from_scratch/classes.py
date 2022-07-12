from functions import *
import pygame
import math
import random
import json

#player images
playerimage = pygame.image.load('assets/player_ship.png')
playerbullet = pygame.image.load('assets/player_bullet.png')
playerhitboximage = pygame.image.load('assets/player_hitbox.png')
#enemy images
enemyimage_red = pygame.image.load('assets/enemy_red.png')
enemybullet_red = pygame.image.load('assets/enemy_bullet_red.png')
#item images
pointitemimage = pygame.image.load('assets/pointitem.png')

json_file_open = open('stage1.json')
json_file_data = json.load(json_file_open)

#main classes
class Shipclass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.shipimage, (self.x, self.y))
    
    def getwidth(self):
        return self.shipimage.get_width()
    def getheight(self):
        return self.shipimage.get_height()

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

class Bulletclass:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity

    def draw(self, window):
        window.blit(self.bulletimage, (self.x, self.y))

    def getwidth(self):
        return self.bulletimage.get_width()
    def getheight(self):
        return self.bulletimage.get_height()

    def collide(self, object):
        return collide(self, object)

class Itemclass():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.itemimage, (self.x, self.y))

    def getwidth(self):
        return self.itemimage.get_width()
    def getheight(self):
        return self.itemimage.get_height()

    def move(self):
        self.y += 2
    
    def collide(self, object):
        return collide(self, object)

#player classes
class Playerclass(Shipclass):
    bullet_static_cooldown = 10
    bomb_static_cooldown = 60
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        #base ship
        self.shipimage = playerimage
        self.ship_velocity = 5
        self.hitboximage = playerhitboximage
        self.mask = pygame.mask.from_surface(self.hitboximage)
        self.score = 0
        self.lives = 3
        self.bombs = 3
        self.can_move = True
        self.just_spawned = False
        #bullets
        self.bulletimage = playerbullet
        self.bullets_on_screen = []
        self.bullet_velocity = 8
        self.bullet_cooldown_counter = 0
        self.bomb_cooldown_counter = 0


    def shoot(self):
        if self.bullet_cooldown_counter == 0:
            self.bullet_cooldown_counter = self.bullet_static_cooldown
            center_x = self.getcenter('x')-playerbullet.get_width()/2
            center_y = self.getcenter('y')-playerbullet.get_height()/2
            bullet_velocity = self.bullet_velocity
            if pygame.key.get_pressed()[pygame.K_UP]:
                bullet_velocity += 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                bullet_velocity -= 1
            bullet = Playerbulletclass(center_x, center_y, bullet_velocity)
            self.bullets_on_screen.append(bullet)

    def drawbullet(self, window):
        for bullet in self.bullets_on_screen:
            bullet.draw(window)
    
    def cool_down_function(self):
        if self.bullet_cooldown_counter > 0:
            self.bullet_cooldown_counter -= 1
        if self.bomb_cooldown_counter > 0:
            self.bomb_cooldown_counter -= 1

    def activate_bomb(self):
        if self.bomb_cooldown_counter == 0 and self.bombs > 0:
            self.bomb_cooldown_counter = self.bomb_static_cooldown
            return True
        else:
            return False
    
    def spawn(self, game_window_width, game_window_height):
        self.can_move = False
        self.y = game_window_height-1
        self.x = game_window_width/2-self.getwidth()/2
        self.just_spawned = True

class Playerbulletclass(Bulletclass):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, velocity)
        self.bulletimage = playerbullet
        self.mask = pygame.mask.from_surface(self.bulletimage)

    def move(self):
        self.y -= self.velocity

#enemy classes
class Enemyclass(Shipclass):
    def __init__(self, x, y, health, cooldown, worth, amount_of_items_to_drop, amount_of_bullets_shoot, angle_offset, angle_spread, path):
        super().__init__(x, y)
        #base ship
        self.shipimage = enemyimage_red
        self.health = health
        self.worth = worth
        self.amount_of_item_to_drop = amount_of_items_to_drop
        self.path = path
        self.ship_velocity = 1
        self.goal_x = None
        self.goal_y = None
        self.current_node = 0
        #bullets
        self.bulletimage = enemybullet_red
        self.bulletvelocity = 3
        self.cooldown = cooldown
        self.cooldown_counter = 0
        self.mask = pygame.mask.from_surface(self.shipimage)
        self.amount_of_bullets_shoot = amount_of_bullets_shoot
        self.angle_offset = angle_offset
        self.angle_spread = angle_spread

    def move(self):
        angle_in_radians = math.atan2(self.goal_y-self.y, self.goal_x-self.x)
        direction_x = math.cos(angle_in_radians)*self.ship_velocity
        direction_y = math.sin(angle_in_radians)*self.ship_velocity
        move_x_done = False
        move_y_done = False
        if self.x+self.ship_velocity > self.goal_x and self.x-self.ship_velocity < self.goal_x:
            self.x = self.goal_x
            move_x_done = True
        else:
            self.x += direction_x
        if self.y+self.ship_velocity > self.goal_y and self.y-self.ship_velocity < self.goal_y:
            self.y = self.goal_y
            move_y_done = True
        else:
            self.y += direction_y
        if move_x_done and move_y_done == True:
            self.current_node += 1
            for path in json_file_data['paths']:
                if self.current_node < len(path[self.path]):
                    if 'die' in path[self.path][self.current_node]:
                        return True
                    else:
                        self.goal_x = path[self.path][self.current_node]['x']
                        self.goal_y = path[self.path][self.current_node]['y']
                        return False

    def shoot(self, target, angle_offset=0):
        self.cooldown_counter = self.cooldown
        angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x')) + angle_offset
        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
        return Enemybulletclass(self.x+self.getwidth()/2-enemybullet_red.get_width()/2, self.y+self.getheight()/2-enemybullet_red.get_height()/2, self.bulletvelocity, direction_x, direction_y)

    def cooldown_function(self):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
    
    def drop_pointitem(self):
        return Pointclass(random.randrange(int(self.x), int(self.x+self.getwidth())), random.randrange(int(self.y), int(self.y+self.getheight())), int(self.worth/self.amount_of_item_to_drop))


class Enemybulletclass(Bulletclass):
    def __init__(self, x, y, velocity, direction_x, direction_y):
        super().__init__(x, y, velocity)
        self.bulletimage = enemybullet_red
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.mask = pygame.mask.from_surface(self.bulletimage)

    def move(self):
        self.x += self.direction_x
        self.y += self.direction_y

#item classes
class Pointclass(Itemclass):
    def __init__(self, x, y, worth):
        super().__init__(x, y)
        self.itemimage = pointitemimage
        self.worth = worth
        self.mask = pygame.mask.from_surface(self.itemimage)
    
    def close_to_player(self, target):
        lenght_x = self.x+self.getwidth()/2 - target.getcenter('x')
        lenght_y = self.y+self.getheight()/2 - target.getcenter('y')
        return math.sqrt(lenght_x*lenght_x + lenght_y*lenght_y)