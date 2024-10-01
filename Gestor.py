from dataFunctions import *
from appFunctions import *
from winsound import MessageBeep, MB_ICONASTERISK

db = Database("data.gc")
table = Table(30, ("Plataforma","Usuario","Email"), (34,10))
table.headStyle(hStyle="bold")

#####################################  Funciones de utilidad  ########################################
#Carga de las plataformas, usuarios y emails de la db en la tabla de la app.
def maskPassword(password):
    mask = ""
    i=0
    while i<len(password):
      mask += "*"
      i += 1 
    return mask
    
def updateLabelCount():
  labelCountNumber.config(text= f"{db.count()}") 
  
def updateLabelUser():
  labelUser.config(text = f"Lista de cuentas de {db.getJoinedMastername()}")
      
#Acciones de los botones
def enableOpButtons(event):
  s = table.getRegister()
  if len(s) == 0:
    readButton.config(state="disabled")
    updateButton.config(state="disabled")
    deleteButton.config(state="disabled")
  else:
    readButton.config(state="normal")
    updateButton.config(state="normal")
    deleteButton.config(state="normal")
    
def confirmMasterData(user='', key=''): 
  if db.loginMaster(user,key):
    platforms = db.listAccounts("platform")
    usernames = db.listAccounts("user")
    emails = db.listAccounts("email")
    table.loadTable(db.count(), platforms,usernames,emails)
    updateLabelCount()
    updateLabelUser()
    return True
  else:
    return False

def loginWindow():
   openWindowLoginMaster(confirmMasterData, db.signUpMaster)
    
###########################################################################################  
############################################ Ventanas de operaciones ###################################        
#Ventana para guardar una cuenta  
def saveAction():
  ###################################
  def save():
    plat = entryPlat.get()
    username = entryUser.get()
    email = entryEmail.get()
    psw = entryPassword.get()
    desc = entryDesc.get()
    
    if plat == '':
      plat = '---'
    if username == '':
      username = '---'
    if email == '':
      email = '---'
    ## Codigo para guardar los datos en la base de datos #######
    if db.saveAccount(plat,username,email,psw,desc) == 0:
    ####
      table.writeRegister((plat,username,email))
      updateLabelCount()
      messagebox.showinfo("Aviso","La cuenta se guardó correctamente")
      windowSaveAction.destroy()
    else:
      messagebox.showerror("ERROR","No se pudo guardar la cuenta")
      windowSaveAction.destroy()
  ###################################
  windowSaveAction = Toplevel()
  windowSaveAction.iconbitmap(img_route)
  windowSaveAction.resizable(False,False)
  windowSaveAction.config(bg="gray26")
  windowSaveAction.title("Guardar cuenta")
  defGeometry(windowSaveAction, 300, 250, True)
  
  placeLabel(f"Plataforma: ",(5,10),windowSaveAction)
  placeLabel(f"Nombre de usuario: ",(5,25),windowSaveAction)
  placeLabel(f"Correo electrónico: ",(5,40),windowSaveAction)
  placeLabel(f"Contraseña: ",(5,55),windowSaveAction)
  placeLabel(f"Descripcion adicional: ",(5,70),windowSaveAction)
  
  entryPlat = placeEntry((50,10),windowSaveAction)
  entryUser = placeEntry((50,25),windowSaveAction)
  entryEmail = placeEntry((50,40),windowSaveAction)
  entryPassword = placeEntry((50,55),windowSaveAction)
  entryPassword.config(show="*")
  entryDesc = placeEntry((50,70),windowSaveAction)
  
  placeButton("Guardar",0, (30,87), window=windowSaveAction, action=save) 
  placeButton("Cancelar",0, (55,87),windowSaveAction.destroy,windowSaveAction)
    
       
