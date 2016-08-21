# Import the generic controller class, which abstracts the differences between
# any controller, and produce a 'generic' controller 
from controllers import generic_controller as GenericController

class GameController(GenericController.PrimaryController):
    """Bridges the gap between the generic controller and the game.
    Pairing controller button names with standard game events. A dictionary of
    links between button types and game actions is provided for each controller.
    Controllers are referred to by their default specified controller system name."""

    def __init__(self, eventManager):
        """Initialise the class variables, register the Event Manager and 
        subscribe to events, initialise the parent class too and inherit as 
        required."""
        # The dictionary of controller-button - game-event pairs.
        self.buttonMatches = {
            "Sony PLAYSTATION(R)3 Controller" : {
                "CROSS" : "CHARACTER_JUMP"
                ,"LEFT_1" : "CHARACTER_FIRE_WEAPON"
                ,"LEFT_2" : "CHARACTER_FIRE_WEAPON"
                ,"ARROW_LEFT" : "CHARACTER_GO_LEFT"
                ,"ARROW_RIGHT" : "CHARACTER_GO_RIGHT"
                ,"TRIANGLE" : "GAME_PAUSE"
            },# End of specific controller dictionary
            "keyboard" : {
                "K_SPACE" : "CHARACTER_JUMP"
                ,"K_a" : "CHARACTER_FIRE_WEAPON"
                ,"K_s" : "CHARACTER_FIRE_WEAPON"
                ,"K_d" : "CHARACTER_FIRE_WEAPON"
                ,"K_LEFT" : "CHARACTER_GO_LEFT"
                ,"K_RIGHT" : "CHARACTER_GO_RIGHT"
                ,"K_p" : "GAME_PAUSE"
            } # End of keyboard controller dictionary
        } # End of buttonMatches dictionary

        # Initialise the parent class
        super().__init__()

        # Bind the Event Manager 
        self.eventManager = eventManager
        self.eventManager.register_listener(self)
        # Initialise the actions array
        self.actions = []

    def get_game_event_values(self):
        """Retrieves the current buttons being depressed by the
        controller. A pressure rating is returned with the button specifying
        the button force."""
        self.actions = []
        values = self.get_input_value()
        if len(values) > 0:
            for value in values:
                if len(value) > 0:
                    if value[0] in self.buttonMatches[self.controllerName]:
                        self.actions.append((self.buttonMatches[self.controllerName][value[0]]))
                        
    def show_actions(self):
        """Display the current controller actions. This method can be useful
        for debugging."""
        if self.actions:
            self.eventManager.post(self.actions)

    def notify_event(self, event):
        """Stub method required by all subscribers of Event Manager."""
        pass
