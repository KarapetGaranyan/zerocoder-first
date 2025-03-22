import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBJECT_SIZE = 30
PLAYER_SPEED = 5
OBJECT_SPEED_BASE = 7
SPAWN_RATE_BASE = 30  # Чем меньше число, тем чаще появляются объекты
MAX_HEALTH = 100
LEVEL_SCORE = 300  # Очки для перехода на следующий уровень

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Летная миссия")

# Загрузка фонов для уровней
backgrounds = [
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),  # Уровень 1 - черный фон
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),  # Уровень 2 - синий фон
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)),  # Уровень 3 - красный фон
    pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Уровень 4 - зеленый фон
]

backgrounds[0].fill(BLACK)
backgrounds[1].fill((50, 50, 150))  # Темно-синий
backgrounds[2].fill((150, 50, 50))  # Темно-красный
backgrounds[3].fill((50, 150, 50))  # Темно-зеленый

# Создание облаков на фоне
for bg in backgrounds[1:]:  # Начиная со второго уровня добавляем облака
    for _ in range(20):
        cloud_size = random.randint(30, 60)
        cloud_x = random.randint(0, SCREEN_WIDTH - cloud_size)
        cloud_y = random.randint(0, SCREEN_HEIGHT - cloud_size)
        cloud_rect = pygame.Rect(cloud_x, cloud_y, cloud_size, cloud_size // 2)
        cloud_color = (255, 255, 255, 150)  # Белый цвет с прозрачностью
        pygame.draw.ellipse(bg, cloud_color, cloud_rect)


# Функция для отображения текста
def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# Класс игрока
class Player:
    def __init__(self):
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLUE, [(0, PLAYER_SIZE // 2),
                                               (PLAYER_SIZE, PLAYER_SIZE // 2),
                                               (PLAYER_SIZE // 2, 0)])
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speedy = 0
        self.health = MAX_HEALTH
        self.score = 0
        self.level = 1

    def update(self):
        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speedy = -PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
            self.speedy = PLAYER_SPEED
        else:
            self.speedy = 0

        # Обновление позиции
        self.rect.y += self.speedy

        # Ограничение движения игрока в пределах экрана
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Проверка на переход на следующий уровень
        if self.score >= LEVEL_SCORE * self.level and self.level < len(backgrounds):
            self.level += 1
            self.health = MAX_HEALTH  # Восстанавливаем здоровье при переходе на новый уровень
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # Отрисовка полоски здоровья
        health_rect = pygame.Rect(self.rect.x, self.rect.y - 10,
                                  self.rect.width * (self.health / MAX_HEALTH), 5)
        pygame.draw.rect(surface, GREEN, health_rect)
        pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y - 10,
                                          self.rect.width, 5), 1)


# Базовый класс для объектов (враги и аптечки)
class GameObject:
    def __init__(self, x, y, is_enemy, level):
        self.image = pygame.Surface((OBJECT_SIZE, OBJECT_SIZE), pygame.SRCALPHA)
        self.is_enemy = is_enemy

        if is_enemy:
            pygame.draw.circle(self.image, RED, (OBJECT_SIZE // 2, OBJECT_SIZE // 2), OBJECT_SIZE // 2)
            self.health_effect = -20 - (level * 5)  # Враги наносят больше урона на высоких уровнях
        else:
            # Рисуем аптечку (крест)
            pygame.draw.rect(self.image, GREEN, (0, 0, OBJECT_SIZE, OBJECT_SIZE))
            pygame.draw.rect(self.image, WHITE, (OBJECT_SIZE // 4, OBJECT_SIZE // 2 - 3,
                                                 OBJECT_SIZE // 2, 6))
            pygame.draw.rect(self.image, WHITE, (OBJECT_SIZE // 2 - 3, OBJECT_SIZE // 4,
                                                 6, OBJECT_SIZE // 2))
            self.health_effect = 30  # Аптечки добавляют здоровье

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = -(OBJECT_SPEED_BASE + level * 2)  # Скорость объектов увеличивается с уровнем

    def update(self):
        self.rect.x += self.speedx
        # Если объект вышел за левую границу экрана, он уничтожается
        if self.rect.right < 0:
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Функция отображения перехода на новый уровень
def show_level_transition(level):
    screen.fill(BLACK)
    draw_text(f"УРОВЕНЬ {level}", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    if level == 1:
        level_description = "Лес"
    elif level == 2:
        level_description = "Горы"
    elif level == 3:
        level_description = "Пустыня"
    elif level == 4:
        level_description = "Арктика"
    else:
        level_description = "???"

    draw_text(f"{level_description}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Нажмите любую клавишу для продолжения", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
    pygame.display.flip()

    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


# Стартовый экран
def show_start_screen():
    screen.fill(BLACK)
    draw_text("ЛЕТНАЯ МИССИЯ", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Используйте стрелки вверх и вниз для управления", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Собирайте аптечки и избегайте врагов", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
    draw_text("Нажмите любую клавишу для начала", 18, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()

    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


# Экран окончания игры
def show_game_over_screen(score, level):
    screen.fill(BLACK)
    draw_text("ИГРА ОКОНЧЕНА", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(f"Ваш счет: {score}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(f"Уровень: {level}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    draw_text("Нажмите R для перезапуска или ESC для выхода", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()

    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return True  # Перезапуск игры
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Основная функция игры
def game():
    show_start_screen()

    # Создание объектов игры
    player = Player()
    objects = []
    clock = pygame.time.Clock()
    spawn_counter = 0
    game_over = False

    # Показываем первый уровень
    show_level_transition(player.level)

    # Основной игровой цикл
    while not game_over:
        # Текущие параметры уровня
        current_level = player.level
        current_spawn_rate = max(5, SPAWN_RATE_BASE - (current_level * 5))  # Увеличение частоты спавна с уровнем

        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Обновление игрока
        if player.update():
            # Переход на новый уровень
            objects.clear()  # Очищаем все объекты при переходе на новый уровень
            show_level_transition(player.level)

        # Создание новых объектов
        spawn_counter += 1
        if spawn_counter >= current_spawn_rate:
            # Решаем, создать врага или аптечку (шанс врага увеличивается с уровнем)
            enemy_chance = 0.6 + (current_level * 0.05)
            is_enemy = random.random() < enemy_chance

            # Создаем объект в случайной позиции по Y
            new_object = GameObject(SCREEN_WIDTH, random.randint(50, SCREEN_HEIGHT - 50), is_enemy, current_level)
            objects.append(new_object)
            spawn_counter = 0

        # Обновление объектов и проверка коллизий
        for obj in objects[:]:
            if obj.update():
                objects.remove(obj)
                continue

            # Проверка коллизий с игроком
            if player.rect.colliderect(obj.rect):
                player.health += obj.health_effect
                player.health = min(MAX_HEALTH, player.health)  # Не превышаем максимальное здоровье

                # Увеличиваем счет при столкновении с аптечкой
                if not obj.is_enemy:
                    player.score += 10 * current_level  # Больше очков на высоких уровнях

                objects.remove(obj)

        # Проверка на проигрыш
        if player.health <= 0:
            game_over = True

        # Очистка экрана и отрисовка фона текущего уровня
        screen.blit(backgrounds[min(current_level - 1, len(backgrounds) - 1)], (0, 0))

        # Отрисовка объектов
        for obj in objects:
            obj.draw(screen)

        # Отрисовка игрока
        player.draw(screen)

        # Отображение здоровья, счета и уровня
        draw_text(f"Здоровье: {player.health}", 30, 100, 10)
        draw_text(f"Счет: {player.score}", 30, 700, 10)
        draw_text(f"Уровень: {current_level}", 30, 400, 10)

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

    # Экран окончания игры и возможность перезапуска
    if show_game_over_screen(player.score, player.level):
        game()  # Перезапуск игры


# Запуск игры
if __name__ == "__main__":
    game()