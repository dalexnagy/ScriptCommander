#!/usr/bin/python3

# This module maintains the XML file of scripts that can be called by
# the program running as the app indicator.

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
import datetime
import xml.etree.ElementTree as XML
#import getopt
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox, QDialogButtonBox
from PyQt5.uic import loadUi

# Global variables
path = os.path.dirname(os.path.abspath(__file__))
scripts_XMLFile = os.path.abspath(path+"/scripts.xml")
#scripts_XMLFile = "/Python/ScriptCmdr/scripts.xml"
# End of global variables

class AddScript(QDialog):
    def __init__(self):
        super(AddScript, self).__init__()
        loadUi('DialogEntry.ui', self)
        self.buttonBox.accepted.connect(self.saveEntry)
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)

        self.txt_Name.textChanged.connect(self.activate_Save)
        self.txt_Path.setReadOnly(True)

        self.btn_typeBash.clicked.connect(self.activate_Save)
        self.btn_typePerl.clicked.connect(self.activate_Save)
        self.btn_typePython.clicked.connect(self.activate_Save)
        self.btn_typePythonGUI.clicked.connect(self.activate_Save)
        #self.box_Type.checked.connect(self.activate_Save())

    def saveEntry(self):
        scriptElement = XML.Element("script")
        scriptElement.set('name', self.txt_Name.text())
        scripts.append(scriptElement)

        pathElement = XML.SubElement(scriptElement, "path")
        pathElement.text = self.txt_Path.text()

        if self.cbx_Args.isChecked():
            pathElement = XML.SubElement(scriptElement, "reqArgs")
            pathElement.text = "yes"
            pathElement = XML.SubElement(scriptElement, "args")
            pathElement.text = self.txt_Args.text()
        else:
            pathElement = XML.SubElement(scriptElement, "reqArgs")
            pathElement.text = "no"

        msgHandler = XML.SubElement(scriptElement, "viewMsgs")
        if self.cbx_ViewMsgs.isChecked():
            msgHandler.text = "yes"
            self.cbx_ViewCode.setChecked(True)
        else:
            msgHandler.text = "no"

        codeHandler = XML.SubElement(scriptElement, "viewCode")
        if self.cbx_ViewCode.isChecked():
            codeHandler.text = "yes"
        else:
            codeHandler.text = "no"

        DescElement = XML.SubElement(scriptElement, "Desc")
        DescElement.text = self.txt_Desc.toPlainText()

        typeElement = XML.SubElement(scriptElement, "type")
        if self.btn_typeBash.isChecked():
            typeElement.text = "bash"
        if self.btn_typePerl.isChecked():
            typeElement.text = "perl"
        if self.btn_typePython.isChecked():
            typeElement.text = "python"
        if self.btn_typePythonGUI.isChecked():
            typeElement.text = "pythongui"

        tree.write(scripts_XMLFile, encoding='utf-8', xml_declaration=True)

    def activate_Save(self):
        if (self.btn_typeBash.isChecked() or self.btn_typePerl.isChecked() or
            self.btn_typePython.isChecked() or self.btn_typePythonGUI.isChecked()):
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)

