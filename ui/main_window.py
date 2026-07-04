from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QCheckBox, QFrame, QGroupBox, QFileDialog, QStackedWidget,
    QMessageBox, QDateEdit, QSplitter, QHeaderView, QInputDialog,
    QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QDate, Signal, Slot
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QPixmap
import math
from datetime import datetime
from typing import List, Optional

from config.settings import GRID_MAX_NUMBER, MAX_MACHINE_NUMBER
from core.data import (
    load_product_dir, load_machine_directories, save_machine_directories,
    get_product_name
)
from core.data import RS232Config, load_rs232_configs
from core.serial_comm import SerialCommunicator, END_SEND_MAP
from core.excel_logger import ExcelLogger
from ui.drawing_viewer import DrawingViewer


def _format_value(value):
    if value is None or value == "":
        return ""
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


KEY_MACHINE_MAP = {
    "q": 0, "w": 1, "e": 2, "r": 3, "t": 4, "y": 5, "u": 6, "i": 7, "o": 8, "p": 9,
    "@": 10, "[": 11,
    "a": 12, "s": 13, "d": 14, "f": 15, "g": 16, "h": 17, "j": 18, "k": 19, "l": 20,
    ";": 21, ":": 22, "]": 23,
    "Q": 24, "W": 25, "E": 26, "R": 27, "T": 28, "Y": 29, "U": 30, "I": 31, "O": 32, "P": 33,
    "`": 34, "{": 35,
    "A": 36, "S": 37, "D": 38, "F": 39, "G": 40, "H": 41, "J": 42, "K": 43, "L": 44,
    "+": 45, "*": 46, "}": 47,
}


class MachineFrame(QWidget):
    row_changed = Signal(int)

    def __init__(self, machine_number: int):
        super().__init__()
        self.machine_number = machine_number
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(GRID_MAX_NUMBER, 8)
        self.table.setFont(QFont("MS UI Gothic", 25))
        self.table.setHorizontalHeaderLabels([
            "番号", "測定値", "判定", "寸法", "上限", "下限", "狙い", "補正"
        ])
        header = self.table.horizontalHeader()
        header.setFont(QFont("MS UI Gothic", 25))
        header.setFixedHeight(50)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 75)
        for i in range(1, 8):
            self.table.setColumnWidth(i, 192)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(50)

        for row in range(GRID_MAX_NUMBER):
            item = QTableWidgetItem(str(row + 1))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item)
            for col in range(1, 8):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.table.cellClicked.connect(self._on_cell_clicked)

    def _on_cell_clicked(self, row: int, col: int):
        if row > 0:
            self.row_changed.emit(row)

    def get_row_data(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        return item.text() if item else ""

    def set_row_data(self, row: int, col: int, value: str):
        item = self.table.item(row, col)
        if item:
            item.setText(value)
        else:
            new_item = QTableWidgetItem(value)
            new_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, col, new_item)

    def find_next_empty_row(self) -> int:
        for row in range(GRID_MAX_NUMBER):
            item = self.table.item(row, 1)
            if not item or not item.text():
                return row
        return 0

    def clear(self):
        for row in range(GRID_MAX_NUMBER):
            for col in range(1, 8):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)


class VerticalButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)


