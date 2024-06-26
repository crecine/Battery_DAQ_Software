import tkinter as tk
from enum import Enum, IntFlag

class FloatEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        if 'floatvariable' in kwargs:
            kwargs['textvariable'] = kwargs.pop('floatvariable')
        super().__init__(*args, **kwargs)
        vcmd = (self.register(self.validate),'%P')
        self.config(validate="all", validatecommand=vcmd)

    def validate(self, text):
        if (
            all(char in "0123456789.-" for char in text) and  # all characters are valid
            "-" not in text[1:] and # "-" is the first character or not present
            text.count(".") <= 1): # only 0 or 1 periods
                return True
        else:
            return False
        
    def get(self):
        return float(super().get())

class IntegerEntry(FloatEntry):
    def __init__(self, *args, **kwargs):
        if 'integervariable' in kwargs:
            kwargs['textvariable'] = kwargs.pop('integervariable')
        super().__init__(*args, **kwargs)

    def validate(self, text):
        if super().validate(text) and (len(text)==0 or round(float(text)) == float(text)):
            return True
        else:
            return False
        
    def get(self):
        return int(super().get())

class PosIntegerEntry(IntegerEntry):
    def validate(self, text):
        if "-" not in text and super().validate(text):
            return True
        else:
            return False

class Variable(Enum):
    VOLTAGE = 'Voltage'
    CURRENT = 'Current'

    def __str__(self):
        return self.value

class Point(IntFlag):
    LOW = 0
    HIGH = 1
