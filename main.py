import pygame #Import the libraries
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
    def __init__(self, x, y, tile):
        self.id = (x, y) #Each Node has a unique identifier
        self.neighbours = []
        self.tile = tile
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

    def pickRandomNode(self):
        return choice(self.graph)

class HealthBar:
    def __init__(self, x, y):
        self.textures = ["Textures\General\Health\health_wheel_dead.png", "Textures\General\Health\health_wheel_hurt.png", "Textures\General\Health\health_wheel_full.png"] #Place all the file locations in an array
        self.pointer = 2 #Have a pointer to help index the files
        self.image = pygame.image.load(self.textures[self.pointer]).convert_alpha() #Show the current Healths
        self.rect = self.image.get_rect(topleft = (x, y))
        self.immunity = False #Create a variable to give immune frames
        self.immunityCounter = 0 #Tracks how long we are immune for

    def damage(self):
        if not(self.immunity):
            self.pointer -= 1 #decrement the pointer
            if self.pointer < 0:
                exit() #When player loses all health the game ends
            self.image = pygame.image.load(self.textures[self.pointer]).convert_alpha() #Show corresponding healthbar
            self.immunity = True #Turn on the immunity
        else:
            self.immunityCounter += 1
            if self.immunityCounter == 60: #Count to 60 (1 second)
                self.immunityCounter = 0 #Reset the counter
                self.immunity = False #Turn off the immunity
        
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
    return ((200 * x) + 960, (200 * y) + 540) #Adding one to x will place it 200 away (length of one tile)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 200, 200))
        self.rect = self.image.get_rect(center = (x, y))
        self.isAttacking = False
        self.health = 3
        self.facingLeft = False

    def attack(self):
        if not(self.isAttacking): #If we are not attacking already
            if self.facingLeft:
                self.attackBox = AttackBox(960, 540, True) #Create an AttackBox
            else:
                self.attackBox = AttackBox(960, 540, False)
            self.isAttacking = True #Now we are attacking

    def update(self):
        if self.isAttacking: #If we are in an attack (the box exists)
            flag = self.attackBox.update() #Update the attack box and return the state
            if flag: #If we are given True, that means we need to kill the attack box                
                del self.attackBox #Kills the attack box
                self.isAttacking = False #Set the attack to False (allowing us to attack again)
                self.slimeSword.image = self.slimeSword.originalImage

class AttackBox(pygame.sprite.Sprite): #Create an AttackBox, any enemy that collides with this will die
    def __init__(self, x, y, flag):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 255, 255)) #Fill for debugging purposes
        if flag:
            self.rect = self.image.get_rect(midleft = (x, y))
        else:
            self.rect = self.image.get_rect(midright = (x, y))

        self.counter = 0 #Have a counter to check it in for 5 frames
        self.positions = [(1000, 545), (920, 545)]

    def update(self):
        self.counter += 1 #Increment the counter
        if self.counter == 6: #When it reaches 5 (5 frames have passed)
            return True #Tell the Player object to kill the attack box
        else:
            return False #Tell the Player not to kill the attack box

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, nodeID, filePath, width, height, numberOfFrames): #Instantiate Enemy Object
        super().__init__()

        self.sheet = pygame.image.load(filePath).convert_alpha() #Create the stylesheet as a pygame surface
        self.animations = []

        for i in range(numberOfFrames):
            self.animations.append(getSprites(self.sheet, i * width, 0, width, height)) #Grab each frame and add it to the sheet

        self.pointer = 0
        self.image = self.animations[self.pointer] #Set the default values
        self.reverse = False
        self.count = 0
        self.max = numberOfFrames

        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.currentNode = nodeID
        self.targetX = 0
        self.targetY = 0
        self.moved = False
        self.freeze = False
        self.freezeTimer = 0
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
        if not(self.freeze): #If we are not frozen
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
        else:
            self.freezeTimer += 1 #Increment the freezetimer
            if self.freezeTimer == 90: #Check if we have waited 90f
                self.freezeTimer = 0 #Reset the freezetimer
                self.freeze = False #Unfreeze the enemy


    def animate(self):
        self.count += 1 #Incremeent the count function
        if self.count == 10: #When 10 frames have passed, I update the animation
            self.count = 0 #Reset the current count
            if self.reverse: #Update pointer
                self.pointer -= 1
            else:
                self.pointer += 1

            self.image = self.animations[self.pointer] #Update image
            
            if self.pointer == 0: #Use a coin to oscillate back and forth in the frames
                self.reverse = False
            elif self.pointer == self.max - 1: #Check if we have reached the last frame
                self.reverse = True

