import tcod

def main():
    window_width = 50
    window_height = 30

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


if __name__ == "__main__":
    main()