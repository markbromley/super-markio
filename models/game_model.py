class GameModel():
    """This class provides a data store for the entire game. Containing level
    configuration, image URLs, score file URLs and level enumeration 
    dictionaries. Getter and setter methods are available as convenient manners
    for accessing level specific values. This allows a level to be set once 
    and for all subsequent asset requests to be automatically tailored to 
    that specific level The level can be set again at a later point to change
    the current level."""
    def __init__(self):
        """Initialise  all class properties, including the level designs and
        asset URLs. Individual sprites are represented by specific letters
        within the level designs. These letters are purely internal and a
        dictionary is provided to enumerate sprite names against their
        internal representations."""

        levelOne =[
            ""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,"               AAA       PP   AA                      AAAA  A         AA                 AAA                          AAA      PP    AA                      AAAA  A         AA                 AAA              "
            ,"     AAAA A  AA         AAAA                         PPP  A             PPPP         PPPP                   AAAA A  AA         AAAA                              A             P         PPPP                    "
            ,"     AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A           AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A         "
            ,"     PPPPPPPPPP  A   AAA AAAA       PPPPPPP                    PP     AAAA      PP             PPPPPPP     AA PPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPP  AAAA                                 "
            ,"                                  "
            ,"                    PPPPPP "
            ,"            A                                                                                                                                                                                                  G"
            ,"                               "
            ,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA                                                                       AAAA                           A" 
            ,"       M        Q           Q   Q        Q                                        X                Q           Q   Q        Q                                        X                Q           Q   Q          "
            ,"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
        ]

        levelTwo =[
            ""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,"               AAA            AA                      AAAA  A         AA                 AAA                          AAA            AA                      AAAA  A         AA                 AAA              "
            ,"     AAAA A  AA         AAAA                         PPPPP  A         PPPP         PPPP                    AAAA A  AA         AAAA                         PPPPP  A         PPPP                             "
            ,"     AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A           AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A         "
            ,"     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA      PP         PPPPPPPPPPPP     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA                                "
            ,"     "
            ,"     "
            ,"                                                                                                                                                                                                               G"
            ,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            ,"          "
            ,"                                                    M     M                                          M      Q                             Q              M                                                       "
            ,"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
        ]

        levelThree =[
            ""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,"               AAA            AA                      AAAA  A         AA                 AAA                          AAA            AA                      AAAA  A         AA                 AAA              "
            ,"     AAAA A  AA         AAAA                         PPPPP  A         PPPP         PPPP                    AAAA A  AA         AAAA                         PPPPP  A         PPPP                                 "
            ,"     AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A           AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A         "
            ,"     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA      PP         PPPPPPPPPPPP     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA                                "
            ,""
            ,""
            ,"                                                                                                                                                                                                              G"
            ,""
            ,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA                                                                       AAAA                           A" 
            ,"                Q           Q   Q        Q                                        X                M           Q   M       Q                                        X                Q           Q   Q          "
            ,"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
        ]
        
        levelFour =[
            ""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,""
            ,"               AAA            AA                      AAAA  A         AA                 AAA                          AAA            AA                      AAAA  A         AA                 AAA              "
            ,"     AAAA A  AA         AAAA                         PPPPP  A         PPPP         PPPP                    AAAA A  AA         AAAA                         PPPPP  A         PPPP                                 "
            ,"     AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A           AAA  AA  A       AAAAAA     AAAA  AA          AAAA         AAAA   AA                   AA  A         "
            ,"     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA      PP         PPPPPPPPPPPP     PPPPPPPPPP  A   AAA AAAA  PPPPPPPPPPPP      PPPPPPPP      PPPPP  AAAA                                "
            ,""
            ,""
            ,"                                          AAAAAAA                                                                                                                                                             G"
            ,""
            ,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA                                                                       AAAA                           A" 
            ,"                Q           Q   Q        Q                                        M                Q           Q   M        Q                                        X                Q           Q   Q          "
            ,"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
        ]
        # Below current game level
        self.currentGameLevel = 0
        # Below number of game levels
        self.levels = [1, 2, 3, 4]
        # Below adds each above level array to an array of level platforms
        self.level_platforms = [levelOne, levelTwo, levelThree, levelFour]
        # Below dictionary allows enumeration of character sprite names 
        # against internal letter representations
        self.characterReps = {
            "block" : "P"
            ,"worm" : "Q"
            ,"coin" : "A"
            ,"invis_block" : "I"
            ,"castle" : "G"
            ,"mouse" : "M"
        }
        # Below provides level background images, with key values equal to 
        # level number minus one
        self.levelBackgroundImages = {
            0 : './assets/images/backgrounds/background.png'
            ,1: './assets/images/backgrounds/background_2.png'
            ,2: './assets/images/backgrounds/background_3.png'
            ,3: './assets/images/backgrounds/background_4.png'
        }
        # Below provides level start images, with key values equal to level 
        # number minus one
        self.levelStartImages = {
            0 : './assets/images/backgrounds/splash_screen.png'
            ,1 : './assets/images/backgrounds/splash_screen_2.png'
            ,2 : './assets/images/backgrounds/splash_screen_3.png'
            ,3 : './assets/images/backgrounds/splash_screen_4.png'
        }
        # Below provides level end images, with key values equal to level 
        # number minus one
        self.levelEndImages = {
            0 : './assets/images/backgrounds/level_end_screen_1.png'
            ,1 : './assets/images/backgrounds/level_end_screen_2.png'
            ,2 : './assets/images/backgrounds/level_end_screen_3.png'
            ,3 : './assets/images/backgrounds/level_end_screen_4.png'
        }
        # Below provides level score files, with key values equal to level
        # number minus one
        self.levelScoreFiles = {
            0 : './models/high_scores/high_scores_1.txt'
            ,1 : './models/high_scores/high_scores_2.txt'
            ,2 : './models/high_scores/high_scores_3.txt'
            ,3 : './models/high_scores/high_scores_4.txt'   
        }

        # Below properties externally accessed, provide access to pause 
        # image, game over image and winning image
        self.pauseImage = './assets/images/backgrounds/paused.png'
        self.gameOverImage = './assets/images/backgrounds/game_over.png'
        self.levelEndEvent = ['CHARACTER_COLLIDE_CASTLE']
        self.levelEndEventTwo = ['CHARACTER_AT_END']
        self.gameWon = './assets/images/backgrounds/win.png'
        self.gameOverEvent = ['CHARACTER_DEAD']
        # End of initialisation method

    def set_game_level(self, levelNumber):
        """Setter method - allows current level to be set, providing a value
        for other methods to use to select level assets. Prevents need to
        specify current method for every element access."""
        self.currentGameLevel = levelNumber - 1

    def get_game_level(self):
        """Method to get the current game level being played. Returns an
        integer value."""
        return self.currentGameLevel + 1

    def get_level_platform(self):
        """Getter method to access current level platform design."""
        return self.level_platforms[self.currentGameLevel]

    def get_level_background_image(self):
        """Getter method to access current level background image."""
        return self.levelBackgroundImages[self.currentGameLevel]

    def get_level_start_image(self):
        """Getter method to access current level start image."""
        return self.levelStartImages[self.currentGameLevel]

    def get_level_end_image(self):
        """Getter method to access current level end image."""
        return self.levelEndImages[self.currentGameLevel]

    def get_level_score_url(self):
        """Getter method to access current level score file."""
        return self.levelScoreFiles[self.currentGameLevel]

    def get_char_representations(self, char):
        """Getter method to return specified character's internal 
        representation i.e. the letter used to represent them in the 
        platform designs."""
        return self.characterReps[char]

