import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar, QAction, 
                             QStatusBar, QDockWidget, QVBoxLayout, QWidget, QTreeView, 
                             QFileDialog, QMessageBox, QSplitter, QTableView, 
                             QTabWidget, QLabel, QPushButton, QHBoxLayout, QCheckBox, 
                             QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QLineEdit, 
                             QComboBox, QDateTimeEdit, QRadioButton, QCheckBox, QGroupBox)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from orbis_publishing_tools import OrbisPublishingTools
import xml.etree.ElementTree as ET

class MainView(QWidget):
    EvModified = pyqtSignal()
    EvUpdated = pyqtSignal()
    EvEnableDel = pyqtSignal()
    EvDisableDel = pyqtSignal()
    EvEnableRename = pyqtSignal()
    EvDisableRename = pyqtSignal()
    EvEnableSelectAll = pyqtSignal()
    EvDisableSelectAll = pyqtSignal()
    EvEnablePlayGoChunk = pyqtSignal()
    EvDisablePlayGoChunk = pyqtSignal()
    EvSaved = pyqtSignal()
    EvEnableImportChunkDef = pyqtSignal()
    EvDisableImportChunkDef = pyqtSignal()
    EvEnableExportChunkDef = pyqtSignal()
    EvDisableExportChunkDef = pyqtSignal()
    EvEnableSortExtent = pyqtSignal()
    EvDisableSortExtent = pyqtSignal()
    EvEnableUpdateCapacity = pyqtSignal()
    EvDisableUpdateCapacity = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        
        # Vista ad albero semplificata
        self.treeView = QTreeView(self)
        self.treeModel = QStandardItemModel()
        self.treeView.setModel(self.treeModel)
        self.treeView.doubleClicked.connect(self.onTreeItemDoubleClicked)
        
        # Vista dettagliata semplificata
        self.detailView = QTableView(self)
        self.detailModel = QStandardItemModel()
        self.detailView.setModel(self.detailModel)
        
        self.layout.addWidget(self.treeView)
        self.layout.addWidget(self.detailView)
        
        self.setLayout(self.layout)
        
        self._fileName = ""
        self.updateViews()

    def updateViews(self):
        # Aggiorna la vista ad albero
        self.treeModel.clear()
        root = QStandardItem("Root")
        self.treeModel.appendRow(root)
        
        # Aggiorna la vista dettagliata
        self.detailModel.clear()
        self.detailModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified"])
        self.detailModel.appendRow([QStandardItem("Image0"), QStandardItem(""), QStandardItem("")])

    def onTreeItemDoubleClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        if item.text() == "Image0":
            self.openImageSettings()

    def openImageSettings(self):
        self.imageSettings = ImageSettingsWindow()
        self.imageSettings.show()

    def fileName(self):
        return self._fileName

    def setFileName(self, name):
        self._fileName = name

    def clearTree(self):
        self.treeModel.clear()

    def setProjInfo(self, update):
        # Implementa la logica per aggiornare le informazioni del progetto
        pass

    def newProj(self, proj_type, proj_flag):
        # Implementa la logica per creare un nuovo progetto
        self.clearTree()
        root = QStandardItem(f"New Project (Type: {proj_type}, Flag: {proj_flag})")
        self.treeModel.appendRow(root)
        self.EvModified.emit()

    def loadProj(self, fname, is_chunk_def):
        self.clearTree()
        root = QStandardItem("Root")
        self.treeModel.appendRow(root)
        
        image0 = QStandardItem("Image0")
        root.appendRow(image0)
        
        # Carica la struttura del progetto dal file GP4
        self.loadProjectStructure(fname)
        
        # Aggiorna la vista dettagliata
        self.updateDetailView(root)
        
        self.treeView.expandAll()
        self.EvModified.emit()
        return 0  # Ritorna 0 se il caricamento è avvenuto con successo

    def loadProjectStructure(self, fname):
        try:
            tree = ET.parse(fname)
            root = tree.getroot()
            
            files = root.find('files')
            if files is not None:
                for file_elem in files.findall('file'):
                    targ_path = file_elem.get('targ_path')
                    if targ_path:
                        self.addFileToTree(targ_path)
        except ET.ParseError:
            print(f"Errore nel parsing del file GP4: {fname}")

    def addFileToTree(self, path):
        parts = path.split('/')
        parent = self.treeModel.item(0, 0).child(0)  # "Image0" item
        
        for i, part in enumerate(parts):
            found = False
            for row in range(parent.rowCount()):
                if parent.child(row, 0).text() == part:
                    parent = parent.child(row, 0)
                    found = True
                    break
            
            if not found:
                new_item = QStandardItem(part)
                parent.appendRow(new_item)
                parent = new_item

    def updateDetailView(self, item):
        self.detailModel.clear()
        self.detailModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified"])
        
        if item.text() == "Root":
            row = [QStandardItem("Image0"), QStandardItem(""), QStandardItem("")]
            self.detailModel.appendRow(row)
        elif item.text() == "Image0" or item.parent() is not None:
            for row in range(item.rowCount()):
                child = item.child(row, 0)
                row_items = [QStandardItem(child.text()), QStandardItem(""), QStandardItem("")]
                self.detailModel.appendRow(row_items)

    def saveProj(self, fname, out_fmt):
        # Implementa la logica per salvare un progetto
        self.EvSaved.emit()
        return 0  # Ritorna 0 se il salvataggio è avvenuto con successo

class ImageSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Setting - Image0")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principale
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Project: PFS Image (nested)"))
        size_button = QPushButton("Used: unknown (update required)\nClick here to update the image size.")
        header_layout.addWidget(size_button)
        layout.addLayout(header_layout)
        
        # Tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.createDirectoryTab(), "Directory")
        self.tabWidget.addTab(self.createLayoutTab(), "Layout")
        self.tabWidget.addTab(self.createChunkTab(), "Chunk")
        layout.addWidget(self.tabWidget)
        
        self.setLayout(layout)

    def createDirectoryTab(self):
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Tree view per la struttura delle directory
        self.treeView = QTreeView()
        self.treeModel = QStandardItemModel()
        self.treeView.setModel(self.treeModel)
        self.treeView.clicked.connect(self.onTreeItemClicked)
        
        # Table view per i file
        self.fileView = QTableView()
        self.fileModel = QStandardItemModel()
        self.fileModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified", "Compression"])
        self.fileView.setModel(self.fileModel)
        
        # Inizializza la struttura base
        root = QStandardItem("Image0 Root")
        self.treeModel.appendRow(root)
        
        # Aggiungi le cartelle di base
        sce_sys = QStandardItem("sce_sys")
        src = QStandardItem("src")
        root.appendRow(sce_sys)
        root.appendRow(src)
        
        layout.addWidget(self.treeView)
        layout.addWidget(self.fileView)
        tab.setLayout(layout)
        return tab

    def onTreeItemClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        self.updateFileView(item.text())

    def updateFileView(self, folder_name):
        self.fileModel.clear()
        self.fileModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified", "Compression"])
        
        if folder_name == "sce_sys":
            self.fileModel.appendRow([
                QStandardItem("sce_sys"),
                QStandardItem(""),
                QStandardItem(""),
                QStandardItem("")
            ])
        elif folder_name == "src":
            self.fileModel.appendRow([
                QStandardItem("src"),
                QStandardItem(""),
                QStandardItem(""),
                QStandardItem("")
            ])
            self.fileModel.appendRow([
                QStandardItem("eboot.bin"),
                QStandardItem("File is missing"),
                QStandardItem(""),
                QStandardItem("Disabled")
            ])

    def createLayoutTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        splitPerLayerCheckbox = QCheckBox("Split per layer")
        layout.addWidget(splitPerLayerCheckbox)
        # Aggiungi qui altri widget per il tab Layout
        tab.setLayout(layout)
        return tab

    def createChunkTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        # Aggiungi qui i widget per il tab Chunk
        tab.setLayout(layout)
        return tab

