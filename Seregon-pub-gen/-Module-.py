import sys
from PyQt5.QtWidgets import QApplication
from main import Form1, main
from orbis_publishing_tools import OrbisPublishingTools

def main(args):
    app = QApplication(sys.argv)
    result = 0
    
    # Inizializza l'applicazione
    init_result = OrbisPublishingTools.run_command("env_info")
    if "Error" in init_result[1]:
        result = 1
    else:
        form = Form1(args[0] if len(args) > 0 else None)
        form.show()
        app.exec_()
        result = 0
    return result

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
