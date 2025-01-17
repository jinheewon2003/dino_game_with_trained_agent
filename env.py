import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
DINO_WIDTH, DINO_HEIGHT = 40, 40
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 20, 40
DINO_X = 50
GROUND_HEIGHT = 300
OBSTACLE_Y = GROUND_HEIGHT - OBSTACLE_HEIGHT
FONT_SIZE = 24
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

class DinoGame(gym.Env):
    def __init__(self):
        super(DinoGame, self).__init__()
        self.state = None
        self.reward = 0
        self.action = {"duck": 2, "jump": 1, "do nothing": 0}
        self.action_space = spaces.Discrete(2) # TODO: Remember how actions were defined the gymnasium documentation? Replace with spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=SCREEN_WIDTH, shape=(3,), dtype=np.float32) # TODO: What is the observation space of the environment? Replace with spaces.Box(low=0, high=SCREEN_WIDTH, shape=(4,), dtype=np.float32)
        # dino_y, dino_velocity, obstacle_x

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Google Dino Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # TODO: Fill these in to represent the starting state of the game
        self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
        self.dino_velocity = 0
        self.is_jumping = False
        self.is_ducking = False
        self.obstacle_x = SCREEN_WIDTH
        self.obstacle_speed = -10
        self.reward = 0

        # TODO: What is the observation space of the environment? When we define the state, what is in it? Fill in the [] in the line below.
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x], dtype=np.float32)
        # dino_y, dino_velocity, obstacle_x

        return self.state, {}

    def step(self, action):
        """ Takes in the self (DinoGame environment) and an action (int) to take a step in the environment.
            self: DinoGame environment
            action: int action to take in the environment, where 0 is do nothing and 1 is jump and 2 is duck
        """

        # TODO: What are the two conditions for the dino to jump? 1. The action needs to be jumping and 2. The dino needs to be on the ground.
        # How can we represent that using existing variables in the envrionment?
        if action == 2 and self.is_jumping == False:
            self.is_ducking = True
            self.dino_y = GROUND_HEIGHT - (DINO_HEIGHT/2)
        else:
            self.is_ducking = False

        if self.dino_y > GROUND_HEIGHT - DINO_HEIGHT and action != 2:
            self.dino_y = GROUND_HEIGHT - DINO_HEIGHT

        if action == 1 and self.is_jumping == False:
            # TODO: What should the below twto variables be when we are jumping?
            self.is_jumping = True
            self.dino_velocity = -15

        # TODO: Check-in with me! What does this if statement do?
        if self.is_jumping:
            self.dino_y += self.dino_velocity
            self.dino_velocity += 1
            if self.dino_y >= GROUND_HEIGHT - DINO_HEIGHT:
                self.dino_y = GROUND_HEIGHT - DINO_HEIGHT
                self.is_jumping = False

        # Update obstacle
        self.obstacle_x += self.obstacle_speed
        if self.obstacle_x < 0:
            self.obstacle_x = SCREEN_WIDTH
            self.reward += 1

        # Check for collisions
        done = False
        # TODO: When does the dino collide with the obstacle? Use what needs to be true about the obstacle & dino's positions?
        if DINO_X + DINO_WIDTH >= self.obstacle_x and self.dino_y + DINO_HEIGHT >= OBSTACLE_Y:
            done = True

        # TODO: Update state and reward
        self.state = np.array([self.dino_y, self.dino_velocity, self.obstacle_x], dtype=np.float32)
        reward = 1 if not done else -100

        return self.state, reward, done, False, {}

    def render(self, mode="human"):
        self.screen.fill(WHITE)

        # TODO: Check in! Explain how you defined the state and reward above. Also explain to me what each line below does.
        pygame.draw.line(self.screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)
        if self.is_ducking:
            pygame.draw.rect(self.screen, BLACK, (DINO_X, self.dino_y, DINO_WIDTH, DINO_HEIGHT/2))
        else:
            pygame.draw.rect(self.screen, BLACK, (DINO_X, self.dino_y, DINO_WIDTH, DINO_HEIGHT))
        pygame.draw.rect(self.screen, RED, (self.obstacle_x, OBSTACLE_Y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        score_text = self.font.render(f"Score: {self.reward}", True, BLACK)

        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return self.screen

    def close(self):
        pygame.quit()
