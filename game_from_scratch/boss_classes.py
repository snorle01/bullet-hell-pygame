from classes import Bossclass, Enemybulletclass
import pygame
import random
import math

class Boss00(Bossclass):
    id = 'boss00'
    def __init__(self, image, midstage_boss):
        super().__init__(image, midstage_boss)
        #ship
        self.max_attacks = 3
        self.attack_count = 0
        #bullet
        self.ammo_count = 0
        self.bullet_angle = 0.0
        self.bullet_offset = 0.0

    def shoot(self, bullet_images, bullet_list, target):
        if self.ready_to_shoot:
            if self.midstage_boss and self.cooldown_counter == 0:
                self.cooldown_counter = 5
                #midstage boss fight
                self.bulletvelocity = 3
                for i in range(6):
                    angle_in_radians = random.uniform(0.0,6.283)
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2, self.y+self.getheight()/2, bullet_images['red'], self.bulletvelocity, direction_x, direction_y))

                self.bulletvelocity = 4
                for i in range(6):
                    angle_in_radians = random.uniform(0.0,6.283)
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2, self.y+self.getheight()/2, bullet_images['blue'], self.bulletvelocity, direction_x, direction_y))

                self.ammo_count += 1
                if self.ammo_count == 6:
                    self.cooldown_counter += 30
                    self.ammo_count = 0

            elif self.midstage_boss == False:
                #boss fight
                if self.attack_count == 0 and self.cooldown_counter == 0:
                    self.cooldown_counter = 20
                    x_cordinate = self.getcenter('x') - 200
                    for i in range(5):
                        angle_in_radians = math.atan2(target.getcenter('y')-self.y, target.getcenter('x')-x_cordinate)
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(x_cordinate, self.y, bullet_images['orange'], self.bulletvelocity, direction_x, direction_y))
                        x_cordinate += 100

                elif self.attack_count == 1 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    times = 0
                    for i in range(7):
                        angle_in_radians = self.bullet_angle+random.uniform(-self.bullet_offset,self.bullet_offset)
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2+(direction_x*times), self.y+self.getheight()/2+(direction_y*times), bullet_images['red'], self.bulletvelocity, direction_x, direction_y))
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

                        bullet_list.append(Enemybulletclass(self.getcenter('x')+spawn_x, self.getcenter('y')+spawn_y, bullet_images['red'], self.bulletvelocity,direction_x,direction_y))
                        bullet_offset += 0.5711818181818182

                elif self.attack_count == 3:
                    #first attack
                    if self.cooldown_counter == 0:
                        self.cooldown_counter = 5

                        spawn_x = math.cos(self.bullet_angle)*50
                        spawn_y = math.sin(self.bullet_angle)*50

                        new_bullet = Enemybulletclass(self.getcenter('x')+spawn_x, self.getcenter('y')+spawn_y, bullet_images['red'], self.bulletvelocity, 0, 0)

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

                            bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['orange'], self.bulletvelocity,direction_x,direction_y,'orange'))

class Boss01(Bossclass):
    id = 'boss01'
    bullet_image = ['red', 'blue', 'green', 'purple']
    def __init__(self, image, midstage_boss):
        super().__init__(image, midstage_boss)
        #ship
        self.max_attacks = 3
        self.attack_count = 0
        #bullet
        self.ammo_count = 0
        self.bullet_angle = 0.0
        self.bullet_offset = 0.0
        self.shoot_right = False

    def shoot(self, bullet_images, bullet_list, target):
        if self.ready_to_shoot:
            if self.midstage_boss and self.cooldown_counter == 0:
                self.cooldown_counter = 1
                angle_in_radians = self.bullet_angle
                direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], self.bulletvelocity, direction_x, direction_y))
                self.bullet_angle += 0.1

            elif self.midstage_boss == False:
                if self.attack_count == 0:
                    if self.cooldown_counter == 0:
                        self.cooldown_counter = 3
                        spawn_y = 0
                        spawn_x = random.randrange(0, 468)
                        bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images[random.choice(self.bullet_image)], self.bulletvelocity, 0, self.bulletvelocity))
                    
                    if self.second_cooldown_counter == 0:
                        self.second_cooldown_counter = 30
                        spawn_y = 0
                        spawn_x = random.randrange(int(target.x), target.getwidth()+int(target.x))
                        bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images[random.choice(self.bullet_image)], self.bulletvelocity, 0, self.bulletvelocity))

                elif self.attack_count == 1 and self.cooldown_counter == 0:
                    self.cooldown_counter = 3
                    angle_in_radians = self.bullet_angle
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity

                    if self.shoot_right:
                        spawn_x = 467
                        self.bullet_angle -= 0.07
                    else:
                        spawn_x = 0
                        self.bullet_angle += 0.07

                    if self.shoot_right and self.bullet_angle < 1.5:
                        self.shoot_right = not self.shoot_right
                        self.bullet_angle = 0-random.uniform(0.0, 0.07)
                    elif self.shoot_right == False and self.bullet_angle > 1.5:
                        self.shoot_right = not self.shoot_right
                        self.bullet_angle = 3+random.uniform(0.0, 0.07)

                    bullet_list.append(Enemybulletclass(spawn_x, 0, bullet_images['red'], self.bulletvelocity, direction_x, direction_y))

                elif self.attack_count == 2 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    self.bullet_offset = 0
                    for i in range(27):
                        angle_in_radians = 0 + self.bullet_offset + self.bullet_angle
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], self.bulletvelocity, direction_x, direction_y))
                        self.bullet_offset += 4.774789113480821
                    
                    if self.shoot_right:
                        self.bullet_angle -= 0.2
                    else:
                        self.bullet_angle += 0.2
                    
                    self.ammo_count += 1
                    if self.ammo_count == 3:
                        self.shoot_right = not self.shoot_right
                        self.bullet_angle = 0
                        self.ammo_count = 0
                        self.cooldown_counter = 50

                elif self.attack_count == 3 and self.cooldown_counter == 0:
                    self.cooldown_counter = 1
                    angle_in_radians = self.bullet_angle
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['purple'], self.bulletvelocity, direction_x, direction_y))
                    
                    angle_in_radians = self.bullet_angle*-1
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], self.bulletvelocity, direction_x, direction_y))
                    
                    self.bullet_angle += 0.1

#set range to 32 to get a rainbow ring of peaople effekt
'''angle_in_radians = 0.0
bullet_velocity = 2
for i in range(84):
    angle_in_radians += 0.2
    bullet_velocity += 0.03
    direction_x = math.cos(angle_in_radians)*bullet_velocity
    direction_y = math.sin(angle_in_radians)*bullet_velocity
    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('x'),bullet_velocity,direction_x,direction_y, bullet_type='bounce', despawn=False, origin_x=self.getcenter('x'), origin_y=self.getcenter('y')))
angle_in_radians = 3.1
bullet_velocity = 2
for i in range(84):
    angle_in_radians += 0.2
    bullet_velocity += 0.03
    direction_x = math.cos(angle_in_radians)*bullet_velocity
    direction_y = math.sin(angle_in_radians)*bullet_velocity
    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('x'),bullet_velocity,direction_x,direction_y, bullet_type='bounce', despawn=False, origin_x=self.getcenter('x'), origin_y=self.getcenter('y')))
self.cooldown_counter += 9999'''