def move(keys, key, x, y):
    if keys[key]: #Check if key has been pressed
        wallGroup.update(x, y) #Move the screen around the player
        pathGroup.update(x, y)
        enemyGroup.update(x, y)
        if pygame.sprite.spritecollide(player, wallGroup, False):
            wallGroup.update(-x, -y) #Move the screen back
            pathGroup.update(-x, -y)
            enemyGroup.update(-x, -y)
            return 0
        else:
            return x

    return 0

class SlimeHunter(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sheet = pygame.image.load("Textures\Slime Hill\Character\playerIdle.png").convert_alpha()
        self.animation = []

        for a in range(3):
            self.animation.append(pygame.transform.flip(getSprites(self.sheet, a * 70, 0, 70, 95), True, False))

        self.pointer = 0
        self.image = self.animation[self.pointer]
        self.rect = self.image.get_rect(center = (x, y))
        self.counter = 0

        self.slimeTank = SlimeTank(1000, 545)
        self.slimeSword = SlimeSword(960, 540)

    def checkFlip(self, vectorx):
        if ((vectorx < 0) and self.facingLeft) or ((vectorx > 0) and not(self.facingLeft)):
            self.flip()
            self.facingLeft = not(self.facingLeft)

    def animate(self):
        self.counter += 1
        if self.counter == 10:
            self.pointer = (self.pointer + 1) % 3
            self.image = self.animation[self.pointer]
            self.counter = 0 
            if self.facingLeft:
                self.flip()

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def slimeSplash(self):
        if self.slimeTank.pointer == 4:
            for enemy in enemyGroup:
                enemy.freeze = True

            self.slimeTank.empty()

class SlimeTank:
    def __init__(self, x, y):
        self.sheet = pygame.image.load("Textures\Slime Hill\Character\characterSlimeTank.png").convert_alpha()
        self.animations = []
        for a in range(5):
            self.animations.append(getSprites(self.sheet, a * 20, 0, 20, 65))
        self.pointer = 0
        self.image = self.animations[self.pointer]
        self.rect = self.image.get_rect(center = (x, y))
        self.positions = [(1000, 545), (920, 545)]        

    def fill(self):
        self.pointer += 1
        if self.pointer > 4:
            self.pointer = 4

        self.image = self.animations[self.pointer]

    def empty(self):
        self.pointer = 0
        self.image = self.animations[self.pointer]

    def flip(self, flip):
        self.rect.center = self.positions[flip]

class SlimeSword:
    def __init__(self, x, y):
        self.sheet = pygame.image.load("Textures\Slime Hill\Character\characterWeapon.png").convert_alpha()
        self.textures = []

        for a in range(3):
            self.textures.append(getSprites(self.sheet, 0, a * 50, 130, 50))

        self.pointer = 2
        self.image = self.textures[self.pointer]
        self.originalImage = self.image
        self.rect = self.image.get_rect(midright = (x, y))
        self.flag = False

    def changeTexture(self):
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 0
        else:
            self.image = self.textures[self.pointer]
            self.originalImage = self.image
    
    def flip(self, isFacingLeft, isAttacking):
        if not(isAttacking):
            if not(isFacingLeft):
                self.image = self.originalImage
            else:
                self.image = pygame.transform.flip(self.originalImage, True, False)

        if isFacingLeft != self.flag:
            self.image = pygame.transform.flip(self.image, True, False)
            if isFacingLeft: 
                self.rect.midleft = (960, 540)
            else:
                self.rect.midright = (960, 540)
            self.flag = isFacingLeft

    def attack(self, isFacingLeft):
        if isFacingLeft:
            self.rect.x += 5
        else:
            self.rect.x -= 5

    def restoreOrignalPosition(self, isFacingLeft):
        if isFacingLeft: 
            self.rect.midleft = (960, 540)
        else:
            self.rect.midright = (960, 540)

def getSprites(sheet, x, y, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.blit(sheet, (0, 0), area=(x, y, width, height))

    return surface

class Slime(Enemy):
    def __init__(self, node): #Instanstiate the object
        super().__init__(node.tile.rect.centerx, node.tile.rect.centery, node.id, "Textures/Slime Hill/Enemies/slime.png", 162, 108, 5) #call parent object
       
class SlimeAlmagamation(Enemy): #Create the Slime Boss Class
    def __init__(self, node):
        super().__init__(node.tile.rect.centerx, node.tile.rect.centery, node.id, "Textures/Slime Hill/Enemies/slimeBoss.png", 140, 140, 3) #Calls the parent object

    def update2(self): #Use Polymorphism to modify the parent function
        if self.freeze:
            self.freeze = False
        super().update2() #Run the original procedure
        self.flip() #Add the flip procedure

    def flip(self):
        if (self.targetX < 0): #If we are travelling to the right and we are facing left
            self.image = pygame.transform.flip(self.animations[self.pointer], True, False) #Flip Image

    def attack(self):
        pass

class SlimeBall(pygame.sprite.Sprite):
    def __init__(self, direction, isX, x, y):
        super().__init__()
        self.isX = isX
        self.direction = direction
        self.image = pygame.image.load("Textures/Slime Hill/Enemies/slimeBall.png").convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        if self.isX:
            self.rect.x += 3 * self.direction
        else:
            self.rect.y += 3 * self.direction

        self.image = pygame.transform.rotate(self.image, 90)

tileMap = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
] #Path 20x20


wallGroup = pygame.sprite.Group() #Create sprite groups
pathGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
graph = Graph()

possibleSpawnLocations = []

for index, row in enumerate(tileMap): #Find the player location
    for index2, column in enumerate(row):
        if column == 2:
            playerStartPos = (index, index2)

for row in range(len(tileMap)): #Iterate each row
    for column in range(len(tileMap[row])): #Iterate each column
        if tileMap[row][column] == 1: #Check if its a wall
            wallGroup.add(Tile(row - playerStartPos[0], column - playerStartPos[1], "Textures/Slime Hill/Biome/wall.png")) #Add a wall at that position to the wall group
        else:
            t = Tile(row - playerStartPos[0], column - playerStartPos[1], "Textures/Slime Hill/Biome/floor.png")
            graph.addNode(Node(row, column, t))
            pathGroup.add(t) #Else add a path at that position

player = SlimeHunter(960, 540)

enemy1 = SlimeAlmagamation(graph.pickRandomNode())
enemyGroup.add(enemy1)

healthBar = HealthBar(0, 0)

slimeSword = player.slimeSword
slimeTank = player.slimeTank

while running: #Create the game loop
    screen.fill((25, 25, 25))

    keys = pygame.key.get_pressed() #Call keys here, so its only called once

    vectorx = 0
    vectorx += move(keys, pygame.K_w, 0, 1) #Pass Keys as a parameter for effieceny
    vectorx += move(keys, pygame.K_s, 0, -1)
    vectorx += move(keys, pygame.K_d, 1, 0)
    vectorx += move(keys, pygame.K_a, -1, 0)

    if pygame.sprite.spritecollide(player, enemyGroup, False):
        healthBar.damage()

    player.update()
    player.animate()
    player.checkFlip(vectorx)
    slimeTank.flip(player.facingLeft)
    slimeSword.flip(player.facingLeft, player.isAttacking)
    
    for enemy in enemyGroup:
        enemy.animate()
        enemy.update2()

    wallGroup.draw(screen)
    pathGroup.draw(screen)
    enemyGroup.draw(screen)
    
    screen.blit(slimeSword.image, slimeSword.rect)
    screen.blit(player.image, player.rect)
    screen.blit(slimeTank.image, slimeTank.rect)
    screen.blit(healthBar.image, healthBar.rect)

    if player.isAttacking: #When we attack
        slimeSword.attack(player.facingLeft) #Then we attack
        if player.attackBox.counter <= 3: #Check how long we have attacks
            for enemy in enemyGroup: #Iterate through the enemies
                if pygame.sprite.collide_rect(slimeSword, enemy): #If we hit the enemies
                    enemyGroup.remove(enemy) #Delete the enemy
                    del enemy
                    slimeTank.fill() #Add more slime to the tank

                    enemy1 = SlimeAlmagamation(graph.pickRandomNode()) #Create a new enemy
                    enemyGroup.add(enemy1)
                    if not(len(enemyGroup) >= 20): #If we have less than 20 enemies
                        enemy2 = SlimeAlmagamation(graph.pickRandomNode()) #Add another enemy
                        enemyGroup.add(enemy2)
    else:
        slimeSword.restoreOrignalPosition(player.facingLeft)

    pygame.display.flip() #Updates and controls the game

    for event in pygame.event.get(): #Create the event handler
        if event.type == pygame.QUIT: #Check if the game has been quitted
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

        if event.type == pygame.KEYDOWN: #Check if we press the key
            if event.key == pygame.K_KP_ENTER: #If we press keypad enter, we exit
                running = False

            if event.key == pygame.K_KP_PLUS: #If we press keypad plus, we take a screen shot
                pygame.image.save(screen, "menuPage.png")

            if event.key == pygame.K_k:
                player.attack()

            if event.key == pygame.K_l:
                player.slimeSplash()

            if event.key == pygame.K_p:
                slimeTank.fill()
    pygame.time.Clock().tick(60)