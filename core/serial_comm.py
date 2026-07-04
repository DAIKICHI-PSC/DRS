import serial
import serial.tools.list_ports
from typing import Optional, Callable

from core.data import RS232Config


HANDSHAKE_MAP = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
}

PARITY_MAP = {
    "E": serial.PARITY_EVEN,
    "M": serial.PARITY_MARK,
    "N": serial.PARITY_NONE,
    "O": serial.PARITY_ODD,
    "S": serial.PARITY_SPACE,
}

STOPBIT_MAP = {
    "1": serial.STOPBITS_ONE,
    "1.5": serial.STOPBITS_ONE_POINT_FIVE,
    "2": serial.STOPBITS_TWO,
}

END_SEND_MAP = {
    "1": "\r",
    "2": "\n",
    "3": "\r\n",
}


class SerialCommunicator:
    def __init__(self):
        self.port: Optional[serial.Serial] = None
        self.config: Optional[RS232Config] = None
        self.buffer = ""
        self.callback: Optional[Callable[[str], None]] = None
        self.timeout_callback: Optional[Callable[[], None]] = None
        self._timer_id = None

    def get_available_ports(self) -> list:
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]

    def configure(self, config: RS232Config):
        self.config = config

    def open_port(self) -> bool:
        if not self.config:
            return False

        try:
            if self.port and self.port.is_open:
                self.port.close()

            self.port = serial.Serial(
                port=f"COM{self.config.com_num}",
                baudrate=int(self.config.baud_rate),
                parity=PARITY_MAP.get(self.config.parity, serial.PARITY_NONE),
                bytesize=int(self.config.data_length),
                stopbits=STOPBIT_MAP.get(self.config.stop_bit, serial.STOPBITS_ONE),
                timeout=0,
                write_timeout=1,
                rtscts=(self.config.handshake == "2"),
                dsrdtr=(self.config.handshake == "3"),
                xonxoff=(self.config.handshake == "1"),
            )
            self.port.handshake = HANDSHAKE_MAP.get(self.config.handshake, 0)
            self.buffer = ""
            return True
        except Exception:
            return False

    def close_port(self):
        if self.port and self.port.is_open:
            try:
                self.port.close()
            except Exception:
                pass

    def send_command(self, command: str) -> bool:
        if not self.port or not self.port.is_open:
            return False

        try:
            ending = END_SEND_MAP.get(self.config.end_send_pc, "\r")
            self.port.write((command + ending).encode("shift_jis", errors="replace"))
            self.port.flush()
            return True
        except Exception:
            return False

    def read_response(self) -> Optional[str]:
        if not self.port or not self.port.is_open:
            return None

        try:
            ending = END_SEND_MAP.get(self.config.end_send_machine, "\r")
            while True:
                data = self.port.read_all().decode("shift_jis", errors="replace")
                if not data:
                    return None
                self.buffer += data
                if ending in self.buffer:
                    break

            start = int(self.config.data_start_pos) - 1
            end = start + int(self.config.data_end_pos)
            result = self.buffer[start:end]
            self.buffer = ""
            return result
        except Exception:
            self.buffer = ""
            return None

    def send_and_receive(self, command: str, timeout_ms: int = 2000) -> Optional[str]:
        if not self.send_command(command):
            return None

        import time
        start_time = time.time()
        ending = END_SEND_MAP.get(self.config.end_send_machine, "\r")

        while time.time() - start_time < timeout_ms / 1000:
            data = self.port.read_all().decode("shift_jis", errors="replace")
            if data:
                self.buffer += data
                if ending in self.buffer:
                    start = int(self.config.data_start_pos) - 1
                    end = start + int(self.config.data_end_pos)
                    result = self.buffer[start:end]
                    raw_buffer = self.buffer
                    self.buffer = ""
                    self._raw_buffer = raw_buffer
                    return result
            time.sleep(0.01)

        self.buffer = ""
        return None
