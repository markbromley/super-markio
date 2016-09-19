import pygame
from easypg.sprites import Sprite
from random import randint

class Markio(Sprite):
    """Represents the Markio character. This is the primary game character -
    allows for manipulating position, applying gravity, changing
    sprite sequence, jumping, dying and checking interaction with other sprites."""

    def __init__(self, screen, eventManager, levelBlocks):
        """Bind the screen, Event Manager and level block positions to the 
        instance and add a dictionary to enumerate character actions to class 
        methods."""
        # Image store for the sprite graphics
        self.images = {}
        # Activate the super class initialisation method
        super().__init__(screen, './assets/images/dinosaur', state = 'run', direction='e')
        # Bind the Event Manager to this class and subscribe as a listener
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        # Store incoming notifications from the Event Manager
        self.inComingNotification = []
        # Bind the screen to this class
        self.screen = screen
        # Add the level brick positions to a single list which is accessible 
        # throughout this class
        self.levelBlocks = levelBlocks[0] + levelBlocks[1]
        # Map character actions between controller events from event manager
        # to their corresponding class methods
        self.actions = {
            "CHARACTER_GO_RIGHT" : self.go_right
            ,"CHARACTER_GO_LEFT" : self.go_left
            ,"CHARACTER_JUMP" : self.jump
            ,"CHARACTER_FIRE_WEAPON" : self.fire
            ,"CHARACTER_COLLIDE_BLOCK" : self.fire
            ,"CHARACTER_AT_END" : self.won_level
            ,"CHARACTER_COLLIDE_WORM" : self.hit_enemy
            ,"CHARACTER_COLLIDE_MOUSE" : self.hit_enemy
        }
        # Below creates the basic rectangle for the sprite, initialising the
        # bottom to the position of the ground level
        self.rect = self.image.get_rect()
        self.screenSize = screen.get_size()
        self.rect.bottom = self.screenSize[1] - 75
        # Below specifies horizontal and vertical velocities for the character
        self.vx = 0
        self.vy = 0
        # Below Boolean value to specify if character at end of level
        self.atEnd = False
        # Below Boolean value specifies if character currently jumping
        self.currentlyJumping = False
        # End of initialisation method

    def notify_event(self, event):
        """Check if the event exists and assign it to the inComingNotification 
        property."""
        if event:
            self.inComingNotification = event

    def hit_enemy(self):
        """Specifies that the character has been hit by an enemy 
        sprite. Allows appropriate action to be taken."""
        # Clear the Event Manager, to allow new events to be posted
        self.eventManager.event_clear(self.inComingNotification)
        # Post a new event to say this character is dead
        self.eventManager.post(["CHARACTER_DEAD"])

    def won_level(self):
        """Handles when the player reaches and wins the end of the 
        level. Sets the character atEnd property to true."""
        self.atEnd = True
        # Below clear the Event Manager, to allow new events to be posted
        self.eventManager.event_clear(self.inComingNotification)

    def fire(self):
        self.eventManager.event_clear(self.inComingNotification)
 
    def new_collision(self):
        """Detects if the sprite will collide with any of the level 
        bricks during its next movement. Uses characters internal representation 
        of block positions to calculate if there will be a collision. """
        for blockTuple in self.levelBlocks:
            if self.rect.collidepoint(blockTuple):
                return True
        return False

    def _get_char_bottom_position(self):
        """Private method to get the character's bottom position"""
        return self.rect.bottom

    def _get_char_right_position(self):
        """Private method to get the character's right position"""
        return self.rect.right


    def move(self):
        """Method to move the character by the next specified amount. Uses 
        gravity, controller requests and additional physics methods to 
        calculate next character position (horizontal and vertical) and 
        reposition character sprite appropriately."""
        # If we aren't at the end of the level
        if not self.atEnd:
            # If the character has room to move left or right
            if (self.rect.left>=0) or (self.rect.right>=0 and self.vx>=0):
                self.rect.centerx += self.vx
            self.rect.centery -= self.vy
        # Apply gravity to the move
        self.gravity()
        # If there are other events occurring, such as new controller input, 
        # set the horizontal velocity to zero
        if self._check_for_incoming_notifications() <= 0:
                self.vx = 0

    def gravity(self):
        """This method applies gravity to the character. Gravity can be set to
        act differently when the character is going upwards or downwards. The
        method takes into account if collisions occur with either the floor or
        with the a platform within the game. The collisions are detected using 
        internal methods."""
        # Check if the player is going to collide anywhere
        hit = self.new_collision()
        # If we have collided
        if hit:
            if self.vy>0: #Going up
                self.vy = 0
                self.rect.centery += 20
                self.currentlyJumping = True
            # Else if we're going down
            else:
                self.vy = 0
                if self.currentlyJumping:
                    self.rect.centery -=38
                    self.currentlyJumping = False
            # If we're colliding stop the horizontal velocity
            if self.vx != 0:
                self.vx =0
        # Else, if we haven't collided with anything
        else:
            # If we're going upwards
            if self.vy>=0:
                self.vy -= 0.41
            # Else, if we're going downwards
            else:
                self.vy -= 4.41
        # Check if we're currently jumping
        if self.currentlyJumping:
            if self.vy>=0:
                self.vy = self.vy -0.41
            else:
                self.vy -= 4.41
            self.vx =0

    def jump(self):
        """Method to initialise character's jumping. Adds a specific sound 
        effect and changes the character sequence too."""
        # Check that we aren't already jumping and if so, put us into 
        # vertical motion true
        if self.currentlyJumping == False:
            # Try to load and play the specific sound file for the jump effect. 
            # If it doesn't load ignore it and carry on anyway.
            try:
                sound = pygame.mixer.Sound('./assets/audio/jump.wav')
                sound.play()
            except Exception:
                pass
            # Set the currentlyJumping property to true, assign a positive 
            # velocity and change the character sequence
            self.currentlyJumping = True
            self.vy = 20
            self._set_char_sequence('roar', self.direction)
        # Clear the Event Manager of the current incoming event that was made
        # to request the character jump, now that we have performed all the 
        # actions required for the character to jump
        self.eventManager.event_clear(self.inComingNotification)

    def go_right(self):
        """Method to move the character to the right. Changes the character 
        sequence to the appropriate direction too, using internal methods."""
        # Set the horizontal velocity and the character sequence
        self.vx = 20
        self._set_char_sequence('run', 'e')
        # Clear the current event from the Event Manager
        self.eventManager.event_clear(self.inComingNotification)

    def go_left(self):
        """Method to move the character to the left. Changes the character 
        sequence to the appropriate direction too, using internal methods."""
        # Set the horizontal velocity and the character sequence
        self.vx = -20
        self._set_char_sequence('run', 'w')
        # Clear the current event from the Event Manager
        self.eventManager.event_clear(self.inComingNotification)

    def update(self):
        """Method to update the sprite. Invokes internal move and 
        check_bounds methods."""
        self.move()
        self.check_bounds()

    def check_bounds(self):
        """Method to check that character is within the physical bounds of 
        the window. Maintains the character in the game window and prevents 
        movement outside."""
        # If there's something to the left of the character
        if self.rect.left < 0:
            # If we are heading in the left direction
            if self.vx < 0 and False:
                self.eventManager.post(["CHARACTER_AT_LEFT"])
                self._blocks_update_left()
                self.eventManager.event_clear(self.inComingNotification)
                self.vx = 0
        # If we're as far as we can go to the right of the screen
        if self.rect.right > self.screenSize[0]-250:
            # If we are heading in the right direction
            if self.vx > 0:
                self.vx = 0
                # If we aren't at the end of the level
                if not self.atEnd:
                    self.eventManager.post(["CHARACTER_AT_RIGHT"])
                # Update the internal representation of the level block positions
                self._blocks_update_right()
                # Clear the current event from the Event Management
                self.eventManager.event_clear(self.inComingNotification)
                self.vx =0
        # If we are at the top of the game window and we're going up, set 
        # the vertical velocity to zero
        if self.rect.top < 0:
            if self.vy > 0:
                self.vy = 0
        # If we're at the bottom of the screen  and we're going down, set
        # the vertical velocity to zero
        if self.rect.bottom > self.screenSize[1]:
            if self.vy < 0:
                self.vy = 0

    def _blocks_update_general(self, nudge):
        """Private method to move the characters representation of the block 
        positions by the appropriate amount, to reflect their new positions 
        within the game."""
        # Empty list for the new brick positions
        newLevelBlocks = []
        # For each block, nudge it by the specified amount in the correct 
        # direction, finally replace the current positions with the new 
        # updated positions
        for block in self.levelBlocks:
            newBlock = (block[0]+nudge, block[1])
            newLevelBlocks.append(newBlock)
        self.levelBlocks = newLevelBlocks

    def _blocks_update_left(self):
        """Private method to move the characters representation of the 
        block positions to the left. Uses internal methods to reposition 
        representation."""
        self._blocks_update_general(10)
 
    def _blocks_update_right(self):
        """Private method to move the characters representation of the 
        block positions to the right. Uses internal methods to reposition 
        representation."""
        self._blocks_update_general(-10)

    def _set_char_sequence(self, state, direction):
        """Private method to set the image sequence for the character. 
        Sets the sequence to the requested state and direction."""
        # Set the state and direction as requested
        self.direction = direction
        self.state = state
        # Reset the sequence as requested
        self.sequence = self.images[self.state][self.direction]
        # Animate the character wit the new sequence
        self.animate()

    def _check_for_incoming_notifications(self):
        """Private method which uses the Event Manager and tries to match 
        current events to those specified in the characters action list."""
        # Local variable to count how many events being registered can be 
        # located in the characters action list
        trueEventCount = 0
        # Look at each event in the incoming notification and try to execute 
        # the corresponding command for that event. If there is no action for
        # this event, an exception is thrown and caught and the loop continues.
        for ev in self.inComingNotification:
            trueEventCount += 1
            try:
                self.actions[ev]()
            except KeyError:
                trueEventCount -= 1
                pass
        # Empty the incoming notifications array
        self.inComingNotification = []
        return trueEventCount
