import pygame #Import the library

pygame.init() #Initialize pygame
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #Set the Display to the full screen
running = True

class Tile(pygame.sprite.Sprite): #Create a Tile Object that inherits from pygame sprites
    def __init__(self, isWall, x, y, filePath): #instantiate the class
        super().__init__() #Inherits from the sprite object
        self.image = pygame.image.load(filePath).convert_alpha() #Creates a rectangular tile
        self.rect = self.image.get_rect(center = placeTile(x, y)) #Places the rectangle at (x, y)

def placeTile(x, y):
    return (200 * x, 200 * y) #Adding one to x will place it 200 away (length of one tile)

tileMap = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
  [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
  [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
  [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
  [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
  [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
  [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
  [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
] #20x20 Tile Map

wallGroup = pygame.sprite.Group() #Create sprite groups
pathGroup = pygame.sprite.Group()

for row in range(len(tileMap)): #Iterate each row
    for column in range(len(tileMap[row])): #Iterate each column
        if tileMap[row][column] == 1: #Check if its a wall
            wallGroup.add(Tile(tileMap[row][column], row, column, "Textures/Slime Hill/Biome/wall.png")) #Add a wall at that position to the wall group
        else:
            pathGroup.add(Tile(tileMap[row][column], row, column, "Textures/Slime Hill/Biome/floor.png")) #Else add a path at that position

while running: #Create the game loop
    screen.fill((25, 25, 25))

    wallGroup.draw(screen)
    pathGroup.draw(screen)

    pygame.display.flip() #Updates and controls the game

    for event in pygame.event.get(): #Create the event handler
        if event.type == pygame.QUIT: #Check if the game has been quitted
            running = False

        if event.type == pygame.KEYDOWN: #Check if we press the key
            if event.key == pygame.K_KP_ENTER: #If we press keypad enter, we exit
                running = False

            if event.key == pygame.K_KP_PLUS: #If we press keypad plus, we take a screen shot
                pygame.image.save(screen, "menuPage.png")

    pygame.time.Clock().tick(60)