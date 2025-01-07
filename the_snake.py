import pygame
import sys
from random import randint
from typing import Tuple

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position: Tuple[int, int] = None):
        """Инициализирует объект с заданной позицией."""
        self.position = position if position else (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        self.body_color = None

    def draw(self, surface: pygame.Surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализирует яблоко с случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )

    def draw(self, surface: pygame.Surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует змейку с начальной позицией и направлением."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)  # Начальное направление: вправо
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % SCREEN_WIDTH,
            (head_y + dy) % SCREEN_HEIGHT
        )

        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None

    def draw(self, surface: pygame.Surface):
        """Отрисовывает змейку на поверхности."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

        if self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


def handle_keys(snake: Snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                snake.next_direction = (0, -GRID_SIZE)
            elif (event.key == pygame.K_DOWN
                  and snake.direction != (0, -GRID_SIZE)):
                snake.next_direction = (0, GRID_SIZE)
            elif (event.key == pygame.K_LEFT
                  and snake.direction != (GRID_SIZE, 0)):
                snake.next_direction = (-GRID_SIZE, 0)
            elif (event.key == pygame.K_RIGHT
                  and snake.direction != (-GRID_SIZE, 0)):
                snake.next_direction = (GRID_SIZE, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
