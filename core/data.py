import os
from dataclasses import dataclass, field
from typing import List

from config.settings import (
    RS232C_DAT, USERS_DAT, PATH_DAT, PRODUCT_DIR_DAT,
    CONFIG_DIR, GRID_MAX_NUMBER, MAX_MACHINE_NUMBER
)


@dataclass
class RS232Config:
    com_num: str = "1"
    baud_rate: str = "4800"
    parity: str = "N"
    data_length: str = "8"
    stop_bit: str = "2"
    get_data_com: str = "1"
    end_send_pc: str = "1"
    end_send_machine: str = "1"
    data_start_pos: str = "5"
    data_end_pos: str = "8"
    machine_name_show: str = "未設定"
    machine_name_excel: str = "M"
    handshake: str = "2"


@dataclass
class User:
    name: str = ""
    path: str = ""


def load_rs232_configs() -> List[RS232Config]:
    configs: List[RS232Config] = []
    if not os.path.exists(RS232C_DAT):
        for _ in range(10):
            configs.append(RS232Config())
        save_rs232_configs(configs)
        return configs

    try:
        with open(RS232C_DAT, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        for i in range(0, min(len(lines), 130), 13):
            cfg = RS232Config()
            cfg.com_num = lines[i] if i < len(lines) else "1"
            cfg.baud_rate = lines[i + 1] if i + 1 < len(lines) else "4800"
            cfg.parity = lines[i + 2] if i + 2 < len(lines) else "N"
            cfg.data_length = lines[i + 3] if i + 3 < len(lines) else "8"
            cfg.stop_bit = lines[i + 4] if i + 4 < len(lines) else "2"
            cfg.get_data_com = lines[i + 5] if i + 5 < len(lines) else "1"
            cfg.end_send_pc = lines[i + 6] if i + 6 < len(lines) else "1"
            cfg.end_send_machine = lines[i + 7] if i + 7 < len(lines) else "1"
            cfg.data_start_pos = lines[i + 8] if i + 8 < len(lines) else "5"
            cfg.data_end_pos = lines[i + 9] if i + 9 < len(lines) else "8"
            cfg.machine_name_show = lines[i + 10] if i + 10 < len(lines) else "未設定"
            cfg.machine_name_excel = lines[i + 11] if i + 11 < len(lines) else "M"
            cfg.handshake = lines[i + 12] if i + 12 < len(lines) else "2"
            configs.append(cfg)
    except Exception:
        for _ in range(10):
            configs.append(RS232Config())

    while len(configs) < 10:
        configs.append(RS232Config())

    return configs


def save_rs232_configs(configs: List[RS232Config]):
    os.makedirs(os.path.dirname(RS232C_DAT), exist_ok=True)
    with open(RS232C_DAT, "w", encoding="utf-8") as f:
        for cfg in configs:
            f.write(f"{cfg.com_num}\n")
            f.write(f"{cfg.baud_rate}\n")
            f.write(f"{cfg.parity}\n")
            f.write(f"{cfg.data_length}\n")
            f.write(f"{cfg.stop_bit}\n")
            f.write(f"{cfg.get_data_com}\n")
            f.write(f"{cfg.end_send_pc}\n")
            f.write(f"{cfg.end_send_machine}\n")
            f.write(f"{cfg.data_start_pos}\n")
            f.write(f"{cfg.data_end_pos}\n")
            f.write(f"{cfg.machine_name_show}\n")
            f.write(f"{cfg.machine_name_excel}\n")
            f.write(f"{cfg.handshake}\n")


def load_users() -> List[User]:
    users: List[User] = []
    names, paths = [], []

    if os.path.exists(USERS_DAT):
        with open(USERS_DAT, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f.readlines() if line.strip()]

    if os.path.exists(PATH_DAT):
        with open(PATH_DAT, "r", encoding="utf-8") as f:
            paths = [line.strip() for line in f.readlines() if line.strip()]

    max_len = max(len(names), len(paths))
    for i in range(max_len):
        name = names[i] if i < len(names) else ""
        path = paths[i] if i < len(paths) else ""
        if name:
            users.append(User(name=name, path=path))

    return users


def save_users(users: List[User]):
    os.makedirs(os.path.dirname(USERS_DAT), exist_ok=True)
    with open(USERS_DAT, "w", encoding="utf-8") as f:
        for u in users:
            f.write(f"{u.name}\n")
    with open(PATH_DAT, "w", encoding="utf-8") as f:
        for u in users:
            f.write(f"{u.path}\n")


def load_product_dir() -> str:
    if not os.path.exists(PRODUCT_DIR_DAT):
        default = "C:\\"
        os.makedirs(os.path.dirname(PRODUCT_DIR_DAT), exist_ok=True)
        with open(PRODUCT_DIR_DAT, "w", encoding="utf-8") as f:
            f.write(default + "\n")
        return default

    with open(PRODUCT_DIR_DAT, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                return line
    return "C:\\"


def save_product_dir(path: str):
    os.makedirs(os.path.dirname(PRODUCT_DIR_DAT), exist_ok=True)
    with open(PRODUCT_DIR_DAT, "w", encoding="utf-8") as f:
        f.write(f"{path}\n")


def load_machine_directories(user_dir: str) -> List[str]:
    dir_path = os.path.join(user_dir, "Directory.dat")
    directories: List[str] = [""] * (MAX_MACHINE_NUMBER + 1)

    if not os.path.exists(dir_path):
        with open(dir_path, "w", encoding="utf-8") as f:
            f.write("\n" * (MAX_MACHINE_NUMBER + 1))
        return directories

    with open(dir_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i <= MAX_MACHINE_NUMBER:
                directories[i] = line.strip()

    return directories


def save_machine_directories(user_dir: str, directories: List[str]):
    dir_path = os.path.join(user_dir, "Directory.dat")
    with open(dir_path, "w", encoding="utf-8") as f:
        for d in directories:
            f.write(f"{d}\n")


def get_product_name(path: str) -> str:
    if not path:
        return ""
    return os.path.basename(path)
