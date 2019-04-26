# File: NeoPixelLib.py ; By: Opas Sirikunchittavorn

from esp import neopixel_write
import time

class NeoPixel:
    ORDER = (1, 0, 2, 3)
    
    def __init__(self, pin, n, bpp=3, timing=1,brightness=1.0):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)
        self.timing = timing
        self.brightness = brightness

    def __setitem__(self, index, val):
        offset = index * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = val[i]

    def __getitem__(self, index):
        offset = index * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]]
                     for i in range(self.bpp))

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def write(self):
      if self.brightness > 0.9 :
        neopixel_write(self.pin, self.buf, self.timing)
      else:
        neopixel_write(self.pin, bytearray([int(i * self.brightness) for i in self.buf]),self.timing)

    def cycle(self,color,wait):
        n = self.n

        for i in range(2 * n):
            for j in range(n):
                self[j] = (0, 0, 0)
            self[i % n] = color
            self.write()
            time.sleep_ms(wait)
            
    def bounce(self,color,wait):
        n = self.n

        # bounce
        for i in range(2 * n):
            for j in range(n):
                self[j] = color
            if (i // n) % 2 == 0:
                self[i % n] = (0, 0, 0)
            else:
                self[n - 1 - (i % n)] = (0, 0, 0)
            self.write()
            time.sleep_ms(wait)

    def fadeinout(self,color):
        n = self.n
        r=color[0]; g=color[1]; b=color[2]; 
        for i in range(0, 21, 1):
            for j in range(n):
                self[j] = (int(r*i/20),int(g*i/20),int(b*i/20))
            self.write()
            time.sleep_ms(50)
        for i in range(20, -1, -1):
            for j in range(n):
                self[j] = (int(r*i/20),int(g*i/20),int(b*i/20))
            self.write()
            time.sleep_ms(50)        
            
    def clear(self):    # clear all SELED
        self.fill((0, 0, 0))
        self.write()
       
    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
 
    def color_chase(self,color, wait):
        for i in range(self.n):
            self[i] = color
            time.sleep_ms(wait)
            self.write()
        time.sleep(0.5)
     
     
    def rainbow_cycle(self,wait):
        n=self.n
        for j in range(255):
            for i in range(n):
                rc_index = (i * 256 // n) + j
                pos = rc_index & 255
                if pos < 0 or pos > 255:
                    self[i] = (0, 0, 0)
                    continue
                if pos < 85:
                    self[i] = (255 - pos * 3, pos * 3, 0)
                    continue
                if pos < 170:
                    pos -= 85
                    self[i] = (0, 255 - pos * 3, pos * 3)
                    continue
                pos -= 170
                self[i] = (pos * 3, 0, 255 - pos * 3)
            self.write()
            time.sleep_ms(wait)   



