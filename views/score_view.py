# Import all the relevant libraries
import pygame
from time import time as timer

class ScoreManager():
    """This class manages the score tally for the character at each level. 
    The class contains methods for updating and displaying the current 
    level's score for the player."""
    def __init__(self, screen, model, eventManager):
        """Initialise the Score Manager values, bind to the Event Manager
        and create a 'Rapid Counter' with the Event Manager (a special way 
            to pass events without checking for duplicates, providing higher
            performance)."""
       # Below bring this class instance to the Event Manager and register a
       # rapid counter listener
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        self.eventManager.create_game_rapid_counter('CHARACTER_COLLIDE_COIN', 10)
        # Bind the model and screen to this object
        self.screen = screen
        self.model = model
        # Initialise class variables
        self.score = 0
        self.updateCounter = 0
        # Record the start time
        self.startTime = timer()
        self.time = 5

    def notify_event(self, event):
        """Method required by Event Manager to pass events to this class. 
        Check if the event matches the Level End event and if so check if 
        the player's score is a high score, using an internal method."""
        if event == ["CHARACTER_AT_END"]:
            self.startTime = (pygame.time.get_ticks()/1000)
            self._register_final_score()

    def update_score(self):
        """Method to update the score displayed. This method does not update 
        the value of the store, but simply gets the value and blits it to 
        the screen. This method only updates every 19 frames, to help maintain
        game performance."""
        if self.updateCounter % 19 == 0:
            self.score = self.eventManager.get_rapid_counter_value("CHARACTER_COLLIDE_COIN")
        self._print_score()
        self._print_time()
        self.updateCounter += 1

    def _print_score(self):
        """Private method which generates the score and blits it to the screen."""
        font = pygame.font.Font('./assets/fonts/font_1.ttf', 40)
        txt = font.render('Score: ' +str(self.score),True,(233,58,33))
        self.screen.blit(txt, (1000, 30))

    def _print_time(self):
        """Private method which generates the time and blits it to the screen."""
        self._calculate_remaining_time()
        font = pygame.font.Font('./assets/fonts/font_1.ttf', 40)
        txt = font.render('Time: ' +str(self.time),True,(233,58,33))
        self.screen.blit(txt, (50, 30))

    def _calculate_remaining_time(self):
        """Private method to calculate time left to complete the curent level."""
        totlalTimeInSeconds = 155
        timeNow = round(totlalTimeInSeconds - (timer() - self.startTime), 1)
        self.time = timeNow
        if timeNow <= 0:
            self.time = 0
            self.eventManager.post(['CHARACTER_DEAD'])

    def _register_final_score(self):
        """Private method which registers if the score is higher than the 
        current top 3 scores. The method opens up the score file for the 
        current level and checks to see if the player's score is higher 
        than any of the current top scores. If it is, the score is added 
        in the correct place within the list."""
        # Get the file name from the model for the current level
        fileName = self.model.get_level_score_url()
        # Use a try statement in case opening and/ or writing to the file 
        # fails for any reason
        try:
            # Open file for read and write access
            with open(fileName, 'r+') as inf:
                finished = False
                # Initialise a counter
                i = 0
                lines = inf.readlines()
                for line in lines:
                    if self.score> int(line.strip()) and not finished:
                        lines[i] = str(self.score) + '\n'
                        finished = True
                    i += 1
                if finished:
                    inf.seek(0)
                    for line in lines:
                        line = str(line)
                        inf.write(line)
        # If reading/ writing to the file fails for any reason, ignore it
        # and move on
        except Exception:
            pass