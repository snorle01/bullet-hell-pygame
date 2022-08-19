from random import randrange
from classes import *
from boss_classes import *
from functions import *
import pygame
import json
pygame.font.init()

#size of the entire window
height_of_window, width_of_window = 700, 700
#size of the game screen
game_screen_height, game_screen_width = 700, 467
#size of the side menu
side_menu_height, side_menu_width = 700, 233

game_window = pygame.display.set_mode((height_of_window, width_of_window))
pygame.display.set_caption('game test')

#Load images
#background image
backgroundimage = [pygame.image.load('assets/background0.png'), pygame.image.load('assets/background1.png')]

#sidemenu
heart_image = pygame.image.load('assets/heart.png')
empty_heart_image = pygame.image.load('assets/empty_heart.png')
heartpice1_image = pygame.image.load('assets/heartpice_1.png')
heartpice2_image = pygame.image.load('assets/heartpice_2.png')
bomb_image = pygame.image.load('assets/bomb.png')
empty_bomb_image = pygame.image.load('assets/empty_bomb.png')
bombpice1_image = pygame.image.load('assets/bombpice_1.png')
bombpice2_image = pygame.image.load('assets/bombpice_2.png')

#boss locator
boss_locator = pygame.image.load('assets/boss_locator.png')

def main_game_loop():
    run = True
    FPS = 60
    fps_counter = 0

    stage_time = 0
    stage_level = 1
    done_spawning_enemys = False
    stage_cleared = False
    stage_cleared_timer = 0

    fade_alpha = 0
    start_to_fade_game_screen = False
    fade_inn_or_out = 'inn'

    player_var = Playerclass()
    player_var.spawn(game_screen_width,game_screen_height)

    boss_var = None
    
    enemys_on_screen = []
    enemybullets_on_screen = []
    pointitems_on_screen = []
    poweritems_on_screen = []
    heartitems_on_screen = []
    bombitems_on_screen = []
    ghostitems_on_screen = []
    text_on_screen = []
    particles_on_screen = []

    backgroundscroll = 0

    side_menu_font = pygame.font.SysFont(None, 25)
    screen_font = pygame.font.SysFont(None, 50)

    #json
    json_file_enemy = json.load(open('enemys.json'))
    json_file_stage = json.load(open('stage1.json'))
    json_file_boss = json.load(open('boss.json'))

    enemy_list_turn = 0

    def redraw_window():#remember that order of items drawn matters!
        #draw background
        game_window.blit(backgroundimage[stage_level-1], (0,backgroundscroll))
        game_window.blit(backgroundimage[stage_level-1], (0,backgroundscroll-backgroundimage[stage_level-1].get_height()))

        if start_to_fade_game_screen:
            fade = pygame.Surface((game_screen_width, game_screen_height))
            fade.fill((0,0,0))
            fade.set_alpha(fade_alpha)
            game_window.blit(fade, (0, 0))

        #draw item collection
        if stage_time < 3:
            item_collection_label = screen_font.render('Item collection zone',1, (255,255,255))
            game_window.blit(item_collection_label, (game_screen_width/2-item_collection_label.get_width()/2, 250-item_collection_label.get_height()))
            pygame.draw.rect(game_window, (255,255,255),(0,250,game_screen_width,3))

        #draws boss
        if boss_var != None:
            boss_var.draw(game_window)

        #draw player, player bullets and player bomb
        player_var.draw(game_window, game_screen_width, game_screen_height)
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            game_window.blit(player_var.hitboximage, (player_var.getcenter('x')-player_var.hitboximage.get_width()/2, player_var.getcenter('y')-player_var.hitboximage.get_height()/2))

        #draw items
        for item in pointitems_on_screen:
            item.draw(game_window)
        for item in poweritems_on_screen:
            item.draw(game_window)
        for item in heartitems_on_screen:
            item.draw(game_window)
        for item in bombitems_on_screen:
            item.draw(game_window)
        for item in ghostitems_on_screen:
            item.draw(game_window)
        for text in text_on_screen:
            text.draw(game_window,)

        #draw enemys and enemy bullets
        for particle in particles_on_screen:
            particle.draw(game_window)
        for bullet in enemybullets_on_screen:
            bullet.draw(game_window)
        for enemy in enemys_on_screen:
            enemy.draw(game_window)

        #boss locator and health bar
        if boss_var != None:
            #boss locator
            game_window.blit(boss_locator, (boss_var.getcenter('x')-boss_locator.get_width()/2, game_screen_height-boss_locator.get_height()))

            #boss health bar
            if boss_var.midstage_boss == True:
                health_bar_full = game_screen_width-20
                health_bar_lenght = health_bar_full/(boss_var.max_health/boss_var.health)
                pygame.draw.rect(game_window, (255, 255, 255), (10, 10, health_bar_lenght, 5))
            elif boss_var.midstage_boss == False and boss_var.special_attack == False:
                health_bar_full = game_screen_width-120
                health_bar_lenght = health_bar_full/(boss_var.max_health/boss_var.health)
                #current healthbar
                pygame.draw.rect(game_window, (255, 255, 255), (110, 10, health_bar_lenght, 5))
                #decoration
                pygame.draw.rect(game_window, (255,255,255),(10,10,100,5))
                pygame.draw.rect(game_window, (0,0,255),(110,10,5,5))
            elif boss_var.special_attack == True:
                health_bar_full = 100
                health_bar_lenght = health_bar_full/(boss_var.max_health/boss_var.health)
                pygame.draw.rect(game_window, (255,255,255),(10,10, health_bar_lenght, 5))

        #draw side menu
        pygame.draw.rect(game_window, (255, 0, 255), (game_screen_width,0,side_menu_width,side_menu_height))
        score_label = side_menu_font.render(f'Score: {player_var.score}', 1, (255,255,255))

        #stage cleared text
        if stage_cleared:
            stage_cleared_label = screen_font.render('Stage cleared!', 1, (255,255,255))
            game_window.blit(stage_cleared_label, (game_screen_width/2-stage_cleared_label.get_width()/2, 250))
            if stage_cleared_timer > 120:
                stage_cleared_label_under = screen_font.render('Moving to next stage', 1, (255,255,255))
                game_window.blit(stage_cleared_label_under, (game_screen_width/2-stage_cleared_label_under.get_width()/2, 280))

        #lives label and hearts
        if player_var.god == True:
            lives_label = side_menu_font.render(f'Lives: God', 1, (255,255,255))
        else:
            lives_label = side_menu_font.render('Lives', 1, (255,255,255))
            offset = 0
            for i in range(8):
                if i+1 <= player_var.lives:
                    game_window.blit(heart_image, (game_screen_width+offset+70, 30))
                elif i == player_var.lives and player_var.heart_pice == 2:
                    game_window.blit(heartpice2_image, (game_screen_width+offset+70, 30))
                elif i == player_var.lives and player_var.heart_pice == 1:
                    game_window.blit(heartpice1_image, (game_screen_width+offset+70, 30))
                else:
                    game_window.blit(empty_heart_image, (game_screen_width+offset+70, 30))
                offset += heart_image.get_width()
        game_window.blit(lives_label, (game_screen_width+10, 30))

        #bombs label and bombs
        bombs_label = side_menu_font.render('Bombs', 1, (255,255,255))
        offset = 0
        for i in range(8):
            if i+1 <= player_var.bombs:
                game_window.blit(bomb_image, (game_screen_width+offset+70, 50))
            elif i == player_var.bombs and player_var.bomb_pice == 2:
                game_window.blit(bombpice2_image,(game_screen_width+offset+70, 50))
            elif i == player_var.bombs and player_var.bomb_pice == 1:
                game_window.blit(bombpice1_image,(game_screen_width+offset+70, 50))
            else:
                game_window.blit(empty_bomb_image, (game_screen_width+offset+70, 50))
            offset += bomb_image.get_width()
        game_window.blit(bombs_label, (game_screen_width+10, 50))

        if player_var.power == 0:
            power = '0.00'
        elif player_var.power < 10:
            power = '0.0'+str(player_var.power)
        elif player_var.power < 100:
            power = '0.'+str(player_var.power)
        else:
            player_power_string = str(player_var.power)
            power = player_power_string[0]+'.'+player_power_string[1:3]
        power_label = side_menu_font.render(f'Power: {power}', 1, (255,255,255))

        game_window.blit(score_label, (game_screen_width+10, 10))
        game_window.blit(power_label, (game_screen_width+10, 70))

        #fps counter
        fps_label = side_menu_font.render('FPS: '+ str(clock.get_fps())[0:4], 1, (255,255,255))
        game_window.blit(fps_label, (game_screen_width+10, game_screen_height-fps_label.get_height()-10))

        pygame.display.update()

    clock = pygame.time.Clock()
    
    while run:
        if backgroundscroll > backgroundimage[stage_level-1].get_height():
            backgroundscroll = 0
        backgroundscroll += 1

        clock.tick(FPS)
        redraw_window()

        #counts seconds
        if fps_counter == 60:
            fps_counter = 0

            if boss_var == None:
                stage_time += 1
            second_passed = True
        else:
            second_passed = False

        fps_counter += 1

        #start new stage
        if stage_cleared:
            stage_cleared_timer += 1
            if stage_cleared_timer == 180:
                start_to_fade_game_screen = True
            if fade_alpha == 255:
                stage_level += 1
                json_file_stage = json.load(open('stage'+str(stage_level)+'.json'))
                enemy_list_turn = 0
                stage_time = 0
                stage_cleared_timer = 0
                done_spawning_enemys = False
                stage_cleared = False

        #player dies
        if player_var.lives == 0 and player_var.god == False:
            run = False

        #boss shoot
        if boss_var != None and boss_var.ready_to_shoot:
            boss_var.shoot(enemybullets_on_screen, player_var)

        #enemy shoot
        for enemy in enemys_on_screen:
            enemy.shoot(player_var, enemybullets_on_screen)
        
        #moves the enemys bullet depending on their velocity
        for bullet in enemybullets_on_screen:
            bullet.move(enemybullets_on_screen, game_screen_height, game_screen_width)

        #move the enemy
        for enemy in enemys_on_screen:
            enemy.move(enemys_on_screen)

        #moves the boss
        if boss_var != None:
            boss_var.move()

        #moves the player bullet depending on their velocity (player bullets can not yet shoot in angels)
        for bullet in player_var.bullets_on_screen:
            bullet.move(game_screen_height, player_var.bullets_on_screen)

        #move the player bomb and kill enemys and their bullets and collects items when they touch the bomb
        enemy_returned = player_var.move_bomb(boss_var, enemys_on_screen, [pointitems_on_screen, poweritems_on_screen, heartitems_on_screen, bombitems_on_screen], [enemybullets_on_screen])
        if boss_var != None and boss_var.health == 0:
            if boss_var.die(enemybullets_on_screen, pointitems_on_screen, poweritems_on_screen, ghostitems_on_screen):
                boss_var = None
        if enemy_returned != None:
            enemys_on_screen.remove(enemy_returned)

        #move player
        player_var.move(game_screen_width, game_screen_height)

        #move text
        for text in text_on_screen:
            text.move()

        #player in item collection zone
        if player_var.y < 250:
            player_var.make_items_go_to_me([pointitems_on_screen, poweritems_on_screen, heartitems_on_screen, bombitems_on_screen])

        #player collide with enemy and their bullet
        player_var.collide_with_bullet_and_enemy(enemybullets_on_screen, enemys_on_screen)

        #player bullet collide with enemy and dies when health reaches 0
        for enemy in enemys_on_screen:
            enemy.collide_with_player_bullet(player_var.bullets_on_screen)
            if enemy.health == 0:
                enemy.die(enemys_on_screen, particles_on_screen, pointitems_on_screen, poweritems_on_screen, heartitems_on_screen, bombitems_on_screen)

        #boss collide with player bullets and dies when health reaches 0
        if boss_var != None:
            boss_var.collide_with_player_bullets(player_var.bullets_on_screen)
            if boss_var.health == 0:
                if boss_var.die(enemybullets_on_screen, pointitems_on_screen, poweritems_on_screen, ghostitems_on_screen):
                    boss_var = None

        #moves the items
        for item in pointitems_on_screen:
            item.move(player_var, game_screen_height, pointitems_on_screen, text_on_screen)
        for item in poweritems_on_screen:
            item.move(player_var, game_screen_height, poweritems_on_screen, text_on_screen)
        for item in heartitems_on_screen:
            item.move(player_var, game_screen_height, heartitems_on_screen, text_on_screen)
        for item in bombitems_on_screen:
            item.move(player_var, game_screen_height, bombitems_on_screen, text_on_screen)
        for item in ghostitems_on_screen:
            item.move(player_var, ghostitems_on_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #cooldown on every object that has it
        player_var.update(game_screen_width, game_screen_height, poweritems_on_screen)
        #changes the fade alpha variable dependig if it fades out or inn (also stops fading)
        if start_to_fade_game_screen:
            if fade_inn_or_out == 'inn':
                fade_alpha += 1
                if fade_alpha == 255:
                    fade_inn_or_out = 'out'
            else:
                fade_alpha -= 1
                if fade_alpha == 0:
                    start_to_fade_game_screen = False
                    fade_inn_or_out = 'inn'

        if boss_var != None:
            boss_var.update()
        for enemy in enemys_on_screen:
            enemy.cooldown_function()
        for text in text_on_screen:
            text.update(text_on_screen)
        for particle in particles_on_screen:
            particle.update(particles_on_screen)

        #reads json file
        if second_passed == True and boss_var == None:
            while json_file_stage['enemy'][enemy_list_turn]['time'] == stage_time and done_spawning_enemys == False:
                if 'respawn_turn_off' in json_file_stage['enemy'][enemy_list_turn]:
                    for enemy in enemys_on_screen:
                        enemy.respawn = False
                #spawns boss (need to make it compatibale with diffrent bosses)
                elif 'spawnboss' in json_file_stage['enemy'][enemy_list_turn]:
                    json_boss = json_file_stage['enemy'][enemy_list_turn]
                    if json_boss['boss_id'] == 0:
                        boss_var = Boss00(json_boss['midstage_boss'])
                        if boss_var.midstage_boss:
                            type_of_boss = 'midstage'
                        else:
                            type_of_boss = 'boss'
                        boss_var.max_health = json_file_boss['boss00'][0][type_of_boss][0]['health']
                        boss_var.health = boss_var.max_health
                        boss_var.bulletvelocity = json_file_boss['boss00'][0][type_of_boss][0]['bulletvelocity']
                        boss_var.special_attack = json_file_boss['boss00'][0][type_of_boss][0]['special']
                    boss_var.spawn(game_screen_width)

                elif 'clear' in json_file_stage['enemy'][enemy_list_turn]:
                    enemys_on_screen.clear()
                    enemybullets_on_screen.clear()
                elif 'stage_clear' in json_file_stage['enemy'][enemy_list_turn]:
                    stage_cleared = True
                    done_spawning_enemys = True
                else:
                    #spawns enemy
                    stage_json = json_file_stage['enemy'][enemy_list_turn]
                    enemy_json = json_file_enemy[stage_json['enemy']][0]
                    new_enemy = Enemyclass(stage_json['x'],stage_json['y'],enemy_json['health'], stage_json['enemy'],enemy_json['image'],enemy_json['speed'],enemy_json['cooldown'],enemy_json['worth'],enemy_json['items'],enemy_json['bullets'],enemy_json['ammo'],enemy_json['angle_offset'],enemy_json['angle_spread'],stage_json['path'])

                    if json_file_stage['paths'][0][stage_json['path']][0]['x'] == 'relative':
                       new_enemy.goal_x = new_enemy.x
                    else:
                        new_enemy.goal_x = json_file_stage['paths'][0][stage_json['path']][0]['x']

                    if json_file_stage['paths'][0][stage_json['path']][0]['y'] == 'relative':
                       new_enemy.goal_y = new_enemy.y
                    else:
                        new_enemy.goal_y = json_file_stage['paths'][0][stage_json['path']][0]['y']

                    if 'shoot' in json_file_stage['paths'][0][stage_json['path']][0]:
                        new_enemy.ready_to_shoot = json_file_stage['paths'][0][stage_json['path']][0]['shoot']
                    enemys_on_screen.append(new_enemy)

                    if 'respawn' in json_file_stage['enemy'][enemy_list_turn]:
                        new_enemy.respawn = True

                    if 'item' in json_file_stage['enemy'][enemy_list_turn]:
                        new_enemy.item = json_file_stage['enemy'][enemy_list_turn]['item']

                if len(json_file_stage['enemy']) > enemy_list_turn+1:
                    enemy_list_turn += 1
                else:
                    enemy_list_turn = 0
                    done_spawning_enemys = True   
        
        #end of while loop
main_game_loop()