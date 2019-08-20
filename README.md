# ScriptCommander
Code to Execute Scripts from an Indicator App

BACKGROUND:

This collection of programs is used to manage and execute scripts without the need to start a terminal and type the directory and command and command-line values to execute the script.

This little utility works for basic BASH and PERL scripts that do not interactively ask for input - it does support command-line values/parameters and prompts for these if necessary.  It also supports Python scripts/programs that do not prompt users for input during execution in a terminal session.  It can start Python programs using GUI frameworks (I use PYQT5) for user interaction.  

PROGRAMS:

There are two programs - ScriptCmdr browses files on your computer to find scripts, sets up the execution rules & parameters, and creates an entry in an XML file.  There are options to remove a script from the list and edit the information associated with a script.  This program can be started from the indicator app (it's in the default XML file).

When setting up a new script in the list (XML file), the user find and selects the script (Bash/Perl/Python) file in a file browser dialog, gives it a descriptive name, and selects whether to prompt for command-line values/parameters, enters what those are, and then chooses whether a dialog pops up after the script executes with any messages and/or the return value.

The second program is the actual indicator app to run a script with two clicks of the mouse.  If the user has said that a script needs parameters or values to execute, a form dialog will pop up.  This program can be started at boot time and has an icon in the 'system tray' where scripts are selected and started.

After a script executes, a dialog may pop up (if requested during setup of a new script or modified later) to show messages or the user can choose just to see the return value (a number that script sets when exiting).

FILES:

DialogEntry.ui        QT form for a new dialog.  Used by ScriptCmdr
scriptcmdrappind.py   Program to select and start a script.  This is the app indicator program
scriptcmdr_icon.png   ICON displayed in OS indicator window
ScriptCmdr.py         Program to add/modify/delete scripts in XML file
ScriptCmdr.ui         QT form displayed by ScriptCmdr program
scripts_base.xml      Starter XML file - Contains entry for ScriptCmdr ONLY
scripts.xml           * NOT IN PACKAGE * This is the XML file containing the list of scripts