class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Setting")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Crea un widget con schede
        tab_widget = QTabWidget()
        
        # Scheda Generale
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # Volume Type
        volume_type_layout = QHBoxLayout()
        volume_type_layout.addWidget(QLabel("Volume Type:"))
        self.volume_type_combo = QComboBox()
        self.volume_type_combo.addItem("Application Package")
        volume_type_layout.addWidget(self.volume_type_combo)
        general_layout.addLayout(volume_type_layout)
        
        # Volume Timestamp
        volume_timestamp_layout = QHBoxLayout()
        volume_timestamp_layout.addWidget(QLabel("Volume Timestamp:"))
        self.volume_timestamp_edit = QDateTimeEdit()
        self.volume_timestamp_edit.setDateTime(QDateTime.currentDateTime())
        volume_timestamp_layout.addWidget(self.volume_timestamp_edit)
        general_layout.addLayout(volume_timestamp_layout)
        
        # Creation Date/Time
        creation_date_group = QGroupBox("Creation Date/Time:")
        creation_date_layout = QVBoxLayout()
        self.use_actual_date_radio = QRadioButton("Use an actual date (default)")
        self.use_actual_date_time_radio = QRadioButton("Use an actual date and time")
        self.use_fixed_date_radio = QRadioButton("Use a fixed date")
        self.fixed_date_edit = QDateTimeEdit()
        self.fixed_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.use_fixed_time_check = QCheckBox("Use a fixed time")
        self.fixed_time_edit = QDateTimeEdit()
        self.fixed_time_edit.setDisplayFormat("HH:mm:ss")
        
        creation_date_layout.addWidget(self.use_actual_date_radio)
        creation_date_layout.addWidget(self.use_actual_date_time_radio)
        creation_date_layout.addWidget(self.use_fixed_date_radio)
        creation_date_layout.addWidget(self.fixed_date_edit)
        creation_date_layout.addWidget(self.use_fixed_time_check)
        creation_date_layout.addWidget(self.fixed_time_edit)
        creation_date_group.setLayout(creation_date_layout)
        general_layout.addWidget(creation_date_group)
        
        general_tab.setLayout(general_layout)
        
        # Scheda Package
        package_tab = QWidget()
        package_layout = QVBoxLayout()
        
        # Content ID
        content_id_layout = QHBoxLayout()
        content_id_layout.addWidget(QLabel("Content ID:"))
        self.content_id_edit = QLineEdit()
        content_id_layout.addWidget(self.content_id_edit)
        self.generate_content_id_button = QPushButton("Generate")
        self.generate_content_id_button.clicked.connect(self.generate_content_id)
        content_id_layout.addWidget(self.generate_content_id_button)
        package_layout.addLayout(content_id_layout)
        
        # Passcode
        passcode_layout = QHBoxLayout()
        passcode_layout.addWidget(QLabel("Passcode (32 chars):"))
        self.passcode_edit = QLineEdit()
        passcode_layout.addWidget(self.passcode_edit)
        self.generate_passcode_button = QPushButton("Generate")
        passcode_layout.addWidget(self.generate_passcode_button)
        package_layout.addLayout(passcode_layout)
        
        # Passcode Fingerprint
        passcode_fingerprint_layout = QHBoxLayout()
        passcode_fingerprint_layout.addWidget(QLabel("Passcode Fingerprint:"))
        self.passcode_fingerprint_label = QLabel("(Passcode is not valid)")
        passcode_fingerprint_layout.addWidget(self.passcode_fingerprint_label)
        package_layout.addLayout(passcode_fingerprint_layout)
        
        # Storage Type
        storage_type_layout = QHBoxLayout()
        storage_type_layout.addWidget(QLabel("Storage Type:"))
        self.storage_type_combo = QComboBox()
        self.storage_type_combo.addItems(["Digital and BD, Max 50GB", "Digital only, Max 50GB", "Digital and BD, Max 100GB"])
        storage_type_layout.addWidget(self.storage_type_combo)
        package_layout.addLayout(storage_type_layout)
        
        # Application Type
        application_type_layout = QHBoxLayout()
        application_type_layout.addWidget(QLabel("Application Type:"))
        self.application_type_combo = QComboBox()
        self.application_type_combo.addItems(["Paid Standalone Full App", "Upgradable App", "Demo App", "Freemium App"])
        application_type_layout.addWidget(self.application_type_combo)
        package_layout.addLayout(application_type_layout)
        
        package_tab.setLayout(package_layout)
        
        # Aggiungi le schede al widget con schede
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(package_tab, "Package")
        
        layout.addWidget(tab_widget)
        
        # Pulsanti OK e Cancel
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def generate_content_id(self):
        # Qui implementiamo la logica per generare un Content ID
        # Per ora, generiamo un ID di esempio
        import random
        import string
        
        # Formato: XXYYY-ZZZZZ_00-AAAAAAAAAAAA
        xx = ''.join(random.choices(string.ascii_uppercase, k=2))
        yyy = ''.join(random.choices(string.ascii_uppercase, k=3))
        zzzzz = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        aaaaaaaaaaaa = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        content_id = f"{xx}{yyy}-{zzzzz}_00-{aaaaaaaaaaaa}"
        self.content_id_edit.setText(content_id)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()

