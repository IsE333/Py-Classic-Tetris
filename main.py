import gameLoop
import pygame
print("Tetris Pygame " + str(pygame.ver))
startLevel=input("Enter start level (0-29):")
gameloop = gameLoop.GameLoop(startLevel)
gameloop.loop()