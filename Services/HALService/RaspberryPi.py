import os
import io

class RPI:

    def __init__(self):
        self.RPI_Valid = False
        return None
    
    def is_RPI(self) -> bool:
        try:
                self.RPI_Valid = 'rpi' in os.uname().release
                return self.RPI_Valid
        except Exception: pass
        return False