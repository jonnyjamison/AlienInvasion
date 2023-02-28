import sys
import pygame
from settings import Settings
from ship import Ship #Ship class from ship.py file 
#Importing Settings class from settings module file
#Instead of adding a bunch of settings throughout code, this allows us to access it in one place

class AlienInvasion:
    """Overall class to manage game assets and behavior."""


#WITHIN __init__, ASSIGN ALL THE INSTANCES YOU NEED FROM OTHER MODULES (to self)
    def __init__(self): 
        """Initialize the game, and create game resources."""
        pygame.init() #Initialises the background settings required for Pygame

        self.settings = Settings() #Brings Settings attributes into this instance
        #for e.g, there is screen_height, screen_width in Settings Module. 

        #Using Settings attributes, we create a screen (using those settings)
        #Create the screen here, then update it using method below
        #pygame.display.setmode is from pygame library
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #Notice how the above is called - SELF.SETTINGS.screen_height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self) #creating an instance of Ship (Ship class was imported from ship file above)
        #this allows us to access Ship's methods within the Alien Invasion class
        #The (self) input arguement refers to the current instance of AlienInvasion and gives Ship access to the game's resouces, e.g. screen
        #Ship's __init__ requires 2 inputs (self, ai_game) - this is because it needs access to the attributes...
        # of an AlienINvasion class to get values such as screen size (and these could be unique to each instance of the class)
        #I.e. - SHIP NEEDS TO ACCESS DATA WITHIN ALIENINVASION


        # Set the background color.
        self.bg_color = (230, 230, 230)


    def run_game(self):
        """Start the main loop for the game."""
        while True: #This loop will run continually 
            #This 'event' loop will 'listen' for user inputs during game
            # Watch for keyboard and mouse events.

            self._check_events() #Starting with a '_' indicates a HELPER METHOD (will be defined outside of this method, in its own method below)
            #^Call this method via SELF._check_events

            self.ship.update() #The ships position will be updated after we have checked for keyboard events

            # Redraw the screen during each pass through the loop.
            self._update_screen()

            # Make the most recently drawn screen visible.
            pygame.display.flip() #Will continually update display to show most recent positions of game 


    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get(): #This function returns a list of events that have taken place since the last time this function was called
            if event.type == pygame.QUIT: #Any keyboard or mouse events will cause this loop to run
                sys.exit()

            elif event.type == pygame.KEYDOWN: #If key pressed DOWN
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP: #if key is UP
                self._check_keyup_events(event)

                

    def _check_keydown_events(self, event): #Requires an event input to determine what button was pressed 
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT: #if right key         
            # Move the ship to the right.
            self.ship.moving_right = True #change the flag to true in the instance of ship
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT: #if it is the right key
            self.ship.moving_right = False #reset flag to false 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to new screen"""
        #self.bg color was defined in __init__
        #As per notes, can acccess all self. methods within a class
        self.screen.fill(self.bg_color)
        self.ship.blitme()


if __name__ == '__main__': #when a file is ran directly, its __name__ variable is set to __main__
    #when a file is imported as a MODULE, its __name__ is set to the file's name
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()