import sys
import pygame
from settings import Settings
from ship import Ship #Ship class from ship.py file 
from bullet import Bullet
from alien import Alien
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
        # could change various settings here if we made the settings class have more inputs, but as it only has init, we 
        # make the changes from within the settings module 

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
        #The (self) input arguement refers to the current instance of AlienInvasion and GIVES Ship ACCESS TO THE GAMES RESOURCES, e.g. screen
        #Ship's __init__ requires 2 inputs (self, ai_game) - this is because it needs access to the attributes...
        # of an AlienINvasion class to get values such as screen size (and these could be unique to each instance of the class)
        #I.e. - SHIP NEEDS TO ACCESS DATA WITHIN ALIENINVASION

        self.bullets = pygame.sprite.Group() #A group behaves like a list with some extra functionality
        #Above is creating an empty group 
        
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color.
        self.bg_color = (230, 230, 230)


    def run_game(self):
        """Start the main loop for the game.""" #This is the 'MAIN LOOP' of the game - i.e. keep running. 
            #It is a method of the AlienInvasion Class
        while True: #This loop will run continually 
            #Will therefore run all below methods continually
            #This 'event' loop will 'listen' for user inputs during game
            # Watch for keyboard and mouse events.

            self._check_events() #Starting with a '_' indicates a HELPER METHOD (will be defined outside of this method, in its own method below)
            #^Call this method via SELF._check_events

            self.ship.update() #The ships position will be updated after we have checked for keyboard events
            #^Looks like the above as there is a self.ship = Ship(Self). I.e. the ship instance will have an update method. 

            self._update_bullets()

            self._update_aliens()

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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT: #if it is the right key
            self.ship.moving_right = False #reset flag to false 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) #adding to group of bullets using the 'add.' method
            #This is similar to the append() method, but it is written specifically for pygame groups

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.

        self.bullets.update() #Updates the position of the bullets each pass through the loop 
        #When you call update on a group, it automatically calls update for each sprite in group
        #I.e. for each bullet we place in the 'bullets' group 

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): #because we can't remove elements from a list during a running for-loop, we use a 'copy' to set up the for loop...
            #... and then modify the actual bullets 
            if bullet.rect.bottom <= 0: #if it has reached top of screen (y=0), remove bullet from bullets group 
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, True, True)
        #The above code compares all the positions of all bullets in self.bullers and aliens in self.aliens. 
        #If there is overlap, groupcollide() adds A KEY VALUE PAIR TO A DICTIONARY WHICH IT RETURNS
        #The two 'True' arugements tell Pygame to delete the bullets and aliens that have collided

        if not self.aliens: #if the aliens group is empty - an empty group evaluates to FALSE
            # Destroy existing bullets and create new fleet.
            self.bullets.empty() #get rid of any existing bullets using the EMPTY method
            self._create_fleet() #new fleet will appear as soon as current fleet is destroyed

    def _update_aliens(self):
        """Check if the fleet is at an edge,then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()        
        self.aliens.update() #update is being called on a group - will therefore update all of them at once 

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens): #spritecollideany takes 2 input argeuments - sprite and a group
            #Loops through the group and returns the first alien that collides with the ship 
            #If no collisions occur, the if block won' execute
            print("Ship hit!!!")

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self) #create an instance so we can access width etc. 
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
                
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) #Adding this to the alien group created in __init__

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites(): #call check edges on each alien
            if alien.check_edges(): #uses the check_edges method in the alien class, which either returns true or false
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites(): #go through each of the aliens in the group
                alien.rect.y += self.settings.fleet_drop_speed  #will drop each aliens vertical (y) position
        self.settings.fleet_direction *= -1 #isnt part of for loop as we only want to change fleet direction once. Fleet direction is used
        #by the alien's update method, so therefore only have to change it once, as self.alien uses self.settings 

    def _update_screen(self):
        """Update images on the screen, and flip to new screen"""
        #self.bg color was defined in __init__
        #As per notes, can acccess all self. methods within a class
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): #bullets.sprites method returns a list of all sprites in the group bullets. 
            bullet.draw_bullet() #We loop through the sprites in bullets and call draw_bullet on each one
            #draw_bullet is a method within the Bullet class

        self.aliens.draw(self.screen) #draw requires one input arguement - the surface on which to draw the element

        # Make the most recently drawn screen visible.
        pygame.display.flip() #Will continually update display to show most recent positions of game 


if __name__ == '__main__': #when a file is ran directly, its __name__ variable is set to __main__
    #when a file is imported as a MODULE, its __name__ is set to the file's name
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()