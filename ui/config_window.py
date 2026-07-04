from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QComboBox, QLineEdit, QGroupBox,
    QFrame, QFileDialog, QMessageBox, QSpinBox,
    QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from typing import List

from core.data import (
    RS232Config, load_rs232_configs, save_rs232_configs,
    load_product_dir, save_product_dir
)
from core.serial_comm import SerialCommunicator, END_SEND_MAP


BAUD_RATES = ["110", "300", "600", "1200", "2400", "4800", "9600",
              "14400", "19200", "28800", "38400", "56000", "128000", "256000"]
PARITIES = ["E", "M", "N", "O", "S"]
DATA_LENGTHS = ["4", "5", "6", "7", "8"]
STOP_BITS = ["1", "1.5", "2"]
HANDSHAKES = ["None", "Xon/Xoff", "RTS/CTS", "DTR/DSR"]
END_CHARS = ["CR", "LF", "CR+LF"]


class RS232ConfigPage(QGroupBox):
    def __init__(self, config: RS232Config, index: int):
        super().__init__(f"F{index + 1}設定")
        self.config = config
        self._setup_ui()
        self._load_config()

    def _setup_ui(self):
        self.setFont(QFont("MS UI Gothic", 10))
        layout = QFormLayout()
        layout.setVerticalSpacing(8)
        layout.setHorizontalSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        layout.setContentsMargins(10, 20, 10, 10)
        font = QFont("MS UI Gothic", 10)

        self._com_combo = QComboBox()
        self._com_combo.setFont(font)
        self._com_combo.setMinimumHeight(15)
        self._com_combo.setMinimumWidth(150)
        for i in range(1, 16):
            self._com_combo.addItem(f"COM{i}")

        self._baud_combo = QComboBox()
        self._baud_combo.setFont(font)
        self._baud_combo.setMinimumHeight(15)
        self._baud_combo.setMinimumWidth(150)
        self._baud_combo.addItems(BAUD_RATES)

        self._parity_combo = QComboBox()
        self._parity_combo.setFont(font)
        self._parity_combo.setMinimumHeight(15)
        self._parity_combo.setMinimumWidth(150)
        self._parity_combo.addItems(PARITIES)

        self._data_combo = QComboBox()
        self._data_combo.setFont(font)
        self._data_combo.setMinimumHeight(15)
        self._data_combo.setMinimumWidth(150)
        self._data_combo.addItems(DATA_LENGTHS)

        self._stop_combo = QComboBox()
        self._stop_combo.setFont(font)
        self._stop_combo.setMinimumHeight(15)
        self._stop_combo.setMinimumWidth(150)
        self._stop_combo.addItems(STOP_BITS)

        self._handshake_combo = QComboBox()
        self._handshake_combo.setFont(font)
        self._handshake_combo.setMinimumHeight(15)
        self._handshake_combo.setMinimumWidth(150)
        self._handshake_combo.addItems(HANDSHAKES)

        self._get_data_edit = QLineEdit()
        self._get_data_edit.setFont(font)
        self._get_data_edit.setMinimumHeight(15)
        self._get_data_edit.setMinimumWidth(150)
        self._end_pc_combo = QComboBox()
        self._end_pc_combo.setFont(font)
        self._end_pc_combo.setMinimumHeight(15)
        self._end_pc_combo.setMinimumWidth(150)
        self._end_pc_combo.addItems(END_CHARS)
        self._end_machine_combo = QComboBox()
        self._end_machine_combo.setFont(font)
        self._end_machine_combo.setMinimumHeight(15)
        self._end_machine_combo.setMinimumWidth(150)
        self._end_machine_combo.addItems(END_CHARS)

        self._start_pos_edit = QLineEdit()
        self._start_pos_edit.setFont(font)
        self._start_pos_edit.setMinimumHeight(15)
        self._start_pos_edit.setMinimumWidth(150)
        self._end_pos_edit = QLineEdit()
        self._end_pos_edit.setFont(font)
        self._end_pos_edit.setMinimumHeight(15)
        self._end_pos_edit.setMinimumWidth(150)
        self._show_name_edit = QLineEdit()
        self._show_name_edit.setFont(font)
        self._show_name_edit.setMinimumHeight(15)
        self._show_name_edit.setMinimumWidth(150)
        self._excel_name_edit = QLineEdit()
        self._excel_name_edit.setFont(font)
        self._excel_name_edit.setMinimumHeight(15)
        self._excel_name_edit.setMinimumWidth(150)

        def make_label(text):
            lbl = QLabel(text)
            lbl.setFont(font)
            lbl.setMinimumHeight(15)
            return lbl

        layout.addRow(make_label("COMポート:"), self._com_combo)
        layout.addRow(make_label("ボーレート:"), self._baud_combo)
        layout.addRow(make_label("パリティ:"), self._parity_combo)
        layout.addRow(make_label("データ長:"), self._data_combo)
        layout.addRow(make_label("ストップビット:"), self._stop_combo)
        layout.addRow(make_label("ハンドシェイク:"), self._handshake_combo)
        layout.addRow(make_label("データ取得コマンド:"), self._get_data_edit)
        layout.addRow(make_label("PC送信終了文字:"), self._end_pc_combo)
        layout.addRow(make_label("機器送信終了文字:"), self._end_machine_combo)
        layout.addRow(make_label("データ開始位置:"), self._start_pos_edit)
        layout.addRow(make_label("データ終了位置:"), self._end_pos_edit)
        layout.addRow(make_label("表示用機器名:"), self._show_name_edit)
        layout.addRow(make_label("Excel用機器名:"), self._excel_name_edit)

        self._test_btn = QPushButton("通信テスト")
        self._test_btn.clicked.connect(self._test_comm)
        self._test_btn.setFixedHeight(25)
        layout.addRow(self._test_btn)

        self.setLayout(layout)

    def _load_config(self):
        try:
            self._com_combo.setCurrentIndex(int(self.config.com_num) - 1)
        except (ValueError, IndexError):
            pass
        try:
            self._baud_combo.setCurrentIndex(BAUD_RATES.index(self.config.baud_rate))
        except ValueError:
            pass
        try:
            self._parity_combo.setCurrentIndex(PARITIES.index(self.config.parity))
        except ValueError:
            pass
        try:
            self._data_combo.setCurrentIndex(DATA_LENGTHS.index(self.config.data_length))
        except ValueError:
            pass
        try:
            self._stop_combo.setCurrentIndex(STOP_BITS.index(self.config.stop_bit))
        except ValueError:
            pass
        try:
            self._handshake_combo.setCurrentIndex(int(self.config.handshake))
        except (ValueError, IndexError):
            pass

        self._get_data_edit.setText(self.config.get_data_com)

        try:
            self._end_pc_combo.setCurrentIndex(int(self.config.end_send_pc) - 1)
        except (ValueError, IndexError):
            pass
        try:
            self._end_machine_combo.setCurrentIndex(int(self.config.end_send_machine) - 1)
        except (ValueError, IndexError):
            pass

        self._start_pos_edit.setText(self.config.data_start_pos)
        self._end_pos_edit.setText(self.config.data_end_pos)
        self._show_name_edit.setText(self.config.machine_name_show)
        self._excel_name_edit.setText(self.config.machine_name_excel)

    def save_config(self):
        self.config.com_num = str(self._com_combo.currentIndex() + 1)
        self.config.baud_rate = self._baud_combo.currentText()
        self.config.parity = self._parity_combo.currentText()
        self.config.data_length = self._data_combo.currentText()
        self.config.stop_bit = self._stop_combo.currentText()
        self.config.handshake = str(self._handshake_combo.currentIndex())
        self.config.get_data_com = self._get_data_edit.text()
        self.config.end_send_pc = str(self._end_pc_combo.currentIndex() + 1)
        self.config.end_send_machine = str(self._end_machine_combo.currentIndex() + 1)
        self.config.data_start_pos = self._start_pos_edit.text()
        self.config.data_end_pos = self._end_pos_edit.text()
        self.config.machine_name_show = self._show_name_edit.text()
        self.config.machine_name_excel = self._excel_name_edit.text()

    def _test_comm(self):
        self.save_config()
        communicator = SerialCommunicator()
        communicator.configure(self.config)

        if not communicator.open_port():
            QMessageBox.critical(self, "DRS - エラー",
                                 "ポートを開けません。COMポートの設定を確認してください。")
            return

        try:
            command = self.config.get_data_com
            result = communicator.send_and_receive(command, timeout_ms=2000)

            if result is not None:
                raw_buffer = getattr(communicator, '_raw_buffer', '')
                formatted = result.strip()
                try:
                    formatted = str(abs(float(formatted))).lstrip()
                except ValueError:
                    pass
                QMessageBox.information(self, "通信結果",
                                        f"受信データ:\n{raw_buffer}\n\n整形データ:\n{formatted}")
            else:
                QMessageBox.critical(self, "DRS - エラー", "通信タイムアウトしました。")
        finally:
            communicator.close_port()


