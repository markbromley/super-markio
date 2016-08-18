#  ________  ___  ___  ________  _______   ________                
# |\   ____\|\  \|\  \|\   __  \|\  ___ \ |\   __  \               
# \ \  \___|\ \  \\\  \ \  \|\  \ \   __/|\ \  \|\  \              
#  \ \_____  \ \  \\\  \ \   ____\ \  \_|/_\ \   _  _\             
#   \|____|\  \ \  \\\  \ \  \___|\ \  \_|\ \ \  \\  \|            
#     ____\_\  \ \_______\ \__\    \ \_______\ \__\\ _\            
#    |\_________\|_______|\|__|     \|_______|\|__|\|__|           
#    \|_________|                                                  
                                                                 
                                                                 
#  _____ ______   ________  ________  ___  __    ___  ________     
# |\   _ \  _   \|\   __  \|\   __  \|\  \|\  \ |\  \|\   __  \    
# \ \  \\\__\ \  \ \  \|\  \ \  \|\  \ \  \/  /|\ \  \ \  \|\  \   
#  \ \  \\|__| \  \ \   __  \ \   _  _\ \   ___  \ \  \ \  \\\  \  
#   \ \  \    \ \  \ \  \ \  \ \  \\  \\ \  \\ \  \ \  \ \  \\\  \ 
#    \ \__\    \ \__\ \__\ \__\ \__\\ _\\ \__\\ \__\ \__\ \_______\
#     \|__|     \|__|\|__|\|__|\|__|\|__|\|__| \|__|\|__|\|_______|

# MADE BY MARK BROMLEY, JANUARY 2014


# Import all the relevant libraries
import pygame
import event_manager as EventManager
from views import game_view as GameView
from controllers import game_controller as Controller
from models import game_model as GameModel

class Game():
    """The Game Class which is responsible for initialising the main Model,
    Controller, View and Event Manager classes. This class has no methods or
    properties and is simply used to initialise the game."""
    def __init__(self):
        """Initialise the whole game, including Model, View, Controller and
        Event Manager. Start the background music playing and initialise
        pygame, setting up the game window and the game clock."""
        # Initialise all Pygame modules. Note that no exceptions will be
        # raised if there is a failure in loading a module. The method returns
        # an integer representing the number of modules loaded.
        pygame.init()

        # Add a caption to the game window, showing the name of the game
        pygame.display.set_caption('Super Markio!')
        # Try to load the music files
        # These should be able to play, but if there's no sound card an
        # exception will be thrown. Additionally, Linux seems to have weak 
        # support for audio files depending on distribution, causing additional
        # excpetions to be thrown. If an exception is thrown, forget about it
        # and continue.
        try:
            pygame.mixer.music.load('./assets/audio/mario_bg.wav')
            pygame.mixer.music.play(-1, 0.0)
        except Exception:
            pass

        # Initialise the Event Manager. The Event Manager allows different 
        # modules and classes to communicate with each other, by posting and 
        # collecting messages and counters. This acts as a mediator between 
        # the models, views and controllers, allowing decoupling between the 
        # code modules.
        eventManager = EventManager.EventManager()

        # Load the game model. This contains assets URLS, platfrom designs, 
        # character names and settings.
        model = GameModel.GameModel()

        # Initialise the model to currently run on level 1. A list of levels 
        # available can be retrieved if required.
        model.set_game_level(1)

        # Initialise the game controller. This module abstracts the 
        # differences between all forms of joystick controller 
        # (PS3, Wii, xBox etc) and the keyboard. The method of control can be
        # accessed, but is not revealed by default beyond the cope of the 
        # module. The Event Manager is passed into to allow the controller to
        # register as a subscriber.
        controller = Controller.GameController(eventManager)

        # Initialise the Pygame clock to be used for timing events and 
        # controlling the frame rate later on.
        clock = pygame.time.Clock()

        # Initialise the game's outer view. This view spawns subviews for
        # each level and menus, when appropriate.
        view = GameView.GameView(clock, model, controller, eventManager)
        
        # Activate and generate the game, to begin.
        view.generate_whole_game()

if __name__ == "__main__":
    print("\nSUPER MARKIO STARTING...")
    game = Game()