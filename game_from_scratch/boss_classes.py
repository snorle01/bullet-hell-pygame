from classes import Bossclass, Enemybulletclass
import pygame, random, math

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
                    bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2, self.y+self.getheight()/2, bullet_images['red'], direction_x, direction_y))

                self.bulletvelocity = 4
                for i in range(6):
                    angle_in_radians = random.uniform(0.0,6.283)
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2, self.y+self.getheight()/2, bullet_images['blue'], direction_x, direction_y))

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
                        bullet_list.append(Enemybulletclass(x_cordinate, self.y, bullet_images['orange'], direction_x, direction_y))
                        x_cordinate += 100

                elif self.attack_count == 1 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    times = 0
                    for i in range(7):
                        angle_in_radians = self.bullet_angle+random.uniform(-self.bullet_offset,self.bullet_offset)
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.x+self.getwidth()/2+(direction_x*times), self.y+self.getheight()/2+(direction_y*times), bullet_images['red'], direction_x, direction_y))
                        times += 5
                    self.bullet_angle += 0.3
                    if self.bullet_offset < 0.5:
                        self.bullet_offset += 0.01

                elif self.attack_count == 2 and self.cooldown_counter == 0:
                    self.cooldown_counter = 30
                    #shoot right
                    self.bullet_angle += random.uniform(0.0, 0.314)
                    for i in range(20):
                        direction_x = math.cos(self.bullet_angle)*(self.bulletvelocity)
                        direction_y = math.sin(self.bullet_angle)*(self.bulletvelocity)
                        bullet_list.append(Enemybulletclass(self.getcenter('x')+50, self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
                        self.bullet_angle += 0.314
                    self.bullet_angle = 0
                    #shoot left
                    for i in range(20):
                        direction_x = math.cos(self.bullet_angle)*(self.bulletvelocity)
                        direction_y = math.sin(self.bullet_angle)*(self.bulletvelocity)
                        bullet_list.append(Enemybulletclass(self.getcenter('x')-50, self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
                        self.bullet_angle += 0.314
                    self.bullet_angle = 0

                elif self.attack_count == 3:
                    #first attack
                    if self.cooldown_counter == 0:
                        self.cooldown_counter = 5

                        spawn_x = math.cos(self.bullet_angle)*50
                        spawn_y = math.sin(self.bullet_angle)*50

                        new_bullet = Enemybulletclass(self.getcenter('x')+spawn_x, self.getcenter('y')+spawn_y, bullet_images['red'], 0, 0)

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

                            bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['orange'], direction_x,direction_y,'orange'))

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
                bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
                self.bullet_angle += 0.1

            elif self.midstage_boss == False:
                if self.attack_count == 0:
                    if self.cooldown_counter == 0:
                        self.cooldown_counter = 3
                        spawn_y = 0
                        spawn_x = random.randrange(0, 468)
                        bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images[random.choice(self.bullet_image)], 0, self.bulletvelocity))
                    
                    if self.second_cooldown_counter == 0:
                        self.second_cooldown_counter = 30
                        spawn_y = 0
                        spawn_x = random.randrange(int(target.x), target.getwidth()+int(target.x))
                        bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images[random.choice(self.bullet_image)], 0, self.bulletvelocity))

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

                    bullet_list.append(Enemybulletclass(spawn_x, 0, bullet_images['red'], direction_x, direction_y))

                elif self.attack_count == 2 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    self.bullet_offset = 0
                    for i in range(27):
                        angle_in_radians = 0 + self.bullet_offset + self.bullet_angle
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
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
                    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['purple'], direction_x, direction_y))
                    
                    angle_in_radians = self.bullet_angle*-1
                    direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                    direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
                    
                    self.bullet_angle += 0.1

