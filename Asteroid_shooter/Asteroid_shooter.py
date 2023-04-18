import pygame
import os
import random

pygame.init()
FPS = 60
VEL = 4
DIFFICULTY = 15  # higher is harder
WIDTH, HEIGHT = 800, 800
MAX_BULLETS = 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Set how big the window is
pygame.display.set_caption("Tap shot")  # Title of the application

SCORE_FONT = pygame.font.SysFont('comicsans', 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BULLET_SIZE = 10
TOWER_SIZE = 100
ENEMY_SIZE = 50

TOWER_HIT = pygame.USEREVENT + 1

TOWER_IMAGE = pygame.image.load(os.path.join('Assets', 'tower.png'))
TOWER = pygame.transform.scale(TOWER_IMAGE, (TOWER_SIZE, TOWER_SIZE))

ENEMY_IMAGE = pygame.image.load(os.path.join('Assets', 'asteroid.png'))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_SIZE, ENEMY_SIZE))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
BULLET = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'circle.png')), (BULLET_SIZE, BULLET_SIZE))


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.y_vel = VEL
        self.x_vel = VEL
        self.img = ENEMY
        self.destroyed = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def moveDown(self):
        self.y += self.y_vel

    def moveUp(self):
        self.y -= self.y_vel

    def moveRight(self):
        self.x += self.x_vel

    def moveLeft(self):
        self.x -= self.x_vel


    def draw(self, win):
        win.blit(ENEMY, (self.x, self.y))

    def collide(self, tower):
        tower_mask = tower.get_mask()
        enemy_mask = pygame.mask.from_surface(self.img)

        top_offset = (self.x - tower.x, self.y - round(tower.y)) # how far top 2 corners are away from each other

        t_point = tower_mask.overlap(enemy_mask, top_offset)


        if t_point:
            return True

        return False

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Towers:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TOWER_SIZE
        self.height = TOWER_SIZE
        self.img = TOWER

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(TOWER, (self.x, self.y))


class Bullets:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = 0
        self.bottom = 0
        self.width = BULLET_SIZE
        self.height = BULLET_SIZE
        self.y_vel = VEL
        self.x_vel = VEL
        self.img = BULLET

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(BULLET, (self.x, self.y))

    def moveDown(self):
        self.y += self.y_vel

    def moveUp(self):
        self.y -= self.y_vel

    def moveRight(self):
        self.x += self.x_vel

    def moveLeft(self):
        self.x -= self.x_vel

    def collide(self, enemy):
        enemy_mask = enemy.get_mask()
        bullet_mask = pygame.mask.from_surface(self.img)

        top_offset = (self.x - enemy.x, self.y - round(enemy.y))  # how far top 2 corners are away from each other

        t_point = enemy_mask.overlap(bullet_mask, top_offset)

        if t_point:
            return True

        return False

def randomDistanceNum(min, max):
    rngDistance = random.randint(min, max)
    return int(rngDistance)


def draw_window(win, main_tower, main_enemys_top, main_enemys_bottom, main_enemys_StartLeft,
                main_enemys_StartRight, bullets_up, bullets_down, bullets_left, bullets_right, tower_health):
    win.blit(SPACE, (0, 0))
    main_tower.draw(win)
    score_text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    health_text = SCORE_FONT.render(f"Health: {tower_health}", True, WHITE)
    WIN.blit(score_text, ((WIDTH-120) - score_text.get_width() // 2, 10))
    WIN.blit(health_text, (120 - score_text.get_width() // 2, 10))
    for enemy in main_enemys_top:
        enemy.draw(win)

    for enemy in main_enemys_bottom:
        enemy.draw(win)

    for enemy in main_enemys_StartLeft:
        enemy.draw(win)

    for enemy in main_enemys_StartRight:
        enemy.draw(win)

    for bullet in bullets_up:
        bullet.draw(win)

    for bullet in bullets_down:
        bullet.draw(win)

    for bullet in bullets_right:
        bullet.draw(win)

    for bullet in bullets_left:
        bullet.draw(win)

    pygame.display.update()

def handle_bullets_up(bullets_up, enemyUp, main_enemys_top):
    global score
    for bullet in bullets_up:
        try:
            if bullet.y < 0:
                bullets_up.remove(bullet)

            if bullet.collide(enemyUp):
                score += 1
                bullets_up.remove(bullet)
                enemyUp.y = -randomDistanceNum(1000, 9000)
                if len(main_enemys_top) >= DIFFICULTY:
                    main_enemys_top.pop(main_enemys_top.index(enemyUp))
                else:
                    main_enemys_top.append(
                        Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), -randomDistanceNum(10, 3010)))
        except ValueError:
            pass

def handle_bullets_down(bullets_down, enemyDown, main_enemys_bottom):
    global score
    for bullet in bullets_down:
        try:
            if bullet.y > HEIGHT:
                bullets_down.remove(bullet)

            if bullet.collide(enemyDown):
                score += 1
                bullets_down.remove(bullet)
                enemyDown.y = randomDistanceNum(1000, 9000)
                if len(main_enemys_bottom) >= DIFFICULTY:
                    main_enemys_bottom.pop(main_enemys_bottom.index(enemyDown))
                else:
                    main_enemys_bottom.append(
                        Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), randomDistanceNum(HEIGHT + 10, HEIGHT + 3810)))
        except ValueError:
            pass

