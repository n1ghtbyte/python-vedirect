import enum
import json

import serial


class VEDirectException(Exception):
    pass


class InvalidChecksumException(VEDirectException):
    pass


class MPPTState(enum.Enum):
    Off = 0
    Limited = 1
    Active = 2


def mA(val: str) -> float:
    """Converts mA (milliamps) to Amps."""
    return float(val) / 1000


def mV(val: str) -> float:
    """Converts mV (millivolts) to Volts."""
    return float(val) / 1000


class VEDirect:
    def __init__(self, device: str = "/dev/ttyUSB0", speed: int = 19200):
        self.device = device
        self.speed = speed
        self._data = {}

        self.refresh()

    def refresh(self):
        frames = self._get_data()
        self.parse_pdu(frames)

    def parse_pdu(self, frames):
        for frame in frames:
            if frame.startswith(b"Checksum"):
                # This entry is useless
                continue
            key, value = frame.strip().decode("utf-8").split("\t")
            self._data[key] = value

    def _get_data(self) -> list[bytes]:
        """Returns a PDU array, one entry per line."""
        data = []
        with serial.Serial(self.device, self.speed, timeout=4) as s:
            # Wait for start of frame
            while True:
                frame = s.readline()
                if frame.startswith(b"PID"):
                    break

            # Slurp all frames
            frame = b""
            while not frame.startswith(b"PID"):
                frame = s.readline()
                data.append(frame)

        # The checksum is for the whole DTU
        if not VEDirect.check_frame_checksum(data):
            raise InvalidChecksumException()

        return data

    @staticmethod
    def check_frame_checksum(frames: list[bytes]):
        """Checks the PDU for validity.
        The "checksum" generates a char so that the sum
        of all characters equals 0 mod 256"""
        chksum = 0
        for frame in frames:
            for char in frame:
                chksum = (chksum + char) % 256
        return chksum == 0

    @property
    def battery_volts(self) -> float:
        """Returns the battery voltage in Volts."""
        return mV(self._data["V"])

    @property
    def battery_amps(self) -> float:
        """Returns the battery charging current in Amps."""
        return mA(self._data["I"])

    @property
    def solar_volts(self) -> float:
        """Returns the solar array voltage in Volts."""
        return mV(self._data["VPV"])

    @property
    def solar_power(self) -> float:
        """Returns the solar array power in Watts."""
        return float(self._data["PPV"])

    @property
    def device_serial(self) -> str:
        """Returns the device serial number."""
        return self._data["SER#"]

    @property
    def device_MPPT_state(self) -> MPPTState:
        """Returns the MPPT state."""
        return MPPTState(int(self._data["MPPT"]))

    # New Getters
    @property
    def firmware_version(self) -> str:
        """Returns the firmware version."""
        return self._data["FW"]

    @property
    def product_id(self) -> str:
        """Returns the product ID."""
        return self._data["PID"]

    @property
    def charge_state(self) -> int:
        """Returns the charge state (0-9)."""
        return int(self._data["CS"])

    @property
    def error_code(self) -> int:
        """Returns the error code (0-119)."""
        return int(self._data["ERR"])

    @property
    def load_state(self) -> str:
        """Returns the load output state (ON/OFF)."""
        return self._data["LOAD"]

    @property
    def load_current(self) -> float:
        """Returns the load current in Amps."""
        return mA(self._data["IL"])

    @property
    def total_yield(self) -> float:
        """Returns the total yield in kWh."""
        return float(self._data["H19"])

    @property
    def yield_today(self) -> float:
        """Returns the yield today in kWh."""
        return float(self._data["H20"])

    @property
    def max_power_today(self) -> float:
        """Returns the maximum power today in Watts."""
        return float(self._data["H21"])

    @property
    def yield_yesterday(self) -> float:
        """Returns the yield yesterday in kWh."""
        return float(self._data["H22"])

    @property
    def max_power_yesterday(self) -> float:
        """Returns the maximum power yesterday in Watts."""
        return float(self._data["H23"])

    @property
    def day_sequence(self) -> int:
        """Returns the day sequence number (0-365)."""
        return int(self._data["HSDS"])


if __name__ == "__main__":
    v = VEDirect()

    print(f"Battery Voltage: {v.battery_volts} V")
    print(f"Battery Current: {v.battery_amps} A")
    print(f"Solar Voltage: {v.solar_volts} V")
    print(f"Solar Power: {v.solar_power} W")
    print(f"Device Serial Number: {v.device_serial}")
    print(f"MPPT State: {v.device_MPPT_state.name}")
    print(f"Firmware Version: {v.firmware_version}")
    print(f"Product ID: {v.product_id}")
    print(f"Charge State: {v.charge_state}")
    print(f"Error Code: {v.error_code}")
    print(f"Load State: {v.load_state}")
    print(f"Load Current: {v.load_current} A")
    print(f"Total Yield: {v.total_yield} kWh")
    print(f"Yield Today: {v.yield_today} kWh")
    print(f"Max Power Today: {v.max_power_today} W")
    print(f"Yield Yesterday: {v.yield_yesterday} kWh")
    print(f"Max Power Yesterday: {v.max_power_yesterday} W")
    print(f"Day Sequence: {v.day_sequence}")
