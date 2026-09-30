import pygame
from .snake import Snake
from .food import Food

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size
        )

        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size
        )

        self.score = 0

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.message_font = pygame.font.SysFont("Arial", 30)

        # Difficulty speeds
        self.difficulty_speeds = {
            "Easy": 5,
            "Medium": 8,
            "Hard": 12
        }

        self.difficulty = "Medium"
        self.moves_per_second = self.difficulty_speeds[self.difficulty]

        self._frame_counter = 0

        self.game_over = False
        self.selecting_difficulty = False

    def handle_keydown(self, key):

        # -----------------------------
        # GAME OVER / DIFFICULTY INPUT
        # -----------------------------
        if self.game_over:

            # First press ENTER to open difficulty selection
            if not self.selecting_difficulty:
                if key == pygame.K_RETURN:
                    self.selecting_difficulty = True
                return

            # Difficulty selection
            if key in (pygame.K_1, pygame.K_KP1):
                self.start_new_game("Easy")

            elif key in (pygame.K_2, pygame.K_KP2):
                self.start_new_game("Medium")

            elif key in (pygame.K_3, pygame.K_KP3):
                self.start_new_game("Hard")

            return

        # -----------------------------
        # NORMAL GAME INPUT
        # -----------------------------
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)

        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)

        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)

        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def start_new_game(self, difficulty):
        """Reset the game and start a new round."""

        self.difficulty = difficulty
        self.moves_per_second = self.difficulty_speeds[difficulty]

        # Reset snake
        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size
        )

        # Reset food
        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size
        )

        # Reset game state
        self.score = 0
        self._frame_counter = 0
        self.game_over = False
        self.selecting_difficulty = False

    def handle_input(self):
        pass

    def update(self):
        # Do nothing while Game Over screen is displayed
        if self.game_over:
            return

        self._frame_counter += 1

        frames_per_move = max(
            1,
            60 // self.moves_per_second
        )

        if self._frame_counter < frames_per_move:
            return

        self._frame_counter = 0

        self.snake.move()

        # Wall collision
        if self.snake.collides_with_wall(
            self.grid_width,
            self.grid_height
        ):
            self.game_over = True
            return

        # Self collision
        if self.snake.collides_with_self():
            self.game_over = True
            return

        # Food collision
        if self.snake.head_rect().colliderect(
            self.food.rect()
        ):
            self.snake.grow()
            self.score += 1
            self.food.respawn(self.snake.body)

    def render(self, screen):

        # -----------------------------
        # NORMAL GAME
        # -----------------------------

        # Draw food
        pygame.draw.rect(
            screen,
            RED,
            self.food.rect()
        )

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(
                screen,
                GREEN,
                rect
            )

        # Draw score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(score_text, (10, 10))

        # -----------------------------
        # GAME OVER SCREEN
        # -----------------------------

        if self.game_over:

            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                WHITE
            )

            final_score_text = self.message_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            game_over_rect = game_over_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 100
                )
            )

            final_score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 30
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            # First screen: press ENTER
            if not self.selecting_difficulty:

                continue_text = self.message_font.render(
                    "Press ENTER to continue",
                    True,
                    WHITE
                )

                continue_rect = continue_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 50
                    )
                )

                screen.blit(
                    continue_text,
                    continue_rect
                )

            # Difficulty selection screen
            else:

                difficulty_title = self.message_font.render(
                    "Choose Difficulty",
                    True,
                    WHITE
                )

                easy_text = self.message_font.render(
                    "1 - Easy",
                    True,
                    WHITE
                )

                medium_text = self.message_font.render(
                    "2 - Medium",
                    True,
                    WHITE
                )

                hard_text = self.message_font.render(
                    "3 - Hard",
                    True,
                    WHITE
                )

                title_rect = difficulty_title.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 30
                    )
                )

                easy_rect = easy_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 80
                    )
                )

                medium_rect = medium_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 120
                    )
                )

                hard_rect = hard_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 160
                    )
                )

                screen.blit(
                    difficulty_title,
                    title_rect
                )

                screen.blit(
                    easy_text,
                    easy_rect
                )

                screen.blit(
                    medium_text,
                    medium_rect
                )

                screen.blit(
                    hard_text,
                    hard_rect
                )
