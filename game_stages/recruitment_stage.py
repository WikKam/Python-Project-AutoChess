import pygame
import static_resources as sr
from game_stages.shop_stage import shopping
from game_elements.gameElements import Player, Hero
import random
from static_resources import clock
from Utilities.recruitments_helper import is_clicked, recruitment_visualizer


def recruitment(current_player, network, screen):
    player_hero = None
    heroes = []
    while len(heroes) < 3:
        insert = sr.heroes[random.randint(0, 8)]
        if insert not in heroes:
            heroes.append(insert)
    heroes_display = [sr.create_image_with_size(heroes[i].icon, 150, 250) for i in range(0, 3)]
    start_time = pygame.time.get_ticks()
    recruitment_visualizer(screen, heroes_display, (sr.recruitment_time - (pygame.time.get_ticks()-start_time)//1000))
    running = True
    while running:
        timer = (sr.recruitment_time - (pygame.time.get_ticks() - start_time) // 1000)
        sr.timer_display(timer, 350, 400, screen, "recruitment")
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in range(len(heroes)):
                    if is_clicked(pos, i):
                        recruitment_visualizer(screen, heroes_display, timer, i)
                        player_hero = heroes[i]
        network.send(current_player)
        if timer == 0:
            if player_hero is None:
                player_hero = heroes[0]
            current_player.recruit_hero(player_hero)
            network.send(current_player)
            running = False
            shopping(current_player, network, screen)
