import random
import pygame
from config import *  # 导入配置文件中的常量

# 初始化
pygame.init()


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()

        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.food = self._generate_food()
        self.score = 0
        self.steps = 0  # 记录蛇移动的步数

    def _generate_food(self):
        while True:
            # 生成食物的位置
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            # 确保食物不在蛇的身体上
            if food not in self.snake:
                return food

    def step(self, action=None):
        # 处理事件（手动模式时使用）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

        # 移动蛇头
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        # 碰撞检测
        if new_head in self.snake:
            return -10, True  # 撞自己，游戏结束
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self._generate_food()
            self.score += 1
            reward = 10
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
            reward = 0

        self.steps += 1  # 增加步数计数
        return reward, False

    def render(self):
        self.screen.fill(BLACK)
        # 绘制蛇
        for i, segment in enumerate(self.snake):
            x, y = segment
            if i == 0:  # 蛇头
                pygame.draw.circle(self.screen, BLUE, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                   GRID_SIZE // 2 - 1)
            else:
                pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        # 绘制食物
        fx, fy = self.food
        pygame.draw.rect(self.screen, RED, (fx * GRID_SIZE, fy * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # 显示当前最高分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 显示当前已行动步数
        steps_text = font.render(f"Steps: {self.steps}", True, WHITE)
        self.screen.blit(steps_text, (WIDTH - steps_text.get_width() - 10, 10))

        pygame.display.flip()
        self.clock.tick(10)  # 控制游戏速度


if __name__ == "__main__":
    game = SnakeGame()
    running = True
    while running:
        reward, done = game.step()
        game.render()
        if done:
            running = False
    pygame.quit()
