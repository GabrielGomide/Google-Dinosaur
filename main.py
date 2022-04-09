import dis
from turtle import write
import pygame
import sys
import random
import time
from classes import *
from settings import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
width, height = 1000, 300
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Google Dino')

myfont = pygame.font.SysFont('Comic Sans MS', 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def create_high_score_file():
    if not os.path.exists('HIGH_SCORE'):
        with open('HIGH_SCORE', 'w') as f:
            f.write('0')

def get_high_score():
    with open('HIGH_SCORE', 'r') as f:
        return int(f.read())

def write_new_high_score(score):
    with open('HIGH_SCORE', 'w') as f:
        f.write(str(score))

def colliding(rect1, rect2):
    if not(rect1.x + rect1.width <= rect2. x or rect2.x + rect2.width <= rect1.x):
        if not(rect1.y + rect1.height <= rect2.y or rect2.y + rect2.height <= rect1.y):
            return True
    return False

def draw_window(player, cactus, birds, points, high_score, game_paused):
    surface.fill(WHITE)

    pygame.draw.line(surface, BLACK, (50, 250), (950, 250))
    surface.blit(player.get_image(), (player.x, player.y))

    for c in cactus:
        c_rect = c.get_rect()
        surface.blit(pygame.transform.scale(c.image, (c_rect.width, c_rect.height)), (c_rect.x, c_rect.y))

    for b in birds:
        b_rect = b.get_rect()
        surface.blit(pygame.transform.scale(b.image, (b_rect.width, b_rect.height)), (b_rect.x, b_rect.y))

    textsurface = myfont.render('HI {:05d} {:05d}'.format(high_score, points), False, BLACK)
    surface.blit(textsurface, (800,20))

    if game_paused:
        restart_text = myfont.render('Press \'space\' to restart', False, BLACK)
        text_rect = restart_text.get_rect(center=(width/2, 80))
        surface.blit(restart_text, text_rect)

    pygame.display.update()

def main():
    player = Player(150, 197, 50, 53, 7, dino)

    cactus = []
    birds = []

    current_speed = 5
    max_distance_between_obstacles = 70
    min_distance_between_obstacles = 70
    last_addition = 0
    last_obtacle_start = 0
    distance_for_next_obstacle = max_distance_between_obstacles

    clock = pygame.time.Clock()
    fps = 60

    iteration = 0
    start_time = time.time() * 1000
    points = 0

    game_paused = False

    create_high_score_file()
    high_score = get_high_score()

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.squat()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.raise_dino()
                    player.wait_to_squat = False

        key = pygame.key.get_pressed()

        if game_paused:
            if key[pygame.K_SPACE]:
                if points > get_high_score():
                    write_new_high_score(points)
                    high_score = points

                current_speed = 5
                max_distance_between_obstacles = 70
                min_distance_between_obstacles = max_distance_between_obstacles
                game_paused = False
                player.image = dino
                cactus = []
                birds = []
                start_time = time.time() * 1000
            continue

        player.handle_movement(key)

        if iteration == 0 or last_obtacle_start + distance_for_next_obstacle == iteration:
            last_obtacle_start = iteration
            distance_for_next_obstacle = random.randint(min_distance_between_obstacles, max_distance_between_obstacles)
            print(min_distance_between_obstacles, max_distance_between_obstacles, distance_for_next_obstacle)

            obstacle = random.randrange(1, 6)

            if obstacle != 5 or points < 400:
                rand = random.randrange(1, 4)
                if rand == 1:
                    cactus.append(Obstacle(850, 203, 35, 47, cactus01))
                elif rand == 2:
                    cactus.append(Obstacle(850, 212, 56, 38, cactus02))
                elif rand == 3:
                    cactus.append(Obstacle(850, 220, 67, 30, cactus03))
            else:
                rand = random.randrange(1, 4)
                if rand == 1:
                    birds.append(Obstacle(850, 205, 53, 33, bird01))
                elif rand == 2:
                    birds.append(Obstacle(850, 175, 53, 33, bird01))
                elif rand == 3:
                    birds.append(Obstacle(850, 145, 53, 33, bird01))

        if  iteration % 10 == 0:
            if not player.jumping and not player.falling:
                if player.down:
                    if player.image == dino_down_walking02 or player.image == dino_down:
                        player.image = dino_down_walking01
                    elif player.image == dino_down_walking01:
                        player.image = dino_down_walking02
                else:
                    if player.image == dino_walking02 or player.image == dino:
                        player.image = dino_walking01
                    elif player.image == dino_walking01:
                        player.image = dino_walking02

            for b in birds:
                if b.image == bird01:
                    b.image = bird02
                elif b.image == bird02:
                    b.image = bird01

        for e in cactus + birds:
            e.update(current_speed)

            player_rect = pygame.Rect(player.x + 15, player.y, 35, 53)
            if colliding(e.get_rect(), player_rect):
                player.raise_dino()
                player.image = dino_died
                game_paused = True 

            if e.x <= 50:
                if e in cactus:
                    cactus.remove(e)
                elif e in birds:
                    birds.remove(e)

        points = int(time.time() * 1000 - start_time) // 100

        if points % 100 == 0 and points != 0:
            pygame.mixer.Sound.play(point_sound)
            pygame.mixer.music.stop()

            if points != last_addition:
                last_addition = points

                if current_speed < 8:
                    current_speed += 1

                if min_distance_between_obstacles > 40:
                    min_distance_between_obstacles -= 10
                    max_distance_between_obstacles -= 5

        draw_window(player, cactus, birds, points, high_score, game_paused)
        iteration += 1

if __name__ == '__main__':
    main()
