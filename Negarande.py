from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtPrintSupport import *


from enchant.checker import SpellChecker

import re
import os
import sys


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
         super().__init__()
         self.window_list = []
         self.initializeUI()
         self.path = None
         self.updatetext=0
         self.update_title()
         self.lasttext=self.text_field.toPlainText()
         self.text_field.textChanged.connect(self.textchanged)
         self.text_field.textChanged.connect(self.update_title)
         self.text_field.setContextMenuPolicy(Qt.CustomContextMenu)
         self.text_field.customContextMenuRequested.connect(self.generate_context_menu)
         self.text_field.selectionChanged.connect(self.selectionchanged)
         self.selectedtext=None
         sizes=["14" ,"16" ,"18","20","22","24","26","28","30","32"]
         self.text = QLineEdit(self)
         self.Combo = QComboBox(self)
         self.Combo.setEditable(True)
         self.Combo.addItems(sizes)
         self.Combo.currentIndexChanged.connect(self.changeText)
         self.initToolbar()
         
    def initToolbar(self):
        self.spellcheckAction = QAction(QIcon("images\spell.png"),"Spellcheck",self)
        self.spellcheckAction.setStatusTip("Spell Check document")
        self.spellcheckAction.setShortcut("Ctrl+E")
        self.spellcheckAction.triggered.connect(self.spellcheckHandler)

        #New
        self.new_act = QAction(QIcon('images/new.png'), 'New', self)
        self.new_act.setShortcut('Ctrl+N')
        self.new_act.triggered.connect(self.savechanges)
       
        #Open
        self.open_act = QAction(QIcon('images/open_file.png'), 'Open', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.openFile)
        #Save
        self.save_act = QAction(QIcon('images/save_file.png'), 'Save', self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.saveToFile)
       
        
        
        #Print
        self.print_act = QAction(QIcon('images/print.png'), 'Print', self)
        self.print_act.setShortcut('Ctrl+P')
        self.print_act.triggered.connect(self.Print_Preview_Dialog)

        #Cut
        self.cut_act = QAction(QIcon('images/cut.png'),'Cut', self)
        self.cut_act.setShortcut('Ctrl+X')
        self.cut_act.triggered.connect(self.text_field.cut)
        
        #Copy
        self.copy_act = QAction(QIcon('images/copy.png'),'Copy', self)
        self.copy_act.setShortcut('Ctrl+C')
        self.copy_act.triggered.connect(self.text_field.copy)

        #Paste
        
        self.paste_act = QAction(QIcon('images/paste.png'),'Paste', self)
        self.paste_act.setShortcut('Ctrl+V')
        self.paste_act.triggered.connect(self.text_field.paste)

        #Font

        self.font_act = QAction(QIcon('images/font.png'), 'Font', self)
        self.font_act.setShortcut('Ctrl+T')
        self.font_act.triggered.connect(self.chooseFont)
        

        self.toolbar = self.addToolBar("Options")
        
        self.toolbar.addAction(self.new_act)
        self.toolbar.addAction(self.open_act)
        self.toolbar.addAction(self.save_act)
        self.toolbar.addAction(self.print_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cut_act)
        self.toolbar.addAction(self.copy_act)
        self.toolbar.addAction(self.paste_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.font_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.spellcheckAction)
        
        
        
    def spellcheckHandler(self):
        self.reset()
        
        chkr = SpellChecker("en_US")
        s = str(self.text_field.toPlainText())
        self.text_field.setTextBackgroundColor(QColor(255,255,255))
        chkr.set_text(s)
        for err in chkr:
            self.replaceAll(err.word)
        
    def findsp(self, query):
        
        text = self.text_field.toPlainText()
        query = r'\b' + query + r'\b'
        flags = 0 
        pattern = re.compile(query,flags)
        start = self.lastMatch.start() + 1 if self.lastMatch else 0
        
        self.lastMatch = pattern.search(text,start)
        if self.lastMatch:
            start = self.lastMatch.start()
            end = self.lastMatch.end()
            self.moveCursor(start,end)
        else:
            self.text_field.moveCursor(QTextCursor.End)

    def replace(self):
        
        cursor = self.text_field.textCursor()
        
        if cursor.hasSelection():
            if self.lastMatch:
                self.text_field.setTextBackgroundColor(QColor(0,255,0))
                self.text_field.setTextCursor(cursor)
            else :
                self.text_field.setTextBackgroundColor(QColor(255,255,255))
                self.text_field.setTextCursor(cursor)
            

    def replaceAll(self, query):
        
        self.lastMatch = None
        self.findsp(query)
        while self.lastMatch:
            self.replace()
            self.findsp(query)
    def reset(self):
        self.text_field.selectAll()
        self.text_field.setTextBackgroundColor(QColor(255,255,255))
        self.text_field.moveCursor(QTextCursor.End)
    

    def moveCursor(self,start,end):
        cursor = self.text_field.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right,QTextCursor.KeepAnchor,end - start)
        self.text_field.setTextCursor(cursor)

  

    def changeText(self, index):
        
        fontsize=int(self.Combo.currentText())
        self.text_field.setFont(QFont('Arial',fontsize))
    def generate_context_menu(self, location):
        menu = self.text_field.createStandardContextMenu()
        
        
            
        
        
        
        objectTest = QObject(self)
        ShapeLayerList = QWidgetAction(objectTest)
        ShapeLayerList.setDefaultWidget(self.Combo)
       
        # add extra items to the menu
        menu.clear()

        #Fontsize
        menu.addAction(ShapeLayerList)
        #Cut
        cut_act = QAction(QIcon('images/cut.png'),'Cut', self)
        cut_act.setShortcut('Ctrl+X')
        cut_act.triggered.connect(self.text_field.cut)
        
        #Copy
        copy_act = QAction(QIcon('images/copy.png'),'Copy', self)
        copy_act.setShortcut('Ctrl+C')
        copy_act.triggered.connect(self.text_field.copy)

        #Paste
        
        paste_act = QAction(QIcon('images/paste.png'),'Paste', self)
        paste_act.setShortcut('Ctrl+V')
        paste_act.triggered.connect(self.text_field.paste)
        #SelectAll
        
        selectall_act = QAction(QIcon('images/selectall.png'),'SelectAll', self)
        selectall_act.setShortcut('Ctrl+A')
        selectall_act.triggered.connect(self.text_field.selectAll)
        
        #HighLight
        
        highlight_act = QAction(QIcon('images/marker.png'), 'Highlight', self)
        highlight_act.triggered.connect(self.chooseFontBackgroundColor)
        menu.addAction(cut_act)
        menu.addAction(copy_act)
        menu.addAction(paste_act)
        menu.addAction(selectall_act)
        menu.addAction(highlight_act)
        ShapeLayerList.setEnabled(True)
        if (self.selectedtext):
           
           highlight_act.setEnabled(True)
            
        else:
           
           highlight_act.setEnabled(False)
           copy_act.setEnabled(False)
           cut_act.setEnabled(False)
        
        # show the menu
        menu.popup(self.mapToGlobal(location))
    def selectionchanged(self):
        text = self.text_field.textCursor().selectedText()
        self.selectedtext=text
        
        
        pass
    def initializeUI(self):

        self.setGeometry(250,250,800,600)
        
        self.createNotepadWidget()
        self.notpadMenu()
        
        self.show()

    def closeEvent(self, event):
        if(self.updatetext==1):
            self.unsaved()
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    def createNotepadWidget(self):
        
        self.text_field=QTextEdit()
        self.setCentralWidget(self.text_field)
        

    def notpadMenu(self):
         
        """        Create menu for notepad GUI        """
        # Create actions for file menu
        #New
        new_act = QAction(QIcon('images/new.png'), 'New', self)
        new_act.setShortcut('Ctrl+N')
        new_act.triggered.connect(self.savechanges)
        #New Window
        newWindow_act = QAction(QIcon('images/new.png'), 'New Window', self)
        newWindow_act.setShortcut('Ctrl+Shift+N')
        newWindow_act.triggered.connect(self.NewWindow)
        #Open
        open_act = QAction(QIcon('images/open_file.png'), 'Open', self)
        open_act.setShortcut('Ctrl+O')
        open_act.triggered.connect(self.openFile)
        #Save
        save_act = QAction(QIcon('images/save_file.png'), 'Save', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.saveToFile)
        #SaveAs
        saveAs_act = QAction(QIcon('images/saveAs_file.png'), 'Save As...', self)
        saveAs_act.setShortcut('Ctrl+Shift+S')
        saveAs_act.triggered.connect(self.saveAsToFile)
        #PageSetup
        pagesetup_act = QAction(QIcon('images/saveAs_file.png'), 'Page Setup...', self)
        
        pagesetup_act.triggered.connect(self.pagesetup)
        #Print
        print_act = QAction(QIcon('images/print.png'), 'Print', self)
        print_act.setShortcut('Ctrl+P')
        print_act.triggered.connect(self.Print_Preview_Dialog)
        #Exit
        exit_act = QAction(QIcon('images/exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.closeEvent)
        # Create actions for edit menu
        undo_act = QAction(QIcon('images/undo.png'),'Undo', self)
        undo_act.setShortcut('Ctrl+Z')
        undo_act.triggered.connect(self.text_field.undo)
        redo_act = QAction(QIcon('images/redo.png'),'Redo', self)
        redo_act.setShortcut('Ctrl+Shift+Z')
        redo_act.triggered.connect(self.text_field.redo)
        cut_act = QAction(QIcon('images/cut.png'),'Cut', self)
        cut_act.setShortcut('Ctrl+X')
        cut_act.triggered.connect(self.text_field.cut)
        copy_act = QAction(QIcon('images/copy.png'),'Copy', self)
        copy_act.setShortcut('Ctrl+C')
        copy_act.triggered.connect(self.text_field.copy)

        paste_act = QAction(QIcon('images/paste.png'),'Paste', self)
        paste_act.setShortcut('Ctrl+V')
        paste_act.triggered.connect(self.text_field.paste)
        find_act = QAction(QIcon('images/find.png'), 'Find', self)
        find_act.setShortcut('Ctrl+F')
        find_act.triggered.connect(self.findTextDialog)
        spellcheckAction = QAction(QIcon("images\spell.png"),"Spellcheck",self)
       
        spellcheckAction.setShortcut("Ctrl+E")
        spellcheckAction.triggered.connect(self.spellcheckHandler)
        # Create actions for tools menu
        font_act = QAction(QIcon('images/font.png'), 'Font', self)
        font_act.setShortcut('Ctrl+T')
        font_act.triggered.connect(self.chooseFont)
        color_act = QAction(QIcon('images/color.png'), 'Color', self)
        color_act.setShortcut('Ctrl+Shift+C')
        color_act.triggered.connect(self.chooseFontColor)
        highlight_act = QAction(QIcon('images/marker.png'), 'Highlight', self)
        highlight_act.setShortcut('Ctrl+Shift+H')
        highlight_act.triggered.connect(self.chooseFontBackgroundColor)
        about_act = QAction(QIcon('images/about.png'),'About', self)
        about_act.triggered.connect(self.aboutDialog)
        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(new_act)
        file_menu.addAction(newWindow_act)
        file_menu.addSeparator()
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)
        file_menu.addAction(saveAs_act)
        file_menu.addSeparator()
        file_menu.addAction(print_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)
        # Create edit menu and add actions
        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(undo_act)
        edit_menu.addAction(redo_act)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_act)
        edit_menu.addAction(copy_act)
        edit_menu.addAction(paste_act)
        edit_menu.addSeparator()
        edit_menu.addAction(find_act)
        edit_menu.addSeparator()
        edit_menu.addAction(spellcheckAction)
        # Create tools menu and add actions
        tool_menu = menu_bar.addMenu('Tools')
        tool_menu.addAction(font_act)
        tool_menu.addAction(color_act)
        tool_menu.addAction(highlight_act)
        # Create help menu and add actions
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(about_act)

    
    def NewWindow(self):
        new_window = MainWindow()
        new_window.show
        self.window_list.append(new_window)

    def openFile(self):
        """        Open a text or html file and display its contents in        the text edit field.        """
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);;All files (*.*)")

        if path:
            try:
                with open(path, 'r',encoding ='utf-8') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.text_field.setPlainText(text)
                self.updatetext=0
                self.update_title()
             
    def saveToFile(self):
         """        If the save button is clicked, display dialog asking user if        they want to save the text in the text edit field to a text file."""
         if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.saveAsToFile()

         self._save_to_path(self.path)
         
    def saveAsToFile(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);;All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.text_field.toPlainText()
        try:
            with open(path, 'w',encoding ='utf-8') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.lasttext=self.text_field.toPlainText()
            self.updatetext=0
            self.update_title()

    def pagesetup(self):
        pass

    def Print(self):
        pass
    def Print_Preview_Dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
 
        previewDialog.paintRequested.connect(self.Print_Preview)
        previewDialog.exec_()
 
    def Print_Preview(self, printer):
        self.text_field.print_(printer)
    def textchanged(self):
        #print("Text changed...>>> "+self.text_field.toPlainText())
        b=self.lasttext
        a=self.text_field.toPlainText()
        if(a==b):
            #print("A is B")
            self.updatetext=0
        else:
            #print("A is NOT B")
            self.updatetext=1

        #print("TEXT UPDAT STATUS= " +str(self.updatetext))
        fontsize=int(self.Combo.currentText())
        self.text_field.setFont(QFont('Arial',fontsize))
        

    

    def clearText(self):
        self.text_field.clear()

   
        

    
    def savechanges(self):
        if(self.updatetext==1):
            self.unsaved()
        else:
            pass
        self.saved()
            

    def unsaved(self):
        answer = QMessageBox.question(self, "Negarande",
                                      "Do you want to save chnages to %s ?" % (os.path.basename(self.path) if self.path else "Untitled"), QMessageBox.Save | QMessageBox.Discard |QMessageBox.Cancel,
                                      QMessageBox.Save)
        if answer == QMessageBox.Discard:
                self.clearText()
        elif answer == QMessageBox.Save:
                self.saveToFile()
                self.clearText()
                self.update_title()
        
    def saved(self):
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("Negarande")
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setText('Do you want to Open New Text in This Window?')
        msgbox.addButton("This Window", QMessageBox.AcceptRole)
        msgbox.addButton("New Window", QMessageBox.RejectRole)
        msgbox.addButton(QMessageBox.Cancel)
        answer = msgbox.exec_()
        
        if (answer==QMessageBox.AcceptRole):
            self.clearText()
            self.path=None
        elif(answer==QMessageBox.RejectRole):
            self.NewWindow()
            
        else:
            pass
            
        self.update_title()
    def findTextDialog(self):
        """        Search for text in QTextEdit widget        """
        # Display input dialog to ask user for text to search for
        find_text, ok = QInputDialog.getText(self, "Search Text", "Find:")
        extra_selections = []

        # Check to make sure the text can be modified
        if ok and not self.text_field.isReadOnly():
            # set the cursor in the textedit field to the beginning
            self.text_field.moveCursor(QTextCursor.Start)
            color = QColor(Qt.yellow)
            # Look for next occurrence of text
            while(self.text_field.find(find_text)):
                # Use ExtraSelections to mark the text you are
                # searching for as yellow
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(color)
                # Set the cursor of the selection
                selection.cursor = self.text_field.textCursor()
                # Add selection to list
                extra_selections.append(selection)
            # Highlight selections in text edit widget
            for i in extra_selections:
                self.text_field.setExtraSelections(extra_selections)
    def chooseFont(self):
        """        Select font for text        """
        (ok, font) = QFontDialog.getFont()
        
 
        if ok:
            self.text_field.setFont(font)
    def chooseFontColor(self):
        """        Select color for text        """

        color = QColorDialog.getColor()
        if color.isValid():
            self.text_field.setTextColor(color)
    def chooseFontBackgroundColor(self):
        """        Select color for text's background        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_field.setTextBackgroundColor(color)
    def aboutDialog(self):
        """        Display information about program dialog box        """
        QMessageBox.about(self, "About Negarande", "Negarande 2.1 \n\nMade By MiladMirza75 \n\nMiladMirza75@Gmail.Com")
    def update_title(self):
        
        if(self.updatetext==1):
            if (self.path):
                Name = "***"+ str(os.path.basename(self.path))
            else:
                Name = "***Untitled"
        elif(self.updatetext==0):
             if (self.path):
                Name = os.path.basename(self.path)
             else:
                Name = "Untitled"
        
        self.setWindowTitle("%s - Negarande" %Name)
    
        
        
   


def main():
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/notpadicon.png"))
    window=MainWindow()
    sys.exit(app.exec_())
    
    

if __name__=='__main__':
    main()
   
