import os
from datetime import datetime
from typing import List, Optional

import xlrd
import xlwt
from xlrd import open_workbook as open_xls
from xlwt import Workbook as XlsWorkbook

from config.settings import GRID_MAX_NUMBER


class ExcelLogger:
    def __init__(self):
        self.workbooks: dict = {}
        self.sheets1: dict = {}
        self.sheets2: dict = {}
        self.file_paths: dict = {}

    def _get_file_path(self, product_path: str, user_name: str, product_name: str,
                       machine_number: int, date: Optional[datetime] = None) -> str:
        if date is None:
            date = datetime.now()
        data_dir = os.path.join(product_path, "data")
        os.makedirs(data_dir, exist_ok=True)
        fname = f"{user_name}_{product_name}_{machine_number}号機_{date.year}年{date.month}月{date.day}日.xls"
        return os.path.join(data_dir, fname)

    def load_or_create(self, product_path: str, user_name: str, product_name: str,
                       machine_number: int, spec_data: List[List],
                       date: Optional[datetime] = None) -> Optional[List[List]]:
        if date is None:
            date = datetime.now()

        file_path = self._get_file_path(product_path, user_name, product_name, machine_number, date)
        self.file_paths[machine_number] = file_path

        if not os.path.exists(file_path):
            self.workbooks[machine_number] = None
            self.sheets1[machine_number] = None
            self.sheets2[machine_number] = None
            return []

        try:
            wb = open_xls(file_path)
            self.workbooks[machine_number] = wb
            self.sheets1[machine_number] = wb.sheet_by_index(0)
            if wb.nsheets > 1:
                self.sheets2[machine_number] = wb.sheet_by_index(1)
            else:
                self.sheets2[machine_number] = None
            return self._read_grid_data(machine_number)
        except Exception:
            return None

    def _create_new(self, file_path: str, machine_number: int,
                    spec_data: List[List], date: datetime) -> Optional[List[List]]:
        try:
            wb = XlsWorkbook()
            sheet1 = wb.add_sheet("Sheet1")
            sheet2 = wb.add_sheet("Sheet2")

            for row_idx, spec_row in enumerate(spec_data, 1):
                if row_idx > GRID_MAX_NUMBER:
                    break
                sheet1.write(row_idx - 1, 0, spec_row[0] if len(spec_row) > 0 else "")
                sheet1.write(row_idx - 1, 1, spec_row[1] if len(spec_row) > 1 else "")
                sheet1.write(row_idx - 1, 2, spec_row[2] if len(spec_row) > 2 else "")
                sheet2.write(row_idx - 1, 0, spec_row[3] if len(spec_row) > 3 else "")

            wb.save(file_path)

            wb2 = open_xls(file_path)
            self.workbooks[machine_number] = wb2
            self.sheets1[machine_number] = wb2.sheet_by_index(0)
            self.sheets2[machine_number] = wb2.sheet_by_index(1)
            self.file_paths[machine_number] = file_path

            return self._read_grid_data(machine_number)
        except Exception:
            return None

    def _read_grid_data(self, machine_number: int) -> List[List]:
        data = []
        sheet1 = self.sheets1.get(machine_number)
        sheet2 = self.sheets2.get(machine_number)

        if not sheet1:
            return data

        for row in range(GRID_MAX_NUMBER):
            measured = sheet1.cell_value(row, 4) if row < sheet1.nrows and sheet1.ncols > 4 else ""
            check = sheet1.cell_value(row, 5) if row < sheet1.nrows and sheet1.ncols > 5 else ""
            remark = sheet2.cell_value(row, 1) if sheet2 and row < sheet2.nrows and sheet2.ncols > 1 else ""
            row_data = [measured, check, "", remark]
            data.append(row_data)

        return data

    def save_row(self, machine_number: int, row: int, micro_name: str,
                 measured_value: str, check_result: str, remark: str = "",
                 spec_data: Optional[List[List]] = None):
        wb = self.workbooks.get(machine_number)
        sheet1 = self.sheets1.get(machine_number)
        sheet2 = self.sheets2.get(machine_number)

        if not wb or not sheet1:
            if spec_data:
                self._create_new(self.file_paths.get(machine_number), machine_number, spec_data, datetime.now())
                wb = self.workbooks.get(machine_number)
                sheet1 = self.sheets1.get(machine_number)
                sheet2 = self.sheets2.get(machine_number)
            else:
                return

        new_wb = XlsWorkbook()
        new_sheet1 = new_wb.add_sheet("Sheet1")
        new_sheet2 = new_wb.add_sheet("Sheet2")

        excel_row = row - 1

        max_rows = max(sheet1.nrows, excel_row + 1, 1)
        max_cols1 = max(sheet1.ncols, 6, 1)
        max_cols2 = max(sheet2.ncols, 2, 1) if sheet2 else 0

        for r in range(max_rows):
            for c in range(max_cols1):
                if r == excel_row and c == 3:
                    new_sheet1.write(r, c, micro_name)
                elif r == excel_row and c == 4:
                    if measured_value is not None and measured_value != "":
                        try:
                            new_sheet1.write(r, c, float(measured_value))
                        except ValueError:
                            new_sheet1.write(r, c, measured_value)
                    else:
                        new_sheet1.write(r, c, "")
                elif r == excel_row and c == 5:
                    new_sheet1.write(r, c, check_result)
                else:
                    val = sheet1.cell_value(r, c) if r < sheet1.nrows and c < sheet1.ncols else ""
                    new_sheet1.write(r, c, val)

        if sheet2:
            for r in range(max(sheet2.nrows, excel_row + 1, 1)):
                for c in range(max_cols2):
                    if r == excel_row and c == 1:
                        if remark is not None and remark != "":
                            try:
                                new_sheet2.write(r, c, float(remark))
                            except ValueError:
                                new_sheet2.write(r, c, remark)
                        else:
                            new_sheet2.write(r, c, "")
                    else:
                        val = sheet2.cell_value(r, c) if r < sheet2.nrows and c < sheet2.ncols else ""
                        new_sheet2.write(r, c, val)
        else:
            for r in range(max(excel_row + 1, 1)):
                new_sheet2.write(r, 0, "")

        file_path = self._get_save_path(machine_number)
        if file_path:
            new_wb.save(file_path)

            wb2 = open_xls(file_path)
            self.workbooks[machine_number] = wb2
            self.sheets1[machine_number] = wb2.sheet_by_index(0)
            self.sheets2[machine_number] = wb2.sheet_by_index(1) if wb2.nsheets > 1 else None

    def _get_save_path(self, machine_number: int) -> Optional[str]:
        return self.file_paths.get(machine_number)

    def load_spec_data(self, product_path: str) -> List[List]:
        spec_file = os.path.join(product_path, "data.xls")
        if not os.path.exists(spec_file):
            return []

        try:
            wb = open_xls(spec_file)
            sheet = wb.sheet_by_index(0)
            spec_data = []
            for row_idx in range(min(sheet.nrows, GRID_MAX_NUMBER)):
                row_data = []
                for col_idx in range(4):
                    value = sheet.cell_value(row_idx, col_idx) if col_idx < sheet.ncols else ""
                    row_data.append(value)
                spec_data.append(row_data)
            return spec_data
        except Exception:
            return []

    def close_all(self):
        self.workbooks.clear()
        self.sheets1.clear()
        self.sheets2.clear()
        self.file_paths.clear()