# End of Markio class

class PlatfromObject(Sprite):
    """This class acts as a general class to create objects for the platform.
    Methods for positioning the object and for passing events to and from the
    object are provided by this class."""

    def __init__(self, screen, position, eventManager, assetUrl, size, state, direction):
        """Initialise the class variables and execute the parent class 
        initialisation method. Bind the Event Manager to the object and 
        set the initial image sequence."""
        # A dictionary to act as an image store for the sprite
        self.images = {}
        # Initialise the parent class
        super().__init__(screen, assetUrl, alpha = True, state = state, 
                         direction = direction, position = position)

        # Bind the Event Manager to this instance and subscribe to new posts
        self.eventManager = eventManager
        self.eventManager.register_listener(self)

        # Initialise the image sequence
        self.image = self.images['-']['-'][0]
        self.image = pygame.transform.scale(self.image, size)
        self.images['-']['-'][0] = self.image

    def notify_event(self, event):
        """Method required by all classes registered as a subscriber to the 
        Event Manager. This is currently a stub method to be overriden by 
        subsequent classes."""
        pass

    def update(self, event):
        """Method to update the sprite. Invokes internal move, animate and 
        check_bounds methods."""
        # If we're moving right move the position of the sprite object back
        # by the corresponding amount
        if event == ["CHARACTER_AT_RIGHT"]:
            self.rect.centerx -= 10
            # Clear the Event Manager of the current event
            self.eventManager.event_clear(event)
        # If we're moving left move the position of the sprite object back 
        # by the corresponding amount
        if event == ["CHARACTER_AT_LEFT"]:
            self.rect.centerx += 10
            # Clear the Event Manager of the current event
            self.eventManager.event_clear(event)
        # Update the position
        self.animate()
        self.move()
        self.check_bounds()

