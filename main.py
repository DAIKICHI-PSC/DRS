import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from config.settings import CONFIG_DIR
from core.data import load_product_dir
from ui.login import LoginWindow
from ui.main_window import MainWindow


def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def main():
    ensure_config_dir()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setOrganizationName("DRS")
    app.setApplicationName("DRS")

    login = LoginWindow()
    if login.exec():
        user_name = login.user_name
        user_dir = login.user_dir
        product_dir = load_product_dir()

        main_win = MainWindow(user_name, user_dir, product_dir)
        main_win.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
