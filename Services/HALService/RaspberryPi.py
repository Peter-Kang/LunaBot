import os
import io

class RPI:

    def __init__(self):
        self.RPI_Valid = False
        return None
    
    def is_RPI(self) -> bool:
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                self.RPI_Valid = 'raspberry pi' in m.read().lower()
                return self.RPI_Valid
        except Exception: pass
        return False