class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self._configs: List[RS232Config] = load_rs232_configs()
        self._pages: List[RS232ConfigPage] = []
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("DRS - 設定")
        self.resize(993, 650)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMinimizeButtonHint)

        self.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                min-height: 15px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QLineEdit {
                padding: 5px 10px;
                min-height: 15px;
            }
            QPushButton {
                min-height: 25px;
                max-height: 25px;
            }
            QGroupBox {
                font-weight: bold;
                margin-top: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self._tab_combo = QComboBox()
        self._tab_combo.setFont(QFont("MS UI Gothic", 10))
        self._tab_combo.setMinimumHeight(30)
        for i in range(10):
            self._tab_combo.addItem(f"F{i + 1}設定")
        self._tab_combo.currentIndexChanged.connect(self._on_tab_changed)

        self._stacked = QStackedWidget()
        for i, cfg in enumerate(self._configs):
            page = RS232ConfigPage(cfg, i)
            self._stacked.addWidget(page)
            self._pages.append(page)

        dir_group = QGroupBox("製品ディレクトリ設定")
        dir_layout = QVBoxLayout()

        self._dir_edit = QLineEdit()
        self._dir_edit.setFont(QFont("MS UI Gothic", 10))
        self._dir_edit.setMinimumHeight(30)
        self._dir_edit.setText(load_product_dir())
        dir_layout.addWidget(self._dir_edit)

        self._dir_btn = QPushButton("参照")
        self._dir_btn.clicked.connect(self._on_select_dir)
        self._dir_btn.setFixedHeight(25)
        dir_layout.addWidget(self._dir_btn)
        dir_group.setLayout(dir_layout)

        left_layout.addWidget(self._tab_combo)
        left_layout.addWidget(self._stacked)
        left_layout.addWidget(dir_group)

        main_layout.addLayout(left_layout)

        btn_layout = QVBoxLayout()
        self._ok_btn = QPushButton("OK")
        self._ok_btn.setMinimumWidth(121)
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setMinimumWidth(121)
        btn_layout.addWidget(self._ok_btn)
        btn_layout.addWidget(self._cancel_btn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        self._ok_btn.clicked.connect(self._on_ok)
        self._cancel_btn.clicked.connect(self.reject)

    def _on_tab_changed(self, index: int):
        self._stacked.setCurrentIndex(index)

    def _on_select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "製品ディレクトリを選択")
        if dir_path:
            self._dir_edit.setText(dir_path)

    def _on_ok(self):
        for page in self._pages:
            page.save_config()

        save_rs232_configs(self._configs)
        save_product_dir(self._dir_edit.text())
        self.accept()

    def reject(self):
        self._configs = load_rs232_configs()
        super().reject()
