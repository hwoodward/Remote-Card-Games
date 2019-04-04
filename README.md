# Remote-Card-Games
Utilities for playing card games online/remotely. Goal is to play a game of hand and foot with multiple groups in different locations.

## Dependencies
First the obvious: This is written in python, so you must have python installed on any machine running it.

We also used a few python libraries that must be installed. I recommend using pip to install them, but they are open source repositories if you want to build them yourself.

Python libraries required:
* podsixnet (for server/client communication)


## Unit Testing
We have tried to include unit tests for classes/methods that aren't making network calls. 

When running those test be sure to run them from the source folder so the imports work from the expected baes path of source (if you get import errors check this).

The command to run the tests is ```python3 -m unittest path.to.test.class```