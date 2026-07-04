import os

SAVE_PATH = os.path.join(os.path.expanduser("~"), "AppData", "Local", "DRS")
CONFIG_DIR = os.path.join(SAVE_PATH, "Config")

USERS_DAT = os.path.join(CONFIG_DIR, "Users.dat")
PATH_DAT = os.path.join(CONFIG_DIR, "Path.dat")
RS232C_DAT = os.path.join(CONFIG_DIR, "RS232C.dat")
PRODUCT_DIR_DAT = os.path.join(CONFIG_DIR, "ProductDir.dat")
CONFIG_DAT = os.path.join(CONFIG_DIR, "Config.dat")
CONFIG_SUB_DAT = os.path.join(CONFIG_DIR, "ConfigSub.dat")
VERSION_DAT = os.path.join(CONFIG_DIR, "Version.dat")
DRAW_POS_DAT = os.path.join(CONFIG_DIR, "DrawPos.dat")
DRAW_POS_MAIN_DAT = os.path.join(CONFIG_DIR, "DrawPosMain.dat")

MAX_MACHINE_NUMBER = 47
GRID_MAX_NUMBER = 300

CUSTOMER_NAME = "サンプル顧客"
VERSION = "2.5"