class Boss02(Bossclass):
    id = 'boss02'
    def __init__(self, image, midstage_boss):
        super().__init__(image, midstage_boss)
        #ship
        self.max_attacks = 5
        self.attack_count = 3
        #bullet
        self.ammo_count = 0
        self.bullet_angle = 0.0
        self.bullet_offset = 0.0
        self.shoot_dir = 'top right'
        self.shoot_right = True
        self.step = 0
        self.current_angle = 0

    def shoot(self, bullet_images, bullet_list, target):
        if self.ready_to_shoot:
            if self.midstage_boss and self.cooldown_counter == 0:
                self.cooldown_counter = 1
                #red bullets
                direction_x = math.cos(self.bullet_angle)*self.bulletvelocity
                direction_y = math.sin(self.bullet_angle)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
                #blue bullets
                direction_x = math.cos(self.bullet_angle+3.141)*self.bulletvelocity
                direction_y = math.sin(self.bullet_angle+3.141)*self.bulletvelocity
                bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
                self.bullet_angle += 0.1

            elif self.midstage_boss == False:
                if self.attack_count == 0 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    #sets shoot_dir
                    if self.shoot_dir == 'top left' and self.bullet_angle > 1.570:
                        self.shoot_dir = 'top right'
                        self.bullet_angle = 1.570 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'top right' and self.bullet_angle > 3.141:
                        self.shoot_dir = 'bottom right'
                        self.bullet_angle = 3.141 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'bottom right' and self.bullet_angle > 4.711:
                        self.shoot_dir = 'bottom left'
                        self.bullet_angle = 4.711 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'bottom left' and self.bullet_angle > 6.283:
                        self.shoot_dir = 'top left'
                        self.bullet_angle = random.uniform(0.0, 0.2)

                    #sets x and y
                    if self.shoot_dir == 'top left':
                        spawn_x = 0
                        spawn_y = 0
                    elif self.shoot_dir == 'top right':
                        spawn_x = 467
                        spawn_y = 0
                    elif self.shoot_dir == 'bottom right':
                        spawn_x = 467
                        spawn_y = 700
                    elif self.shoot_dir == 'bottom left':
                        spawn_x = 0
                        spawn_y = 700

                    direction_x = math.cos(self.bullet_angle)*self.bulletvelocity
                    direction_y = math.sin(self.bullet_angle)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images['red'], direction_x, direction_y))
                    self.bullet_angle += 0.2

                elif self.attack_count == 1 and self.cooldown_counter == 0:
                    self.cooldown_counter = 60
                    angle = random.uniform(0.0,6.283)
                    speed_offset = 0
                    for i in range(90):
                        direction_x = math.cos(angle)*(self.bulletvelocity+speed_offset)
                        direction_y = math.sin(angle)*(self.bulletvelocity+speed_offset)
                        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
                        speed_offset += 0.05
                        angle += 0.209

                elif self.attack_count == 2 and self.cooldown_counter == 0:
                    self.cooldown_counter = 20
                    self.bullet_angle = random.uniform(0.0, 0.627)
                    #finds the angle to player and sets target
                    angle_in_radians = math.atan2(target.getcenter('y')-self.getcenter('y'), target.getcenter('x')-self.getcenter('x'))
                    target_x = self.getcenter('x')+(math.cos(angle_in_radians)*100)
                    target_y = self.getcenter('y')+(math.sin(angle_in_radians)*100)
                    #makes bullet circle
                    for i in range(10):
                        bullet_x = self.getcenter('x')+(math.cos(self.bullet_angle)*50)
                        bullet_y = self.getcenter('y')+(math.sin(self.bullet_angle)*50)
                        #aims bullet to target
                        angle_in_radians = math.atan2(target_y-bullet_y, target_x-bullet_x)
                        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
                        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(bullet_x, bullet_y, bullet_images['red'], direction_x, direction_y))
                        self.bullet_angle += 0.627

                elif self.attack_count == 3:
                    if self.cooldown_counter == 0:
                        self.cooldown_counter = 1
                        if self.step == 0:
                            self.current_angle = angle_in_radians = math.atan2(target.y-self.getcenter('y'), target.x-self.getcenter('x'))
                        self.step += 5
                        spawn_x = math.cos(self.current_angle)*self.step
                        spawn_y = math.sin(self.current_angle)*self.step
                        random_angle = random.uniform(0.0, 6.283)
                        direction_x = math.cos(random_angle)*self.bulletvelocity
                        direction_y = math.sin(random_angle)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.getcenter('x')+spawn_x, self.getcenter('y')+spawn_y, bullet_images['red'], direction_x, direction_y))
                        if self.step > 800:
                            self.step = 0

                elif self.attack_count == 4 and self.cooldown_counter == 0:
                    self.cooldown_counter = 10
                    for i in range(30):
                        direction_x = math.cos(self.bullet_angle+self.bullet_offset)*self.bulletvelocity
                        direction_y = math.sin(self.bullet_angle+self.bullet_offset)*self.bulletvelocity
                        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
                        if self.shoot_right:
                            self.bullet_angle -= 0.209
                        else:
                            self.bullet_angle += 0.209
                    for i in range(30):
                        direction_x = math.cos(self.bullet_angle+self.bullet_offset)*(self.bulletvelocity+1)
                        direction_y = math.sin(self.bullet_angle+self.bullet_offset)*(self.bulletvelocity+1)
                        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
                        if self.shoot_right:
                            self.bullet_angle -= 0.209
                        else:
                            self.bullet_angle += 0.209

                    if self.shoot_right:
                        self.bullet_offset -= 0.07
                    else:
                        self.bullet_offset += 0.07

                    self.ammo_count += 1
                    if self.ammo_count == 5:
                        self.ammo_count = 0
                        self.cooldown_counter = 80
                        self.shoot_right = not self.shoot_right

                elif self.attack_count == 5 and self.cooldown_counter == 0:
                    self.cooldown_counter = 5
                    #sets shoot_dir
                    if self.shoot_dir == 'top left' and self.bullet_angle > 1.570:
                        self.shoot_dir = 'top right'
                        self.bullet_angle = 1.570 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'top right' and self.bullet_angle > 3.141:
                        self.shoot_dir = 'bottom right'
                        self.bullet_angle = 3.141 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'bottom right' and self.bullet_angle > 4.711:
                        self.shoot_dir = 'bottom left'
                        self.bullet_angle = 4.711 + random.uniform(0.0, 0.2)
                    elif self.shoot_dir == 'bottom left' and self.bullet_angle > 6.283:
                        self.shoot_dir = 'top left'
                        self.bullet_angle = random.uniform(0.0, 0.2)

                    #sets x and y
                    if self.shoot_dir == 'top left':
                        spawn_x = 0
                        spawn_y = 0
                    elif self.shoot_dir == 'top right':
                        spawn_x = 467
                        spawn_y = 0
                    elif self.shoot_dir == 'bottom right':
                        spawn_x = 467
                        spawn_y = 700
                    elif self.shoot_dir == 'bottom left':
                        spawn_x = 0
                        spawn_y = 700

                    direction_x = math.cos(self.bullet_angle)*self.bulletvelocity
                    direction_y = math.sin(self.bullet_angle)*self.bulletvelocity
                    bullet_list.append(Enemybulletclass(spawn_x, spawn_y, bullet_images['red'], direction_x, direction_y))
                    self.bullet_angle += 0.2