class MainWindow(QMainWindow):
    def __init__(self, user_name: str, user_dir: str, product_dir: str):
        super().__init__()
        self.user_name = user_name
        self.user_dir = user_dir
        self.product_dir = product_dir
        self.machine_number = 0
        self.micro_number = 1
        self.started = False
        self.comm_flag = False

        self._configs: List[RS232Config] = load_rs232_configs()
        self._directories: List[str] = load_machine_directories(user_dir)
        self._product_names: List[str] = [""] * (MAX_MACHINE_NUMBER + 1)
        self._frames: List[MachineFrame] = []
        self._excel_logger = ExcelLogger()
        self._serial = SerialCommunicator()
        self._current_date = datetime.now()
        self._spec_data: List[List] = [[]] * (MAX_MACHINE_NUMBER + 1)

        self._setup_ui()
        self._setup_shortcuts()
        self._load_data()
        self._update_button_states()
        self._show_drawing_if_exists()

    def _setup_ui(self):
        self.setWindowTitle("DRS")
        self.resize(1546, 788)
        self.setMinimumSize(1546, 788)
        self.setFont(QFont("MS UI Gothic", 21))

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        top_layout = self._create_top_layout()
        main_layout.addLayout(top_layout)

        middle_layout = self._create_middle_layout()
        main_layout.addLayout(middle_layout, 1)

        bottom_layout = self._create_bottom_layout()
        main_layout.addLayout(bottom_layout)

        self._current_row = 0

    def _create_top_layout(self):
        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)

        self._micro_label = QLineEdit()
        self._micro_label.setReadOnly(True)
        self._micro_label.setFixedWidth(235)
        if self._configs:
            self._micro_label.setText(self._configs[0].machine_name_show)

        self._machine_label = QLineEdit()
        self._machine_label.setReadOnly(True)
        self._machine_label.setFixedWidth(100)
        self._machine_label.setText(f"{self.machine_number}号機")

        self._product_label = QLineEdit()
        self._product_label.setReadOnly(True)
        self._product_label.setFixedWidth(525)
        self._product_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._product_select_btn = QPushButton("選択")
        self._product_select_btn.clicked.connect(self._on_register_product)
        self._product_select_btn.setFixedWidth(60)

        self._date_display = QLineEdit()
        self._date_display.setReadOnly(True)
        self._date_display.setFixedWidth(150)
        self._date_display.setText(self._current_date.strftime("%Y/%m/%d"))

        self._date_select_btn = QPushButton("選択")
        self._date_select_btn.clicked.connect(self._on_change_date)
        self._date_select_btn.setFixedWidth(60)

        self._date_picker = QDateEdit()
        self._date_picker.setDate(QDate.currentDate())
        self._date_picker.setCalendarPopup(True)
        self._date_picker.dateChanged.connect(self._on_date_changed)
        self._date_picker.setFixedWidth(150)
        self._date_picker.setVisible(False)

        top_layout.addWidget(QLabel("測定器"))
        top_layout.addWidget(self._micro_label)
        top_layout.addWidget(QLabel("機械番号"))
        top_layout.addWidget(self._machine_label)
        top_layout.addWidget(QLabel("製品名"))
        top_layout.addWidget(self._product_label)
        top_layout.addWidget(self._product_select_btn)
        top_layout.addWidget(QLabel("日付"))
        top_layout.addWidget(self._date_display)
        top_layout.addWidget(self._date_select_btn)
        top_layout.addWidget(self._date_picker)
        top_layout.addStretch()

        return top_layout

    def _create_middle_layout(self):
        middle_layout = QHBoxLayout()

        grid_group = QGroupBox("測定値リスト")
        grid_layout = QVBoxLayout(grid_group)
        grid_layout.setContentsMargins(5, 5, 5, 5)

        self._stacked = QStackedWidget()
        for i in range(MAX_MACHINE_NUMBER + 1):
            frame = MachineFrame(i)
            frame.row_changed.connect(lambda r, mn=i: self._on_table_row_clicked(r, mn))
            self._stacked.addWidget(frame)
            self._frames.append(frame)

        grid_layout.addWidget(self._stacked)
        self._stacked.setCurrentIndex(0)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 31, 0, 0)
        self._start_btn = QPushButton("開始")
        self._start_btn.clicked.connect(self._on_start)
        self._start_btn.setFixedHeight(100)
        self._start_btn.setFont(QFont("MS UI Gothic", 21))
        right_layout.addWidget(self._start_btn)

        self._status_label = QLabel("測定")
        self._status_label.setFont(QFont("MS UI Gothic", 21))
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setFixedHeight(100)
        right_layout.addWidget(self._status_label)

        right_layout.addStretch()
        middle_layout.addWidget(grid_group, 1)
        middle_layout.addLayout(right_layout)

        return middle_layout

    def _create_bottom_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(5)

        self._input_group = QGroupBox("入力先番号")
        input_layout = QHBoxLayout(self._input_group)
        input_layout.setContentsMargins(5, 5, 5, 5)

        self._row_edit = QLineEdit("1")
        self._row_edit.setFixedWidth(60)
        self._row_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._row_edit.returnPressed.connect(self._on_row_search)

        self._auto_row_cb = QCheckBox("自動")
        self._auto_row_cb.setChecked(True)

        self._row_search_btn = QPushButton("検索")
        self._row_search_btn.clicked.connect(self._on_row_search)
        self._row_search_btn.setFixedWidth(60)

        input_layout.addWidget(self._row_edit)
        input_layout.addWidget(self._auto_row_cb)
        input_layout.addWidget(self._row_search_btn)

        self._num_input_group = QGroupBox("手動数値入力")
        num_input_layout = QHBoxLayout(self._num_input_group)
        num_input_layout.setContentsMargins(5, 5, 5, 5)
        self._num_input_edit = QLineEdit()

        self._num_input_edit.setFixedWidth(240)
        self._num_input_edit.returnPressed.connect(self._on_input_measured)

        self._num_clear_cb = QCheckBox("削除")
        self._num_clear_cb.setChecked(True)

        self._num_input_btn = QPushButton("入力")
        self._num_input_btn.clicked.connect(self._on_input_measured)
        self._num_input_btn.setFixedWidth(60)

        num_input_layout.addWidget(self._num_input_edit)
        num_input_layout.addWidget(self._num_clear_cb)
        num_input_layout.addWidget(self._num_input_btn)

        self._text_input_group = QGroupBox("手動文字入力")
        text_input_layout = QHBoxLayout(self._text_input_group)
        text_input_layout.setContentsMargins(5, 5, 5, 5)
        self._text_input_edit = QLineEdit()

        self._text_input_edit.setFixedWidth(240)
        self._text_input_edit.returnPressed.connect(self._on_input_text)

        self._text_clear_cb = QCheckBox("削除")
        self._text_clear_cb.setChecked(True)

        self._text_input_btn = QPushButton("入力")
        self._text_input_btn.clicked.connect(self._on_input_text)
        self._text_input_btn.setFixedWidth(60)

        text_input_layout.addWidget(self._text_input_edit)
        text_input_layout.addWidget(self._text_clear_cb)
        text_input_layout.addWidget(self._text_input_btn)

        bottom_layout.addWidget(self._input_group)
        bottom_layout.addWidget(self._num_input_group)
        bottom_layout.addWidget(self._text_input_group)

        return bottom_layout

    def _setup_shortcuts(self):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            key = event.key()
            text = event.text() if event.text() else ""

            if key == Qt.Key.Key_Space:
                self._on_space()
                return True
            elif key == Qt.Key.Key_Escape:
                self._on_escape()
                return True
            elif key == Qt.Key.Key_F1:
                self._change_micro(1)
                return True
            elif key == Qt.Key.Key_F2:
                self._change_micro(2)
                return True
            elif key == Qt.Key.Key_F3:
                self._change_micro(3)
                return True
            elif key == Qt.Key.Key_F4:
                self._change_micro(4)
                return True
            elif key == Qt.Key.Key_F5:
                self._change_micro(5)
                return True
            elif key == Qt.Key.Key_F6:
                self._change_micro(6)
                return True
            elif key == Qt.Key.Key_F7:
                self._change_micro(7)
                return True
            elif key == Qt.Key.Key_F8:
                self._change_micro(8)
                return True
            elif key == Qt.Key.Key_F9:
                self._change_micro(9)
                return True
            elif key == Qt.Key.Key_F10:
                self._change_micro(10)
                return True
            elif key == Qt.Key.Key_F11:
                self._on_f11_ng()
                return True
            elif key == Qt.Key.Key_F12:
                self._on_f12_ok()
                return True

            focused = self.focusWidget()
            if focused is not None and not isinstance(focused, QLineEdit):
                if text in KEY_MACHINE_MAP:
                    self._change_machine(KEY_MACHINE_MAP[text])
                    return True

        return super().eventFilter(obj, event)

    def _update_button_states(self):
        if self.started:
            self._start_btn.setEnabled(False)
            self._product_select_btn.setEnabled(False)
            self._date_select_btn.setEnabled(False)
            self._micro_label.setEnabled(False)
            self._machine_label.setEnabled(False)
            self._product_label.setEnabled(False)
            self._date_display.setEnabled(False)
            self._row_edit.setEnabled(False)
            self._auto_row_cb.setEnabled(False)
            self._row_search_btn.setEnabled(False)
            self._num_input_edit.setEnabled(False)
            self._num_clear_cb.setEnabled(False)
            self._num_input_btn.setEnabled(False)
            self._text_input_edit.setEnabled(False)
            self._text_clear_cb.setEnabled(False)
            self._text_input_btn.setEnabled(False)
            self._status_label.setText("測定")
        else:
            self._start_btn.setEnabled(True)
            self._product_select_btn.setEnabled(True)
            self._date_select_btn.setEnabled(True)
            self._micro_label.setEnabled(True)
            self._machine_label.setEnabled(True)
            self._product_label.setEnabled(True)
            self._date_display.setEnabled(True)
            self._row_edit.setEnabled(True)
            self._auto_row_cb.setEnabled(True)
            self._row_search_btn.setEnabled(True)
            self._num_input_edit.setEnabled(True)
            self._num_clear_cb.setEnabled(True)
            self._num_input_btn.setEnabled(True)
            self._text_input_edit.setEnabled(True)
            self._text_clear_cb.setEnabled(True)
            self._text_input_btn.setEnabled(True)
            self._status_label.setText("")

    def _load_data(self):
        for i in range(MAX_MACHINE_NUMBER + 1):
            if self._directories[i]:
                self._product_names[i] = get_product_name(self._directories[i])
                self._load_excel(i)

        self._update_machine_display()

    def _load_excel(self, machine_number: int):
        if not self._directories[machine_number]:
            return

        product_path = self._directories[machine_number]
        product_name = self._product_names[machine_number]
        spec_data = self._excel_logger.load_spec_data(product_path)
        self._spec_data[machine_number] = spec_data

        grid_data = self._excel_logger.load_or_create(
            product_path, self.user_name, product_name, machine_number, spec_data, self._current_date
        )

        frame = self._frames[machine_number]

        # Load spec data from data.xls
        for row_idx, spec_row in enumerate(spec_data):
            if row_idx >= GRID_MAX_NUMBER:
                break
            if len(spec_row) >= 1:
                frame.set_row_data(row_idx, 3, _format_value(spec_row[0]))
            if len(spec_row) >= 2:
                frame.set_row_data(row_idx, 4, _format_value(spec_row[1]))
            if len(spec_row) >= 3:
                frame.set_row_data(row_idx, 5, _format_value(spec_row[2]))
            if len(spec_row) >= 4:
                frame.set_row_data(row_idx, 6, _format_value(spec_row[3]))

        # Load measurement data from existing Excel file
        if grid_data:
            for row_idx, row_vals in enumerate(grid_data):
                if row_idx >= GRID_MAX_NUMBER:
                    break
                if len(row_vals) >= 1:
                    frame.set_row_data(row_idx, 1, _format_value(row_vals[0]))
                if len(row_vals) >= 2:
                    frame.set_row_data(row_idx, 2, _format_value(row_vals[1]))
                if len(row_vals) >= 4:
                    frame.set_row_data(row_idx, 7, _format_value(row_vals[3]))

    def _update_machine_display(self):
        self._machine_label.setText(f"{self.machine_number}号機")
        self._product_label.setText(self._product_names[self.machine_number])
        self._stacked.setCurrentIndex(self.machine_number)
        self._row_edit.setText(str(self._current_row + 1))

    def _change_machine(self, number: int):
        if self.comm_flag:
            return
        self.machine_number = number
        self._update_machine_display()
        self._show_drawing_if_exists()
        if self._auto_row_cb.isChecked():
            frame = self._frames[self.machine_number]
            self._current_row = frame.find_next_empty_row()
            self._row_edit.setText(str(self._current_row + 1))

    def _change_micro(self, number: int):
        self.micro_number = number
        cfg = self._configs[number - 1]
        self._serial.configure(cfg)
        self._micro_label.setText(cfg.machine_name_show)

    def _on_table_row_clicked(self, row: int, machine_number: int):
        if machine_number == self.machine_number:
            self._current_row = row
            self._row_edit.setText(str(row + 1))

    def _on_start(self):
        self.started = True
        self._update_button_states()

    def _on_escape(self):
        if self.started:
            self.started = False
            self._update_button_states()

    def _on_space(self):
        if self.comm_flag or not self.started:
            return

        if not self._directories[self.machine_number]:
            return

        cfg = self._configs[self.micro_number - 1]
        ending = END_SEND_MAP.get(cfg.end_send_pc, "\r")
        command = cfg.get_data_com + ending

        self.comm_flag = True
        self._status_label.setText("通信中")

        if not self._serial.open_port():
            self.comm_flag = False
            self._status_label.setText("エラー")
            QMessageBox.critical(self, "DRS - エラー",
                                  "ポートを開けません。COMポートの設定を確認してください。")
            return

        try:
            result = self._serial.send_and_receive(cfg.get_data_com, timeout_ms=2000)
            if result is not None:
                self._write_data(result)
            else:
                self.comm_flag = False
                self._status_label.setText("タイムアウト")
                QMessageBox.critical(self, "DRS - エラー", "通信タイムアウトしました。")
        finally:
            self._serial.close_port()

    def _write_data(self, data: str):
        cfg = self._configs[self.micro_number - 1]
        micro_name = cfg.machine_name_excel
        frame = self._frames[self.machine_number]
        row = self._current_row

        measured = abs(float(data)) if data.strip() else 0
        frame.set_row_data(row, 1, _format_value(measured))
        self._check_value(row)
        self._calculate_deviation(row)
        self._save_excel(row, micro_name)

        self.comm_flag = False
        self._status_label.setText("測定")

        self._move_to_next_row()

    def _check_value(self, row: int):
        frame = self._frames[self.machine_number]
        upper = frame.get_row_data(row, 4)
        lower = frame.get_row_data(row, 5)
        nominal = frame.get_row_data(row, 6)
        measured = frame.get_row_data(row, 1)

        if not upper or not lower or not nominal or not measured:
            frame.set_row_data(row, 2, "")
            return

        try:
            upper_val = float(upper)
            lower_val = float(lower)
            measured_val = float(measured)
            nominal_val = float(nominal)

            if measured_val <= (nominal_val + upper_val) and measured_val >= (nominal_val + lower_val):
                frame.set_row_data(row, 2, "合")
            else:
                frame.set_row_data(row, 2, "不")
                self._log_ng(row)
        except ValueError:
            frame.set_row_data(row, 2, "")

    def _calculate_deviation(self, row: int):
        frame = self._frames[self.machine_number]
        target = frame.get_row_data(row, 6)
        measured = frame.get_row_data(row, 1)

        if not target or not measured:
            return

        try:
            deviation = (float(target) - float(measured)) * 1000 + 0.5
            deviation = math.floor(deviation) / 1000
            frame.set_row_data(row, 7, str(deviation))
        except ValueError:
            pass

    def _save_excel(self, row: int, micro_name: str):
        if not self._directories[self.machine_number]:
            return

        frame = self._frames[self.machine_number]
        product_path = self._directories[self.machine_number]
        product_name = self._product_names[self.machine_number]
        measured = frame.get_row_data(row, 1)
        check = frame.get_row_data(row, 2)
        remark = frame.get_row_data(row, 7)

        self._excel_logger.save_row(
            self.machine_number, row + 1, micro_name, measured, check, remark,
            self._spec_data[self.machine_number]
        )

    def _log_ng(self, row: int):
        frame = self._frames[self.machine_number]
        upper = frame.get_row_data(row, 4)
        lower = frame.get_row_data(row, 5)
        nominal = frame.get_row_data(row, 6)
        measured = frame.get_row_data(row, 1)

        ng_text = (
            f"{self._current_date.year}年{self._current_date.month}月{self._current_date.day}日_"
            f"{self.user_name}_{self.machine_number}機_"
            f"{self._product_names[self.machine_number]}_"
            f"上限{upper}下限{lower}公称{nominal}測定値{measured}"
        )

        ng_dir = f"{self.product_dir}\\測定不良\\不良リスト"
        import os
        os.makedirs(ng_dir, exist_ok=True)

        with open(f"{ng_dir}\\{ng_text}.txt", "w", encoding="utf-8") as f:
            f.write(ng_text.replace("_", "\n"))

    def _move_to_next_row(self):
        if not self._auto_row_cb.isChecked():
            return
        frame = self._frames[self.machine_number]
        next_row = frame.find_next_empty_row()
        self._current_row = next_row
        self._row_edit.setText(str(next_row + 1))
        frame.table.scrollToItem(frame.table.item(next_row, 0))

    def _on_row_search(self):
        frame = self._frames[self.machine_number]
        next_row = frame.find_next_empty_row()
        self._current_row = next_row
        self._row_edit.setText(str(next_row + 1))
        frame.table.scrollToItem(frame.table.item(next_row, 0))
        frame.table.selectRow(next_row)
        frame.table.setFocus()

    def _on_cancel_product(self):
        if not self._directories[self.machine_number]:
            return

        self._directories[self.machine_number] = ""
        self._product_names[self.machine_number] = ""
        self._product_label.setText("")
        save_machine_directories(self.user_dir, self._directories)
        self._frames[self.machine_number].clear()

    def _on_input_measured(self):
        if not self._directories[self.machine_number]:
            return

        text = self._num_input_edit.text().strip()
        if not text:
            return

        frame = self._frames[self.machine_number]
        row = self._current_row

        try:
            value = abs(float(text))
            frame.set_row_data(row, 1, _format_value(value))
            self._check_value(row)
            self._calculate_deviation(row)
            self._save_excel(row, "")

            if self._num_clear_cb.isChecked():
                self._num_input_edit.clear()

            self._move_to_next_row()
            self._num_input_edit.setFocus()
        except ValueError:
            QMessageBox.warning(self, "DRS - エラー", "数値を入力してください。")

    def _on_input_text(self):
        if not self._directories[self.machine_number]:
            return

        text = self._text_input_edit.text().strip()
        if not text:
            return

        frame = self._frames[self.machine_number]
        row = self._current_row

        frame.set_row_data(row, 1, text)
        frame.set_row_data(row, 2, "")
        baseline = frame.get_row_data(row, 6)
        if baseline:
            frame.set_row_data(row, 7, "")

        self._save_excel(row, "")

        if self._text_clear_cb.isChecked():
            self._text_input_edit.clear()

        self._move_to_next_row()
        self._text_input_edit.setFocus()

    def _on_change_date(self):
        self._date_display.setVisible(False)
        self._date_select_btn.setVisible(False)
        self._date_picker.setVisible(True)
        self._date_picker.setFocus()
        self._date_picker.setDate(QDate(self._current_date.year, self._current_date.month, self._current_date.day))

    def _on_date_changed(self, date: QDate):
        self._current_date = datetime(date.year(), date.month(), date.day())
        self._date_display.setText(self._current_date.strftime("%Y/%m/%d"))
        self._date_display.setVisible(True)
        self._date_select_btn.setVisible(True)
        self._date_picker.setVisible(False)
        for i in range(MAX_MACHINE_NUMBER + 1):
            if self._directories[i]:
                self._frames[i].clear()
                self._load_excel(i)
                self._frames[i].table.setCurrentCell(0, 0)
                self._frames[i].table.scrollTo(self._frames[i].table.currentIndex())
        self.machine_number = 0
        self._update_machine_display()
        frame = self._frames[self.machine_number]
        self._current_row = frame.find_next_empty_row()
        self._row_edit.setText(str(self._current_row + 1))

    def _on_register_product(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "製品ディレクトリを選択", self.product_dir
        )
        if not dir_path:
            self._directories[self.machine_number] = ""
            self._product_names[self.machine_number] = ""
            self._product_label.setText("")
            save_machine_directories(self.user_dir, self._directories)
            self._frames[self.machine_number].clear()
            return

        self._directories[self.machine_number] = dir_path
        self._product_names[self.machine_number] = get_product_name(dir_path)
        self._product_label.setText(self._product_names[self.machine_number])
        save_machine_directories(self.user_dir, self._directories)
        self._load_excel(self.machine_number)
        self._show_drawing_if_exists()

    def _on_f11_ng(self):
        if self.comm_flag or not self._directories[self.machine_number]:
            return

        frame = self._frames[self.machine_number]
        row = self._current_row
        frame.set_row_data(row, 1, "NG")
        frame.set_row_data(row, 2, "不")
        self._save_excel(row, "")
        self._move_to_next_row()

    def _on_f12_ok(self):
        if self.comm_flag or not self._directories[self.machine_number]:
            return

        frame = self._frames[self.machine_number]
        row = self._current_row
        frame.set_row_data(row, 1, "OK")
        frame.set_row_data(row, 2, "合")
        self._save_excel(row, "")
        self._move_to_next_row()

    def _show_drawing_if_exists(self):
        import os
        if not hasattr(self, '_drawing_viewer') or self._drawing_viewer is None:
            self._drawing_viewer = DrawingViewer()
            self._drawing_viewer.show()
        product_name = self._product_names[self.machine_number]
        product_dir = self._directories[self.machine_number]
        if not product_name or not product_dir:
            self._drawing_viewer.clear_image()
            return
        image_path = os.path.join(product_dir, f"{product_name}.jpg")
        if not os.path.exists(image_path):
            self._drawing_viewer.clear_image()
            return
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self._drawing_viewer.clear_image()
            return
        self._drawing_viewer.set_pixmap(pixmap)

    def closeEvent(self, event):
        if self.started:
            event.ignore()
            return
        if hasattr(self, '_drawing_viewer') and self._drawing_viewer is not None:
            self._drawing_viewer.close()
        self._excel_logger.close_all()
        self._serial.close_port()
        event.accept()
