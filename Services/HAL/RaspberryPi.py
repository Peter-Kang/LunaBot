import os
import io

class RPI:

    def __init__(self):
        self.RPI_Valid = False
        return None
    
    def is_RPI() -> bool:
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower(): 
                    self.RPI_Valid = True
                    return True
        except Exception: pass
        return False