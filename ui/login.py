from typing import List
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QGroupBox,
    QMessageBox, QWidget, QInputDialog, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from config.settings import USERS_DAT, PATH_DAT, CONFIG_DIR
from core.data import load_users, save_users, User


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self._users: List[User] = []
        self.user_name = ""
        self.user_dir = ""
        self._setup_ui()
        self._load_users()

    def _setup_ui(self):
        self.setWindowTitle("DRS - ユーザー選択")
        self.setFixedSize(745, 593)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMinimizeButtonHint)

        frame = QGroupBox("ユーザー選択")
        frame.setFont(QFont("MS UI Gothic", 16))

        self._list_widget = QListWidget()
        self._list_widget.setFont(QFont("MS UI Gothic", 21))
        self._list_widget.setMinimumWidth(550)

        self._login_btn = QPushButton("決定")
        self._login_btn.setFont(QFont("MS UI Gothic", 14))
        self._login_btn.setMinimumHeight(41)

        self._exit_btn = QPushButton("終了")
        self._exit_btn.setFont(QFont("MS UI Gothic", 14))
        self._exit_btn.setMinimumHeight(41)

        self._create_btn = QPushButton("新規作成")
        self._create_btn.setFont(QFont("MS UI Gothic", 14))
        self._create_btn.setMinimumHeight(41)

        self._edit_btn = QPushButton("新規登録")
        self._edit_btn.setFont(QFont("MS UI Gothic", 14))
        self._edit_btn.setMinimumHeight(41)

        self._delete_btn = QPushButton("削除")
        self._delete_btn.setFont(QFont("MS UI Gothic", 14))
        self._delete_btn.setMinimumHeight(41)

        self._config_btn = QPushButton("設定")
        self._config_btn.setFont(QFont("MS UI Gothic", 14))
        self._config_btn.setMinimumHeight(41)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self._login_btn)
        btn_layout.addWidget(self._exit_btn)
        btn_layout.addWidget(self._create_btn)
        btn_layout.addWidget(self._edit_btn)
        btn_layout.addWidget(self._delete_btn)
        btn_layout.addWidget(self._config_btn)
        btn_layout.addStretch()

        frame_layout = QHBoxLayout()
        frame_layout.addWidget(self._list_widget)
        frame_layout.addLayout(btn_layout)
        frame.setLayout(frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

        self._login_btn.clicked.connect(self._on_login)
        self._exit_btn.clicked.connect(self._on_exit)
        self._create_btn.clicked.connect(self._on_create)
        self._edit_btn.clicked.connect(self._on_register)
        self._delete_btn.clicked.connect(self._on_delete)
        self._config_btn.clicked.connect(self._on_config)

    def _load_users(self):
        self._users = load_users()
        self._list_widget.clear()
        for user in self._users:
            item = QListWidgetItem(user.name)
            item.setData(Qt.ItemDataRole.UserRole, user.path)
            self._list_widget.addItem(item)

    def _save(self):
        save_users(self._users)

    def _on_login(self):
        current = self._list_widget.currentRow()
        if current < 0:
            return

        item = self._list_widget.item(current)
        self.user_name = item.text()
        self.user_dir = item.data(Qt.ItemDataRole.UserRole)

        if not self.user_dir:
            QMessageBox.critical(self, "DRS - エラー", "ユーザーディレクトリが設定されていません。")
            return

        self.accept()

    def _on_exit(self):
        self.reject()

    def _on_create(self):
        folder_name = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if not folder_name:
            return

        user_name, ok = QInputDialog.getText(self, "新規ユーザー作成", "ユーザー名:")
        if not ok or not user_name:
            return

        import os
        new_path = os.path.join(folder_name, user_name)
        os.makedirs(new_path, exist_ok=True)

        self._users.append(User(name=user_name, path=new_path))
        self._save()
        self._load_users()

    def _on_edit(self):
        current = self._list_widget.currentRow()
        if current < 0:
            return

        user_name = self._users[current].name
        folder_name, ok = QInputDialog.getText(self, "ユーザー編集", "フォルダ名を入力:")
        if not ok or not folder_name:
            return

        import os
        new_path = os.path.join(os.path.dirname(self._users[current].path) if os.path.dirname(self._users[current].path) else ".", folder_name)
        os.makedirs(new_path, exist_ok=True)

        self._users[current].path = new_path
        self._save()
        self._load_users()

    def _on_delete(self):
        current = self._list_widget.currentRow()
        if current < 0:
            return

        self._users.pop(current)
        self._save()
        self._load_users()

    def _on_register(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダ選択")
        if not folder:
            return

        import os
        folder_name = os.path.basename(folder)
        from core.data import User
        self._users.append(User(folder_name, folder))
        self._save()
        self._load_users()

    def _on_config(self):
        from ui.config_window import ConfigWindow
        cfg = ConfigWindow()
        if cfg.exec():
            pass
