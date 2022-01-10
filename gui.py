import tcod
import enum
import handler
import constants


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