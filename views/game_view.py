import pygame
from views import level_view as PrimaryView

class GameView():
    """Generates the game and spawns subviews for individual levels as the 
    player enters the corresponding level. Responsible for the overall control 
    flow of the game views, ordering of levels, display of splash screens and game over screens."""

    def __init__(self, clock, model, controller, eventManager):
        """Binds the model instance, controller instance, clock and Event 
        Manager to the game view."""
        # Bind Event Manager controller, level view and clock to object
        self.eventManager = eventManager
        self.model = model
        self.view = PrimaryView.PrimaryView(self.model, self.eventManager)
        self.controller = controller
        self.clock = clock
        # Register as as subscriber to the Event Manager
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        # Initialise start
        self.levelRunning = True
        self.firstRun = 0
        self.systemRunning = True
        self.levelComplete = False
        self.gameOver = False

    def generate_whole_game(self):
        """Generates each level of game in correct order. Controls flow of 
        levels, splash screen display and game over screen display."""
        while self.systemRunning:
            # For each level described by the level model, if the system is
            # running set the level number and initialise the level
            for level in self.model.levels:
                if self.systemRunning:
                    self.model.set_game_level(level)
                    # Clear the Event Manager if the previous loop produced
                    # a game over event
                    self.eventManager.currentEvent = None
                    # Local variable to define if the level should be
                    # restarted after a game over event
                    start = True
                    while self.gameOver or start:
                        # Reset all the class properties and local variables
                        # if we are starting the level afresh
                        start = False
                        self.levelComplete = False
                        self.levelRunning = True
                        self.gameOver = False
                        self.firstRun = 0
                        # Set the current view to the current level's view
                        self.view = PrimaryView.PrimaryView(self.model, self.eventManager)
                        # Private method to generate the whole level inside a
                        # running loop to allow frames to repeat
                        self._create_current_level_loop()
            # When the game has finished, let the player enjoy looking at 
            # the winning screen for a bit!
            if self.systemRunning:
                pygame.time.delay(20000)

    def notify_event(self, event):
        """Required by Event Manager to pass events to this class. 
        Check if the event is a level end event or level complete event and 
        set this object instance's levelComplete property to true if it is."""
        if ((event == self.model.levelEndEvent or
            event == self.model.levelEndEventTwo) and
            self.levelComplete == False):
                self.levelComplete = True
                self.eventManager.event_clear(event)

    def _create_current_level_loop(self):
        """Generate a running loop for the current level.
        This allows the level to continuously iterate through recalculated 
        frames until the level is finished or a game over event is fired."""
        while self.levelRunning and self.systemRunning:
            # Listen for the termination event to break the while loop
            self._listen_for_level_kill_event()
            showEndScreen = False
            # If levelRunning is false, the game has just finished, so display 
            # the end screen at the beginning of the next loop
            if self.levelRunning ==False:
                # Game has just finished
                showEndScreen = True
            self.clock.tick(150)
            # Check to see if the user has pressed the escape key to close 
            # the game
            self._top_level_event_handling()
            # Access the  current controller values for this frame and ensure
            # they are passed to the Event Manager
            self.controller.get_game_event_values()
            self.controller.show_actions()
            # Get the return value from the level running loop and assign it
            # to the firstRun property to be checked for actions later on
            self.firstRun = self.view.activate_running_loop(self.firstRun, showEndScreen)
            # Flip the display and show everything to the user
            pygame.display.flip()
            # If the firstRun variable is negative, the gameOver event has 
            # fired within the level and therefore we should set the gameOver
            # and levelRunning properties accordingly
            if self.firstRun<0:
                self.gameOver = True
                self.levelRunning = False

    def _listen_for_level_kill_event(self):
        """Listens for kill events. Changes the object instance property 
        levelRunning to false if a kill event is found."""
        if self.levelComplete:
            self.levelRunning = False

    def _top_level_event_handling(self):
        """Allows bypass of controller for the keyboard escape key. This is 
        useful as the controller can be slow at allowing events to be propagated 
        and can allow individual level sub-views to handle events before the 
        outermost view. This method is ONLY for the escape key, no other 
        control events should be caught here - they are the responsibility of 
        the Controller module."""
        for event in pygame.event.get():
            # Check if a quit event or escape key event is in the pygame event
            # queue and set systemRunning to false if they are
            if event.type == pygame.QUIT:
                self.systemRunning = False
            if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.systemRunning = False