class Block(PlatfromObject):
    """Class to generate a single Block object for the game platform at a 
    specific given position."""

    def __init__(self, screen, position, eventManager):
        """Initialise the block object and position at the requested 
        location."""
        super().__init__(screen, position, eventManager, 
                         './assets/images/block', (32,32), '-', '-')

class InvisibleBlock(PlatfromObject):
    """Class to generate a single Invisible Block object for the game 
    platform at a specific given position."""

    def __init__(self, screen, position, eventManager):
        """Initialise the Invisible Block object and position at the 
        requested location."""
        super().__init__(screen, position, eventManager,
                        './assets/images/invis_block', (32,32), '-', '-')

class Castle(PlatfromObject):
    """Class to generate a single Castle object for the game platform 
    at a specific given position."""

    def __init__(self, screen, position, levelEndPoint, eventManager):
        """Initialise the Castle object and position at the requested 
        location."""
        super().__init__(screen, position, eventManager, 
                        './assets/images/castle', (354,592), '-', '-')

    def update(self, event):
        """Method to update the sprite. Invokes internal move, animate and 
        check_bounds methods."""
        # If we're moving right move the position of the sprite object back
        # by the corresponding amount
        if event == ["CHARACTER_AT_RIGHT"]:
            self.rect.centerx -= 10
            self.eventManager.event_clear(event)
            if self.rect.centerx <= 1250:
                self.eventManager.post(["CHARACTER_AT_END"])
        # If we're moving left move the position of the sprite object back
        # by the corresponding amount
        if event == ["CHARACTER_AT_LEFT"]:
            self.rect.centerx += 10
            self.eventManager.event_clear(event)
        # Update the sprite position
        self.animate()
        self.move()

