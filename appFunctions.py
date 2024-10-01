from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, ttk, font, Frame
#Algunas constantes
_defaultBackground = "gray26"
mainWindowBackground = "dark green"
_defaultForeground = "snow"
img_route = "icon.ico"

#Ventana principal
_root = Tk()
_root.withdraw()
#Ventana de login

################################################################################################
################################################################################################
#Clase para manejar la tabla de la aplicación donde se muestra las cuentas de cada usuario maestro
class Table:
   """Clase para manejar la tabla de todas las cuentas.\n
   maxRegisters: Cantidad maxima de registros mostrables\n
   columnNames: Tupla que contiene el nombre de las columnas (son 3 en total)\n
   position: Tupla con la posicion relativa en (x,y)"""
   def __init__(self, maxRegisters, columnNames = (), position = ()):
      self.__table = ttk.Treeview(_root,columns=("#1","#2"), height = maxRegisters)
      self.__table.column("#0", width=100)
      self.__table.column("#1", width=150,anchor="center")
      self.__table.column("#2", width=200,anchor="center")
      self.__table.heading("#0", text= columnNames[0],anchor="center")
      self.__table.heading("#1", text= columnNames[1],anchor="center")
      self.__table.heading("#2", text= columnNames[2],anchor="center")
      self.__table.place(relx= position[0]/100, rely=position[1]/100)
      self.headStyle()
   
   #Asignamos una accion o funcion para ejecutarla al momento de seleccionar un item de la tabla   
   def eventSelect(self, action):
      self.__table.bind("<<TreeviewSelect>>", action)
   
   #Obtenemos los datos de un solo registro de la tabla
   def getRegister(self):
      if self.__table.selection() != ():
         idRegister = self.__table.selection()[0]
         textRegister = self.__table.item(idRegister,"text")
         valuesRegister = self.__table.item(idRegister,"values")
         register = (textRegister, valuesRegister[0], valuesRegister[1])
         return register
      else:
         return ()
   #Escribimos un registro nuevo en la tabla   
   def writeRegister(self, dataColumns = ()):    
      self.__table.insert("", "end", text = dataColumns[0], values = (dataColumns[1], dataColumns[2]))
   #Actualizamos un registro escrito en la tabla   
   def updateRegister(self, newValue, numColumn):
      if self.__table.selection()!=() and numColumn>=0 and numColumn<=2:
         idRegister = self.__table.selection()[0]
         register = self.getRegister()
         
         newRegister = list(register)
         newRegister[numColumn] = newValue
         self.__table.item(idRegister, text=newRegister[0], values=(newRegister[1],newRegister[2]) )
         return 0
      else:
         return -1  
   #Borramos un registro de la tabla   
   def deleteRegister(self):
      idData = self.__table.selection()[0]
      self.__table.delete(idData)
   #Borramos toda la tabla   
   def cleanTable(self):
      for register in self.__table.get_children():
        self.__table.delete(register)
   #Colocamos varios registros en la tabla, borrando previamente el contenido anterior   
   def loadTable(self, size, valuesColumn0, valuesColumn1, valuesColumn2):
      self.cleanTable()
      for i in range(0, size):
         self.writeRegister((valuesColumn0[i], valuesColumn1[i], valuesColumn2[i]))
   
   def headStyle(self, hFont = "Arial", hWidth = 10, hStyle = ""):
      style = ttk.Style()
      style.configure("Treeview.Heading", font=(hFont,hWidth,hStyle))
      
##########################################################################
################################################################################################
#Funciones para colocar elementos y configurarlos

def placeFrame(pos = ()):
   frame = Frame(_root)
   frame.place(relx= pos[0]/100, rely= pos[1]/100)
   return frame
   

def placeLabel(myText, position = (), window = _root, fg_clr= _defaultForeground, bg_clr= _defaultBackground):
   x = position[0]
   y = position[1]
   lb = Label(window, text = myText, fg=fg_clr, bg = bg_clr, font=("Arial",10))
   lb.place(relx=x/100, rely=y/100, height=18)
   
   return lb
################################################################################################    
def placeButton(myText, wd, position = (), action = "", window = _root, color = "gray"):
   x = position[0]
   y = position[1]
   btn = Button(window, text = myText, bg= color, fg= _defaultForeground, command = action, font=("Arial",9))
   if wd != 0:
      btn.place(relx=x/100, rely=y/100, width= wd, height=21)
   else:
      btn.place(relx=x/100, rely=y/100, height=21)
   
   #Le asociamos al boton el evento de presionar el ENTER, para que ejecute la accion pasada en "action"
   def pressEnter(event):
      action()
   btn.bind('<Return>', pressEnter)   
      
   return btn
################################################################################################   
def placeEntry(position = (), window = _root):
   x = position[0]
   y = position[1]
   entry = Entry(window)
   entry.place(relx=x/100, rely=y/100)
   return entry 
################################################################################################
################################################################################################
#Funciones de configuracion y ejecucion del gestor de contraseñas

