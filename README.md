# MP2

Created as part of requirements for CS11 Subject

By:

Abcede, Ma. Pauline <br>
Heffron, Joaquin <br>
Reyes, Victor Edwin <br>

## Introduction

This document is made as external documentation of the algorithms and logic underpinning our implementation of the Mastermind Game. The User Manual for lay users explaining how to play the game is located in a section of the document.

In case this project was distributed by other means, this project also has a GitHub repository here: https://github.com/VeeIsForVanana/MP2

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

## Implementation 1: `mastermind.py`

This script implements the algorithm below. Do note that there is not an exact one-to-one correspondence between the code and this algorithm.

```
Define a function to validate input taking a list of accepted inputs and the player input as parameters:
  The function returns the player input if it is in the list of accepted values. Otherwise it outputs nothing.

Define a function to validate a color code input taking the desired code length, a list of accepted characters, and the player input as parameters:
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
  The function returns either a random sequence of color codes if it may repeat codes or permutates the string of all codes and cuts down the length if not.
  
Define a function to check the computer's code against the player's guess, taking both as input:
  The function creates a dictionary with the colors as keys and the number of their occurences in the computer's code.
  The function traverses both the code and guess and stores the number of exact matches as "red". For each exact match of a color, 1 is subtracted from its corresponding entry in the dictionary.
  The function traverses the player's guess only and stores the number of times the colors in the player's guess appears in the code (excepting the already-present exact matches) as long as the dictionary entry for that color is not zero or less. Then it subtracts this count from the corresponding dictionary entry. The count is also stored as "white".
  The function returns red and white as results.
  
Define a function to handle lifeline 1, taking only the computer's code as input:
  
```
