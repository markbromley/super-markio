# Import all the relevant libraries
import pygame
from time import time as timer

class ScoreManager():
    """Manages the score tally for the character at each level. Allows updating 
    and displaying the current level's score for the player."""
    def __init__(self, screen, model, eventManager):
        """Initialise the Score Manager values and binds to Event Manager
        and create a 'Rapid Counter' with the Event Manager (a way to pass 
        events without checking for duplicates, providing higher performance)."""

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
        """ Check if the event matches the Level End event and if so check if 
        the player's score is a high score."""
        if event == ["CHARACTER_AT_END"]:
            self.startTime = (pygame.time.get_ticks()/1000)
            self._register_final_score()

    def update_score(self):
        """Update the score displayed. Does not update the value of the store, 
        but simply gets the value and blits it to the screen. This method only 
        updates every 19 frames, to help maintain performance."""
        if self.updateCounter % 19 == 0:
            self.score = self.eventManager.get_rapid_counter_value("CHARACTER_COLLIDE_COIN")
        self._print_score()
        self._print_time()
        self.updateCounter += 1

    def _print_score(self):
        """Generates the score and blits to screen."""
        font = pygame.font.Font('./assets/fonts/font_1.ttf', 40)
        txt = font.render('Score: ' +str(self.score),True,(233,58,33))
        self.screen.blit(txt, (1000, 30))

    def _print_time(self):
        """Generates the time and blits to screen."""
        self._calculate_remaining_time()
        font = pygame.font.Font('./assets/fonts/font_1.ttf', 40)
        txt = font.render('Time: ' +str(self.time),True,(233,58,33))
        self.screen.blit(txt, (50, 30))

    def _calculate_remaining_time(self):
        """Calculates time left to complete current level."""
        totlalTimeInSeconds = 155
        timeNow = round(totlalTimeInSeconds - (timer() - self.startTime), 1)
        self.time = timeNow
        if timeNow <= 0:
            self.time = 0
            self.eventManager.post(['CHARACTER_DEAD'])

    def _register_final_score(self):
        """Registers if score is higher than current top 3 scores. Logs score
        in top scores file as necessary."""
        # Get the file name from the model for the current level
        fileName = self.model.get_level_score_url()
        try:
            with open(fileName, 'r+') as inf:
                finished = False
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