def configApp(name = "", width = 100, height = 100):
   _root.title(name)
   defGeometry(_root, width, height, True)
   _root.resizable(False, False)
   _root.config(bg = mainWindowBackground)
   _root.iconbitmap(img_route)
   
def exeApp():
   _root.mainloop()  
################################################################################################   
################################################################################################
#Funcion para configurar el tamaño de cualquier ventana o centrarla en la pantalla
def defGeometry(window, width, height, center=False):
   if center:
      screenWd = window.winfo_screenwidth()
      screenHg = window.winfo_screenheight()
      posX = (screenWd - width) // 2
      posY = (screenHg - height) // 2
      window.geometry(f"{width}x{height}+{posX}+{posY}")
   else:
      window.geometry(f"{width}x{height}")
#####################################################################################      
################################################################################################
#Funciones para la gestion de las cuentas maestras

def openWindowLoginMaster(confirmMethod,signUpMethod):
   ## Acciones de los botones ##
   ###################################
   def readAndConfirm():
      masterUser = entryUser.get()
      masterKey = entryKey.get()
      
      #Confirm es una funcion que recibe los 2 parametros y devuelve T o F en caso de que se encuentre o no el usuario maestro
      if confirmMethod(masterUser, masterKey):
         _root.deiconify() #Hacemos que la ventana principal reaparezca
         windowMasterKey.destroy() 
         #NOTA: se debe comparar con todos los masteruser y masterkeys de cada regitros que cumplan ambas condiciones  
      else:
         messagebox.showwarning("Acceso denegado","Los datos de acceso son inválidos")
      return
   
   def cancel():
      windowMasterKey.destroy()
      _root.destroy()

   def signUp():
      openWindowSignUp(signUpMethod)
      return
   ###################################
   
   _root.withdraw() #ocultamos la ventana principal
   windowMasterKey = Toplevel()
   windowMasterKey.withdraw()
   defGeometry(windowMasterKey,320,200,True)
   windowMasterKey.iconbitmap(img_route)
   windowMasterKey.resizable(False,False)
   windowMasterKey.config(bg = _defaultBackground)
   windowMasterKey.title("Ingrese su cuenta maestra")
   windowMasterKey.protocol("WM_DELETE_WINDOW", cancel)
   
   labelTitle = placeLabel("Ingrese los datos del usuario maestro", (13,3),windowMasterKey,"yellow")
   labelTitle.config(font=("",10,"bold"))
   placeLabel("Usuario",(5,20),windowMasterKey)
   placeLabel("Contraseña",(5,40),windowMasterKey)
   entryUser = placeEntry((30,20),windowMasterKey)
   entryKey = placeEntry((30,40),windowMasterKey)
   entryKey.config(show="*") #Enmascaramos la contraseña
   
   placeButton("Acceder",0, (25,66),readAndConfirm,windowMasterKey)
   placeButton("Cancelar",0, (55,66),cancel,windowMasterKey)
   
   placeLabel("No tenes tu cuenta maestra?", (1, 85),windowMasterKey)
   placeButton("Crear cuenta maestra",0, (57,85),signUp,windowMasterKey)
   windowMasterKey.deiconify()
################################################################################################   
def openWindowSignUp(method):
   ###################################
   def signUpAction():
      mastUser = entryUser.get()
      mastKey = entryKey.get()
      
      if mastUser == "" or mastKey == "":
         messagebox.showwarning("Advertencia","Por favor, complete todos los datos")
      elif mastKey != entryRepKey.get():
         messagebox.showwarning("Advertencia","Las contraseñas no coinciden")
      else:
         flag = method(mastUser,mastKey)
         if flag == 0:
            messagebox.showinfo("Aviso","Tu cuenta maestra se ha creado correctamente.")
            windowSignUp.destroy()
         elif flag == -2:
            messagebox.showwarning("Advertencia",f"Ya existe una cuenta de nombre {mastUser}")
         else:
            messagebox.showerror("ERROR","No se pudo crear tu cuenta")      
        
   ##################################
   
   windowSignUp = Toplevel()
   windowSignUp.withdraw()
   windowSignUp.iconbitmap(img_route)
   windowSignUp.resizable(False,False)
   windowSignUp.config(bg = _defaultBackground)
   windowSignUp.title("Crear cuenta maestra")
   windowSignUp.protocol("WM_DELETE_WINDOW", windowSignUp.destroy)
   defGeometry(windowSignUp,300,200,True)
   
   placeLabel("Usuario Maestro",(5,20),windowSignUp)
   entryUser = placeEntry((50,20),windowSignUp)
   placeLabel("Contraseña Maestra",(5,35),windowSignUp)
   entryKey = placeEntry((50,35),windowSignUp)
   entryKey.config(show="*")
   placeLabel("Repetir contraseña",(5,50),windowSignUp)
   entryRepKey = placeEntry((50,50),windowSignUp)
   entryRepKey.config(show="*")
   
   placeButton("Crear",60, (25,85),signUpAction,windowSignUp)
   placeButton("Cancelar",60, (55,85),windowSignUp.destroy,windowSignUp)
   windowSignUp.deiconify()