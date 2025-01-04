from game import run
from menu import runMenu
import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.NOFRAME) #Set the Display to the full screen
isPlaying = True
theme = 0 #Initialize with theme being Slime Hill

while isPlaying: #Have we quitted the game
    state, theme = runMenu(screen, theme) #run the menu
    if state: #If we selected to go to the menu
        state = run(screen, theme) #Start the game
        if state: #If they die normally
            continue #Go back to the menu
        else:
            isPlaying = False #They must of quitted the game and so we quit the program
    else:
        isPlaying = False #The player quitted the program so the game closes