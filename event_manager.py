import pygame

class EventManager():
    """Acts as interaction mediator. Weak references are used to allow 
    garbage collection to remove listeners that are no longer referenced, 
    even if they haven't unregistered with the Event Manager. """

    def __init__(self):
        """Creates empty array for event queue and sets 
        current event and score values to defaults."""
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        # Initialise class properties
        self.eventQueue = []
        self.currentEvent = None
        self.score = 0

        # Initialise rapid counter material
        self.rapidCounterName = ''
        self.rapidCounterValue = 0
        self.rapidCounterIncrementLevel = 1

    def register_listener(self, listener):
        """Register for events. N.B. All subscribers are passed all events. 
        Event types can be used if the game is required to scale."""
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """Remove listener from event manager. """
        if listener in self.listeners.keys():
            del self.listeners[listeners]

    def post(self, event):
        """Post event to be distributed to the other subscribers"""
        # Send the event to the Event Manager's Rapid Counter method to check
        # if the counter's need incrementing
        self._rapid_counter_update(event)

        # If the event is in the list of events to be ignored, return 0 and 
        if (event == ["CHARACTER_COLLIDE_COIN"] or
            event == ["CHARACTER_COLLIDE_INVIS"] or
            event == ["CHARACTER_COLLIDE_CLOUD"] or
            event == ["CHARACTER_COLLIDE_DRAGONFLY"]):
            return 0

        # If there currently isn't an event being dealt with by the Event 
        # manager, then set the latest event and notify all the classes 
        # currently subscribing. If there is currently an event being dealt 
        # with, ignore this event. If the game is required to scale, the event
        # queue can be used. Using this method, prevents duplicate events 
        # being generated by controllers etc.
        if self.currentEvent == None:
            self.currentEvent = event
            for listener in self.listeners.keys():
                listener.notify_event(event)

    def create_game_rapid_counter(self, rapidCounterName, incrementLevel):
        """This can be used to manager a counter, such as health, time or scores 
        etc. Unlike the standard Event Manager this counter does acknowledge 
        duplicate events and as such has corresponding property differences."""
        # Initialises details
        self.rapidCounterName = rapidCounterName
        self.rapidCounterValue = 0
        self.rapidCounterIncrementLevel = incrementLevel
        
    def _rapid_counter_update(self, event):
        """Increments the counter if the current event 
        corresponds to the counter's rapid counter initialisation properties."""
        if event[0] == self.rapidCounterName:
            self.rapidCounterValue += self.rapidCounterIncrementLevel

    def get_rapid_counter_value(self, event):
        """Returns current Rapid Counter value."""
        return self.rapidCounterValue

    def event_clear(self, event):
        """Empties current array when previous action's method has finished,
        thus preventing the Event Manager from blocking."""
        if self.currentEvent == event:
            self.currentEvent = None
