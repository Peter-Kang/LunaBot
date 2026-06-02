import os
try:
    import board
    import adafruit_dht
except ImportError:pass

class RPI:

    def __init__(self):
        self.RPI_Valid:bool = False
    
    def is_RPI(self) -> bool:
        try:
            self.RPI_Valid = 'rpi' in os.uname().release
            return self.RPI_Valid
        except Exception: pass
        return False
    
    def GetTemperatureAndHumidity(self) -> str:
        if self.RPI_Valid:
            try:
                sensor = adafruit_dht.DHT22(board.D4)
                temperature_c = sensor.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = sensor.humidity
                return "{0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity)
            except Exception as error:
                print(error)
            return 
        return "Not connected"