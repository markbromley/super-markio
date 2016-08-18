# Import the pygame library
import pygame

class PrimaryController():
    """Class to abstract the differences between all different controllers,
    including the keyboard. The class uses pygame's joystick class to access 
    any connected controllers and the event class to access the keyboard. 
    Differences between all types of controller are smoothed over and a 
    dictionary is used to create links between the joystick axes and user-defined
    names for those axes. This class can later be inherited and accessed
    throughout the GameController class, where joystick events can be paired
    with game-specific events. The keyboard details is built-in and abstracted
    to the same level as the joystick details. """
    # Below lists to enumerate through the buttons found on the PS3 Controller.
    # All buttons based on practical experimentation. Comes with default initial
    # pressure values, although these are automatically overridden after usage
    # and this can just be an empty dictionary at the initialisation stage
    supportedControllers = {
        "Sony PLAYSTATION(R)3 Controller" : {
            "buttons" : {
                "SELECT": 0
                ,"LEFT_ANALOGUE": 1
                ,"RIGHT_ANALOGUE": 2
                ,"START": 3
                ,"ARROW_UP": 4
                ,"ARROW_RIGHT": 5
                ,"ARROW_DOWN": 6
                ,"ARROW_LEFT": 7
                ,"LEFT_2": 8
                ,"RIGHT_2": 9
                ,"LEFT_1": 10
                ,"RIGHT_1": 11
                ,"TRIANGLE": 12
                ,"CIRCLE": 13
                ,"CROSS": 14
                ,"SQUARE": 15
                ,"WEIRDCIRCLEBUTTON": 16
            },
            "axis" : {
                "LEFT_ANALGOUE_HORIZONTAL": 0
                ,"LEFT_ANALOGUE_VERTICAL": 1
                ,"RIGHT_ANALOGUE_HORIZONTAL": 2
                ,"RIGHT_ANALOGUE_VERTICAL": 3
                # I suspect that 4 - 7 supports the accelerometer (3 Axis) 
                # and gyroscope (YAW only) within the controller, but PyGame
                # doesn't have support for these sensors...
                ,"ARROW_UP" : 8
                ,"ARROW_RIGHT": 9
                ,"ARROW_DOWN": 10
                # ,"ARROW_LEFT":  #Can't access the left arrow for some 
                # reason- should be 11, but doesn't respond. Could be fault
                # with the controller?
                ,"LEFT_2": 12
                ,"RIGHT_2": 13
                ,"LEFT_1": 14
                ,"RIGHT_1": 15
                ,"TRIANGLE": 16
                ,"CIRCLE": 17
                ,"CROSS": 18
                ,"SQUARE": 19
            },
            # The below details are not mandatory. They are auto-calculated
            # and later replaced as the controller is used. Without them the
            # initial values are all set to 0 and updated as possible.
            "temporaryButtonPressureCache": {
                'SQUARE': -0.0206298828125, 
                'TRIANGLE': -0.93817138671875, 
                'ARROW_RIGHT': -0.16497802734375, 
                'CROSS': -0.91754150390625, 
                'ARROW_UP': -0.649505615234375, 
                'RIGHT_1': -0.134033203125, 
                'RIGHT_2': -0.288665771484375, 
                'ARROW_DOWN': -0.876312255859375, 
                'LEFT_ANALGOUE_HORIZONTAL': 0.453582763671875, 
                'RIGHT_ANALOGUE_VERTICAL': 0.010284423828125, 
                'CIRCLE': -0.515472412109375, 
                'RIGHT_ANALOGUE_HORIZONTAL': -0.103118896484375, 
                'LEFT_ANALOGUE_VERTICAL': -0.422698974609375, 
                'LEFT_1': -0.433013916015625, 
                'LEFT_2': 0.999969482421875
            }
        },# End of controller dictionary for PS3 Controller
        "keyboard" : {
        # The keyboard dictionary is different because PyGame has already
        # bothered to integrate... annoyingly back to front when compared to
        # the controller method.... this is hardwired in any way and is not
        # to be edited when new controllers added...
            8: 'K_BACKSPACE', 
            9: 'K_TAB',
            12: 'K_CLEAR',
            13: 'K_RETURN', 
            19: 'K_PAUSE', 
            27: 'K_ESCAPE', 
            32: 'K_SPACE',
            33: 'K_EXCLAIM',
            34: 'K_QUOTEDBL',
            35: 'K_HASH',
            36: 'K_DOLLAR',
            38: 'K_AMPERSAND',
            39: 'K_QUOTE', 
            40: 'K_LEFTPAREN',
            41: 'K_RIGHTPAREN',
            42: 'K_ASTERISK',
            43: 'K_PLUS',
            44: 'K_COMMA',
            45: 'K_MINUS',
            46: 'K_PERIOD',
            47: 'K_SLASH',
            48: 'K_0',
            49: 'K_1',
            50: 'K_2',
            51: 'K_3',
            52: 'K_4', 
            53: 'K_5', 
            54: 'K_6', 
            55: 'K_7', 
            56: 'K_8', 
            57: 'K_9', 
            58: 'K_COLON', 
            59: 'K_SEMICOLON', 
            60: 'K_LESS', 
            61: 'K_EQUALS', 
            62: 'K_GREATER', 
            63: 'K_QUESTION', 
            64: 'K_AT', 
            91: 'K_LEFTBRACKET', 
            92: 'K_BACKSLASH', 
            93: 'K_RIGHTBRACKET', 
            94: 'K_CARET', 
            95: 'K_UNDERSCORE', 
            96: 'K_BACKQUOTE', 
            97: 'K_a', 
            98: 'K_b', 
            99: 'K_c', 
            100: 'K_d', 
            101: 'K_e', 
            102: 'K_f', 
            103: 'K_g', 
            104: 'K_h', 
            105: 'K_i', 
            106: 'K_j', 
            107: 'K_k', 
            108: 'K_l', 
            109: 'K_m', 
            110: 'K_n', 
            111: 'K_o', 
            112: 'K_p', 
            113: 'K_q', 
            114: 'K_r', 
            115: 'K_s', 
            116: 'K_t', 
            117: 'K_u', 
            118: 'K_v', 
            119: 'K_w', 
            120: 'K_x', 
            121: 'K_y', 
            122: 'K_z', 
            127: 'K_DELETE', 
            256: 'K_KP0', 
            257: 'K_KP1', 
            258: 'K_KP2', 
            259: 'K_KP3', 
            260: 'K_KP4', 
            261: 'K_KP5', 
            262: 'K_KP6', 
            263: 'K_KP7',
            264: 'K_KP8', 
            265: 'K_KP9', 
            266: 'K_KP_PERIOD', 
            267: 'K_KP_DIVIDE', 
            268: 'K_KP_MULTIPLY', 
            269: 'K_KP_MINUS', 
            270: 'K_KP_PLUS', 
            271: 'K_KP_ENTER', 
            272: 'K_KP_EQUALS', 
            273: 'K_UP', 
            274: 'K_DOWN', 
            275: 'K_RIGHT', 
            276: 'K_LEFT', 
            277: 'K_INSERT', 
            278: 'K_HOME', 
            279: 'K_END', 
            280: 'K_PAGEUP', 
            281: 'K_PAGEDOWN', 
            282: 'K_F1', 
            283: 'K_F2', 
            284: 'K_F3', 
            285: 'K_F4', 
            286: 'K_F5', 
            287: 'K_F6', 
            288: 'K_F7', 
            289: 'K_F8', 
            290: 'K_F9', 
            291: 'K_F10', 
            292: 'K_F11', 
            293: 'K_F12', 
            294: 'K_F13', 
            295: 'K_F14', 
            296: 'K_F15', 
            300: 'K_NUMLOCK', 
            301: 'K_CAPSLOCK', 
            302: 'K_SCROLLOCK', 
            303: 'K_RSHIFT', 
            304: 'K_LSHIFT', 
            305: 'K_RCTRL', 
            306: 'K_LCTRL', 
            307: 'K_RALT', 
            308: 'K_LALT', 
            309: 'K_RMETA', 
            310: 'K_LMETA', 
            311: 'K_LSUPER', 
            312: 'K_RSUPER', 
            313: 'K_MODE', 
            315: 'K_HELP', 
            316: 'K_PRINT', 
            317: 'K_SYSREQ', 
            318: 'K_BREAK', 
            319: 'K_MENU', 
            320: 'K_POWER', 
            321: 'K_EURO'

        }# End of keyboard dictionary
    }# End of supportedControllers dictionary

    def __init__(self):
        """Initialise all the class properties and locate any connected 
        joysticks, selecting the joysticks in order of preference based on 
        the order in which they are specified. Initialise the top preference
        joystick."""

        # Initialise all pygame modules if they aren't already initialised
        pygame.init() 

        # Specify the type of controller, to begin with we'll assume it's a
        # computer keyboard
        self.controlType = "keyboard"
        self.controllerName = "keyboard"
        self.joystickController = ""

        # Below two values help to create button pressures when there isn't
        # one available for real
        self.defaultPressureValue = 1

        # Below is a list comprehension which lists all joysticks attached 
        #to the computer at the initialisation point
        joysticks = [x for x in range(pygame.joystick.get_count()) 
                    if self._test_joystick_supported(pygame.joystick.Joystick(x))]

        # If there are any joysticks attached, initialise them and set the 
        # class properties as appropriate
        if(joysticks):
            self.controlType = "joystick"
            # Create some shorthand properties to assign the selected 
            # controller attributes to for reference within the class internally
            self.buttons = self.supportedControllers[self.controllerName]['buttons']
            self.axis = self.supportedControllers[self.controllerName]['axis']
            # Initialise the controller and activate
            self.joystickController = pygame.joystick.Joystick(joysticks[0])
            self.joystickController.init()

            # Specify the controller name in the terminal
            print('Decided to use following controller: ' + self.controllerName)
        else:
            self.controlType = "keyboard"

    def get_controller_value(self):
        """Method to retrieve the controller values. Uses internal methods
        to search for axes or buttons if not available and fills pressure
        values where not available. Returns a list of lists, each inner list
        containing the specified axis name and its current pressure rating."""

        # Cache values for axis and button using the internal methods
        axisVal = self._get_controller_axis()
        buttonVal = self._get_controller_button()

        # Determine which is best to use, wherever possible use the axis 
        # value, because it contains more data
        if(len(axisVal)!=0):
            # Read the fiirst value if it exists
            if(len(axisVal[0])!=0):
                for indivAxisVal in axisVal:
                    # set the cache values for future use
                    self._set_cache_axis_values(indivAxisVal)
                # Return the value as appropriate
                return axisVal
        elif(len(buttonVal)!=0):
            # Read the first value of the button if it exists
            if(len(buttonVal[0])!=0):
                for indivButtonVal in buttonVal:
                    #Add a pressure value, as it doesn't already exist
                    indivButtonVal.append(self._get_cache_axis_values(indivButtonVal)) 
                return buttonVal
        else:
            # If there are no buttons being pressed return an empty list, 
            # containing a single empty button list
            return [[]]

    def get_keyboard_value(self):
        """This method reads the values of the keyboard using pygame's internal
        key module. Converting the output to the abstracted format using
        internal methods. """
        # get pygame key pressed list
        keys = pygame.key.get_pressed()
        # Convert to abstracted format
        key_values = self._convert_keyboard_button_to_name_value(keys)
        return key_values

    def get_input_value(self):
        """Method to get input value, irrelevant of controller type. Uses
        internal methods to select between joysticks and keyboards available.
        Provides all data in a consistent structured format."""
        if(self.controlType == 'keyboard'):
            return self.get_keyboard_value()
        else:
            return self.get_controller_value()

    def _test_joystick_supported(self, joystick):
        """Private method. Checks to see if the specified controller 
        (found via the initialisation procedure) is given in the 
        supportedControllers dictionary and if the information to connect 
        and abstract is available. """
        for title, details in self.supportedControllers.items():
            if(joystick.get_name() == title):
                self.controllerName = title
                return True 
        return False

    def _get_controller_button(self):
        """Private method. This method retrieves the currently depressed 
        controller buttons and returns a list of the buttons active."""
        # Below get a list of all the buttons which are showing a value 
        # greater than 0 i.e. buttons being pressed.

        # Below pygame pump statement pumps the latest information to 
        # appropriate functions for each frame in event loop
        pygame.event.pump()

        # Below return each depressed button (list comprehension)
        return [[word] for word, number in self.buttons.items()
                if(self.joystickController.get_button(number)) != 0 ]

    def _get_controller_axis(self):
        """Private method. This method retrieves the currently active
        controller axes and returns a list of those active axes."""
        
        # Update all events and ensure the latest information is available
        pygame.event.pump()

        # Return a list comprehension of axes currently active on the selected controller
        return [[word, self.joystickController.get_axis(number)]
                for word, number in self.axis.items()
                if((self.joystickController.get_axis(number)) not in (0,1,-1)) ]

    def _set_cache_axis_values(self, curAxisVal):
        """Private method. This method updates and generates (if necessary)
        the temporaryButtonPressureCache data for the currently selected
        controller, to allow the final abstraction to emulate pressure
        values if not available."""

        # Below assigns the axis value to the appropriate cache key 
        self.supportedControllers[self.controllerName]["temporaryButtonPressureCache"][curAxisVal[0]] = curAxisVal[1]

    def _get_cache_axis_values(self, curAxisVal):
        """Get the cached pressure value for the specified axis. If it isn't
        available provide an alternate default where possible."""

        # Get the current cache values
        tmpCache = self.supportedControllers[self.controllerName]["temporaryButtonPressureCache"]

        # If the value is in the cache return that, otherwise return the default pressure value
        if(curAxisVal[0] in tmpCache):
            return tmpCache[curAxisVal[0]]
        else:
            return self.defaultPressureValue

    def _convert_keyboard_button_to_name_value(self, keys):
        """Private method. Converts all the keys supplied to their 
        corresponding name values, supplied in the correct format for 
        the abstraction."""
        # Loop through all the keys and compare them to the dictionary at 
        # the top to get a name for the key, if and only if the key is
        # currently active, return this as the list for the keyboard
        return [[self.supportedControllers['keyboard'][i], 1] 
                for i,key in enumerate(keys) if key != 0]



# // note on plain values:
# // buttons are either 0 or 1
# // button axes go from 0 to -1
# // stick axes go from 0 to +/-1

if __name__ == "__main__":
    """Main 'Controller' class test method. Allows unit testing inside the 
    Terminal. This will display both the axis and button results from the 
    controller as they change. Buttons held in the same position will only 
    register once, so an to preserve Terminal screen space."""

    # Print a startup message
    print('\nThis is the \'Controller\' Class test function.\nThis will \
        display both axis and button results as they change.\n\
        Buttons held in the same position will only register once, so as to \
        preserve Terminal screen space.\n\n')
    # Initialise the controller and set everything up...
    ps3 = primaryController()
    # These variables are used to store the previous values, to help 
    # preserve terminal screen space
    curButtonVal = []
    curAxisVal = []
    # Create an infinite loop for the program to run inside
    while True:
        liveValue = ps3.get_input_value()
        if(liveValue and liveValue not in (curButtonVal, [], [[]])):
            print(liveValue)
            curButtonVal = liveValue

