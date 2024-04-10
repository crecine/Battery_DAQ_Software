import tkinter as tk
from utils import round_it, FloatEntry
from numpy import loadtxt
from enum import Enum, auto
from data_utils import dataacq
from window_settings import configuration

class Variable(Enum):
    VOLTAGE = 'Voltage'
    CURRENT = 'Current'

    def __str__(self):
        return self.value

class Point(Enum):
    LOW = 0
    HIGH = 1

class calibration(tk.Tk): #Display the settings for editing
    def __init__(self, screenName: tuple[str, None] = None, baseName: tuple[str, None] = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: tuple[str, None] = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title('Calibrate')
        self.geometry('535x300')
        self.dispframe = tk.Frame(self,borderwidth=2,relief='groove')
        self.recordframe = tk.Frame(self,border=2,relief='groove')
        self.calcframe = tk.Frame(self)
        self.dispframe.pack(fill='x')
        self.recordframe.pack(fill='x')
        self.calcframe.pack(side=tk.BOTTOM)
        self.dataavg = [[0]*8,[1]*8]

        self.s_vals, self.z_vals = read_cal_file()
        self.Ss = self.add_data_row(self.s_vals,'Spans')
        self.Zs = self.add_data_row(self.z_vals,'Zeros')

        self.lowframe = tk.LabelFrame(self.recordframe,labelanchor='nw',text='Low')
        self.highframe = tk.LabelFrame(self.recordframe,labelanchor='nw',text='High')
        self.lowframe.pack(fill='x')
        self.highframe.pack(fill='x')

        self.v_low = self.add_calibration(Variable.VOLTAGE,Point.LOW)
        self.c_low = self.add_calibration(Variable.CURRENT,Point.LOW,tk.RIGHT)
        self.v_high = self.add_calibration(Variable.VOLTAGE,Point.HIGH)
        self.c_high = self.add_calibration(Variable.CURRENT,Point.HIGH,tk.RIGHT)

        calc_button = tk.Button(self.calcframe,text='Calculate',command=self.calculate_calibration)
        save_button = tk.Button(self.calcframe,text='Save',command=self.save_cal)
        calc_button.pack(side=tk.LEFT)
        save_button.pack(side=tk.LEFT)
    
    def add_data_row(self,data_set,title):
        data = [round_it(x,5) for x in data_set]
        frame = tk.LabelFrame(self.dispframe,labelanchor='nw',text=title)
        frame.pack(fill='x')

        row = []
        for ii in range(len(data)):
            cell = tk.Text(frame, width=10, height=1)
            cell.pack(side=tk.LEFT)
            cell.insert(tk.END,data[ii])
            cell.config(state=tk.DISABLED, wrap=tk.WORD)
            row.append(cell)
        
        return row
    
    def update_data_row(self,row,data_set):
        data = [round_it(x,5) for x in data_set]
        for ii in range(len(row)):
            cell = row[ii]
            cell.config(state=tk.NORMAL)
            cell.delete('1.0',tk.END)
            cell.insert(tk.END,data[ii])
            cell.config(state=tk.DISABLED)

    
    def add_calibration(self,variable,point,side=tk.LEFT):
        if point is Point.LOW:
            master = self.lowframe
        else:
            master = self.highframe
        label = tk.Label(master, text=str(variable)+':')
        truth_val = tk.DoubleVar()
        entry = FloatEntry(master,floatvariable=truth_val)
        cmd = lambda var=variable, pt=point: self.record_calibration_data(var,pt)
        record = tk.Button(master,text='Record',command=cmd)
        if side == tk.LEFT:
            cells = [label, entry, record]
        elif side == tk.RIGHT:
            cells = [record, entry, label]
        else:
            raise ValueError('side should be tk.LEFT or tk.RIGHT')
        for cell in cells:
            cell.pack(side=side)
        return entry

    def record_calibration_data(self,variable,point):
        board = configuration.board
        sample_rate = configuration.board
        sample_period = configuration.board
        dataavg = dataacq(board, sample_rate=sample_rate, sample_period=sample_period)
        if variable is Variable.CURRENT:
            self.dataavg[point][0] = dataavg[0]
        else:
            self.dataavg[point][1:] = dataavg[1:]
        
    def calculate_calibration(self):
        s, z = [0]*8, [0]*8
        [dataavglow,dataavghigh] = self.dataavg
        s[0]=(self.c_high.get()-self.c_low.get())/(dataavghigh[0]- dataavglow[0])
        z[0]=self.c_high.get()-s[0]* dataavghigh[0]

        for i in range(1,len(dataavghigh)):
            s[i]= (self.v_high.get()-self.v_low.get())/(dataavghigh[i]- dataavglow[i])
            z[i] = self.v_high.get()-s[i]* dataavghigh[i]

        self.update_data_row(self.Ss,s)
        self.update_data_row(self.Zs,z)

        self.s_vals = s
        self.z_vals = z
        
    def save_cal(self): #Save the changes to the calibration file
        self.update_data_row(self.Ss,self.s_vals)
        self.update_data_row(self.Zs,self.z_vals)
        write_cal_file(self.s_vals, self.z_vals)

        self.destroy()
    
def read_cal_file(filename="cal.dat"):
    lines = loadtxt(filename, comments="#", delimiter=",", unpack=False)
    [s,z] = lines
    return list(s), list(z)

def write_cal_file(s, z, filename="cal.dat"):
    with open(filename, 'w') as output_file:
        output_file.write(str(s).strip('[]'))
        output_file.write('\n')
        output_file.write(str(z).strip('[]'))

