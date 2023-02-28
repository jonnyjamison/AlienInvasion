import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""

        #ai_game input gives Ship access to all the game resources defined in AlienInvasion
        #(AlienInvasion is a class defined in alien_invasion.py)
        #By referencing this INSTANCE of ai_game, we can access all the attributes being defined in the __init__ of the other file, such as screen parameters etc. 

        self.screen = ai_game.screen #Accessing the screen attribute of the AlienInvasion class
        #^This allows us to easily access it with the methods of this class
        self.settings = ai_game.settings #Always better to use an existing isntance (instances should be made where possible by main programme)
        self.screen_rect = ai_game.screen.get_rect() #Accessing the screen's rect attribute, allowing us to place the ship at the correct position etc. by gaining quantities associated witht the screen

        # Load the ship image and get its rect.
        self.image = pygame.image.load('Project1_AlienInvasion/images/ship.bmp')
        self.rect = self.image.get_rect() #Getting the ship's 'rectangle' values so we can better position it 
        #get_rect is a pygame method. Using it on the image attribute of Ship 

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom #Assigning a variable of the middle bottom of the ship as the middle bottom of the screen 

        #Store a decimal value for the ship's horz position. 
        self.x = float(self.rect.x) #require this as rect will only store integer value. We therefore use float to convert to decimal

        #Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        #Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right: #self.rect.right returns the x coordinate of the right edge of the ships rect. 
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object from self.x
        self.rect.x = self.x
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) #'Draws' the ship at the position determined
        #'blit' essentially means 'draw on top of'
        #blit is an inbuilt method of the Pygame library in Python