# Remote-Card-Games
Utilities for playing card games online/remotely. Goal is to play a game of hand and foot with multiple groups in different locations.

## Dependencies
First the obvious: This is written in python, specifically python3, so you must have python3 installed on any machine running it.

We also used a few python libraries that must be installed. I recommend using pip to install them, but they are open source repositories if you want to build them yourself.

Python libraries required:
* podsixnet (for server/client communication)
* pygame (for the UI)

## Running the game
Currently the game only runs from command line, in the future an executable may be created for ease of use.

To run from commandline (NOTE: commands are in unix format, remember to adjust for windows command prompt usage):
1. Open a terminal for the server and one for each client you want to launch
2. Go to the source folder of the repository in all terminals
3. Launch the server using `pythong3 RunServer.py <server:port> HandAndFoot`
4. Launch each client using `python3 RunClient.py <server:port> HandAndFoot`
5. For each client specify a name by entering it in the terminal as prompted
6. Hit enter in the server terminal and press enter to begin the game
7. You can end the game by pressing enter again in the server terminal

## Unit Testing
We have tried to include unit tests for classes/methods that aren't making network calls. 

When running those test be sure to run them from the source folder so the imports work from the expected baes path of source (if you get import errors check this).

The command to run the tests is ```python3 -m unittest path.to.test.class```

Tests are located in folder called test in the appropriate package. For example, the tests for the Card class code are in common/test/TestCard.py.


In the future we may make a script to run all the test classes in one go, but for now they need to be run individually.
