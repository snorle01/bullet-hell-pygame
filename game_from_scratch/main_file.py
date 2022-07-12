from random import randrange
from classes import *
from functions import *
import pygame
import json
pygame.font.init()

height_of_window, width_of_window = 700, 700
game_screen_height, game_screen_width = 700, 467
side_menu_height, side_menu_width = 700, 233

game_window = pygame.display.set_mode((height_of_window, width_of_window))
pygame.display.set_caption('game test')

#Load images
backgroundimage = pygame.image.load('assets/background.png')

def main_game_loop():
    run = True
    FPS = 60
    fps_counter = 0
    stage_time = 0

    player_var = Playerclass()
    player_var.spawn(game_screen_width,game_screen_height)
    
    enemys_on_screen = []
    enemybullets_on_screen = []
    pointitems_on_screen = []

    backgroundscroll = 0

    bomb_sircle = 0
    bomb_on = False

    side_menu_font = pygame.font.SysFont(None, 50)

    #json
    json_file_open = open('stage1.json')
    json_file_data = json.load(json_file_open)

    def redraw_window():#remember that order of items drawn matters!
        #draw background
        game_window.blit(backgroundimage, (0,backgroundscroll))
        game_window.blit(backgroundimage, (0,backgroundscroll-backgroundimage.get_height()))

        #draw player and player bullets
        player_var.drawbullet(game_window)
        player_var.draw(game_window)
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            game_window.blit(player_var.hitboximage, (player_var.x+player_var.getwidth()/2-player_var.hitboximage.get_width()/2, player_var.y+player_var.getheight()/2-player_var.hitboximage.get_height()/2))

        #draw items
        for item in pointitems_on_screen:
            item.draw(game_window)

        #draw enemys and enemy bullets
        for bullet in enemybullets_on_screen:
            bullet.draw(game_window)
        for enemy in enemys_on_screen:
            enemy.draw(game_window)

        #draw_bomb_sircle
        if bomb_on == True:
            pygame.draw.circle(game_window, (255,255,255), [player_var.getcenter('x'), player_var.getcenter('y')], bomb_sircle, 3)

        #draw side menu
        pygame.draw.rect(game_window, (255, 0, 255), pygame.Rect(game_screen_width,0,side_menu_width,side_menu_height))
        score_label = side_menu_font.render(f'Score {player_var.score}', 1, (255,255,255))
        lives_label = side_menu_font.render(f'Lives {player_var.lives}', 1, (255,255,255))
        bombs_label = side_menu_font.render(f'Bombs {player_var.bombs}', 1, (255,255,255))

        game_window.blit(score_label, (game_screen_width+10, 10))
        game_window.blit(lives_label, (game_screen_width+10, 50))
        game_window.blit(bombs_label, (game_screen_width+10, 90))

        pygame.display.update()

    clock = pygame.time.Clock()
    
    while run:
        if backgroundscroll > backgroundimage.get_height():
            backgroundscroll = 0
        backgroundscroll += 1

        clock.tick(FPS)
        redraw_window()

        #counts seconds
        if fps_counter == 60:
            fps_counter = 0

            stage_time += 1
            second_passed = True
        else:
            second_passed = False

        fps_counter += 1
        

        if bomb_on == True:
            if bomb_sircle > 850:
                bomb_on = False
            else:
                bomb_sircle += 15

        #enemy shoot
        for enemy in enemys_on_screen:
            if enemy.cooldown_counter == 0:
                angle_offset = enemy.angle_offset
                for i in range(enemy.amount_of_bullets_shoot):
                    angle_offset += enemy.angle_spread
                    enemybullets_on_screen.append(enemy.shoot(player_var, angle_offset))

        #moves the players bullet depending on their velocity (player bullets can not yet shoot in angels)
        for bullet in player_var.bullets_on_screen:
            bullet.move()
            if bullet.y > game_screen_height or bullet.y+bullet.getheight() < 0 or bullet.x > game_screen_width or bullet.x+bullet.getwidth() < 0:
                player_var.bullets_on_screen.remove(bullet)
            #bullet collide with enemy
            for enemy in enemys_on_screen:
                if bullet.collide(enemy):
                    enemy.health -= 1
                    if enemy.health == 0:
                        for i in range(enemy.amount_of_item_to_drop):
                            pointitems_on_screen.append(enemy.drop_pointitem())
                        enemys_on_screen.remove(enemy)
                    if bullet in player_var.bullets_on_screen:
                        player_var.bullets_on_screen.remove(bullet)

        #moves the enemys bullet depending on their velocity
        for bullet in enemybullets_on_screen:
            bullet.move()
            if bullet.y > game_screen_height or bullet.y+bullet.getheight() < 0 or bullet.x > game_screen_width or bullet.x+bullet.getwidth() < 0:
                enemybullets_on_screen.remove(bullet)
            if bullet.collide(player_var):
                enemybullets_on_screen.remove(bullet)
                player_var.lives -= 1

        #moves the items
        for item in pointitems_on_screen:
            item.move()
            if item.y > game_screen_height:
                pointitems_on_screen.remove(item)
            if item.close_to_player(player_var) < 60:
                player_var.score += item.worth
                pointitems_on_screen.remove(item)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #arrow keys to move
        if player_var.can_move == True:
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if player_var.y+player_var.ship_velocity > height_of_window-player_var.getheight():
                    player_var.y = height_of_window-player_var.getheight()
                else:
                    player_var.y += player_var.ship_velocity
            if pygame.key.get_pressed()[pygame.K_UP]:
                if player_var.y - player_var.ship_velocity < 0:
                    player_var.y = 0
                else:
                    player_var.y -= player_var.ship_velocity
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if player_var.x + player_var.ship_velocity > game_screen_width-player_var.getwidth():
                    player_var.x = game_screen_width-player_var.getwidth()
                else:
                    player_var.x += player_var.ship_velocity
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if player_var.x - player_var.ship_velocity < 0:
                    player_var.x = 0
                else:
                    player_var.x -= player_var.ship_velocity
            #if player holds shift make ship slow down
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                player_var.ship_velocity = 3
            else:
                player_var.ship_velocity = 5
            #player shoot
            if pygame.key.get_pressed()[pygame.K_z]:
                player_var.shoot()
            #player bomb
            if pygame.key.get_pressed()[pygame.K_x] and player_var.activate_bomb():
                bomb_on = True
                bomb_sircle = 0
                enemybullets_on_screen.clear()
                enemys_on_screen.clear()
                player_var.bombs -= 1
        elif player_var.just_spawned == True:
            player_var.y -= 3
            if player_var.y < game_screen_height-player_var.getheight()-40:
                player_var.just_spawned = False
                player_var.can_move = True

        #move the enemy
        for enemy in enemys_on_screen:
            if enemy.move() == True:
                enemys_on_screen.remove(enemy)
            if enemy.collide(player_var):
                enemys_on_screen.remove(enemy)
                player_var.lives -= 1

        player_var.cool_down_function()
        for enemy in enemys_on_screen:
            enemy.cooldown_function()

        if second_passed == True:
            for enemy in json_file_data['enemy']:
                if enemy['time'] == stage_time:
                    new_enemy = Enemyclass(enemy['x'],enemy['y'],enemy['health'],enemy['cooldown'],enemy['worth'],enemy['items'], enemy['bullets'], enemy['angle_offset'], enemy['angle_spread'], enemy['path'])
                    enemys_on_screen.append(new_enemy)
                    for path in json_file_data['paths']:
                        new_enemy.goal_x = path[new_enemy.path][0]['x']
                        new_enemy.goal_y = path[new_enemy.path][0]['y']

main_game_loop()