class Coin(PlatfromObject):
    """Class to generate a single Coin object for the game platform at a 
    specific given position."""

    def __init__(self, screen, position, eventManager):
        """Initialise the Coin object and position at the requested 
        location."""
        super().__init__(screen, position, eventManager, 
                        './assets/images/coin', (32,32), '-', '-')

class EnemySprite(Sprite):
    """This class acts as a general class to create enemy sprite objects. 
    Methods for positioning the object and for passing events to and from 
    the object are provided by this class."""

    def __init__(self, screen, position, eventManager,assetUrl, state, direction):
        """Initialise the class variables and execute the parent class 
        initialisation method. Bind the Event Manager to the object and 
        set the initial image sequence."""
        # Create a store for the images for the sprite sequence
        self.images = {}
        # Execute the parent class initialisation method
        super().__init__(screen, assetUrl, alpha = False, state = state, 
                         direction = direction, position = position)
        # Get the game window screen size
        self.screenSize = screen.get_size()
        # Bind the Event Manager to this object and register as a 
        # subscriber to posts
        self.eventManager = eventManager
        self.eventManager.register_listener(self)

    def notify_event(self, event):
        """Method required by all classes registered as a subscriber to the 
        Event Manager. This is currently a stub method to be overridden by 
        subsequent classes."""
        pass

    def move(self):
        """Method to move sprite by the next specified amount. Calculates 
        next character position (horizontal and vertical) and 
        repositions sprite appropriately."""
        self.rect.centerx += self.vx

    def update(self, event):
        """Method to update the sprite. Invokes internal move, animate 
        and check_bounds methods. Also updates position of enemy sprites 
        to reflect the new position of the character i.e. to make them 
        move backwards as the character moves forwards to create the 
        illusion of the character travelling forward through the world."""
        # If we're currently at the right of the game window, move the enemy
        # sprites backwards
        if event == ["CHARACTER_AT_RIGHT"]:
            self.rect.centerx -= 10
            # Remove the event for the Event Manager now it is finished with
            self.eventManager.event_clear(event)
        # If we're currently at the left of the window, move the enemy
        # sprites forwards
        if event == ["CHARACTER_AT_LEFT"]:
            self.rect.centerx += 10
            # Remove the event for the Event Manager now it is finished with
            self.eventManager.event_clear(event)
        # Update the sprite details
        self.animate()
        self.move()
        self.check_bounds()

    def _set_char_sequence(self, state, direction):
        """Private method to set the image sequence for the character. 
        Sets the sequence to the requested state and direction."""
        self.direction = direction
        self.state = state
        self.sequence = self.images[self.state][self.direction]
        self.animate()

    def _alter_state(self):
        """Private method to inverse the horizontal state direction of the 
        sprite. If the direction is currently set to East, it will be set to 
        West and vice versa. Automatically resets the character image sequence
         to reflect the new direction using internal methods."""
        if self.direction =='e':
            self.direction = 'w'
            # Set character sequence
            self._set_char_sequence(self.state, self.direction)
        else:
            self.direction = 'e'
            # Set character sequence
            self._set_char_sequence(self.state, self.direction)

