import pygame
from pygame.locals import *
import random
from enum import Enum
from collections import namedtuple
pygame.init()

font = pygame.font.SysFont('arial',25)
class Direction(Enum):
    UP =  1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

Point = namedtuple('Point', "x, y")

BLOCK_SIZE = 20
SPEED = 20

#rgb colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
RED = (200,0,0)

class SnakeGame():
    def __init__(self, w = 640, h=400) -> None:
        self.w = w
        self.h = h
        
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("snake game")
        self.clock = pygame.time.Clock()
        #init snake
        self.direction = Direction.UP
        self.head = Point(w//2, h//2)
        self.snake = [self.head , Point(self.head.x - BLOCK_SIZE, self.head.y), Point(self.head.x - BLOCK_SIZE , self.head.y)];
        #init game state
        self.score = 0
        self.food = None
        self._place_food()
    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        else:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)
    
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            # pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x , self.food.y , BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render('score: ' + str(self.score) , True, WHITE)
        self.display.blit(text, [0 , 0])
        pygame.display.flip()
        
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE)// BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)// BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        
        if self.food in self.snake:
            self._place_food()
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # hits itself
        if self.head in self.snake[1: ]:
            return True
        
        return False
    
    def play_step(self):
        # collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                
                    
        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # check if it game over
        game_over = False
        
        if self._is_collision():
            game_over = True
            return game_over , self.score
        
        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
            
        # update the UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # return game over and game score
        game_over = False
        return game_over, self.score
        
if __name__ == "__main__" :
    pygame.init()
    snake_game = SnakeGame()
    
    while True:
        game_over, score = snake_game.play_step()
        if game_over:
            print("game over and your final score is : ", score)
            break;
    pygame.quit()
    
    
    