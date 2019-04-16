# ScriptCommander
Code to Execute Scripts from Indicator App

This collection of programs is used to manage and execute scripts without the need to start a terminal, find the script, and type the command.

This little utility works for basic BASH and PERL scripts that do not interactively ask for input - it does support command-line values/parameters and prompts for these if necessary.  It also supports Python scripts/programs that do not need to run in a terminal session and can start Python programs using GUI frameworks (I use PYQT5) for user interaction.  

There are two programs - one to browse files on your computer to find scripts, set up the execution rules & parameters, and create an entry in an XML file.  This code can be used to remove a script from the list and edit the information associated with a script.

The second is the actual indicator app that lets you run a script with two clicks of the mouse.  
