import pygame

class GenerateGroups():
    """Generates sprite groups for individual sprites. Contains methods to 
    update all sprites in all groups and to check for collision detection with 
    the primary character (the first sprite supplied)."""

    def __init__(self, screen, listOfCharactors, listOfCharactorNames, destroyOnCollision, eventManager):
        """Bind to the Event Manager and register as a 
        subscriber. Additionally create a sprite image mask, using pygame for 
        the main character, to provide additional collision accuracy and cache 
        this mask, to prevent calling this method too often (because the method 
        is expensive)."""
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        self.event = None
        self.screen = screen
        self.groupList = []
        self.listOfCharactorNames = listOfCharactorNames
        self.listOfCharactors = listOfCharactors
        self.destroyOnCollision = destroyOnCollision
        # Create the sprite mask for the player character
        self.listOfCharactors[0].mask = pygame.mask.from_surface(self.listOfCharactors[0].image)
        groupNumber = 0
        # Create each type of sprite
        for charactorData in listOfCharactors:
            self.groupList.append(pygame.sprite.Group(charactorData))
            groupNumber += 1

    def update_all_player_groups(self):
        """Updates all sprites in all groups; posts the latest events
        to each sprite if appropriate and draws the sprites to the screen."""
        # Clear the event property
        self.event = None
        # Check for any new sprite collisions
        self._check_player_collide()
        # For each sprite group, update appropriately
        for group in self.groupList:
            if self.groupList.index(group) == self.listOfCharactorNames.index('block'):
                group.update(self.event)
            elif self.groupList.index(group) == self.listOfCharactorNames.index('worm'):
                group.update(self.event)
            elif self.groupList.index(group) == self.listOfCharactorNames.index('invis'):
                group.update(self.event)
            elif self.groupList.index(group) == self.listOfCharactorNames.index('coin'):
                group.update(self.event)
            elif self.groupList.index(group) == self.listOfCharactorNames.index('castle'):
                group.update(self.event)
            elif self.groupList.index(group) == self.listOfCharactorNames.index('mouse'):
                group.update(self.event)
            else:
                group.update()
            # Draw each group on the game window
            group.draw(self.screen)

    def notify_event(self, event):
        """Attaches current event to object instance 'event' property."""
        self.event = event

    def _check_player_collide(self):
        """Check if any sprites in any groups are colliding with the player 
        sprite. If so checks to see if the sprites should be removed from their 
        corresponding group and does so if required, then emits event specifying 
        collision type."""
        i = 1 
        # For each group check for collisions
        for group in self.groupList[1:]:
            if self.destroyOnCollision[i]:
                collide = pygame.sprite.spritecollide(self.listOfCharactors[0], 
                                                      group,
                                                      True,
                                                      pygame.sprite.collide_mask)
            else:
                collide = pygame.sprite.spritecollide(self.listOfCharactors[0],
                                                      group,
                                                      False,
                                                      pygame.sprite.collide_mask)
            if collide:
                collision = ["CHARACTER_COLLIDE_" + self.listOfCharactorNames[i].upper()]
                self.eventManager.post(collision)
            i +=1