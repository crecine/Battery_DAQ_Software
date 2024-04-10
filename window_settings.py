import tkinter as tk

class settings(tk.Tk):
    def __init__(self, screenName: tuple[str, None] = None, baseName: tuple[str, None] = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: tuple[str, None] = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title('Settings')
        # self.geometry('300x200')
        self.num_settings = 0
        self.frame = tk.Frame(self)
        self.frame.pack(fill='x')
        self.entries = []
        for name in configuration.get_attrs().keys():
            self.entries.append(self.add_setting(name))
        save_button = tk.Button(self,text='Save',command=self.save_set)
        save_button.pack()

    def add_setting(self,name):
        attr = configuration.getattr(name)
        if isinstance(attr,str):
            var = tk.StringVar()
        elif isinstance(attr,float):
            var = tk.DoubleVar()
        elif isinstance(attr,int):
            var = tk.IntVar
        else:
            raise TypeError(f'{type(attr)} is not a valid type')
        label = tk.Label(self.frame,text=name)
        label.grid(column=0,row=self.num_settings,sticky='w')
        entry = tk.Entry(self.frame,textvariable=var)
        entry.insert(0,str(attr))
        entry.grid(column=1,row=self.num_settings,sticky='w')
        self.num_settings+=1
        return (name,entry)
        
    def save_set(self): #Save the changes to the settings file
        for (name,entry) in self.entries:
            setattr(configuration,name,entry.get())

        self.destroy()

class configuration():
    board = None
    filename = 'test_results'
    max_successive=12
    tol=.05
    max_iter=20000
    sample_rate=200
    sample_period=5

    @classmethod
    def get_attrs(cls):
        return {
            'filename':cls.filename,
            'max_successive':cls.max_successive,
            'tol':cls.tol,
            'max_iter':cls.max_iter,
            'sample_rate':cls.sample_rate,
            'sample_period':cls.sample_period,
            }
    
    @classmethod
    def getattr(cls,name):
        return cls.__getattribute__(cls,name)
    
    @classmethod
    def setattr(cls,name,value):
        return cls.__setattr__(cls,name,value)