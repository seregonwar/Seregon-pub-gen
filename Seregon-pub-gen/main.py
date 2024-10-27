import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from orbis_publishing_tools import OrbisPublishingTools

def main(args):
    app = QApplication(sys.argv)
    
    # Inizializza l'applicazione
    init_result = OrbisPublishingTools.env_info()
    if "Error" in init_result[1]:
        print("Error initializing application:", init_result[1])
        return 1
    
    main_window = MainWindow(args[0] if len(args) > 0 else None)
    main_window.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
