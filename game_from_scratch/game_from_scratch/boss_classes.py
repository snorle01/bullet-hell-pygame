from classes import Bossclass, Enemybulletclass, Pointclass, Powerclass
import pygame
import random
import math

#images
#boss images
bossimage00 = pygame.image.load('assets/boss00.png')
#bulletimages
enemybullet_green = pygame.image.load('assets/enemy_bullet_green.png')
enemybullet_blue = pygame.image.load('assets/enemy_bullet_blue.png')
enemybullet_red = pygame.image.load('assets/enemy_bullet_red.png')
enemybullet_orange = pygame.image.load('assets/enemy_bullet_orange.png')

class Boss00(Bossclass):
    image = bossimage00
    mask = pygame.mask.from_surface(image)
    def __init__(self, midstage_boss):
        super().__init__(midstage_boss)
        #ship
        self.max_attacks = 3
        self.attack_count = 0
        #bullet
        self.ammo_count = 0
        self.bullet_angle = 0.0
        self.bullet_offset = 0.0

    def shoot(self, bullet_list, target):
        #shoot patterns
        #set range to 32 to get a rainbow ring of peaople effekt
        '''angle_in_radians = 0.0
        bullet_velocity = 2
        for i in range(84):
            angle_in_radians += 0.2
            bullet_velocity += 0.03
            direction_x = math.cos(angle_in_radians)*bullet_velocity
            direction_y = math.sin(angle_in_radians)*bullet_velocity
            bullet_list.append(Enemybulletclass(self.getcenter('x')-enemybullet_red.get_width()/2, self.getcenter('x')-enemybullet_red.get_width()/2,bullet_velocity,direction_x,direction_y, bullet_type='bounce', despawn=False, origin_x=self.getcenter('x'), origin_y=self.getcenter('y')))
        angle_in_radians = 3.1
        bullet_velocity = 2
        for i in range(84):
            angle_in_radians += 0.2
            bullet_velocity += 0.03
            direction_x = math.cos(angle_in_radians)*bullet_velocity
            direction_y = math.sin(angle_in_radians)*bullet_velocity
            bullet_list.append(Enemybulletclass(self.getcenter('x')-enemybullet_red.get_width()/2, self.getcenter('x')-enemybullet_red.get_width()/2,bullet_velocity,direction_x,direction_y, bullet_type='bounce', despawn=False, origin_x=self.getcenter('x'), origin_y=self.getcenter('y')))
        self.cooldown_counter += 9999'''

        if self.midstage_boss == True and self.cooldown_counter == 0:
            self.cooldown_counter = 5
            #midstage boss fight
            self.bulletvelocity = 3
            bullet_color = 'red'
            for i in range(6):
                angle_in_radians = random.uniform(0.0,6.283)
                direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2-enemybullet_red.get_width()/2, self.y+self.getheight()/2-enemybullet_red.get_height()/2, self.bulletvelocity, direction_x, direction_y, bullet_color))

            self.bulletvelocity = 4
            bullet_color = 'blue'
            for i in range(6):
                angle_in_radians = random.uniform(0.0,6.283)
                direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2-enemybullet_blue.get_width()/2, self.y+self.getheight()/2-enemybullet_blue.get_height()/2, self.bulletvelocity, direction_x, direction_y, bullet_color))

            self.ammo_count += 1
            if self.ammo_count == 6:
                self.cooldown_counter += 30
                self.ammo_count = 0
        
        if self.midstage_boss == False:
            #boss fight
            if self.attack_count == 0 and self.cooldown_counter == 0:
                self.cooldown_counter = 20
                x_cordinate = self.getcenter('x')-enemybullet_orange.get_width()/2 - 200
                for i in range(5):
                    angle_in_radians = math.atan2(target.getcenter('y')-self.y, target.getcenter('x')-x_cordinate)
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(x_cordinate, self.y, self.bulletvelocity, direction_x, direction_y, 'orange'))
                    x_cordinate += 100

            elif self.attack_count == 1 and self.cooldown_counter == 0:
                self.cooldown_counter = 5
                times = 0
                for i in range(7):
                    angle_in_radians = self.bullet_angle+random.uniform(-self.bullet_offset,self.bullet_offset)
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2-enemybullet_red.get_width()/2+(direction_x*times), self.y+self.getheight()/2-enemybullet_red.get_height()/2+(direction_y*times), self.bulletvelocity, direction_x, direction_y))
                    times += 5
                self.bullet_angle += 0.3
                if self.bullet_offset < 0.5:
                    self.bullet_offset += 0.01

            elif self.attack_count == 2 and self.cooldown_counter == 0:
                self.cooldown_counter = 50
                bullet_offset = 0

                angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x'))
                direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                direction_y = math.sin(angle_in_radians)*self.bulletvelocity

                for i in range(11):
                    spawn_x = math.cos(bullet_offset)*50
                    spawn_y = math.sin(bullet_offset)*50

                    bullet_list.append(Enemybulletclass(self.getcenter('x')-enemybullet_red.get_width()/2+spawn_x, self.getcenter('y')-enemybullet_red.get_height()/2+spawn_y,self.bulletvelocity,direction_x,direction_y))
                    bullet_offset += 0.5711818181818182

            elif self.attack_count == 3:
                #first attack
                if self.cooldown_counter == 0:
                    self.cooldown_counter = 5

                    spawn_x = math.cos(self.bullet_angle)*50
                    spawn_y = math.sin(self.bullet_angle)*50

                    new_bullet = Enemybulletclass(self.getcenter('x')-enemybullet_red.get_width()/2+spawn_x, self.getcenter('y')-enemybullet_red.get_width()/2+spawn_y, self.bulletvelocity, 0, 0)

                    angle_in_radians = math.atan2(target.getcenter('y')-new_bullet.getcenter('y'), target.getcenter('x')-new_bullet.getcenter('x'))
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity

                    new_bullet.direction_x = direction_x
                    new_bullet.direction_y = direction_y

                    bullet_list.append(new_bullet)
                    self.bullet_angle += 0.4

                    self.ammo_count += 1
                    if self.ammo_count == 30:
                        self.ammo_count = 0
                        self.cooldown_counter = 50

                #second attack
                if self.second_cooldown_counter == 0:
                    self.second_cooldown_counter = 60

                    bullet_offset = 0
                    for i in range(30):
                        angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x'))+bullet_offset
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_offset += 0.20943

                        bullet_list.append(Enemybulletclass(self.getcenter('x')-enemybullet_red.get_width()/2, self.getcenter('y')-enemybullet_red.get_height()/2,self.bulletvelocity,direction_x,direction_y,'orange'))
