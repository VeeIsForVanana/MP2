import tcod
import mastermind as ms
import enum
import handler
import constants

class game_state(enum.Enum):
    main_menu = enum.auto()
    play_state = enum.auto()


def on_render(current_state, window_width, window_height, console: tcod.Console):
    """
    Called with every run of the game loop
    :param current_state: current state of the game before running this function
    :param window_width: width of console
    :param window_height: height of console
    :param console: console object used to handle displaying of visual elements
    """

    if current_state == game_state.main_menu:
        printing_base = window_height // 3      # This is the height of the first line to be printed
        console.print(window_width // 2 - 6, printing_base, "MASTERMIND")
        console.print(window_width // 2 - 2, printing_base + 2, "Play")
        console.print(window_width // 2 - 2, printing_base + 3, "Quit")
        console.draw_frame(0, (window_height // 5) * 4, window_width, window_height // 5, "Helpful Tip!")
    return console


def main():
    window_height = constants.window_height
    window_width = constants.window_width

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        window_width,
        window_height,
        tileset = tileset,
        title = "Mastermind MP2",
        vsync = True,
    ) as terminal:
        console = tcod.Console(window_width, window_height, order = "F")
        current_handler = handler.MenuHandler(console)

        while True:
            console.clear()
            console = current_handler.on_render()
            terminal.present(console)

            for event in tcod.event.wait():

                terminal.convert_event(event)
                current_handler = current_handler.handle_events(event)
        

if __name__ == "__main__":
    main()