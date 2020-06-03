import pygame
import static_resources as sr
from game_stages.shop_and_combat_stage import shopping, create_image_with_size
from utilities.timer_helper import recruitment_time, timer_display
import random
from static_resources import clock
from gui.stages_visualiser import recruitment_visualizer
from game_elements.game_enums import PlayerState


def recruitment(current_player, network, screen):
    player_hero = None
    heroes = []
    while len(heroes) < 3:
        insert = sr.heroes[random.randint(0, 8)]
        if insert not in heroes:
            heroes.append(insert)
    heroes_display = [sr.create_image_with_size(heroes[i].icon, 150, 250) for i in range(0, 3)]
    start_time = pygame.time.get_ticks()
    recruitment_visualizer(screen, heroes_display, (recruitment_time - (pygame.time.get_ticks() - start_time) // 1000))
    running = True
    clicked_hero = None
    while running:
        timer = (recruitment_time - (pygame.time.get_ticks() - start_time) // 1000)
        timer_display(timer, 350, 400, screen, "recruitment")
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                current_player.recruit_hero(heroes[0])
                current_player.get_hero().current_hp = 0
                current_player.status = PlayerState.dead
                network.send(current_player)
                return True
            if e.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i in range(len(heroes)):
                    if is_clicked(pos, i):
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            clicked_hero = i
                            recruitment_visualizer(screen, heroes_display, timer, clicked_hero)
                            player_hero = heroes[i]
                            break
                        elif e.type == pygame.MOUSEMOTION:
                            show_hero_power(heroes, i, screen)
                            break
                    else:
                        recruitment_visualizer(screen, heroes_display, timer, clicked_hero)

        if timer == 0:
            if player_hero is None:
                player_hero = heroes[0]
            current_player.recruit_hero(player_hero)
            network.send(current_player)
            running = False
            pygame.time.delay(500)
            return False
            #shopping(current_player, network, screen)
        pygame.display.flip()


def show_hero_power(heroes, index, screen):
    img = create_image_with_size(heroes[index].hero_power.hover_icon, 200, 300)
    screen.blit(img, (160 + index * 175 + 100, 120))


def is_clicked(pos, hero_nr):
    x1 = pos[0]
    y1 = pos[1]
    return (160 + hero_nr * 175) <= x1 <= (310 + hero_nr * 175) and 120 <= y1 <= 370
