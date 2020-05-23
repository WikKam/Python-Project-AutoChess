import pygame
from static_resources import create_image_with_size


def draw_scoreboard(players, curren_player, screen):
    scoreboard = []
    for player in players:
        if player.get_hero() is None:
            return
        scoreboard.append((player.id, player.get_hero().current_hp, player.get_hero().icon))
    scoreboard.sort(key=lambda x: x[1], reverse = True)
    print(scoreboard)
    for i, (id, hp, icon) in enumerate(scoreboard):
        if id == curren_player.id:
            active = create_image_with_size("images/heroes_portraits/Active.png", 90, 130)
            screen.blit(active, (710, 5 + 120 * i, 90, 130))
        img = create_image_with_size(icon, 80, 120)
        screen.blit(img, (715, 10 + 120 * i, 80, 120))
        if hp > 0:
            hp_font = pygame.font.Font('Fonts/Belwe Medium.otf', 30)
            screen.blit(hp_font.render(str(hp), True, (255, 255, 255)),  (730, 60 + 120 * i))
        else:
            skull = create_image_with_size("images/Skull.png", 70, 100)
            screen.blit(skull, (720, 20 + 120 * i, 70, 100))

