from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QComboBox, QDateTimeEdit, QRadioButton, QCheckBox, 
                            QPushButton, QGroupBox, QWidget, QTabWidget)
from PyQt5.QtCore import QDateTime  # Aggiungi questa importazione

class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seregon Publishing Tools - Project Setting")
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
        import random
        import string
        
        xx = ''.join(random.choices(string.ascii_uppercase, k=2))
        yyy = ''.join(random.choices(string.ascii_uppercase, k=3))
        zzzzz = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        aaaaaaaaaaaa = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        content_id = f"{xx}{yyy}-{zzzzz}_00-{aaaaaaaaaaaa}"
        self.content_id_edit.setText(content_id)
