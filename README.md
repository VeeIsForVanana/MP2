# MP2

Created as part of requirements for CS11 Subject

By:

Abcede, Ma. Pauline <br>
Heffron, Joaquin <br>
Reyes, Victor Edwin <br>

## Introduction

This document is made as external documentation of the algorithms and logic underpinning our implementation of the 
Mastermind Game. The User Manual for lay users explaining how to play the game is also located in this document.

In case this project was distributed by other means, this project also has a GitHub repository here: 
https://github.com/VeeIsForVanana/MP2

## About the Project

### Requirements

This project's GUI implementation requires the tcod python package. Install it using `pip install tcod` or refer to this link https://python-tcod.readthedocs.io/en/latest/installation.html.

### Project Structure

The directory containing this project will contain two scripts of interest:

- `mastermind.py` Contains the base implementation of the game, with minimum features as detailed in the project specifications.
- `gui.py` Contains an implementation of the game that makes use of a graphical user interface courtesy of the tcod package. This implementation makes use of concepts not taught in the CS11 curriculum such as classes, inheritance, and enums. These concepts were used out of sheer necessity due to the complex demands of the GUI implementation. This script has two dependencies contained in the project:
  - `handler.py` Contains an implementation of event handler classes inherited from the tcod package. Said handlers also handle most of the game's logic.
  - `constants.py` Contains vital game data detailing color data and window size.

Both implementations will be documented in separate sections of this document.

## User Manual

### User Manual 1: `mastermind.py`

This script makes use primarily of text inputs and a textual interface. 
The program solely implements Mastermind with some added features.
Guiding prompts are in all parts of the program, but this manual will still provide a detailed guide into the game.

The game opens with prompts asking for required parameters (code length, and whether colors will repeat) 
for the game setup. Input is validated and the request will loop until it receives what is considered valid input. By
default, length is expected to be within 4 and 8, inclusive. Meanwhile, repeat will always be either "Yes" or "No".

Afterward, the game proper will start. 

To summarize, in Mastermind, the player is expected to make guesses what the computer-generated code is. Said code will 
consist of "colors" (numbers from 1 to 8 by default). The player is expected to match this code with their guess to win 
the game. Otherwise, if they fail to do so within ten turns, they lose. When the player inputs a guess, the computer 
prints out feedback in the form of "Red" and "White" numbers, based on which they may alter their input. They may also
make use of lifelines, as shall be detailed below.

At the start of every turn, the computer will prompt the user to input their valid guess. The player has the option of
inputting a guess for the computer's code or to ask for a lifeline by inputting "lifeline#1" or "lifeline#2". The game
will loop until a valid input is entered.

When a valid guess is entered, it will be checked against the computer's code.  

## Implementations

### Implementation 1: `mastermind.py`

This script implements the algorithm below. Do note that there is not an exact one-to-one correspondence between the 
code and this algorithm.

```
Define a function to validate input taking a list of accepted inputs and the player input as parameters:
  The function returns the player input if it is in the list of accepted values. Otherwise it outputs nothing.

Define a function to validate a color code input taking the desired code length, a list of accepted characters, and the 
 player input as parameters:
  The function returns the player input if it is of the desired length and if all its characters are accepted else
  The function returns a request for a lifeline if the player input is such else
  The function returns nothing

Define a function to request a valid player code length with a maximum and minimum value as parameters:
  The function prints a request to the player for a valid length.
  The function validates the player's input against a list of integers between the minimum and maximum length.
  The function only returns the input when valid.

Define a function to request a valid player input for whether the code will repeat colors or not:
  The function prints a request for player input of "Yes" or "No".
  The function validates the player's lowercase input against "Yes" and "No".
  The function only returns the input when valid.

Define a function to randomize a code, taking a length and whether the code repeats colors or not as input:
  The function returns either a random sequence of color codes if it may repeat codes or permutates the string of all 
   codes and cuts down the length if not.
  
Define a function to check the computer's code against the player's guess, taking both as input:
  The function creates a dictionary with the colors as keys and the number of their occurences in the computer's code.
  The function traverses both the code and guess and stores the number of exact matches as "red". For each exact match 
  of a color, 1 is subtracted from its corresponding entry in the dictionary.
  The function traverses the player's guess only and stores the number of times the colors in the player's guess appears
   in the code (excepting the already-present exact matches) as long as the dictionary entry for that color is not zero 
   or less. Then it subtracts this count from the corresponding dictionary entry. The count is also stored as "white".
  The function returns red and white as results.
  
Define a function to handle lifeline 1, taking only the computer's code as input:
  The function picks a random element of the code and prints it out without location data.

Define a function to handle lifeline 2, taking only the computer's code as input:
  The function picks a random position in the code and prints it out with element data.
  The function returns the position.


~~MASTERMIND IMPLEMENTATION BEGINS HERE~~
START

Define the 'usable_colors' (by default integers 1 to 8)
Define boolean values to track, all start as False:
    Whether the player has won, 'win'
    Whether the player has used lifeline1, 'used_lifeline1'
    Whether the player has used lifeline2, 'used_lifeline2'
Set integer values:
    For how much a call of lifeline1 deducts from turns, 'lifeline1_loss' (by default 1)
    For how much a call of lifeline2 deducts from turns, 'lifeline2_loss' (by default 2)

Set 'length' to be None (an value)
While 'length' is None (while 'length' is an invalid value):
    Set 'length' to be the validated player length as in the function above.
Set 'repeat' to be None (an value)
While repeat is None (while 'repeat' is an invalid value):
    Set 'repeat' to be the validated player repeat choice as in the function above.
Randomize 'code' using the function defined above.
Set 'turns' to be 1
Set 'visible_code' to be a string of only '*' with length equal to code length 

While turns <= 10 and the player has not won:
    Set 'player_input' to be None (an invalid value)
    While 'player_input' is None (while 'player_input' is invalid):
        Print a prompt detailing turn count and a code hint (visible_code)
        Set 'player_input' to be the validated code as in the function above
        If the player asks for a lifeline x and the lifeline x has already been used ('used_lifelinex'):
            Invalidate player_input by setting to None
        Else if player input is still invalid (None):
            Print a corrective message
    
    If the player requested for lifeline 1:
        Execute function lifeline1 with argument 'code' as defined above
        Add the specified 'lifeline1_loss' to 'turns' 
    Else if the player requested for lifeline 2:
        Execute function lifeline2 with argument 'code' as defined above. Take its return value as 'position'
        Change the value of the character at 'position' of 'visible_code' to the element at 'position' in 'code'
        Add the specified 'lifeline2_loss' to 'turns'
    Else (if the player entered a validated guess):
        Let 'red', 'white' be the variable outputs of the code checking between 'player_input' and 'code' 
         as defined above
        If 'red' is the same as the length of the code (i.e. if there is a one-to-one match across the full length):
            The player has won. Set 'win' to True
        Else:
            Print out 'red' and 'white' in player-readable format.
    Increment 'turn' by 1

If win (if the player has won):
    Print congratulatory message
Else (if turns >= 10 and the player has not yet won):
    Print loss message

END        
```

