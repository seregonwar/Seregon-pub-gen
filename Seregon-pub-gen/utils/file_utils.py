from PyQt5.QtWidgets import QFileDialog

def get_open_file_name(parent, title, filter=""):
    return QFileDialog.getOpenFileName(parent, title, "", filter)[0]

def get_save_file_name(parent, title, filter=""):
    return QFileDialog.getSaveFileName(parent, title, "", filter)[0]