class Mouse(EnemySprite):
    """Class to generate a single Mouse object for the game. The Mouse is an
     enemy in the game and hence inherits from the EnemySprite class. The
      Mouse has a random horizontal velocity assigned at initialisation and
       repeatedly moves back and forth by an allowableTravel property, set
        at initialisation."""

    def __init__(self, screen, position, eventManager):
        """Initialise the Mouse object and position at the requested location.
         Pass in the screen and eventManager to bind them to the instance."""
        super().__init__(screen, position, eventManager,
                        './assets/mouse', 'move', 'w' )
        # Cache the original position. This will be used later to work out 
        # the distance the Mouse has travelled
        self.originalPosition = position
        # Set the initial velocity to a random amount
        self.vx = -1 * (randint(1,2))
        # Limit the distance the mouse can travel in either direction to +- 20px
        self.allowableTravel = 20

    def check_bounds(self):
        """Method to check that character is within the physical bounds of 
        their allowableTravel property. Maintains the character in the game 
        window and prevents movement outside the allowableTravel distance."""
        # If we've gone too far left, turn around
        if self.rect.centerx< self.originalPosition[0]-self.allowableTravel:
            self.vx *=-1
            # Use internal method to change sprite direction in image sequence
            self._alter_state()
        # If we've gone too far left, turn around
        if self.rect.centerx > self.originalPosition[0] + self.allowableTravel:
            self.vx *= -1
            # Use internal method to change sprite direction in image sequence
            self._alter_state()
        # If we go off the screen, delete the sprite to reclaim the memory etc
        if self.rect.left < 0:
            self.kill()
        
class Worm(EnemySprite):
    """Class to generate a single Worm object for the game.The Worm is an 
    enemy in the game and hence inherits from the EnemySprite class. The Worm 
    has a random horizontal velocity assigned at initialisation and constantly
    moves leftward until reaching the edge of the game window and automatically 
    being removed from its containing group."""

    def __init__(self, screen, position, eventManager):
        """Initialise the Mouse object and position at the requested location.
        Pass in the screen and eventManager to bind them to the instance."""
        # Call the EnemySprite initialisation method and pass in all 
        # required information
        super().__init__(screen, position, eventManager,
            './assets/images/worm', 'creep', 'w' )
        # Generate the random horizontal velocity
        self.vx = -0.06 * (randint(2,9))

    def check_bounds(self):
        """Method to check that character is within the physical bounds of the
        window. Maintains the character in the game window and kills the 
        character on movement outside."""
        if self.rect.left < 0:
            self.kill()

