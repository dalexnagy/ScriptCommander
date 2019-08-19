#!/usr/bin/env python3

# This module activates an 'app indicator' on the status line of a
# Ubuntu Linux screen.  Clicking on the indicator icon shows a list
# of defined scripts (Bash, Perl, Python) that can be executed.
#
# If starting this module from a terminal screen, use '&' after the
# command to run it as a background task.  The preferred method to
# start this program is at boot time.  See your Linux  & desktop
# distribution's documentation to learn how to do this.
#

#     This file is part of ScriptCmdr.
#
#     ScriptCmdr is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     ScriptCmdr is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You can get a copy of the GNU General Public License at
#     <https://www.gnu.org/licenses/>

import sys
import os
import signal
import subprocess
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
from threading import Thread
import xml.etree.ElementTree as XML

# Global variables
path = os.path.dirname(os.path.abspath(__file__))
scripts_XMLFile = os.path.abspath(path+"/scripts.xml")
#scripts_XMLFile = "/Python/ScriptCmdr/scripts.xml"
scriptArgsText = ""
whoami = os.path.abspath(__file__)
# End of global variables

class ScriptCodeOnly(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Request Done")
        self.set_default_size(250, 50)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_homogeneous(False)
        self.lbl_ScriptName = Gtk.Label()
        self.box.add(self.lbl_ScriptName)
        #self.box.pack_start(self.lbl_ScriptName, True, True, 0)
        self.lbl_CompCode = Gtk.Label()
        self.box.add(self.lbl_CompCode)
        #self.box.pack_start(self.lbl_CompCode, True, True, 0)
        self.btn_Done = Gtk.Button(label="Done")
        self.btn_Done.connect("clicked", self.closeMe)
        self.box.add(self.btn_Done)
        #self.box.pack_start(self.btn_Done, True, True, 0)
        self.add(self.box)

    def closeMe(self, widget):
        self.close()


class ScriptResults(Gtk.Window):
    def __init__(self):
        hor_size = 450
        Gtk.Window.__init__(self, title="Script/Command Ended")
        self.set_default_size(hor_size, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.box = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box.set_homogeneous(False)
        self.add(self.box)

        # Script name
        self.lbl_ScriptName = Gtk.Label()
        self.box.add(self.lbl_ScriptName)

        # Script path
        self.lbl_1 = Gtk.Frame()
        self.lbl_1.set_label("Command as run:")
        self.lbl_ScriptPath = Gtk.Label()
        self.lbl_1.add(self.lbl_ScriptPath)
        self.box.add(self.lbl_1)

        # Script arguments
        self.lbl_2 = Gtk.Frame()
        self.lbl_2.set_label("Arguments:")
        self.lbl_ScriptArgs = Gtk.Label()
        self.lbl_2.add(self.lbl_ScriptArgs)
        self.box.add(self.lbl_2)

        # Script completion code
        self.lbl_3 = Gtk.Frame()
        self.lbl_3.set_label("Completion Code: ")
        self.lbl_CompCode = Gtk.Label()
        self.lbl_3.add(self.lbl_CompCode)
        self.box.add(self.lbl_3)

        # Script messages
        self.lbl_4 = Gtk.Frame()
        self.lbl_4.set_label("Messages")
        self.scrolled_window_1 = Gtk.ScrolledWindow()
        self.scrolled_window_1.set_border_width(20)
        self.scrolled_window_1.set_size_request(hor_size, 150)
        # we scroll only if needed
        self.scrolled_window_1.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # a text buffer (stores text)
        self.bfr_Messages = Gtk.TextBuffer()
        # a textview (displays the buffer)
        self.txt_Messages = Gtk.TextView(buffer=self.bfr_Messages)
        # wrap the text, if needed, breaking lines in between words
        self.txt_Messages.set_wrap_mode(Gtk.WrapMode.WORD)
        self.txt_Messages.set_editable(False)
        self.txt_Messages.set_cursor_visible(False)
        self.scrolled_window_1.add(self.txt_Messages)
        self.lbl_4.add(self.scrolled_window_1)
        self.box.add(self.lbl_4)

        # Script Error Messages
        self.lbl_5 = Gtk.Frame()
        self.lbl_5.set_label("Error Messages")
        self.scrolled_window_2 = Gtk.ScrolledWindow()
        self.scrolled_window_2.set_border_width(10)
        self.scrolled_window_2.set_size_request(hor_size, 50)
        self.scrolled_window_2.set_policy(
            Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        # we scroll only if needed
        self.scrolled_window_2.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.bfr_errMsgs = Gtk.TextBuffer()
        # a textview (displays the buffer)
        self.txt_errMsgs = Gtk.TextView(buffer=self.bfr_errMsgs)
        # wrap the text, if needed, breaking lines in between words
        self.txt_errMsgs.set_wrap_mode(Gtk.WrapMode.WORD)
        self.txt_errMsgs.set_editable(False)
        self.txt_errMsgs.set_cursor_visible(False)
        self.scrolled_window_2.add(self.txt_errMsgs)
        self.lbl_5.add(self.scrolled_window_2)
        self.box.add(self.lbl_5)

        # 'Done' button
        self.btn_Done = Gtk.Button(label="Done")
        self.btn_Done.connect("clicked", self.closeMe)
        self.box.add(self.btn_Done)

    def closeMe(self, widget):
        self.close()

class ScriptArgsWin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Script Arguments")

        dialog = ScriptArgsDlg(self)
        dialog.run()

        self.scriptArgsText = dialog.ent_Args.get_text()

        dialog.destroy()

    def returnArgs(self):
        return self.scriptArgsText

class ScriptArgsDlg(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Script Arguments", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(250, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.box = self.get_content_area()
        self.box.set_homogeneous(False)
        # Field for entering arguments
        self.label = Gtk.Label("Enter or Change Command Line Arguments")
        self.box.pack_start(self.label, True, True, 0)
        self.ent_Args = Gtk.Entry()
        self.ent_Args.set_text(scriptArgsText)
        self.box.pack_start(self.ent_Args, True, True, 0)
        self.show_all()

class Indicator():
    def __init__(self):
        self.app = 'ScriptCmdr'
        path = os.path.dirname(os.path.abspath(__file__))
        self.indicator = AppIndicator3.Indicator.new(
            self.app, os.path.abspath(path+"/scriptcmdr_icon.png"),
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.update = Thread(target=self.do_nothing())
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        global tree
        global scripts
        global menu
        menuItems = []

        try:
            tree = XML.parse(scripts_XMLFile)
        except:
            # Not found --Big Time Error!
            print("No XML file found with list of scripts")

        menu = Gtk.Menu()

        scripts = tree.getroot()
        # make menu of script names
        for script in scripts:
            menuItems.append(script.get('name'))
        menuItems.sort()

        for menuEntry in menuItems:
            menuItem = Gtk.MenuItem(menuEntry)
            menuItem.connect('activate', self.run_script)
            menu.append(menuItem)

        item_sep1 = Gtk.MenuItem('-------------')
        menu.append(item_sep1)

        item_restartme = Gtk.MenuItem('Restart')
        item_restartme.connect('activate', self.restartme)
        menu.append(item_restartme)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        #tree.close()
        return menu

    def run_script(self, menuitem):
        findScript = menuitem.get_label()
        #print("Running:", findScript)

        for script in scripts:
            if script.get('name') == findScript:
                scriptPath = script.find("path").text

                scriptArgsText = ""

                if script.find("reqArgs") is not None:
                    if script.find("reqArgs").text == "yes":
                        #print("Ask for arguments: args=", script.find("args").text)
                        if script.find("args").text is None:
                            scriptArgsText = "<none specified>"
                        else:
                            scriptArgsText = script.find("args").text
                        #print("Before ScriptArgsWin: ", scriptArgsText)
                        showArgsWin = ScriptArgsWin()
                        scriptArgsText = showArgsWin.returnArgs()
                        print("After ScriptArgsWin: ", scriptArgsText)

                    shell_value = False
                    if script.find("type").text == "pythongui":
                        shell_value = True
                    #print("Type=", script.find("type").text, ", Shell=",shell_value)

                os.chdir(os.path.dirname(scriptPath))
                out = subprocess.Popen([scriptPath, scriptArgsText], shell=shell_value,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

                stdout, stderr = out.communicate()

                #print("Execution has ended")

                if out.returncode == 0:
                    #print("Return code was ", str(out.returncode))
                    fg = 'black'
                    bg = 'white'
                else:
                    #print("Return code was ", str(out.returncode))
                    fg = 'yellow'
                    bg = 'red'

                if script.find("viewMsgs") is None:
                    viewMsgs = True
                else:
                    if script.find("viewMsgs").text == "yes":
                        viewMsgs = True
                        viewCode = False
                    else:
                        viewMsgs = False

                if script.find("viewCode") is None:
                    if viewMsgs is True:
                        viewCode = False
                    else:
                        viewCode = True
                else:
                    if script.find("viewCode").text == "yes" and viewMsgs is False:
                        viewCode = True
                    else:
                        viewCode = False

                if viewMsgs:
                    showResults = ScriptResults()
                    showResults.lbl_ScriptName.set_markup("<big><b>"+findScript+"</b></big>")
                    showResults.lbl_ScriptPath.set_text(scriptPath)
                    showResults.lbl_ScriptArgs.set_text(scriptArgsText)
                    showResults.lbl_CompCode.set_text(str(out.returncode))
                    showResults.bfr_Messages.set_text(stdout.decode('ascii'))
                    #print("Stdout: ",stdout.decode('ascii'),"\n---")
                    if stderr is not None:
                        #print("Stderr: ", stderr.decode('ascii'),"\n---")
                        showResults.bfr_errMsgs.set_text(stderr.decode('ascii'))

                    showResults.show_all()

                if viewCode:
                    showCodeOnly = ScriptCodeOnly()
                    showCodeOnly.lbl_ScriptName.set_markup("<big><b>"+findScript+"</b></big>")
                    showCodeOnly.lbl_CompCode.set_markup("Completion Code: "+
                        "<span foreground='"+fg+"' background='"+bg+"'><big><b>" + str(out.returncode) +
                                                         "</b></big></span>")
                    showCodeOnly.show_all()

    def restartme(self, source):
        # print("Restarting via ", whoami)
        subprocess.Popen([whoami], shell=False)
        Gtk.main_quit()

    def stop(self, source):
        Gtk.main_quit()

    def do_nothing(self):
        pass

Indicator()
GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()