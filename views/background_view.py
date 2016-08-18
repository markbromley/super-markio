# Import all the relevant libraries
import pygame

class BackgroundImage():
    """Class to position and animate the background image for each level.
    This class contains methods to blit and reposition the background."""

    def __init__(self, screenSize, screen, background, eventManager):
        """ """
        # Below bring this class instance to the Event Manager and register
        # as a subscriber
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        self.event = None
        # Initialise properties
        self.width, self.height = screenSize
        self.screen = screen
        # x is horizontal, y is vertical
        # 0 represents top left coordinate for first background and 1 
        # represents top left coordinate for second background
        self.x0 = 0
        self.y0 = 0
        self.x1 = self.width
        self.y1 = 0
        # Load the background in using pygame and scale it to the size of the
        # game window
        background = pygame.image.load(background)
        background = background.convert()
        background = pygame.transform.scale(background, screenSize)
        # Bind the background to the object 'background' property
        self.background = background

    def reposition_background(self):
        """Method to reposition the background. Speed increases if the player 
        sprite is to the far sides of the game to create the illusion that 
        they are moving throughout the game."""
        # Move slowly if at the left hand side 
        if self.event == ["CHARACTER_AT_LEFT"]:
            # print(event)
            self.x1 += 0.01
            self.x0 += 0.01
        # Move fast if at the right hand side
        elif self.event == ["CHARACTER_AT_RIGHT"]:
            self.x1 -= 11.0
            self.x0 -= 11.0
        # Default rate of movement
        else:
            self.x1 -= 0.5
            self.x0 -=0.5
        # Actually reposition the background on the screen here
        self.screen.blit(self.background,(self.x0,self.y0))
        self.screen.blit(self.background,(self.x1,self.y1))

        # Prepare for the next iteration
        if self.x0 < -self.width:
            self.x0 = +self.width
        if self.x1 < -self.width:
            self.x1 = +self.width
        # Reset the event property
        self.event = None

    def notify_event(self, event):
        """Method required by Event Manager to pass events to this class. 
        Simply attaches any current event to this objects 'event' property."""
        self.event = event
