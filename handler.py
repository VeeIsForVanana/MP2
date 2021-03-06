import tcod
import constants
import enum
import mastermind as ms


class Handler(tcod.event.EventDispatch):

    def __init__(self, console: tcod.console.Console) -> None:
        super().__init__()
        self.console = console

    def handle_events(self, event):
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
            self.cursor_position = min(2, self.cursor_position + 1)
        elif key == tcod.event.K_RETURN:
            if self.cursor_position == 1:
                return MainGameHandler(self.console)
            elif self.cursor_position == 2:
                raise SystemExit()
        return None

    def on_render(self):
        printing_base = constants.window_height // 3  # This is the height of the first line to be printed
        self.console.print(constants.window_width // 2 - 5, printing_base, "MASTERMIND")
        self.console.print(
            constants.window_width // 2 - 2,
            printing_base + 2,
            "Play",
            fg=constants.red if self.cursor_position == 1 else constants.white,
            bg=constants.white if self.cursor_position == 1 else constants.black)
        self.console.print(
            constants.window_width // 2 - 2,
            printing_base + 4,
            "Quit",
            fg=constants.black if self.cursor_position == 2 else constants.white,
            bg=constants.white if self.cursor_position == 2 else constants.black)
        self.console.draw_frame(
            0,
            (constants.window_height // 5) * 4,
            constants.window_width,
            constants.window_height - (constants.window_height // 5) * 4,
            "Helpful Tip!")
        self.console.print(
            constants.window_width // 2 - 27,
            ((constants.window_height // 5) * 4) + 2,
            "  There are no helpful tips. Turn back while you can  \n"
            "Also you can use the arrow and enter keys to navigate",
            fg=constants.orange
        )
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
        self.edit_guess = [0 for i in range(8)]
        self.current_guess = None
        self.past_guesses = [[None for i in range(8)] for i in range(10)]
        self.win_state = False
        self.turn_counter = 0
        self.lifeline1 = False
        self.lifeline2 = False
        self.active_lifeline = False
        self.temporary_length = 1
        self.end_state = False
        self.pre_quit = False

    def ev_keydown(self, event):
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            if self.end_state or self.pre_quit:
                return MenuHandler(self.console)
            self.pre_quit = True
            self.message_log.append("Are you sure you want to quit? Press ESC again to confirm.")
            return None
        if key == tcod.event.K_RETURN:
            if self.state == game_state.game_setup:
                if self.code_length is None:
                    self.code_length = self.cursor_location + 4
                elif self.code_repeat is None:
                    self.code_repeat = ("yes", "no")[self.cursor_location]  # Selects from a tuple, avoiding if-else
            elif self.state == game_state.game_play:
                if not self.end_state:
                    if self.current_guess is None and not self.active_lifeline:  # Registers the input guess as current_guess, validation takes place in update_game
                        if not any([i != 8 for i in self.edit_guess[0: self.code_length]]):
                            self.edit_guess = [9 for i in range(8)]
                            temp_guess = [str(9) for i in range(8)]
                        else:
                            temp_guess = [str(i + 1) for i in self.edit_guess][0: self.code_length]
                        self.current_guess = ''.join(temp_guess)
                    elif self.active_lifeline:
                        self.current_guess = str(self.edit_guess[0] + 1)
            self.cursor_location = 0
        if key == tcod.event.K_RIGHT:
            if not self.end_state:
                self.cursor_location += 1
        if key == tcod.event.K_LEFT:
            if not self.end_state:
                self.cursor_location -= 1
        if key == tcod.event.K_UP and self.state == game_state.game_play:
            if not self.end_state:
                self.edit_guess[self.cursor_location] = (self.edit_guess[self.cursor_location] + 1) % 9
        if key == tcod.event.K_DOWN and self.state == game_state.game_play:
            if not self.end_state:
                self.edit_guess[self.cursor_location] = (self.edit_guess[self.cursor_location] - 1) % 9
        if self.pre_quit:
            self.message_log.append("I guess you didn't want to go after all.")
            self.pre_quit = False
        return None

    def turn_iterator(self):
        # Iterates through turn numbers. Made into a function so that it doesn't accidentally get tripped.
        self.turn_counter += 1

    def update_game(self):
        # This function actually handles the entire game because I'm a genius programmer
        if self.state == game_state.game_setup:  # If the game has not yet been set up
            self.message_log.clear()
            if self.code_length is None:  # If the game does not have a code_length yet
                self.cursor_location %= 5
                self.message_log.append("Please select the length of your code \n "
                                        "(Colors on the left not indicative of code palette)")
            elif self.code_repeat is None:  # If the game does not have a code_repeat setting yet
                self.cursor_location %= 2
                self.message_log.append("Shall we allow the code to repeat?")
            else:  # If the game has a code_length and a code_repeat, generate code
                self.code = ms.code_randomizer(self.code_length, self.code_repeat)
                self.state = game_state.game_play
                self.message_log.append("Helpful Tip: Use the arrow keys to control the input device to the left")
        else:
            self.cursor_location %= self.code_length
            if self.current_guess is None:
                if self.active_lifeline:                                    # When lifeline active and no input
                    self.edit_guess[0] %= 2
                return None
            else:
                checking = False
                if any(i == '9' for i in self.current_guess) and not all(i == '9' for i in self.current_guess):
                    # Validates code, checks for lifeline where there shouldn't be
                    message = "Oops! You used a lifeline code where you maybe shouldn't have..."
                elif all(i == '9' for i in self.current_guess) and not (self.lifeline1 or self.lifeline2): # Lifelines activated
                    message = "Choose a lifeline using the code input. There is no going back."
                    self.active_lifeline = True
                    self.code_length, self.temporary_length = self.temporary_length, self.code_length
                elif all(i == '9' for i in self.current_guess) and (self.lifeline1 or self.lifeline2):
                    message = "You have already used up your lifeline."
                elif self.active_lifeline:                                  # Lifeline active and input given
                    lifeline_code = [9 for i in range(8)]
                    if self.current_guess == "1" and not self.lifeline1:
                        message = ms.lifeline1(self.code)
                        self.lifeline1 = True
                        self.past_guesses[self.turn_counter] = lifeline_code
                        self.turn_iterator()
                    elif self.current_guess == "2" and not self.lifeline2:
                        message, index = ms.lifeline2(self.code)
                        self.lifeline2 = True
                        self.past_guesses[self.turn_counter] = lifeline_code
                        self.turn_iterator()
                        self.past_guesses[self.turn_counter] = lifeline_code
                        self.turn_iterator()
                    elif self.current_guess == "1" and self.lifeline1:
                        message = "You have already used this lifeline"
                    elif self.current_guess == "2" and self.lifeline2:
                        message = "You have already used this lifeline"
                    self.code_length, self.temporary_length = self.temporary_length, self.code_length
                    self.active_lifeline = False
                elif self.current_guess == self.code:                       # Player guesses correct code
                    self.win_state = True
                    self.end_state = True
                    self.past_guesses[self.turn_counter] = self.edit_guess
                    message = f"You won in {self.turn_counter + 1} turns! Press ESC to return to menu."
                elif (self.turn_counter >= 9 or self.end_state) and not self.win_state:
                    self.end_state = True
                    self.past_guesses[self.turn_counter] = self.edit_guess
                    message = f"You lost. The code was {self.code}. Press ESC to return to menu."
                    self.message_log.append(message)
                else:                                                       # Player enters an incorrect guess
                    checking = True
                    red, white = ms.code_checker(self.current_guess, self.code)
                    to_red = f"{tcod.COLCTRL_FORE_RGB:c}{constants.red[0]:c}{constants.red[1]:c}{constants.red[2]:c}"
                    to_white = f"{tcod.COLCTRL_FORE_RGB:c}{constants.white[0]:c}{constants.white[1]:c}{constants.white[2]:c}"
                    message = f"{to_red}RED: {red}, {to_white}WHITE {white}"
                    self.past_guesses[self.turn_counter] = self.edit_guess
                    self.turn_iterator()

                # Resets relevant variables for reuse in next turn
                if not self.message_log[len(self.message_log) - 1] == message or checking:  # Checks if the message repeats
                    self.message_log.append(message)
                self.current_guess = None
                self.edit_guess = [0 for i in range(8)]

                # Iterates turn

        return None

    def on_render(self):
        # This function will handle the entire game because I'm a genius programmer.
        self.update_game()
        self.render_background()
        printing_base = (18, 1)  # Sets a reliable variable for where the message_log should start
        for i in range(min(len(self.message_log), 24)):
            # Prints the message log up to a certain length, then scrolls
            messages = self.message_log[max(0, len(self.message_log) - 24):]
            self.console.print(printing_base[0], printing_base[1] + i, messages[i], fg=constants.orange)
        if self.state == game_state.game_setup:  # When the game is at the setup stage
            if self.code_length is None:  # If the game has not yet set up a code (STEP 1)
                for i in range(3, 8):
                    self.console.print(
                        printing_base[0] + (2 * i - 6),
                        printing_base[1] + 3,
                        string=str(i + 1),
                        bg=constants.white if i == self.cursor_location + 3 else constants.black,
                        fg=constants.black if i == self.cursor_location + 3 else constants.white)
                for i in range(10):
                    for j in range(self.cursor_location + 4):
                        self.console.print(
                            1 + (2 * j),
                            6 + (2 * i),
                            "*",
                            bg=constants.code_colors[((i + j) % (self.cursor_location + 4))],
                            fg=constants.black if constants.code_colors[((i + j) % (self.cursor_location + 4))] !=
                               constants.black else constants.white
                        )
            elif self.code_repeat is None:  # If the game has not yet decided repeat or not (STEP 2)
                yes_no = ["Yes", "No"]
                for i in range(len(yes_no)):
                    self.console.print(
                        printing_base[0] + (5 * i),
                        printing_base[1] + 2,
                        string=yes_no[i],
                        bg=constants.white if i == self.cursor_location else constants.black,
                        fg=constants.black if i == self.cursor_location else constants.white
                    )
        if self.state == game_state.game_play:  # When the game is in play
            guess_printing_base = (1, 2)  # Where printing the current guess takes place
            past_printing_base = (1, 6)  # Where printing past guesses takes place

            # Displaying highlighted up arrows for the length of the active guess (within the code_length)
            # Only up and down arrows are highlighted when cursor location is on them.

            for i in range(self.code_length):
                self.console.print(
                    1 + (2 * i),
                    1,
                    "^",
                    fg=constants.white,
                    bg=constants.gray if self.cursor_location == i else constants.black
                )

            # Displaying the selected digits of the guess

            for i in range(self.code_length):
                entry = int(self.edit_guess[i])
                lifeline = "LIFELINE"
                self.console.print(
                    1 + (2 * i),
                    2,
                    str(entry + 1) if entry != 8 else lifeline[i],
                    bg=constants.code_colors[entry] if entry != 8 else constants.gray,
                    fg=constants.white if constants.code_colors[entry] == constants.black else constants.black
                )

            # Render LIFELINE for the whole guess when all characters correspond

            if not any([i != 8 for i in self.edit_guess[0: self.code_length]]):
                for i in range(len("LIFELINE")):
                    self.console.print(1 + (i * 2), 2, "LIFELINE"[i], bg=constants.gray)

            # Displaying highlighted down arrows for the length of the active guess (within the code_length)

            for i in range(self.code_length):
                self.console.print(
                    1 + (2 * i),
                    3,
                    "v",
                    fg=constants.white,
                    bg=constants.gray if self.cursor_location == i else constants.black
                )

            # Render past guesses

            for i in range(min(len(self.past_guesses), 10)):
                for j in range(len(self.past_guesses[i][0:self.code_length])):
                    entry = self.past_guesses[i][j]
                    if entry != 9:
                        self.console.print(
                            1 + (2 * j),
                            6 + (2 * i),
                            "*" if entry is None or j >= self.code_length else str(entry + 1),
                            bg=constants.d_gray if entry is None or j >= self.code_length else constants.code_colors[entry],
                            fg=constants.white if constants.code_colors.get(entry, None) == constants.black else
                            constants.black
                        )
                    else:
                        self.console.print(
                            1 + (2 * j),
                            6 + (2 * i),
                            "LIFELINE"[j],
                            bg = constants.gray,
                            fg = constants.white
                        )

        return self.console

    def render_background(self):
        """
        Renders the background of the game screen before handing it over to a proper renderer
        """
        # Renders the 17 x 5 frame where the player's guesses will be displayed
        self.console.draw_frame(0, 0, 17, 5, "Your Guess")
        self.console.print(1, 1, "^ ^ ^ ^ ^ ^ ^ ^", fg=constants.d_gray)
        self.console.print(1, 2, "* * * * * * * *", fg=constants.d_gray)
        self.console.print(1, 3, "v v v v v v v v", fg=constants.d_gray)

        # Renders the 17 x 20 frame where the player's old guesses are recorded
        self.console.draw_frame(0, 5, 17, 21)
        for i in range(10):
            self.console.print(1, 6 + (2 * i), "* * * * * * * *", fg=constants.d_gray)

        # Renders the new frame containing the message log
        self.console.draw_frame(17, 0, 73, 26, "THE MASTERMIND")
