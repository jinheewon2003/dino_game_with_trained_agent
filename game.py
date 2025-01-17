from env import DinoGame
import pygame

if __name__ == "__main__":
    env = DinoGame()
    done = False
    obs, _ = env.reset()

    # Instructions
    print("Press SPACE to jump. Close the game window to exit.")

    ducking = False
    
    while not done:
        env.render()
        action = 0 # do nothing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # TODO: When is the action to jump?
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # TODO: How can we express the action to jump?
                action = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                # TODO: How can we express the action to duck?
                ducking = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                ducking = False
        
        if ducking:
            action = 2

        # TODO: Think back at the Q-learning notebook. What do we need to do to go from one state to another?
        obs, reward, done, truncated, info = env.step(action)

    env.close()