#set range to 32 to get a rainbow ring of people effekt
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

#kaneko flower spellcard
#first row
'''self.cooldown_counter = 120
#first layer
for number in range(5):#finds spawn angle
    spawn_angle = 1.570+6.283/5*(number+1)
    spawn_x = math.cos(spawn_angle)*80
    spawn_y = math.sin(spawn_angle)*80
    for i in range(41):
        direction_x = math.cos(spawn_angle-2.5+self.bullet_angle)
        direction_y = math.sin(spawn_angle-2.5+self.bullet_angle)
        bullet_list.append(Enemybulletclass(self.getcenter('x')+spawn_x+direction_x*70, self.getcenter('y')+spawn_y+direction_y*70, bullet_images['red'], direction_x*self.bulletvelocity*-1, direction_y*self.bulletvelocity*-1))
        self.bullet_angle += 0.125
    self.bullet_angle = 0
#second layer
for number in range(5):
    spawn_angle = 4.712+6.283/5*(number+1)
    spawn_x = math.cos(spawn_angle)*120
    spawn_y = math.sin(spawn_angle)*120
    for i in range(18):
        direction_x = math.cos(spawn_angle-1.413+self.bullet_angle)
        direction_y = math.sin(spawn_angle-1.413+self.bullet_angle)
        bullet_list.append(Enemybulletclass(self.getcenter('x')+spawn_x+direction_x*100, self.getcenter('y')+spawn_y+direction_y*100, bullet_images['blue'], direction_x*self.bulletvelocity*-1, direction_y*self.bulletvelocity*-1))
        self.bullet_angle += 0.157
    self.bullet_angle = 0
#third layer
for number in range(5):
    spawn_angle = 1.570+6.283/5*(number+1)
    spawn_x = math.cos(spawn_angle)*200
    spawn_y = math.sin(spawn_angle)*200
    for i in range(21):
        direction_x = math.cos(spawn_angle-1.570+self.bullet_angle)
        direction_y = math.sin(spawn_angle-1.570+self.bullet_angle)
        bullet_list.append(Enemybulletclass(self.getcenter('x')+spawn_x+direction_x*130, self.getcenter('y')+spawn_y+direction_y*130, bullet_images['green'], direction_x*self.bulletvelocity*-1, direction_y*self.bulletvelocity*-1))
        self.bullet_angle += 0.157
    self.bullet_angle = 0'''