###########################################################################################    
###########################################################################################  
#Ventana para leer datos de una cuenta
def readAction():
  ###################################   
  def copyPlat():
    windowReadAction.clipboard_clear()
    windowReadAction.clipboard_append(plat)
  def copyUser():
    windowReadAction.clipboard_clear()
    windowReadAction.clipboard_append(user)
  def copyEmail():
    windowReadAction.clipboard_clear()
    windowReadAction.clipboard_append(mail)
  def copyPassword():
    windowReadAction.clipboard_clear()
    windowReadAction.clipboard_append(psw)
  def copyDesc():
    windowReadAction.clipboard_clear()
    windowReadAction.clipboard_append(desc)  
  ###################################
  register = table.getRegister()
  plat = register[0]
  user = register[1]
  mail = register[2]
  
  #### Codigo para leer los datos en la base de datos #######
  psw = db.readAccount(db.getAccountID(plat,user), "password")
  desc = db.readAccount(db.getAccountID(plat,user), "description")
  ####
  
  if psw == [] or desc == []:
    messagebox.showerror("ERROR","No se pudo obtener datos de esta cuenta")
    return
  
  windowReadAction = Toplevel()
  windowReadAction.iconbitmap(img_route)
  windowReadAction.resizable(False,False)
  windowReadAction.config(bg="gray26")
  windowReadAction.title("Leer cuenta")
  defGeometry(windowReadAction, 370, 250, True)
  
  placeLabel(f"Plataforma: {plat}",(20,10),windowReadAction)
  placeLabel(f"Nombre de usuario: {user}",(20,25),windowReadAction)
  placeLabel(f"Correo electrónico: {mail}",(20,40),windowReadAction)
  placeLabel(f"Contraseña: {maskPassword(psw)}",(20,55),windowReadAction)
  placeLabel(f"Descripcion adicional: {desc}",(20,70),windowReadAction)
  
  placeButton("Copiar",0, (3,10), window=windowReadAction, action=copyPlat)
  placeButton("Copiar",0, (3,25), window=windowReadAction, action=copyUser)
  placeButton("Copiar",0, (3,40), window=windowReadAction, action=copyEmail)
  placeButton("Copiar",0, (3,55), window=windowReadAction, action=copyPassword)
  placeButton("Copiar",0, (3,70), window=windowReadAction, action=copyDesc)
  placeButton("Cancelar",0, (40,87),windowReadAction.destroy,windowReadAction)  
###########################################################################################    
###########################################################################################   
#Ventana para actualizar cuenta 
def updateAction():
  #Funcion para crear una ventanita para ingresar el dato nuevo
  ###################################
  def createNewValueWindow(dataToModify, columnNumber = -1):
      ###################################
      #Leemos el valor ingresado en la ventanita y actualizamos la tabla
      def readNewValue():
        newVal = entryNewValue.get()
        windowNewValue.destroy()
        if newVal == '':
          newVal = '---'
        
        ######## Realizamos la actualizacion en la base de datos #######
        if db.updateAccount(db.getAccountID(plat,user), dataToModify, newVal) == 0:
          messagebox.showinfo("Aviso","Actualizacion exitosa")
        else:
          messagebox.showerror("ERROR","No se pudo realizar la actualización")
          windowUpdateAction.destroy()
          return
        ###################################################################
        
        if columnNumber>=0 and columnNumber<=2:  
          table.updateRegister(newVal, columnNumber)  
           
        windowUpdateAction.destroy()
      #############################################
      windowNewValue = Toplevel(windowUpdateAction)
      windowNewValue.config(bg="gray26")
      windowNewValue.title("Actualizar")
      windowNewValue.iconbitmap(img_route)
      windowNewValue.resizable(False,False)
      defGeometry(windowNewValue,300,120,True)
      
      placeLabel(f"Nuevo valor:", (3,30), windowNewValue) 
      entryNewValue = placeEntry((50,30),windowNewValue)
      if dataToModify == db.getColumnNames()[3]:
        entryNewValue.config(show='*')
      
      placeButton("Aceptar",0, (25,80),readNewValue,windowNewValue)
      placeButton("Cancelar",0, (55,80),windowNewValue.destroy,windowNewValue)
  ################################################################################     
  #Funciones que utilizan la ventanina de ingreso de nuevo valor para modificar el dato solicitado
  def updatePlat():
    createNewValueWindow(db.getColumnNames()[0], 0)  
  def updateUser():
    createNewValueWindow(db.getColumnNames()[1], 1)
  def updateEmail():
    createNewValueWindow(db.getColumnNames()[2], 2)
  def updatePassword():
    createNewValueWindow(db.getColumnNames()[3])
  def updateDesc():
    createNewValueWindow(db.getColumnNames()[4])
  ######################################################################
  windowUpdateAction = Toplevel()
  windowUpdateAction.resizable(False,False)
  windowUpdateAction.config(bg="gray26")
  windowUpdateAction.title("Actualizar cuenta")
  windowUpdateAction.iconbitmap(img_route)
  defGeometry(windowUpdateAction, 250, 250, True)
  
  register = table.getRegister()
  plat = register[0]
  user = register[1]
  
  placeLabel(f"Plataforma",(30,10),windowUpdateAction)
  placeLabel(f"Nombre de usuario",(30,25),windowUpdateAction)
  placeLabel(f"Correo electrónico",(30,40),windowUpdateAction)
  placeLabel(f"Contraseña",(30,55),windowUpdateAction)
  placeLabel(f"Descripcion adicional",(30,70),windowUpdateAction)
  
  placeButton("Cambiar",0, (3,10), window=windowUpdateAction, action=updatePlat)
  placeButton("Cambiar",0, (3,25), window=windowUpdateAction, action=updateUser)
  placeButton("Cambiar",0, (3,40), window=windowUpdateAction, action=updateEmail)
  placeButton("Cambiar",0, (3,55), window=windowUpdateAction, action=updatePassword)
  placeButton("Cambiar",0, (3,70), window=windowUpdateAction, action=updateDesc)
  placeButton("Cancelar",0, (40,87),windowUpdateAction.destroy,windowUpdateAction)
  