class Dragonfly(EnemySprite):
    """Class to generate a single Dragonfly object for the game. 
    The Dragonfly is an enemy in the game and hence inherits from the 
    EnemySprite class. The Dragonfly has a random horizontal and vertical 
    velocity assigned at initialisation and repeatedly moves back and 
    forth within the game window."""

    def __init__(self, screen, eventManager):
        """Initialise the Dragonfly object and position at the requested 
        location. Pass in the screen and eventManager to bind them 
        to the instance."""
        # Call the parent class initialisation method
        super().__init__(screen, None, eventManager, 
                         './assets/images/dragonfly', '-', 'e' )
        # Set the random vertical and horizontal velocities
        self.vx = 2 * (randint(2,9))
        self.vy = 2
        # Set the random start position from the top
        self.rect.top = 5 * (randint(2,9))

    def move(self):
        """Method to move sprite by the next specified amount. Calculates 
        next character position (horizontal and vertical) and repositions 
        sprite appropriately."""
        self.rect.centerx += self.vx
        self.rect.centery += self.vy 

    def update(self):
        """Method to update the sprite. Invokes internal move, animate and 
        check_bounds methods."""
        self.animate()
        self.move()
        self.check_bounds()

    def check_bounds(self):
        """Method to check that sprite is within the physical bounds of the 
        window. Maintains the character in the game window and alters 
        direction of the sprite on collision with the edges of the window."""
        # If the sprite hits the sides, inverse the horizontal direction 
        # and update the sprite sequence
        if self.rect.left < 0 or self.rect.right > self.screenSize[0]:
            if self.direction =='e':
                self.direction = 'w'
            else:
                self.direction = 'e'
            # Refresh the sprite sequence using internal private method 
            # inherited from EnemySprite class
            self._set_char_sequence(self.state, self.direction)
            # Change direction
            self.vx *= -1
        # If the sprite hits the top of the window or the imaginary lower 
        # limit, inverse the vertical direction
        if (self.rect.top < 0 or 
            self.rect.bottom > (self.screenSize[1] * (randint(2, 3)*0.1))):
                self.vy *= -1


class Cloud(Sprite):
    """Class to create a single cloud instance. This object produces a simple
    animated cloud graphic for the game, to add dynamically positioned clouds 
    which move over the background layer."""

    def __init__(self, screen, eventManager):
        """Initialise the cloud instance and set the dictionary for the image
        store, bind the screen and Event Manager to the instance and
        initialise the vertical and horizontal velocities."""
        # Create a dictionary for the image store for the image sequences
        self.images = {}
        # Invoke the parent class initialisation method
        super().__init__(screen, './assets/images/cloud', alpha = True)
        # Bind the Event Manager to the instance of the Cloud object
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        # Set the initial image in the image sequence
        self.image = self.images['-']['-'][0]
        self.image = pygame.transform.scale(self.image, (300, 101))
        self.images['-']['-'][0] = self.image
        # Get the size of the image and assign to the rect property
        self.rect = self.image.get_rect()
        # Bind the screen size to the Cloud instance for later use in 
        # boundary checking
        self.screenSize = screen.get_size()
        # Set the initial horizontal and vertical velocities
        self.vx = 1
        self.vy = 10

    def notify_event(self, event):
        """Method required by all classes registered as a subscriber to the 
        Event Manager. Currently a stub method which performs no operations."""
        pass

    def move(self):
        """Method to move the cloud object horizontally by the specified 
        current horizontal velocity. method maintains a fixed position on 
        screen relative to the top of the game window."""
        self.rect.top = 30
        self.rect.centerx += self.vx


    def update(self):
        """method to update the state of the Cloud instance to the current 
        values. Invokes the internal methods move and check_bounds."""
        self.move()
        self.check_bounds()

    def check_bounds(self):
        """Method to check that sprite is within the physical bounds of the 
        window. Maintains the sprite in the game window and alters direction 
        of the sprite on collision with the edges of the window."""
        # If the sprite hits the sides, inverse the horizontal direction
        if self.rect.left < 0 or self.rect.right > self.screenSize[0]:
            self.vx *= -1