# Open front page window
Ui_MainWindow, QtBaseClass = uic.loadUiType("ScriptCmdr.ui")

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_Exit.clicked.connect(self.exitNow)
        self.btn_Browse.clicked.connect(self.browseFiles)
        self.btn_Edit.clicked.connect(self.editEntry)
        self.btn_Delete.clicked.connect(self.deleteEntry)
        self.get_ScriptList()

    def exitNow(self):
        sys.exit(0)

    def get_ScriptList(self):
        self.list_Scripts.clear()
        global tree
        global scripts

        try:
            tree = XML.parse(scripts_XMLFile)
        except:
            # Not found so let's create a new one!
            root = XML.Element("scripts")
            tree = XML.ElementTree(root)
            tree.write(scripts_XMLFile)

        scripts = tree.getroot()

        # all items data
        for script in scripts:
            self.list_Scripts.addItem(script.get('name'))

    def browseFiles(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Browse All Files", "",
            "All Files (*)", options=options)

        if fileName == "":
            return(0)

        script_add = AddScript()
        script_add.txt_Path.insert(fileName)
        baseName = os.path.basename(fileName)
        script_add.txt_Name.insert(baseName)

        if fileName.endswith("sh"):
            script_add.btn_typeBash.setChecked(True)
        if fileName.endswith("pl"):
            script_add.btn_typePerl.setChecked(True)
        if fileName.endswith("py"):
            script_add.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
        #    script_add.btn_typePython.setChecked(True)

        script_add.exec_()
        self.get_ScriptList()

    def editEntry(self):
        script_edit = AddScript()
        script_edit.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)

        findScript = self.list_Scripts.currentItem().text()
        for script in scripts:
            if script.get('name') == findScript:

                script_edit.txt_Name.insert(findScript)

                script_edit.txt_Path.insert(script.find("path").text)

                if script.find("reqArgs") != None:
                    if script.find("reqArgs").text == "yes":
                        script_edit.cbx_Args.setChecked(True)
                        script_edit.txt_Args.setEnabled(True)
                    else:
                        script_edit.cbx_Args.setChecked(False)
                        script_edit.txt_Args.setEnabled(False)
                else:
                    script_edit.cbx_Args.setChecked(False)
                    script_edit.txt_Args.setEnabled(False)

                if script.find("args") != None:
                    script_edit.txt_Args.insert(script.find("args").text)

                if script.find("viewMsgs") == None:
                    script_edit.cbx_ViewMsgs.setChecked(False)
                else:
                    if script.find("viewMsgs").text == "yes":
                        script_edit.cbx_ViewMsgs.setChecked(True)
                        script_edit.cbx_ViewCode.setChecked(False)
                    else:
                        script_edit.cbx_ViewMsgs.setChecked(False)

                if script.find("viewCode") == None:
                    script_edit.cbx_ViewCode.setChecked(False)
                else:
                    if script.find("viewCode").text == "yes":
                        if script.find("viewMsgs").text == "yes":
                            script_edit.cbx_ViewCode.setChecked(False)
                        else:
                            script_edit.cbx_ViewCode.setChecked(True)
                    else:
                        script_edit.cbx_ViewCode.setChecked(False)

                script_edit.txt_Desc.clear()
                if script.find("Desc") != None:
                    script_edit.txt_Desc.append(script.find("Desc").text)

                if script.find("type").text == "bash":
                    script_edit.btn_typeBash.setChecked(True)
                else:
                    script_edit.btn_typeBash.setChecked(False)

                if script.find("type").text == "perl":
                    script_edit.btn_typePerl.setChecked(True)
                else:
                    script_edit.btn_typePerl.setChecked(False)

                if script.find("type").text == "python":
                    script_edit.btn_typePython.setChecked(True)
                else:
                    script_edit.btn_typePython.setChecked(False)

                if script.find("type").text == "pythongui":
                    script_edit.btn_typePythonGUI.setChecked(True)
                else:
                    script_edit.btn_typePythonGUI.setChecked(False)

                scripts.remove(script)

        script_edit.exec_()
        self.get_ScriptList()

    def deleteEntry(self):

        delete_Script = self.list_Scripts.currentItem().text()
        delete_Msg = "Are you sure you want to remove the list entry for \n'" + delete_Script +"'"
        delete_Reply = QMessageBox.question(self, 'Confirmation Required', delete_Msg,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if delete_Reply == QMessageBox.Yes:
            for script in scripts:
                if script.get('name') == delete_Script:
                    scripts.remove(script)
                    QMessageBox.about(self, "Script Deleted", "Selected Script Deleted from the List")
                    tree.write(scripts_XMLFile, encoding='utf-8', xml_declaration=True)
                    self.get_ScriptList()

    # END OF FUNCTIONS

    # Main Processing Loop

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
