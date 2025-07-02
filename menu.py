import pygame

class RadioButtons:
    def __init__(self, x, y, width, height, id, isDefault): #Initalize the object
        self.id = id #Assign a unique identifier to the buttons
        if 0 <= id <= 5:
            self.sheet = pygame.image.load("Textures/Menu/radioButtons.png").convert_alpha()
            self.image = getSprites(self.sheet, 0, 200 * id , 500, 200)#The buttons will be squares
        else:
            self.image = pygame.Surface((width, height)) #Creates a surface of dimensions height
            if isDefault:
                self.image.fill((0, 255, 0))
            else:
                self.image.fill((255, 0, 0)) #Fill in the object accordingly
        self.rect = self.image.get_rect(center = (x, y)) #Positions Radio Buttons correctly

class RadioButtonManager:
    def __init__(self, positions, width, height, theme):
        self.currentSelected = 0
        self.radioButtonsList = []

        for id, position in enumerate(positions):
            self.radioButtonsList.append(RadioButtons(position[0], position[1], width, height, id, id==theme))

    def update(self, currentSelected):
        if currentSelected != self.currentSelected:
            self.currentSelected = currentSelected
            return self.currentSelected
        return currentSelected

    def draw(self, screen):
        for button in self.radioButtonsList:
            screen.blit(button.image, button.rect)

class BackButton:
    def __init__(self):
        self.image = pygame.image.load("Textures/Menu/playButton.png")
        self.rect = self.image.get_rect(midbottom = (960, 1055))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BigCharacter:
    def __init__(self, x, y, theme):
        self.sheet = pygame.image.load(f"Textures/{convertCode(theme)}/Character/playerIdle.png").convert_alpha()
        self.image = getSprites(self.sheet, 0, 0, 70, 95)
        self.image =  pygame.transform.scale(self.image, (490, 665))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, theme):
        self.sheet = pygame.image.load(f"Textures/{convertCode(theme)}/Character/playerIdle.png").convert_alpha()
        self.image = getSprites(self.sheet, 0, 0, 70, 95)
        self.image =  pygame.transform.scale(self.image, (490, 665))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def getSprites(sheet, x, y, width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.blit(sheet, (0, 0), area=(x, y, width, height))

    return surface

def convertCode(themeCode):
    if themeCode == 0:
        return "Slime Hill"
    elif themeCode == 1:
        return "Underwater"
    elif themeCode == 2:
        return "Space"
    elif themeCode == 3:
        return "Snowy"
    elif themeCode == 4:
        return "Jurassic"
    else:
        return "Mine"
    
def runMenu(screen, theme):
    size = pygame.display.get_window_size()

    currentSelected = 0
    
    positions = [(1000, 150), (1000, 425), (1000, 700), (1640, 150), (1640, 425), (1640, 700)] #Positions of all the buttons

    radioButtonsManager = RadioButtonManager(positions, 500, 200, theme) #Manages the buttons
    backButton = BackButton()
    character = BigCharacter(50, 50, theme)

    while True:
        screen.fill((0, 0, 100))

        radioButtonsManager.draw(screen)
        backButton.draw(screen)
        character.draw(screen)
        pygame.display.flip() #Update the screen

        for event in pygame.event.get(): #Create the event handler
            if event.type == pygame.QUIT: #Check if the game has been quitted
                return False, theme #Tell the main file to quit

            if event.type == pygame.KEYDOWN: #Check if we press the key
                if event.key == pygame.K_KP_ENTER: #If we press keypad enter, we exit
                    return False, theme #Tell the main file to quit

                if event.key == pygame.K_KP_PLUS: #If we press the keypad plus, we take a screenshot
                    pygame.image.save(screen, "menuwu.png")

            if event.type == pygame.MOUSEBUTTONDOWN: #When we press the mouse button
                for button in radioButtonsManager.radioButtonsList: #Loop though all the radio buttons
                    if button.rect.collidepoint(event.pos): #If we click a radio button
                        currentSelected = button.id #Update the selected id
                        theme = radioButtonsManager.update(currentSelected) #Update the radiobuttons manager
                        character.update(theme)
                    
                if backButton.rect.collidepoint(event.pos): #If we press the back button we will go back
                    return True, theme #Tell the main code to start the game