###########################################################################################   
###########################################################################################  
#Ventana para eliminar una cuenta         
def deleteAction():
  MessageBeep(MB_ICONASTERISK) #Funcion para reproducir el sonido de la messagebox.showinfo()
  if messagebox.askyesno("Aviso","Esta seguro de eliminar esta cuenta?"):
    regAccount = table.getRegister()
    plat = regAccount[0]
    username = regAccount[1]
    #### Codigo para borrar la cuenta en la base de datos ####
    if db.deleteAccount(db.getAccountID(plat,username)) == 0:
    ####
      messagebox.showinfo("Aviso","La cuenta se borró correctamente")
      table.deleteRegister()
      updateLabelCount()
    else:
      messagebox.showerror("ERROR","No se pudo borrar la cuenta")

###########################################################################################    
###########################################################################################   
#Ventana para configurar los datos del master    
def configMasterAction():
  ###################################
  def closeSession():
      loginWindow()
      windowConfigMaster.destroy()
      
  def updateDataMaster():
      ###################################
      def update():
          name = entryName.get()
          key = entryKey.get()
          if db.updateMaster(name,key) == 0:
            updateLabelUser()
            messagebox.showinfo("Aviso","Tus datos se han actualizado")
          else:
            messagebox.showerror("ERROR","No se pudieron actualizar los datos")
          windowConfigMaster.destroy()
          windowUpdateDataMaster.destroy()
      #########################################################
      windowUpdateDataMaster = Toplevel()
      windowUpdateDataMaster.resizable(False,False)
      windowUpdateDataMaster.config(bg="gray26")
      windowUpdateDataMaster.title("Actualizar")
      windowUpdateDataMaster.iconbitmap(img_route)
      defGeometry(windowUpdateDataMaster, 300, 120, True)
      windowUpdateDataMaster.protocol("WM_DELETE_WINDOW", windowUpdateDataMaster.destroy)
      
      placeLabel("Nuevo nombre: ",(3,10),windowUpdateDataMaster)
      placeLabel("Nueva contraseña: ",(3,30),windowUpdateDataMaster)
      entryName = placeEntry((50,10),windowUpdateDataMaster)
      entryKey = placeEntry((50,30),windowUpdateDataMaster)
      entryKey.config(show="*")
      placeButton("Aceptar",0, (25,80),update,windowUpdateDataMaster)
      placeButton("Cancelar",0, (60,80),windowUpdateDataMaster.destroy,windowUpdateDataMaster)
  ######################################################################    
  
  windowConfigMaster = Toplevel()
  windowConfigMaster.resizable(False,False)
  windowConfigMaster.iconbitmap(img_route)
  windowConfigMaster.config(bg="gray26")
  windowConfigMaster.title("Configuración")
  defGeometry(windowConfigMaster, 250, 200, True)
  windowConfigMaster.protocol("WM_DELETE_WINDOW", windowConfigMaster.destroy)
  
  placeLabel(f"Maestro logeado: {db.getJoinedMastername()}",(5,10),windowConfigMaster)
  placeLabel(f"Maestros registrados: {db.countMaster()}", (5,30),windowConfigMaster)
  
  placeButton("Actualizar", 82, (15,87),updateDataMaster,windowConfigMaster)
  placeButton("Cerrar sesión", 82, (55,87), action=closeSession, window=windowConfigMaster)
      
###########################################################################################       
###########################################################################################   
#####################################  MAIN  ####################################
#Aca asociamos la funcion "enableOpButtons" con el evento de seleccion de un 
table.eventSelect(enableOpButtons)

labelUser = placeLabel("Lista de cuentas de",(33.4,4),bg_clr=mainWindowBackground)
labelUser.config(font=("",13,"bold"))
labelCountText = placeLabel("Cuentas guardadas: ", (6.5,70),bg_clr=mainWindowBackground)
labelCountText.config(font=("",11))
labelCountNumber = placeLabel("0", (26,70.1),bg_clr=mainWindowBackground) 
labelCountNumber.config(font=("", 11, "bold"))
     
readButton = placeButton("Leer cuenta",100,(7,20), color="chartreuse4", action=readAction)
updateButton = placeButton("Actualizar cuenta",100,(7,30), color="chartreuse4", action=updateAction)
deleteButton = placeButton("Eliminar cuenta",100,(7,40), color="red4", action= deleteAction)
readButton.config(state="disabled")
updateButton.config(state="disabled")
deleteButton.config(state="disabled")
placeButton("Guardar cuenta", 100, (7,50), action=saveAction, color="DodgerBlue2")
placeButton("Configuración", 100, (7,60), action=configMasterAction)

configApp("Gestor de contraseñas", 700, 710)
loginWindow()
exeApp()