def handle_bullets_left(bullets_left, enemyLeft, main_enemys_StartLeft):
    global score
    for bullet in bullets_left:
        try:
            if bullet.x < 0:
                bullets_left.remove(bullet)

            if bullet.collide(enemyLeft):
                score += 1
                bullets_left.remove(bullet)
                enemyLeft.x = -randomDistanceNum(1000, 9000)
                if len(main_enemys_StartLeft) >= DIFFICULTY:
                    main_enemys_StartLeft.pop(main_enemys_StartLeft.index(enemyLeft))
                else:
                    main_enemys_StartLeft.append(
                        Enemy(-randomDistanceNum(10, 3010), (HEIGHT // 2) - (ENEMY_SIZE // 2)))
        except ValueError:
            pass

def handle_bullets_right(bullets_right, enemyRight, main_enemys_StartRight):
    global score
    for bullet in bullets_right:
        try:
            if bullet.x > WIDTH:
                bullets_right.remove(bullet)

            if bullet.collide(enemyRight):
                score += 1
                bullets_right.remove(bullet)
                enemyRight.x = randomDistanceNum(1000, 9000)
                if len(main_enemys_StartRight) >= DIFFICULTY:
                    main_enemys_StartRight.pop(main_enemys_StartRight.index(enemyRight))
                else:
                    main_enemys_StartRight.append(
                        Enemy(randomDistanceNum(WIDTH + 10, WIDTH + 3810), (HEIGHT // 2) - (ENEMY_SIZE // 2)))
        except ValueError:
            pass

def draw_winner():
    draw_win_results = SCORE_FONT.render(f"Final Score: {score}", True, WHITE)
    WIN.blit(draw_win_results,
             (WIDTH // 2 - draw_win_results.get_width() // 2, HEIGHT // 2 - draw_win_results.get_height() // 2))
    pygame.display.update()  # Display text above
    pygame.time.delay(3000)  # Pause at the win results for a few seconds



def main():
    global score
    score = 0
    tower_health = 3
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    main_tower = Towers((WIDTH // 2) - (TOWER_SIZE // 2), (HEIGHT // 2) - (TOWER_SIZE // 2))
    main_enemys_top = [Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), -randomDistanceNum(100, 500))]
    main_enemys_bottom = [Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), randomDistanceNum(HEIGHT + 100, HEIGHT + 500))]
    main_enemys_StartLeft = [Enemy(-randomDistanceNum(100, 500), (HEIGHT // 2) - (ENEMY_SIZE // 2))]
    main_enemys_StartRight = [Enemy(randomDistanceNum(WIDTH + 100, WIDTH + 500), (HEIGHT // 2) - (ENEMY_SIZE // 2))]

    # Bullets
    bullets_up = []
    bullets_down = []
    bullets_left = []
    bullets_right = []

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == TOWER_HIT:
                tower_health -= 1


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and len(bullets_up) < MAX_BULLETS:
                    bullets_up.append(Bullets((WIDTH // 2) - (BULLET_SIZE // 2), (HEIGHT // 2) - (TOWER_SIZE // 2)))

                if event.key == pygame.K_s and len(bullets_down) < MAX_BULLETS:
                    bullets_down.append(Bullets((WIDTH // 2) - (BULLET_SIZE // 2), (HEIGHT // 2) + (TOWER_SIZE // 2)))

                if event.key == pygame.K_a and len(bullets_left) < MAX_BULLETS:
                    bullets_left.append(Bullets((WIDTH // 2) - (TOWER_SIZE // 2), (HEIGHT // 2) - (BULLET_SIZE // 2)))

                if event.key == pygame.K_d and len(bullets_right) < MAX_BULLETS:
                    bullets_right.append(Bullets((WIDTH // 2) + (TOWER_SIZE // 2), (HEIGHT // 2) - (BULLET_SIZE // 2)))

        for enemy in main_enemys_top:
            enemyUp = enemy
            enemy.moveDown()
            handle_bullets_up(bullets_up, enemyUp, main_enemys_top)
            if enemy.collide(main_tower):
                pygame.event.post(pygame.event.Event(TOWER_HIT))
                enemy.y = -randomDistanceNum(1000, 9000)
                if len(main_enemys_top) >= DIFFICULTY:
                    main_enemys_top.pop(main_enemys_top.index(enemy))
                else:
                    main_enemys_top.append(
                        Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), -randomDistanceNum(10, 3010)))

        for enemy in main_enemys_bottom:
            enemyDown = enemy
            enemy.moveUp()
            handle_bullets_down(bullets_down, enemyDown, main_enemys_bottom)
            if enemy.collide(main_tower):
                pygame.event.post(pygame.event.Event(TOWER_HIT))
                enemy.y = randomDistanceNum(1000, 9000)
                if len(main_enemys_bottom) >= DIFFICULTY:
                    main_enemys_bottom.pop(main_enemys_bottom.index(enemy))
                else:
                    main_enemys_bottom.append(
                        Enemy((WIDTH // 2) - (ENEMY_SIZE // 2), randomDistanceNum(HEIGHT + 10, HEIGHT + 3810)))

        for enemy in main_enemys_StartLeft:
            enemyLeft = enemy
            enemy.moveRight()
            handle_bullets_left(bullets_left, enemyLeft, main_enemys_StartLeft)
            if enemy.collide(main_tower):
                pygame.event.post(pygame.event.Event(TOWER_HIT))
                enemy.x = -randomDistanceNum(1000, 9000)
                if len(main_enemys_StartLeft) >= DIFFICULTY:
                    main_enemys_StartLeft.pop(main_enemys_StartLeft.index(enemy))
                else:
                    main_enemys_StartLeft.append(
                        Enemy(-randomDistanceNum(10, 3010), (HEIGHT // 2) - (ENEMY_SIZE // 2)))

        for enemy in main_enemys_StartRight:
            enemyRight = enemy
            enemy.moveLeft()
            handle_bullets_right(bullets_right, enemyRight, main_enemys_StartRight)
            if enemy.collide(main_tower):
                pygame.event.post(pygame.event.Event(TOWER_HIT))
                enemy.x = randomDistanceNum(1000, 9000)
                if len(main_enemys_StartRight) >= DIFFICULTY:
                    main_enemys_StartRight.pop(main_enemys_StartRight.index(enemy))
                else:
                    main_enemys_StartRight.append(
                        Enemy(randomDistanceNum(WIDTH + 10, WIDTH + 3810), (HEIGHT // 2) - (ENEMY_SIZE // 2)))

        for bullet in bullets_up:
            bullet.moveUp()

        for bullet in bullets_down:
            bullet.moveDown()

        for bullet in bullets_right:
            bullet.moveRight()

        for bullet in bullets_left:
            bullet.moveLeft()

        if tower_health == 0:
            # pass to draw window function first so health updates to 0 before the game ends
            draw_window(win, main_tower, main_enemys_top, main_enemys_bottom, main_enemys_StartLeft,
                    main_enemys_StartRight, bullets_up, bullets_down, bullets_left, bullets_right, tower_health)
            draw_winner()
            break
        draw_window(win, main_tower, main_enemys_top, main_enemys_bottom, main_enemys_StartLeft,
                    main_enemys_StartRight, bullets_up, bullets_down, bullets_left, bullets_right, tower_health)

    main()

if __name__ == "__main__":
    main()