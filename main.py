import pygame #Import the library
from random import choice

pygame.init() #Initialize pygame
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #Set the Display to the full screen
running = True

def exists(neighbourList, x, y, direction):
    if 0 <= x < len(tileMap): #Perform a validation check to see if its properly within the grid
        if 0 <= y < len(tileMap[x]):
            if tileMap[x][y] == 0: #Check its neighbour is a path
                neighbourList.append((x, y, direction)) #Add it to the list

class Node:
    def __init__(self, x, y):
        self.id = (x, y) #Each Node has a unique identifier
        self.neighbours = []
        exists(self.neighbours, x + 1, y, "up") #Iterate though each of the 4 neighbours
        exists(self.neighbours, x - 1, y, "down")
        exists(self.neighbours, x, y + 1, "right")
        exists(self.neighbours, x, y - 1, "left")

    def giveNeighour(self):
        return choice(self.neighbours)[2] #Returns the direction that is possible

class Graph:
    def __init__(self): #The graph acts as a collection of nodes
        self.graph = []

    def addNode(self, node): #Add nodes to the graph
        self.graph.append(node)

    def findNode(self, nodeID): #Locate node within the graph
        for node in self.graph:
            if node.id == nodeID:
                return node

class Tile(pygame.sprite.Sprite): #Create a Tile Object that inherits from pygame sprites
    def __init__(self, x, y, filePath): #instantiate the class
        super().__init__() #Inherits from the sprite object
        self.image = pygame.image.load(filePath).convert_alpha() #Creates a rectangular tile
        self.rect = self.image.get_rect(center = placeTile(x, y)) #Places the rectangle at (x, y)
        self.velocity = 5

    def update(self, dx, dy):
        self.rect.x -= dx * self.velocity #updates x position
        self.rect.y += dy * self.velocity #updates y position

def placeTile(x, y):
    return (200 * x, 200 * y) #Adding one to x will place it 200 away (length of one tile)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 200, 200))
        self.rect = self.image.get_rect(center = (x, y))
        self.isAttacking = False

    def attack(self):
        if not(self.isAttacking): #If we are not attacking already
            self.attackBox = AttackBox(*self.rect.midleft) #Create an AttackBox
            self.isAttacking = True #Now we are attacking
            attackBoxGroup.add(self.attackBox)

    def update(self):
        if self.isAttacking: #If we are in an attack (the box exists)
            flag = self.attackBox.update() #Update the attack box and return the state
            if flag: #If we are given True, that means we need to kill the attack box
                attackBoxGroup.remove(self.attackBox) #Delete the Box
                del self.attackBox #Kills the attack box
                self.isAttacking = False #Set the attack to False (allowing us to attack again)

class AttackBox(pygame.sprite.Sprite): #Create an AttackBox, any enemy that collides with this will die
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 255, 255)) #Fill for debugging purposes
        self.rect = self.image.get_rect(midright = (x, y))
        self.counter = 0 #Have a counter to check it in for 5 frames

    def update(self):
        self.counter += 1 #Increment the counter
        if self.counter == 5: #When it reaches 5 (5 frames have passed)
            return True #Tell the Player object to kill the attack box
        else:
            return False #Tell the Player not to kill the attack box

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, nodeID): #Instantiate Enemy Object
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.currentNode = nodeID
        self.targetX = 0
        self.targetY = 0
        self.moved = False
        self.move()

    def update(self, dx, dy):
        self.rect.x -= dx * self.velocity #updates x position
        self.rect.y += dy * self.velocity #updates y position

    def move(self):
        if not(self.moved):
            n = graph.findNode(self.currentNode) #Get the current node that the enemy is at
            direction = n.giveNeighour() #Find next direction to travel in
            if direction == "up":
                self.targetX = -200 #Check each direction and set the target accordingly
                self.currentNode = (self.currentNode[0] + 1, self.currentNode[1])
            elif direction == "down":
                self.targetX = 200
                self.currentNode = (self.currentNode[0] - 1, self.currentNode[1])
            elif direction == "right":
                self.targetY = -200
                self.currentNode = (self.currentNode[0], self.currentNode[1] + 1)
            elif direction == "left":
                self.targetY = 200
                self.currentNode = (self.currentNode[0], self.currentNode[1] - 1) 

            self.moved = True

    def update2(self):
        if self.targetX > 0: #Use this to travel towards the target position
            self.rect.x -= 5
            self.targetX -= 5
        elif self.targetX < 0:
            self.rect.x += 5
            self.targetX += 5
        elif self.targetY > 0:
            self.rect.y -= 5
            self.targetY -= 5
        elif self.targetY < 0:
            self.rect.y += 5
            self.targetY += 5

        if self.targetX == 0 and self.targetY == 0 and self.moved: #If we are at the target position
            self.moved = False #Then find next node to travel to
            self.move()

def move(keys, key, x, y):
    if keys[key]: #Check if key has been pressed
        wallGroup.update(x, y) #Move the screen around the player
        pathGroup.update(x, y)
        enemyGroup.update(x, y)
        if pygame.sprite.groupcollide(playerGroup, wallGroup, False, False):
            wallGroup.update(-x, -y) #Move the screen back
            pathGroup.update(-x, -y)
            enemyGroup.update(-x, -y)
'''
def getSprites(sheet, x, y, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.blit(sheet, (0, 0), area=(x, y, width, height))

    return surface
'''

tileMap = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
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
enemyGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.GroupSingle()
attackBoxGroup = pygame.sprite.GroupSingle()
graph = Graph()

#sheet = pygame.image.load("Textures\Slime Hill\Character\playerCharacter.png").convert_alpha()

#playerImage = getSprites(sheet, 200, 0, 140, 190) 

for row in range(len(tileMap)): #Iterate each row
    for column in range(len(tileMap[row])): #Iterate each column
        if tileMap[row][column] == 1: #Check if its a wall
            wallGroup.add(Tile(row, column, "Textures/Slime Hill/Biome/wall.png")) #Add a wall at that position to the wall group
        else:
            graph.addNode(Node(row, column))
            pathGroup.add(Tile(row, column, "Textures/Slime Hill/Biome/floor.png")) #Else add a path at that position

player = Player(960, 540) 
playerGroup.add(player)

enemy1 = Enemy(200, 200, (1, 1))
enemyGroup.add(enemy1)

while running: #Create the game loop
    screen.fill((25, 25, 25))

    keys = pygame.key.get_pressed() #Call keys here, so its only called once

    if keys[pygame.K_k]:
        player.attack()

    move(keys, pygame.K_w, 0, 1) #Pass Keys as a parameter for effieceny
    move(keys, pygame.K_s, 0, -1)
    move(keys, pygame.K_d, 1, 0)
    move(keys, pygame.K_a, -1, 0)

    playerGroup.update()
    enemy1.update2()

    wallGroup.draw(screen)
    pathGroup.draw(screen)
    playerGroup.draw(screen)
    enemyGroup.draw(screen)
    attackBoxGroup.draw(screen)

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