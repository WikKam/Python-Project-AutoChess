import pygame
import static_resources as sr
from network import Network
from shop_stage import shopping
from gameElements import Minion, Player, Hero
# from gameElements import Tribe
# from gameElements import State
# from gameElements import Stats
import random


def is_clicked(pos, hero_nr):
    x1 = pos[0]
    y1 = pos[1]
    return (160 + hero_nr * 175) <= x1 <= (310 + hero_nr * 175) and 120 <= y1 <= 370


def recruitment_visualizer(screen, heroes, time, active=None):
    screen.blit(sr.recruitment_background, (0, 0))
    sr.timer_display(time, 350, 400, screen, "recruitment")
    if active is not None:
        pygame.draw.rect(screen, (255, 0, 0), (155 + active*175, 115, 160, 260))
    for i in range(len(heroes)):
        screen.blit(heroes[i], (160 + i * 175, 120))
    pygame.display.update()


def recruitment(players, current_player, n, clock, screen):
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
        n.send(players[current_player])
        if timer == 0:
            if player_hero is None:
                player_hero = heroes[0]
            players[current_player].recruit_hero(player_hero)
            n.send(players[current_player])
            running = False
            shopping(players, current_player, n, clock, screen)