#give to a stage 4 boss not a stage 3
'''self.cooldown_counter = 15
#random bullets back
for i in range(10):
    angle_in_radians = random.uniform(2.641,6.583)
    direction_x = math.cos(angle_in_radians)*(self.bulletvelocity+2)
    direction_y = math.sin(angle_in_radians)*(self.bulletvelocity+2)
    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
#sets bullet angle
if self.shoot_right:
    self.bullet_angle -= 0.05
else:
    self.bullet_angle += 0.05
#spawn left
direction_x = math.cos(1.570+self.bullet_angle)*self.bulletvelocity
direction_y = math.sin(1.570+self.bullet_angle)*self.bulletvelocity
bullet_list.append(Enemybulletclass(self.getcenter('x')-100, self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
bullet_list.append(Enemybulletclass(self.getcenter('x')-150, self.getcenter('y'), bullet_images['purple'], direction_x, direction_y))
bullet_list.append(Enemybulletclass(self.getcenter('x')-200, self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
#spawn right
direction_x = math.cos(1.570+self.bullet_angle)*self.bulletvelocity
direction_y = math.sin(1.570+self.bullet_angle)*self.bulletvelocity
bullet_list.append(Enemybulletclass(self.getcenter('x')+100, self.getcenter('y'), bullet_images['red'], direction_x, direction_y))
bullet_list.append(Enemybulletclass(self.getcenter('x')+150, self.getcenter('y'), bullet_images['purple'], direction_x, direction_y))
bullet_list.append(Enemybulletclass(self.getcenter('x')+200, self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
#checks if need to change angle
if self.shoot_right and self.bullet_angle < -1.570:
    self.shoot_right = False
    self.bullet_angle = 0
elif self.shoot_right == False and self.bullet_angle > 1.570:
    self.shoot_right = True
    self.bullet_angle = 0'''
#also give to a stage 4 boss
'''self.cooldown_counter = 10
for i in range(30):
    direction_x = math.cos(self.bullet_angle+self.bullet_offset)*self.bulletvelocity
    direction_y = math.sin(self.bullet_angle+self.bullet_offset)*self.bulletvelocity
    bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
    self.bullet_angle += 0.209
self.bullet_offset += 0.1'''

'''self.cooldown_counter = 60
    self.bullet_angle = 0
    for i in range(30):
        bullet_x = self.getcenter('x')+(math.cos(self.bullet_angle)*150)
        bullet_y = self.getcenter('y')+(math.sin(self.bullet_angle)*
        angle_in_radians = math.atan2(target.getcenter('y')-bullet_y, target.getcenter('x')-bullet_x)
        direction_x = math.cos(angle_in_radians)*self.bulletvelocity
        direction_y = math.sin(angle_in_radians)*self.bulletvelocity
        bullet_list.append(Enemybulletclass(bullet_x, bullet_y, bullet_images['red'], direction_x, direction_y))
        self.bullet_angle += 0
if self.second_cooldown_counter == 0:
    self.second_cooldown_counter = 30
    self.bullet_angle = random.uniform(0.0, 0.209)
    for i in range(30):
        direction_x = math.cos(self.bullet_angle)*self.bulletvelocity
        direction_y = math.sin(self.bullet_angle)*self.bulletvelocity
        bullet_list.append(Enemybulletclass(self.getcenter('x'), self.getcenter('y'), bullet_images['blue'], direction_x, direction_y))
        self.bullet_angle += 0.209'''