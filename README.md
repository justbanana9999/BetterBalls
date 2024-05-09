# BetterBalls
My ball physics engine but better AND with links

There are two main files which I will explain below:

Ball physics:
    This file simulates the ineractions between the balls. Also simulates links, if there are any.
    Must have the 'Info.txt' file to load all the positions and links, or else it won't load anything.
Controls:
    Left-click to add balls continuously, and SPACE to add one ball.
    Right-click to delete a balls near the mouse.
    Middle-click or C to grab and move a ball
    ESCAPE to exit the simulation.

Ball editor:
    This file is an editor for the ball positions and links.
    Must have the 'Info.txt' file or else it raises an error.
Controls:
    Left-click to add a ball under the mouse (snaps it to the grid).
    Right-click to delete the ball under the mouse.
    SPACE to select a ball for further actions.
    M to move the selected ball to the mouse position (snaps it to the grid).
    D to delete the link between the selected ball and the ball under the mouse.
    Z to change the link/spring strength (won't change aleready placed links).
    S to change the strength of the link between the selected ball and the ball under the mouse.
    Press both Y and U to reset the file.
    ESCAPE to save the file and exit the editor.
