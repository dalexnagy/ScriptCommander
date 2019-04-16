# ScriptCommander
Code to Execute Scripts from an Indicator App

BACKGROUND:

This collection of programs is used to manage and execute scripts without the need to start a terminal and type the directory and command and command-line values to execute the script.

This little utility works for basic BASH and PERL scripts that do not interactively ask for input - it does support command-line values/parameters and prompts for these if necessary.  It also supports Python scripts/programs that do not prompt users for input during execution in a terminal session.  It can start Python programs using GUI frameworks (I use PYQT5) for user interaction.  

PROGRAMS:

There are two programs - ScriptCMDR is used to browse files on your computer to find scripts, set up the execution rules & parameters, and create an entry in an XML file.  This code can be used to remove a script from the list and edit the information associated with a script.  This program can be started from the indicator app.

When setting up a new script in the list (XML file), the user will define the name for it, the program plugs in the path and file name in the dialog, and the user selects whether to prompt for command-line values/parameters, enters what those are, and then chooses whether a dialog pops up after the script executes with any messages and/or the return value.

The second program is the actual indicator app that lets you run a script with two clicks of the mouse.  If the user has said that a script needs parameters or values to execute, a dialog will pop up for entry of these.  This program can be started during boot time and has an icon in the 'system tray' where scripts are selected and started.

After a script executes, a dialog can be chosen to pop up and show messages from the script or the user can choose just to see the return value (a number that script sets when exiting).
