import tcod
import constants

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
            constants.window_height // 5, 
            "Helpful Tip!")
        return self.console


class MainGameHandler(Handler):
    def on_render(self):
        self.console.print(x = 0, y = 0, string = "NOT YET IMPLEMENTED")