import pygame
from pygame.sprite import Sprite

class Bullet(Sprite): #Bullet class inherits from sprite
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_game): #Requries the current instance of Alien Invasion
        """Create a bullet object at the ship's current position."""
        
        super().__init__() #Super is used here to properly inherit methods etc from SPRITE 
        
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
        self.settings.bullet_height) #Creating the rect attribute as bullet isn't based on an image, so build a rect from scratch using Rect()
        #rect requires the xy coords of top left corner, and width and height of rect.        
        self.rect.midtop = ai_game.ship.rect.midtop #Matching the bullet's midtop to the ship's midtop 
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)


    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed #Bullet moving up the screen refers to a decreasing y value 
        # Update the rect position using y.
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)