class MainWindow(QMainWindow):
    def __init__(self, fname=None):
        super().__init__()
        self.fname = fname
        self.mDirty = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Orbis Publishing Tools')
        self.setGeometry(100, 100, 862, 485)

        self.mainView = MainView(self)
        self.setCentralWidget(self.mainView)

        self.createMenuBar()
        self.createStatusBar()

        self.initForm(self.fname)

        # Connetti i segnali del MainView
        self.mainView.EvModified.connect(self.onModified)
        self.mainView.EvUpdated.connect(self.onUpdated)
        self.mainView.EvEnableDel.connect(self.onEnableDel)
        self.mainView.EvDisableDel.connect(self.onDisableDel)
        self.mainView.EvEnableRename.connect(self.onEnableRename)
        self.mainView.EvDisableRename.connect(self.onDisableRename)
        self.mainView.EvEnableSelectAll.connect(self.onEnableSelectAll)
        self.mainView.EvDisableSelectAll.connect(self.onDisableSelectAll)
        self.mainView.EvEnablePlayGoChunk.connect(self.onEnablePlayGoChunk)
        self.mainView.EvDisablePlayGoChunk.connect(self.onDisablePlayGoChunk)
        self.mainView.EvSaved.connect(self.onSaved)
        self.mainView.EvEnableImportChunkDef.connect(self.onEnableImportChunkDef)
        self.mainView.EvDisableImportChunkDef.connect(self.onDisableImportChunkDef)
        self.mainView.EvEnableExportChunkDef.connect(self.onEnableExportChunkDef)
        self.mainView.EvDisableExportChunkDef.connect(self.onDisableExportChunkDef)
        self.mainView.EvEnableSortExtent.connect(self.onEnableSortExtent)
        self.mainView.EvDisableSortExtent.connect(self.onDisableSortExtent)
        self.mainView.EvEnableUpdateCapacity.connect(self.onEnableUpdateCapacity)
        self.mainView.EvDisableUpdateCapacity.connect(self.onDisableUpdateCapacity)

    def initForm(self, fname):
        self.clearDirty()
        try:
            self.setWindowIcon(QIcon(QApplication.applicationFilePath()))
        except Exception as ex:
            pass
        
        # Aggiorna i testi dei menu con OrbisPublishingTools
        newProjMenu = self.findChild(QMenu, 'newProjMenu')
        if newProjMenu:
            for action in newProjMenu.actions():
                if action.text().startswith('Application Package Project for ORBIS'):
                    action.setText(OrbisPublishingTools.projTypeToInfoStr(9, 0) + "(&A)")
                elif action.text().startswith('Patch Package Project for ORBIS'):
                    action.setText(OrbisPublishingTools.projTypeToInfoStr(10, 0) + "(&P)")
                # ... (aggiorna gli altri elementi del menu in modo simile)

        if fname:
            self.doOpenProj(fname)

    def clearDirty(self):
        self.mDirty = False
        self.updateWindowTitle()

    def setDirty(self):
        self.mDirty = True
        self.updateWindowTitle()

    def updateWindowTitle(self):
        title = f"{OrbisPublishingTools.progName()}{OrbisPublishingTools.progNameSuffix()}"
        if self.mainView.fileName():
            title += f" - {self.mainView.fileName()}"
            if self.mDirty:
                title += " *"
        self.setWindowTitle(title)

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
        editMenu.addSeparator()
        editMenu.addAction(self.createAction('Cut(&T)', self.cut, False))
        editMenu.addAction(self.createAction('Copy(&C)', self.copy, False))
        editMenu.addAction(self.createAction('Paste(&P)', self.paste, False))
        editMenu.addAction(self.createAction('Delete(&D)', self.delete, False))
        editMenu.addSeparator()
        editMenu.addAction(self.createAction('Rename(&R)', self.rename, False))
        editMenu.addSeparator()
        editMenu.addAction(self.createAction('Select All(&A)', self.selectAll, False))

        commandMenu = menubar.addMenu('Command(&C)')
        commandMenu.addAction(self.createAction('Package Generator Setting(&G)...', self.userConf))
        commandMenu.addSeparator()
        commandMenu.addAction(self.createAction('Project Setting(&P)...', self.volume))
        commandMenu.addAction(self.createAction('PlayGo System Setting(&L)...', self.editPlayGoChunk))
        commandMenu.addAction(self.createAction('Update/Display the Estimated Image Size(&U)...', self.updateCapacity))
        commandMenu.addAction(self.createAction('Media Type(&M)', self.mediaType))
        commandMenu.addAction(self.createAction('Edit Layout Information(&L)...', self.layout))
        commandMenu.addSeparator()
        commandMenu.addAction(self.createAction('Build Image(&B)...', self.genImg))
        commandMenu.addSeparator()
        commandMenu.addAction(self.createAction('Verify Package/ISO Image/Blu-ray Disc (Launch Image Checker)(&V)...', self.verifyImg))
        commandMenu.addSeparator()
        commandMenu.addAction(self.createAction('Sort Files according to the Chunk Order(&S)...', self.sortExtent))
        commandMenu.addSeparator()
        commandMenu.addAction(self.createAction('Burn ISO Image to Blu-ray Disc(&D)...', self.burnImg))
        commandMenu.addAction(self.createAction('Copy ISO Image from Blu-ray Disc(&F)...', self.copyImg))

        helpMenu = menubar.addMenu('Help(&H)')
        helpMenu.addAction(self.createAction('About(&A)...', self.about))
        helpMenu.addAction(self.createAction('Release Notes(&R)...', self.relNote))
        helpMenu.addAction(self.createAction("User's Guide(&U)...", self.usrGuide))

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def createAction(self, text, slot, enabled=True):
        action = QAction(text, self)
        action.triggered.connect(slot)
        action.setEnabled(enabled)
        return action

    def newProj(self):
        sender = self.sender()
        proj_type = 9
        proj_flag = 0
        
        # Determina il tipo di progetto in base all'azione selezionata
        if sender.text().startswith('Application Package Project for ORBIS'):
            proj_type = 9
        elif sender.text().startswith('Patch Package Project for ORBIS'):
            proj_type = 10
        # ... (aggiungi altri casi per i diversi tipi di progetto)

        if self.askIfDirty():
            self.mainView.newProj(proj_type, proj_flag)
            self.mainView.setFileName(None)
            self.clearDirty()
            self.mainView.setProjInfo(False)

    def openProj(self):
        if self.askIfDirty():
            fname, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.gp4);;All Files (*)")
            if fname:
                self.doOpenProj(fname)

    def doOpenProj(self, fname):
        num = self.mainView.loadProj(fname, False)
        if num == 0:
            self.mainView.setFileName(fname)
            self.mainView.loadProjectStructure(fname)  # Aggiungi questa riga
            self.clearDirty()
            self.mainView.setProjInfo(False)
            self.updateWindowTitle()
            self.statusBar.showMessage(f"Loaded Project: {fname}")

    def saveProj(self):
        if not self.mainView.fileName():
            self.saveAsProj()
        else:
            self.doSaveProj(False, False)

    def saveAsProj(self):
        self.doSaveProj(True, False)

    def doSaveProj(self, save_as, save_as_gp3):
        fname = self.mainView.fileName()
        out_fmt = "gp3" if save_as_gp3 else "gp4"
        if save_as or not fname:
            fname, _ = QFileDialog.getSaveFileName(self, "Save Project", fname, f"Project Files (*.{out_fmt});;All Files (*)")
            if not fname:
                return False
        
        num = self.mainView.saveProj(fname, out_fmt)
        if num != 0:
            return False
        
        self.mainView.setFileName(fname)
        self.clearDirty()
        return True

    def importChunkDef(self):
        if self.askIfDirty():
            fname, _ = QFileDialog.getOpenFileName(self, "Import Chunk Definition", "", "XML Files (*.xml);;All Files (*)")
            if fname:
                num = self.mainView.loadProj(fname, True)
                if num == 0:
                    self.mainView.setFileName(None)
                    self.clearDirty()
                    self.mainView.setProjInfo(False)

    def exportChunkDef(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Export Chunk Definition", "", "XML Files (*.xml);;All Files (*)")
        if fname:
            self.mainView.saveProj(fname, "playgo-chunks")

    def exitApp(self):
        if self.askIfDirty():
            self.close()

    def askIfDirty(self):
        if not self.mDirty:
            return True
        reply = QMessageBox.question(self, 'Unsaved Changes',
                                     "Do you want to save your changes?",
                                     QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                     QMessageBox.Save)
        if reply == QMessageBox.Save:
            return self.saveProj()
        elif reply == QMessageBox.Cancel:
            return False
        return True

    # Implementa gli altri metodi (undo, redo, cut, copy, paste, delete, rename, selectAll, etc.)

    def onModified(self):
        self.setDirty()

    def onUpdated(self):
        self.mainView.setProjInfo(False)

    def onEnableDel(self):
        self.findChild(QAction, 'actionDelete').setEnabled(True)

    def onDisableDel(self):
        self.findChild(QAction, 'actionDelete').setEnabled(False)

    def onEnableRename(self):
        self.findChild(QAction, 'actionRename').setEnabled(True)

    def onDisableRename(self):
        self.findChild(QAction, 'actionRename').setEnabled(False)

    def onEnableSelectAll(self):
        self.findChild(QAction, 'actionSelectAll').setEnabled(True)

    def onDisableSelectAll(self):
        self.findChild(QAction, 'actionSelectAll').setEnabled(False)

    def onEnablePlayGoChunk(self):
        self.findChild(QAction, 'actionEditPlayGoChunk').setEnabled(True)

    def onDisablePlayGoChunk(self):
        self.findChild(QAction, 'actionEditPlayGoChunk').setEnabled(False)

    def onSaved(self):
        self.clearDirty()

    def onEnableImportChunkDef(self):
        self.findChild(QAction, 'actionImportChunkDef').setEnabled(True)

    def onDisableImportChunkDef(self):
        self.findChild(QAction, 'actionImportChunkDef').setEnabled(False)

    def onEnableExportChunkDef(self):
        self.findChild(QAction, 'actionExportChunkDef').setEnabled(True)

    def onDisableExportChunkDef(self):
        self.findChild(QAction, 'actionExportChunkDef').setEnabled(False)

    def onEnableSortExtent(self):
        self.findChild(QAction, 'actionSortExtent').setEnabled(True)

    def onDisableSortExtent(self):
        self.findChild(QAction, 'actionSortExtent').setEnabled(False)

    def onEnableUpdateCapacity(self):
        self.findChild(QAction, 'actionUpdateCapacity').setEnabled(True)

    def onDisableUpdateCapacity(self):
        self.findChild(QAction, 'actionUpdateCapacity').setEnabled(False)

    def volume(self):
        dialog = ProjectSettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Qui puoi gestire i dati inseriti dall'utente
            # Ad esempio, puoi chiamare OrbisPublishingTools per aggiornare le impostazioni del progetto
            result = OrbisPublishingTools.gp4_component_setup(
                volume_type=dialog.volume_type_combo.currentText(),
                volume_timestamp=dialog.volume_timestamp_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
                content_id=dialog.content_id_edit.text(),
                passcode=dialog.passcode_edit.text(),
                storage_type=dialog.storage_type_combo.currentText(),
                application_type=dialog.application_type_combo.currentText()
            )
            self.showCommandResult("Project Setting", result)

    def undo(self):
        print("Undo action")

    def redo(self):
        print("Redo action")

    def cut(self):
        print("Cut action")

    def copy(self):
        print("Copy action")

    def paste(self):
        print("Paste action")

    def delete(self):
        print("Delete action")

    def rename(self):
        print("Rename action")

    def selectAll(self):
        print("Select All action")

    def userConf(self):
        print("User Configuration action")

    def editPlayGoChunk(self):
        print("Edit PlayGo Chunk action")

    def updateCapacity(self):
        print("Update Capacity action")

    def mediaType(self):
        print("Media Type action")

    def layout(self):
        print("Layout action")

    def genImg(self):
        print("Generate Image action")

    def verifyImg(self):
        print("Verify Image action")

    def sortExtent(self):
        print("Sort Extent action")

    def burnImg(self):
        print("Burn Image action")

    def copyImg(self):
        print("Copy Image action")

    def about(self):
        print("About action")

    def relNote(self):
        print("Release Notes action")

    def usrGuide(self):
        print("User Guide action")

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
