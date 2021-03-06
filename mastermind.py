def input_validation(accepted_values, player_input = None):
    """
    Validates player input based on a list of accepted_values
    :param accepted_values: List of accepted inputs
    :param player_input: Player input or otherwise input to be validated
    :return: Player input if in accepted_values, else returns None
    """
    output = player_input if player_input in accepted_values else None

    return output


def code_input_validation(required_length, accepted_characters, player_input = None):
    """
    Validates code input based on a set length and a set of accepted characters or checks to see if it is a lifeline call
    :param required_length: Length of expected string
    :param accepted_characters: Characters expected in string
    :param player_input: Player input or otherwise input to be validated
    :return: None if any character in player_input is invalid or length of input != required_length else player_input
    """
    output = None if len(player_input) != required_length or any([char not in accepted_characters for char in player_input]) \
        else player_input

    # If output is still none (considered invalid as a code, check to see if player was asking for a lifeline)

    if output is None:
        output = input_validation(["lifeline#1", "lifeline#2"], player_input)

    return output


def set_length(minimum_len = 4, maximum_len = 8):
    """
    Requests player input and awaits valid input for length of code
    :param minimum_len: minimum length
    :param maximum_len: maximum length
    :return: Returns player input when valid
    """
    player_input = None
    print(f"Please input a number between {minimum_len} and {maximum_len} inclusive for the code length")
    while player_input is None:
        player_input = input_validation(range(minimum_len, maximum_len + 1), int(input()))
    return player_input


def set_repeat():
    """
    Requests player input to repeat or not
    :return:
    """
    player_repeat_input = None
    print("Are colors allowed to repeat? (YES/NO)")
    while player_repeat_input is None:
        player_repeat_input = input_validation(["yes", "no"], input().lower())
    return player_repeat_input

def code_randomizer(length, repeat):
    """
    Randomizes a color code
    :param length: desired length of code
    :param repeat: string, 'yes' if repeated colors are allowed else 'no'
    :return: Returns an appropriate color code
    """
    import random
    if repeat == 'yes' or repeat == 'y':
        return ''.join((random.choice('12345678') for i in range(length)))
    else:
        return ''.join(random.sample('12345678', length))


def present_colors(color_code):
    """
    Creating a set for all the colors present in the randomized code
    """
    color_set = set({})
    for i in color_code:
        if i not in color_set:
            color_set.add(i)
    return color_set


def visible_code_generator(length):
    """
    Creating a visible code of asterisks to serve as a guide for the player
    :param length: desired length of string
    :return: Returns a string of asterisks
    """
    visible_code = "".join('*' for i in range(length))

    return visible_code


def code_checker(player_input, code):
    """
    Comparing player_input and the computer code
    :param player_input: player input
    :param code: color code generated by computer
    :return: Returns two integers representing red and white values
    """
    red, white = 0, 0
    red_dict = {}
    for i in range(1, 9):
        red_dict[str(i)] = 0
    for i in code:
        red_dict[i] = red_dict.get(i, 0) + 1
    for i in range(len(player_input)):
        red += int(player_input[i] == code[i])      # I am far too proud of this addition - v
        red_dict[code[i]] -= int(player_input[i] == code[i])
    for i in range(len(player_input)):
        white += int(player_input[i] in code and red_dict[player_input[i]] > 0 and not player_input[i] == code[i])
        red_dict[player_input[i]] -= int(player_input[i] in code and red_dict[player_input[i]] > 0 and not player_input[i] == code[i])
    return red, white

def lifeline1(code):
    """
    Selects a random index of the code and reveals its contents but not its position
    :param code: String whose element is to be revealed
    :return: None
    """
    import random
    element = random.choice(list(code))
    return (f"The element {element} exists somewhere... but where I wonder.")


def lifeline2(code):
    """
    Selects a random index of the code and reveals its contents and position
    :param code: String whose element is to be revealed
    :return: Index of known element
    """
    import random
    position = random.randint(1, len(code))
    return (f"The element {code[position - 1]} exists at position {position}."), position - 1


def main():

    # Game setup

    usable_colors = (1, 2, 3, 4, 5, 6, 7, 8)
    win = False
    used_lifeline = False
    lifeline1_loss, lifeline2_loss = 1, 2
    turns = 1

    length = set_length()

    code = code_randomizer(length, set_repeat())

    visible_code = visible_code_generator(length)

    # Game loop

    while turns <= 10 and not win:
        # Accept and validate player input
        player_input = None

        while player_input is None:
            print(f"Turn #: {turns}")
            print(f"lifeline#1: {'AVAILABLE' if not used_lifeline else 'USED UP'}")
            print(f"lifeline#2: {'AVAILABLE' if not used_lifeline else 'USED UP'}")
            print(f"Code  : {visible_code}")
            player_input = code_input_validation(len(code), [chr(i + ord("0")) for i in usable_colors], input("Guess : "))
            if player_input == "lifeline#1" and (used_lifeline or 10 - turns <= lifeline1_loss + 1):
                player_input = None
                print("Lifeline 1 can no longer be used.")
            elif player_input == "lifeline#2" and (used_lifeline or 10 - turns <= lifeline2_loss + 1):
                player_input = None
                print("Lifeline 2 can no longer be used.")
            elif player_input is None:
                print("Please enter a color code or ask for a valid lifeline (lifeline#1 or lifeline#2).")
            print()

        # Handle user input. First try to treat it as a lifeline, afterward pass it through a code checker.

        if player_input == "lifeline#1":
            print("Lifeline 1 Activated... but at what cost?")
            used_lifeline = True
            turns += lifeline1_loss
            print(lifeline1(code))
        elif player_input == "lifeline#2":
            print("Lifeline 2 Activated... you feel the time drain away.")
            used_lifeline = True
            turns += lifeline2_loss
            visible_code = list(visible_code)
            message, index = lifeline2(code)
            print(message)
            visible_code[index] = code[index]
            visible_code = "".join(visible_code)
        else:
            red, white = code_checker(player_input, code)
            if red == len(code):
                win = True
            else:
                print(f"Red: {red}\nWhite: {white}")

        if 10 - turns <= lifeline1_loss + 1 and not used_lifeline:
            print("Your chance to use your first lifeline has come and gone.")
        elif 10 - turns <= lifeline2_loss + 1 and not used_lifeline:
            used_lifeline = True
            print("Your chance to use your second lifeline has come and gone.")

        turns += 1
        print()

    if win:
        print("You, flesh-mind, have beaten me... but you will come again soon, \n "
              "and when you do, we will see if luck shall favor you again")
    else:
        print(f"I have beaten you. Now do you see, feeble flesh-mind, why I am the Mastermind? Code: {code}")

    player_input = None

    while player_input is None:
        player_input = input_validation(["yes", "no"], input("Do you dare challenge me again, flesh-mind? (Yes/No)").lower())

    if player_input == "yes":
        main()
    else:
        raise SystemExit()

if __name__ == "__main__":
    main()