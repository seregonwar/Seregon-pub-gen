from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeView, QTableView, QTabWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from constants import *
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QStyle  # Aggiungi questa importazione

class ImageSettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seregon Publishing Tools - Image Setting")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Project: PFS Image (nested)"))
        size_button = QPushButton("Used: unknown (update required)\nClick here to update the image size.")
        header_layout.addWidget(size_button)
        layout.addLayout(header_layout)

        # Directory tab content
        directory_tab = QWidget()
        directory_layout = QHBoxLayout()
        
        # Tree view
        self.treeView = QTreeView()
        self.treeModel = QStandardItemModel()
        self.treeView.setModel(self.treeModel)
        directory_layout.addWidget(self.treeView)
        
        # File view
        self.fileView = QTableView()
        self.fileModel = QStandardItemModel()
        self.fileModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified", "Compression"])
        self.fileView.setModel(self.fileModel)
        directory_layout.addWidget(self.fileView)
        
        directory_tab.setLayout(directory_layout)

        # Tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(directory_tab, "Directory")
        self.tabWidget.addTab(QWidget(), "Layout")
        self.tabWidget.addTab(QWidget(), "Chunk")
        layout.addWidget(self.tabWidget)

        self.setLayout(layout)
        self.loadProjectStructure()

    def loadProjectStructure(self):
        self.treeModel.clear()
        root = QStandardItem("Image0 Root")
        self.treeModel.appendRow(root)
        
        sce_sys = QStandardItem("sce_sys")
        src = QStandardItem("src")
        root.appendRow(sce_sys)
        root.appendRow(src)
        
        include = QStandardItem("include")
        src.appendRow(include)
        
        self.treeView.expandAll()

    def onTreeItemClicked(self, index):
        item = self.treeModel.itemFromIndex(index)
        self.updateFileView(item)

    def updateFileView(self, item):
        self.fileModel.clear()
        self.fileModel.setHorizontalHeaderLabels(["File Name", "Length", "Last Modified", "Compression"])
        
        if item.text() == "sce_sys":
            self.fileModel.appendRow([
                QStandardItem(self.style().standardIcon(QStyle.SP_DirIcon), "sce_sys"),
                QStandardItem(""),
                QStandardItem(""),
                QStandardItem("")
            ])
        elif item.text() == "src":
            self.fileModel.appendRow([
                QStandardItem(self.style().standardIcon(QStyle.SP_DirIcon), "src"),
                QStandardItem(""),
                QStandardItem(""),
                QStandardItem("")
            ])
            self.fileModel.appendRow([
                QStandardItem(self.style().standardIcon(QStyle.SP_FileIcon), "eboot.bin"),
                QStandardItem("File is missing"),
                QStandardItem(""),
                QStandardItem("Disabled")
            ])
