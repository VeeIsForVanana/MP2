import tcod
import constants
import enum
import mastermind as ms

class Handler(tcod.event.EventDispatch):

    def __init__(self, console: tcod.console.Console) -> None:
        super().__init__()
        self.console = console

    def handle_events(self, event):
        print(event)
        new_handler = self.dispatch(event)
        if new_handler is None:
            new_handler = self
        return new_handler

    def on_render(self):
        print("on_render called for Handler... oops")
    
    def ev_quit(self, event):
        raise SystemExit()

class MenuHandler(Handler):

    cursor_position = 1

    def ev_keydown(self, event):
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_UP:
            self.cursor_position = max(1, self.cursor_position - 1)
        elif key == tcod.event.K_DOWN:
            self.cursor_position = min(3, self.cursor_position + 1)
        elif key == tcod.event.K_RETURN:
            if self.cursor_position == 1:
                return MainGameHandler(self.console)
        return None
    
    def on_render(self):
        printing_base = constants.window_height // 3      # This is the height of the first line to be printed
        self.console.print(constants.window_width // 2 - 6, printing_base, "MASTERMIND")
        self.console.print(
            constants.window_width // 2 - 2, 
            printing_base + 2, 
            "Play",
            fg = constants.red if self.cursor_position == 1 else constants.white,
            bg = constants.white if self.cursor_position == 1 else constants.black)
        self.console.print(
            constants.window_width // 2 - 2, 
            printing_base + 3, 
            "Help",
            fg = constants.black if self.cursor_position == 2 else constants.white,
            bg = constants.white if self.cursor_position == 2 else constants.black)
        self.console.print(
            constants.window_width // 2 - 2, 
            printing_base + 4, 
            "Quit",
            fg = constants.black if self.cursor_position == 3 else constants.white,
            bg = constants.white if self.cursor_position == 3 else constants.black)
        self.console.draw_frame(
            0, 
            (constants.window_height // 5) * 4, 
            constants.window_width, 
            constants.window_height - (constants.window_height // 5) * 4, 
            "Helpful Tip!")
        return self.console


class game_state(enum.Enum):
    game_setup = enum.auto()
    game_play = enum.auto()


class MainGameHandler(Handler):
    
    # This class handles basically the entire game. Supposed to be an input handler but nope.
    # Contains all game variables
    # Also handles the message log

    def __init__(self, console):
        super().__init__(console)
        self.state = game_state.game_setup
        self.cursor_location = 0
        self.message_log = []
        self.code_length = None
        self.code_repeat = None
        self.code = None

    def ev_keydown(self, event):
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            raise SystemExit()
        if key == tcod.event.K_RETURN:
            if self.state == game_state.game_setup:
                if self.code_length == None:
                    self.code_length = self.cursor_location + 4
                elif self.code_repeat == None:
                    self.code_repeat = ("yes", "no")[self.cursor_location]      # Selects from a tuple, avoiding if-else
            self.cursor_location = 0
        if key == tcod.event.K_RIGHT:
            self.cursor_location += 1
        if key == tcod.event.K_LEFT:
            self.cursor_location -= 1
        return None

    def update_game(self):
        # This function actually handles the entire game because I'm a genius programmer
        self.message_log.clear()
        if self.state == game_state.game_setup:     # If the game has not yet been set up
            if self.code_length is None:            # If the game does not have a code_length yet
                self.cursor_location %= 5
                self.message_log.append("Please select the length of your code")
            elif self.code_repeat is None:          # If the game does not have a code_repeat setting yet
                self.cursor_location %= 2
                self.message_log.append("Shall we allow the code to repeat?")
            else:                                   # If the game has a code_length and a code_repeat, generate code
                self.code = ms.code_randomizer(self.code_length, self.code_repeat)
                self.state = game_state.game_play
        else:
            self.message_log.append(self.code)
        return None

    def on_render(self):
        # This function will handle the entire game because I'm a genius programmer.
        self.update_game()
        self.render_background()
        printing_base = (18, 1)  # Sets a reliable variable for where the message_log should start
        for i in range(len(self.message_log)):  # Prints the message log
            self.console.print(printing_base[0], printing_base[1] + i, self.message_log[i], fg=constants.orange)
        if self.state == game_state.game_setup:     # When the game is at the setup stage
            if self.code_length is None:            # If the game has not yet set up a code (STEP 1)
                for i in range(3, 8):
                    self.console.print(
                        printing_base[0] + (2 * i - 6),
                        printing_base[1] + 2,
                        string = str(i + 1),
                        bg = constants.white if i == self.cursor_location + 3 else constants.black,
                        fg = constants.black if i == self.cursor_location + 3 else constants.white)
            elif self.code_repeat is None:            # If the game has not yet decided repeat or not (STEP 2)
                yes_no = ["Yes", "No"]
                for i in range(len(yes_no)):
                    self.console.print(
                        printing_base[0] + (5 * i),
                        printing_base[1] + 2,
                        string = yes_no[i],
                        bg=constants.white if i == self.cursor_location else constants.black,
                        fg=constants.black if i == self.cursor_location else constants.white
                    )

        return self.console
    
    def render_background(self):
        """
        Renders the background of the game screen before handing it over to a proper renderer
        """
        # Renders the 17 x 5 frame where the player's guesses will be displayed
        self.console.draw_frame(0, 0, 17, 5, "Your Guess")
        self.console.print(1, 1, "^ ^ ^ ^ ^ ^ ^ ^")
        self.console.print(1, 2, "* * * * * * * *")
        self.console.print(1, 3, "V V V V V V V V")
        
        # Renders the 17 x 20 frame where the player's old guesses are recorded
        self.console.draw_frame(0, 5, 17, 21)
        for i in range(10):
            self.console.print(1, 6 + (2 * i), "* * * * * * * *")

        # Renders the new frame containing the message log
        self.console.draw_frame(17, 0, 53, 26, "THE MASTERMIND")