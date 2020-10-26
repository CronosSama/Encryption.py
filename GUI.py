import tkinter as tk
from tkinter import filedialog,Text
from Logic import mainApp

class GUI():
    def __init__(self):
        self.all_Selected = []
        self.typeOfOperation = None
        self.frame = None
        self.passwordEntry = None
        self.canvas = None
        self.KeyCode = None
        self.EncryptN = False
        self.root = tk.Tk()

        self.canvasF()
        self.Buttons()
        self.filesFrame()
        self.Entries()
        
        self.root.mainloop()

    def canvasF(self):
        self.canvas = tk.Canvas(self.root,height=600,width=600,bg="#263D42")
        self.canvas.pack()

    def Entries(self):
        self.password = tk.Entry(self.root)
        self.canvas.create_window(200, 20, window=self.password)
    
    def Buttons(self):
        pickButton = tk.Button(self.root,text="Pick Files",command=self.Select_Files)
        encButton = tk.Button(self.root,text="Encrypt !!", command=self.enc)
        dncButton = tk.Button(self.root,text="Decrypt !!", command=self.dnc)
        clearButton = tk.Button(self.root,text="Clear Selected",command=self.clear_Selected)
        nameDEButton = tk.Button(self.root,text="Encrypt/Decrypt Name",command=self.EncryptName)

        runButton = tk.Button(self.root,text="RUN !!",command=self.run)
        pickButton.pack()
        clearButton.pack()
        encButton.pack()
        dncButton.pack()
        nameDEButton.pack()
        runButton.pack()

    def filesFrame(self):
        fileFrame = tk.Frame(self.root,bg="white")
        fileFrame.place(relwidth=0.8,relheight=0.6,relx=0.1,rely=0.1)
        self.frame = fileFrame

    def Select_Files(self):
        print('we are in Select_Files')
        tupleFiles = filedialog.askopenfilenames(filetypes=[("all", "*")])
        
        for filename in tupleFiles:
            if not filename in self.all_Selected and not filename==" ":
                print(filename)
                self.all_Selected.append(filename)
                self.Show_Selected_files()

            else:

                print('ALL READY SELECTED')
                continue
        
        

    def Show_Selected_files(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for Oneselected in self.all_Selected:
            #Adding Text to the screen or frame 
            label = tk.Label(self.frame,text=Oneselected, bg="gray")
            label.pack()

    def clear_Selected(self):
        self.all_Selected = []
        for widget in self.frame.winfo_children():
            widget.destroy()

    def run(self):
        self.KeyCode = self.password.get()
        print(self.KeyCode)
        x=mainApp(self.all_Selected,self.typeOfOperation,self.KeyCode,self.EncryptN)
    
    def EncryptName(self):
        oldEncryptName = self.EncryptN
        self.EncryptN = not oldEncryptName
        print(self.EncryptN)

    def enc(self):
        self.typeOfOperation = 'enc'
        print(self.typeOfOperation)
    def dnc(self):
        self.typeOfOperation = 'dnc'
        print(self.typeOfOperation)


x=GUI()


    

    
