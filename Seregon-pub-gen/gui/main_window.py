from PyQt5.QtWidgets import (QMainWindow, QSplitter, QTreeView, QTableView, 
                            QVBoxLayout, QWidget, QMessageBox, QDialog, QStyle, 
                            QStatusBar, QAction, QFileDialog, QMenu)  # Aggiunto QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from .image_settings_window import ImageSettingsWindow
from .project_settings_dialog import ProjectSettingsDialog
from utils.file_utils import get_open_file_name, get_save_file_name
from constants import *
from orbis_publishing_tools import OrbisPublishingTools

class MainWindow(QMainWindow):
    def __init__(self, fname=None):
        super().__init__()
        self.fname = fname
        self.mDirty = False
        self.initUI()

    def clearDirty(self):
        self.mDirty = False
        self.updateWindowTitle()

    def updateWindowTitle(self):
        title = "Seregon Publishing Tools"
        if self.fname:
            title += f" - {self.fname}"
            if self.mDirty:
                title += " *"
        self.setWindowTitle(title)

    def initUI(self):
        self.setWindowTitle("Seregon Publishing Tools")
        self.setGeometry(100, 100, 862, 485)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.splitter)

        self.treeView = QTreeView()
        self.treeModel = QStandardItemModel()
        self.treeView.setModel(self.treeModel)
        self.treeView.doubleClicked.connect(self.onTreeItemDoubleClicked)
        self.splitter.addWidget(self.treeView)

        self.detailView = QTableView()
        self.detailModel = QStandardItemModel()
        self.detailView.setModel(self.detailModel)
        self.splitter.addWidget(self.detailView)

        self.createMenuBar()
        self.createStatusBar()

        self.initForm(self.fname)

    # ... (altri metodi come prima, ma utilizzando le costanti da constants.py)

    def volume(self):
        dialog = ProjectSettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Converti i parametri in una lista di argomenti
            args = [
                dialog.volume_type_combo.currentText(),
                dialog.volume_timestamp_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
                dialog.content_id_edit.text(),
                dialog.passcode_edit.text(),
                dialog.storage_type_combo.currentText(),
                dialog.application_type_combo.currentText()
            ]
            result = OrbisPublishingTools.gp4_component_setup(*args)
            self.showCommandResult("Project Setting", result)



    def initForm(self, fname):
        self.clearDirty()
        self.updateTreeView()
        if fname:
            self.doOpenProj(fname)

    def updateTreeView(self):
        self.treeModel.clear()
        root = QStandardItem("<b>Root</b>")
        self.treeModel.appendRow(root)
        self.updateDetailView()
        self.treeView.expandAll()

    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if item.text() == "Image0":
            self.openImageSettings()

    def openImageSettings(self):
        self.image_settings = ImageSettingsWindow(self)
        self.image_settings.show()

    def doOpenProj(self, fname):
        self.updateTreeView()
        self.updateDetailView()
        self.setWindowTitle(f"Seregon Publishing Tools - {fname}")
        self.statusBar.showMessage(f"Loaded Project: {fname}")  # Corretto da statusBar() a statusBar

    def updateDetailView(self):
        self.detailModel.clear()
        self.detailModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified"])
        image_item = QStandardItem("<b>Image0</b>")
        self.detailModel.appendRow([image_item, QStandardItem(""), QStandardItem("")])


    def createMenuBar(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File(&F)')
        newProjMenu = QMenu('New Project(&N)', self)
        newProjMenu.addAction(self.createAction('Application Package Project for ORBIS', self.newProj))
        newProjMenu.addAction(self.createAction('Application Package Project for ORBIS(Multi Disc)', self.newProj))
        newProjMenu.addAction(self.createAction('Patch Package Project for ORBIS', self.newProj))
        newProjMenu.addAction(self.createAction('Remaster Package Project for ORBIS', self.newProj))
        newProjMenu.addAction(self.createAction('Remaster Package Project for ORBIS(digixl)', self.newProj))
        newProjMenu.addAction(self.createAction('Remaster Package Project for ORBIS(Multi Disc)', self.newProj))
        newProjMenu.addAction(self.createAction('Additional Content Package with extra data for ORBIS', self.newProj))
        newProjMenu.addAction(self.createAction('Additional Content Package without extra data for ORBIS', self.newProj))
        newProjMenu.addAction(self.createAction('SHARE factory addon', self.newProj))
        newProjMenu.addAction(self.createAction('Custom Theme', self.newProj))
        newProjMenu.addAction(self.createAction('*exFAT Image Project', self.newProj))
        newProjMenu.addAction(self.createAction('*PFS Image (plain) Project', self.newProj))
        newProjMenu.addSeparator()
        newProjMenu.addAction(self.createAction('iso bd50', self.newProj))
        newProjMenu.addAction(self.createAction('iso bd50_50', self.newProj))
        newProjMenu.addAction(self.createAction('iso bd50_50_50', self.newProj))
        newProjMenu.addAction(self.createAction('iso bd50_compilation_disc', self.newProj))
        fileMenu.addMenu(newProjMenu)
        fileMenu.addAction(self.createAction('Open(&O)', self.openProj))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAction('Save(&S)', self.saveProj))
        fileMenu.addAction(self.createAction('Save as(&A)...', self.saveAsProj))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAction('Import Chunk Definition File(&I)...', self.importChunkDef))
        fileMenu.addAction(self.createAction('Export Chunk Definition File(&E)...', self.exportChunkDef))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAction('Exit(&X)', self.exitApp))

        editMenu = menubar.addMenu('Edit(&E)')
        editMenu.addAction(self.createAction('Undo(&U)', self.undo, False))
        editMenu.addAction(self.createAction('Redo(&R)', self.redo, False))

        commandMenu = menubar.addMenu('Command(&C)')
        commandMenu.addAction(self.createAction('Project Setting(&P)...', self.volume))

        helpMenu = menubar.addMenu('Help(&H)')
        helpMenu.addAction(self.createAction('About(&A)...', self.about))

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def createAction(self, text, slot, enabled=True):
        action = QAction(text, self)
        action.triggered.connect(slot)
        action.setEnabled(enabled)
        return action

    def openProj(self):
        file_filter = (
            "All Supported (*.gp4 *.pkg *.sfo *.pfs *.dat);;"
            "PKG Projects (*.gp4);;"
            "PKG Files (*.pkg);;"
            "SFO Files (*.sfo);;"
            "PFS Files (*.pfs);;"
            "DAT Files (*.dat);;"
            "All Files (*)"
        )
        
        fname, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            file_filter
        )
        
        if fname:
            extension = fname.lower().split('.')[-1]
            if extension == 'gp4':
                self.loadGp4Project(fname)
            elif extension == 'pkg':
                self.loadPkgFile(fname)
            elif extension == 'sfo':
                self.loadSfoFile(fname)
            elif extension == 'pfs':
                self.loadPfsFile(fname)
            elif extension == 'dat':
                self.loadDatFile(fname)

    def loadGp4Project(self, fname):
        self.doOpenProj(fname)

    def loadPkgFile(self, fname):
        result = OrbisPublishingTools.pkg_file_list(fname)
        self.showCommandResult("Load PKG File", result)
        # Implementa la logica per visualizzare il contenuto del PKG

    def loadSfoFile(self, fname):
        result = OrbisPublishingTools.sfo_export(fname)
        self.showCommandResult("Load SFO File", result)
        # Implementa la logica per visualizzare il contenuto del SFO

    def loadPfsFile(self, fname):
        # Implementa la logica per caricare file PFS
        # Usa i comandi appropriati di OrbisPublishingTools
        pass

    def loadDatFile(self, fname):
        # Implementa la logica per caricare file DAT
        # Usa i comandi appropriati di OrbisPublishingTools
        pass

    def updateTreeView(self):
        self.treeModel.clear()
        root = QStandardItem("<b>Root</b>")
        self.treeModel.appendRow(root)
        self.updateDetailView()
        self.treeView.expandAll()

    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if item.text() == "Image0":
            self.openImageSettings()

    def openImageSettings(self):
        self.image_settings = ImageSettingsWindow(self)
        self.image_settings.show()

    def updateDetailView(self):
        self.detailModel.clear()

        image_item = QStandardItem("Image0")
        self.detailModel.appendRow([image_item, QStandardItem(""), QStandardItem("")])


    def volume(self):
        dialog = ProjectSettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            args = [
                dialog.volume_type_combo.currentText(),
                dialog.volume_timestamp_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
                dialog.content_id_edit.text(),
                dialog.passcode_edit.text(),
                dialog.storage_type_combo.currentText(),
                dialog.application_type_combo.currentText()
            ]
            result = OrbisPublishingTools.gp4_component_setup(*args)
            self.showCommandResult("Project Setting", result)

    def undo(self):
        print("Undo action")

    def redo(self):
        print("Redo action")

    def about(self):
        QMessageBox.information(self, "About", "Seregon Publishing Tools\nVersion 1.0")

    def exitApp(self):
        self.close()

    def connectSignals(self):
        # Non abbiamo più bisogno di questi segnali poiché non stiamo più usando MainView
        pass

    def newProj(self):
        sender = self.sender()
        proj_type = 9
        proj_flag = 0
        
        # Determina il tipo di progetto in base all'azione selezionata
        if sender.text().startswith('Application Package Project for ORBIS'):
            proj_type = 9
        elif sender.text().startswith('Patch Package Project for ORBIS'):
            proj_type = 10
        elif sender.text().startswith('Remaster Package Project for ORBIS'):
            proj_type = 11
        elif sender.text().startswith('Additional Content Package'):
            proj_type = 12
        elif sender.text().startswith('SHARE factory addon'):
            proj_type = 14
        elif sender.text().startswith('Custom Theme'):
            proj_type = 15
        
        # Gestione dei flag per i progetti multi-disco
        if '(Multi Disc)' in sender.text():
            proj_flag = 1
        elif '(digixl)' in sender.text():
            proj_flag = 4

        result = OrbisPublishingTools.gp4_proj_create(str(proj_type), str(proj_flag))
        self.showCommandResult("New Project", result)

    def saveProj(self):
        if not self.fname:
            self.saveAsProj()
        else:
            self.doSaveProj(False)

    def saveAsProj(self):
        self.doSaveProj(True)

    def doSaveProj(self, save_as):
        if save_as or not self.fname:
            fname, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Project Files (*.gp4);;All Files (*)")
            if not fname:
                return False
            self.fname = fname

        result = OrbisPublishingTools.gp4_proj_update(self.fname)
        self.showCommandResult("Save Project", result)
        return True

    def importChunkDef(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Import Chunk Definition", "", "XML Files (*.xml);;All Files (*)")
        if fname:
            result = OrbisPublishingTools.gp4_chunk_def_import(fname)
            self.showCommandResult("Import Chunk Definition", result)

    def exportChunkDef(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Chunk Definition", "", "XML Files (*.xml);;All Files (*)")
        if fname:
            result = OrbisPublishingTools.gp4_chunk_def_export(fname)
            self.showCommandResult("Export Chunk Definition", result)

    def showCommandResult(self, title, result):
        if result[1]:  # Se c'è un errore
            QMessageBox.warning(self, title, result[1])
        else:
            QMessageBox.information(self, title, result[0] if result[0] else "Operation completed successfully")
