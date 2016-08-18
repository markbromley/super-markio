# Import all the relevant libraries
import pygame
from easypg.sprites import Sprite

class PlatformDesign():
    """Class to build the entire level's platform as specified by the details
    given in the platform model. This class is responsible for generating 
    individual sprites passed and assigning specific position based on the 
    data return by the model for the current level."""

    def __init__(self, model):
        """Method to initialise the object, bind the model to the instance 
        and get the corresponding values for each sprite from the model. 
        Additionally initialises the class properties."""
        # Add the model to the object
        self.model = model
        # Get the level platform design from the model for the current level
        self.levelPlatform = model.get_level_platform()
        # Get each charactor's corresponding value
        self.block = self.model.get_char_representations("block")
        self.worm = self.model.get_char_representations("worm")
        self.coin = self.model.get_char_representations("coin")
        self.invisBlock = self.model.get_char_representations("invis_block")
        self.castle = self.model.get_char_representations("castle")
        self.mouse = self.model.get_char_representations("mouse")
        # Initialise the class properties
        self.abstractLevelMaxHeight = 0
        self.abstractLevelMaxWidth = 0
        self.endPoint = None
        self.widthScaleFactor = 1
        self.heightScaleFactor =1

    def get_level_block_positions(self):
        """Method to return the positions of the block sprites."""
        return self._get_level_sprite_positions(self.block)

    def get_level_worm_positions(self):
        """Method to return the positions of the worm sprites."""
        return self._get_level_sprite_positions(self.worm)

    def get_level_coin_positions(self):
        """Method to return the positions of the coin sprites."""
        return self._get_level_sprite_positions(self.coin)

    def get_level_invis_positions(self):
        """Method to return the positions of the invisible block sprites."""
        return self._get_level_sprite_positions(self.invisBlock)

    def get_level_castle_positions(self):
        """Method to return the positions of the castle sprites."""
        return self._get_level_sprite_positions(self.castle)

    def get_level_mouse_positions(self):
        """Method to return the positions of the mouse sprites."""
        return self._get_level_sprite_positions(self.mouse)

    def get_level_end_point(self):
        """Method to return the end point of the level i.e. the point at 
        which the player has finished the level and won."""
        if self.endPoint == None:
            self._get_level_sprite_positions(self.block)
            self.endPoint = self.abstractLevelMaxWidth*32
            return self.endPoint
        else:
            return self.endPoint

    def _get_max_abstract_size(self):
        """Private method to get the maximum level platform width and height 
        at any point from the data supplied by the model. Note these are 
        relative units and do not yet correspond to pixel value positions."""
        self.abstractLevelMaxHeight = len(self.levelPlatform)
        self.abstractLevelMaxWidth = max((len(line) for line in self.levelPlatform))

    def _get_scale_factors(self):
        """Private method to get the scale factors for calculating the pixel 
        positions for each sprite within the level. This invokes another 
        internal method to retrieve the maximum relative width and then 
        calculates a scale factor for the game window size."""
        self._get_max_abstract_size()
        # This is the screen height minus the block
        # width minus the ground height
        max_height = 768 -32 +10 
        self.widthScaleFactor = 32
        self.heightScaleFactor = max_height/ self.abstractLevelMaxHeight

    def _get_level_sprite_positions(self, element):
        """Private method to return the position of every instance of a 
        given sprite in the current level according to the game model. A 
        sprite value can be passed in to check for its corresponding list 
        of positions. Returns a list of 2 pair tuples."""
        level = self.levelPlatform

        self._get_scale_factors()
        self.elements = []
        xPosition = -1
        yPosition = -1
        for row in level:
            yPosition += 1
            xPosition = -1
            for col in row:
                xPosition += 1
                if col.upper() == element:
                    # create the element on the game where necessary
                    position = (xPosition*self.widthScaleFactor, yPosition*self.heightScaleFactor)
                    self.elements.append(position)
        return self.elements
                    