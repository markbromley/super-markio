# Import all the relevant libraries, including pygame and all the necessary sub-views
import pygame
from views import sprite_views as Sprites
from views import sprite_groups_view as SpriteGroups
from views import platforms_view as Platform
from views import background_view as Background
from views import score_view as ScoreManager
from time import time as timer

class PrimaryView():
    """Generates the current level view. Several properties are available to 
    assign 'Game Over', 'Pause Game' and 'Current Score' to etc. The class is 
    responsible for generating all sub-views within the level, including the 
    primary character, platform objects, background objects and enemy sprites."""

    def __init__(self, model, eventManager):
        """Initialise the outer level view. Assigns the model
        instance to the view and defines and initialises the basic properties 
        of the outer view. Additionally spawns all the necessary sub-views for 
        the character, platform and enemy sprites."""
        # Bind the Event Manager to the instance and register as a subscriber        
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        # Bind the model to the instance
        self.model = model
        # set to False because game is NOT over
        self.gameOver = False
        # Get the current level background image from the game model
        self.background = model.get_level_background_image()
        # Set screen size and display resolution
        # The below three lines can be commented/ uncommented to set the game
        # to full screen or window mode, depending on preference. In the future 
        # this could be attached to a controller event, to give the user the 
        # choice potentially
        self.size = (1366, 768)
        self.screen = pygame.display.set_mode(self.size)
        # self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        # Currently starting so not paused 
        self.pause = False
        self.pauseTime = 0
        self.noStart = True
        # Get the platform layout by passing the model to the platformDesign
        # class and generating the necessary platform positions
        self.levelPlatform = Platform.PlatformDesign(model)
        # Initialise the Score Manager for this level and pass in the screen,
        # model and Event Manager
        self.scoreManager = ScoreManager.ScoreManager(self.screen, 
                                                      self.model, 
                                                      self.eventManager)
        # Get the level end point, this will be used to figure out when the 
        # character has reached a finish position
        levelEndPoint = self.levelPlatform.get_level_end_point()
        # Assign the background image and initialise the background movement
        self.background = Background.BackgroundImage(self.size,
                                                     self.screen,
                                                     self.background,
                                                     self.eventManager)
        # Create a default list of high scores to beat. These will hopefully 
        # be overridden later by reading the high scores file.
        self.highScores = [0,0,0]
        # Generate a list of all characters and their positions. This list 
        # can consist of initialised sprite objects directly, or generator 
        # expressions of initialised sprite objects (useful for spawning 
        # sprites in multiple positions).
        self.listOfCharactors = [
            # Add the main character
            Sprites.Markio(self.screen,
                           self.eventManager,
                           [self.levelPlatform.get_level_block_positions(), self.levelPlatform.get_level_invis_positions()])
            # Add the Cloud sprite to the game
            ,Sprites.Cloud(self.screen, self.eventManager)
            # Add 4 Dragonfly sprites to the game
            # Use a generator expression to produce desired number in group
            ,(Sprites.Dragonfly(self.screen, self.eventManager)
                for i in range(4))
            # Add the platform Blocks to the game
            ,(Sprites.Block(self.screen, i, self.eventManager)
                for i in self.levelPlatform.get_level_block_positions())
            # Add the enemy Mice sprites to the game
            ,(Sprites.Mouse(self.screen, i, self.eventManager)
                for i in self.levelPlatform.get_level_mouse_positions())
            # Add the enemy Worm sprites to the game
            ,(Sprites.Worm(self.screen, i, self.eventManager)
                for i in self.levelPlatform.get_level_worm_positions())
            # Add the gold coins to be collected to the game
            ,(Sprites.Coin(self.screen, i, self.eventManager)
                for i in self.levelPlatform.get_level_coin_positions())
            # Add the invisble block sprites to the game, these can be used
            # to build platforms in the game, which are not visible to the 
            # user e.g. the floor for instance
            ,(Sprites.InvisibleBlock(self.screen, i, self.eventManager) 
                for i in self.levelPlatform.get_level_invis_positions())
            # Add the Castle sprite, (level end) to the game
            ,(Sprites.Castle(self.screen, i, levelEndPoint, self.eventManager) 
                for i in self.levelPlatform.get_level_castle_positions())
        ]# End of list of Characters array
        # Additionally provide the names for each of the charactors lsited 
        # above and a list of whether or not they should be destroyed on 
        # collision with the first sprite (the player charactor)
        self.listOfCharactorNames = ['markio',
                                     'cloud',
                                     'dragonfly',
                                     'block',
                                     'mouse',
                                     'worm',
                                     'coin',
                                     'invis',
                                     'castle']
        self.destroyOnCollision = [False, 
                                   False, 
                                   False, 
                                   False,
                                   True, 
                                   True, 
                                   True, 
                                   False, 
                                   False]
        # Initialise all the characters and assign them to their new groups
        self.players = SpriteGroups.GenerateGroups(self.screen,
                                                   self.listOfCharactors,
                                                   self.listOfCharactorNames,
                                                   self.destroyOnCollision,
                                                   self.eventManager)

    def activate_running_loop(self, firstRun, showEndScreen):
        """Activates the loop in which the level will refresh. This 
        initially displays the start scren, continuously check for 'game Over',
        'Win' and 'Pause' events and continue to refresh the display at the 
        given interval otherwise. The method returns the counter variable at 
        the end of each iteration, to state where it is within the loop. A 
        negative value indicates the game is over and to restart the whole 
        level."""
        # If this is one of the first two loops in the current level show the
        # start screen for a specified period of time
        if firstRun < 2:
            self._show_start_screen()
            self._show_high_scores()
            if firstRun ==1:
                if self.model.get_game_level() == 1:
                    # If we're at the splash screen for the start level, 
                    # wait for user to start
                    if self.noStart:
                        # Below reduce the firstRun counter to stay where we 
                        # are until the user wants to start
                       firstRun -=1 
                    self.pause = False
                else:
                    pygame.time.delay(2000)
            firstRun += 1
        # If we're beyond the first couple of loops within the current level, 
        # check for pause/ game over events and display the next iteration 
        # otherwise. if the game is paused, wait and if the game is over 
        # return a negative value to indicate the level should be restarted
        if firstRun >=2:
            if self.pause:
                self._puase_game()
            elif showEndScreen:
                self._show_end_screen()
                pygame.time.delay(1000)
            elif self.gameOver == False:
                # Update the background position
                self.background.reposition_background()
                self.scoreManager.update_score()
                # Add/ remove players to/ from the screen and update their actions
                self.players.update_all_player_groups()
            else:
                self.game_over()
                # Return negative to indicate level should be restarted
                return -1
        return firstRun

    def game_over(self):
        """Performs 'Game Over' functions, primarily displaying the 
        'Game Over' image on the game window screen."""
        # Display image
        bg = self.model.gameOverImage
        self._display_game_image(bg)

    def notify_event(self, event):
        """Listens for the 'Game Pause' event and 'Game Over' event 
        and invokes corresponding methods as appropriate."""
        # Check for game paused event 
        if event == ["GAME_PAUSE"]:
            if self.noStart:
                # Clear the initial load screen
                self.noStart = False
            else:
                if self.pause:
                    self.pause = False
                    self.scoreManager.startTime += (timer()-self.pauseTime)
                else:
                    self.pause = True
                    self.pauseTime = timer()
                    
            # Pause for a second to prevent duplicate events being 
            # transmitted by the controller
            pygame.time.delay(50)
            # Now clear the Event Manager of this event so that it can move on
            self.eventManager.event_clear(event)
        # Check for game over event
        if event == self.model.gameOverEvent:
            self.gameOver = True
            # Now clear the Event Manager of this event so that it can move on
            self.eventManager.event_clear(event)

    def _display_game_image(self, imUrl):
        """Displays an image from a given image url and blits
        it to the game screen. Resizes the image to fill the screen 
        and attaches it directly to the game window."""
        # Load image, convert, transform and blit
        img = pygame.image.load(imUrl)
        img = img.convert()
        img = pygame.transform.scale(img, self.size)
        self.screen.blit(img,(0,0))

    def _display_game_text(self, text, font, fontSize, position):
        """Displays a given string in a given font at a given 
        position and blits it on to the game screen. Automatically 
        sets colour."""
        font = pygame.font.Font(font, fontSize)
        txt = font.render(text,True,(0,0,0))
        self.screen.blit(txt, position)

    def _show_start_screen(self):
        """Shows the current level's Splash screen image and 
        blits it to the game window. Acts as a wrapper to other internal 
        methods."""
        bg = self.model.get_level_start_image()
        self._display_game_image(bg)

    def _show_high_scores(self):
        """Displays a list of the high scores for the current
        level and blits the list to a predefined position on the game window
        screen. Uses internal methods to retrieve the high scores."""
        self._get_high_scores()
        i = 0
        # For each high score display it in a lower position on the screen 
        for highScore in self.highScores:
            i += 60
            self._display_game_text('High Score ' +str(int(i/60)) +': ' + str(highScore),
                                    './assets/fonts/font_1.ttf',
                                    20,
                                    (20,i))

    def _get_high_scores(self):
        """Opens the corresponding high score file for this 
        level and retrieves the contents before assigning."""
        # If file can't be found...
        # ignore the problem, because the default high scores of zero will be 
        # used instead.
        try:
            fileName = self.model.get_level_score_url()
            with open(fileName, 'r') as scoreFile:
                self.highScores = scoreFile.readlines()
        except Exception:
            # Ignore any exceptions and continue. It isn't worth stopping 
            #the whole game just for this.
            pass

    def _puase_game(self):
        """Displays the pause game image and performs any
        other actions for pausing the level."""
        # Display pause image
        bg = self.model.pauseImage
        self._display_game_image(bg)

    def _show_end_screen(self):
        """Displays the 'Game Won' screen with a corresponding 
        message to congratulate the player if they have generated a new high 
        score for the level."""
        self._get_high_scores()
        # Display the game won graphic over the entire screen
        bg = self.model.get_level_end_image()
        self._display_game_image(bg)
        # Check the current high score and display congratulation message if
        # appropriate
        for highScore in self.highScores:
            if self.scoreManager.score > int(highScore):
                self._display_game_text('New High Score ' + str(self.scoreManager.score),
                                    './assets/fonts/font_1.ttf',
                                    20,
                                    (20,20))
