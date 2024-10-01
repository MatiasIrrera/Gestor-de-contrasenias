import sqlite3
#columnas de la tabla Accounts: ID, platform, user, email, password, description
#columnas de la tabla Master: ID, Mastername, Masterkey, MasterID

class Database: 
    "Clase para el manejo de base de datos. Recibe la ruta de la ubicacion de la base de datos"
    def __init__(self, strRoute): #U0 es para indicar que aun no se selecciono a ningun usuario
        self.__route = strRoute  #Aca guardamos la ruta donde esta guardada la base de 
        self.__masterId = "" #ID del usuario. Al seleccionar el ID del master, se trabaja solo con las cuentas de ese usuario
        self.__errorNum = 0  #Flag para indicar si la ejecución de la consulta SQL fue exitosa. 0 si lo fue y -1 si hubo error     
        self.__createTables()
        
    def __exeQuery(self, comm, arg = ()):
        "Los argumentos se pasan de esta manera para evitar inyecciones SQL"
        r = []
        try:
            connection = sqlite3.connect(self.__route)
            cursor = connection.cursor()
            cursor.execute(comm, arg)
            connection.commit() 
            r = cursor.fetchall()
            connection.close()
            self.__errorNum = 0
        except Exception as ex:
            print("Error in SQL Query: " + str(ex))
            self.__errorNum = -1    
        return r      

    def __createTables(self):
        self.__exeQuery("""CREATE TABLE IF NOT EXISTS Master(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Mastername varchar(255),
                                Masterkey varchar(255), 
                                MasterID varchar(255)
                        );""")
        self.__exeQuery("""CREATE TABLE IF NOT EXISTS Accounts(
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Platform varchar(255),
                                User varchar(255),
                                Email varchar(255),
                                Password varchar(255),
                                Description varchar(255),
                                MasterID varchar(255)
                        );""")
        
    def deleteTables(self):
        self.__exeQuery("DROP TABLE Master") 
        self.__exeQuery("DROP TABLE Accounts")   
        return
        
    def getColumnNames(self):
        return ["platform","user","email","password","description"]

    def saveAccount(self, platform, user, email, password, description = ''):
        r = self.__exeQuery(f'INSERT INTO Accounts (platform, user, email, password, description, MasterID) VALUES (?,?,?,?,?,?)',(platform, user, email, password, description, self.__masterId,))
        return self.__errorNum
       
    def readAccount(self, id, dataAccount):
        r_query = self.__exeQuery(f'SELECT {dataAccount} FROM Accounts WHERE ID = ? AND MasterID = ?', (id,self.__masterId,))
        if len(r_query) == 0:
            return []
        return r_query[0][0]
    
    def updateAccount(self, id, dataModify, newValue):
        self.__exeQuery(f'UPDATE Accounts SET {dataModify} = ? WHERE ID = ? AND MasterId = ?', (newValue,id,self.__masterId,))
        return self.__errorNum
        
    def deleteAccount(self, id):
        self.__exeQuery(f'DELETE FROM Accounts WHERE ID = ? AND MasterId = ?', (id,self.__masterId,))
        return self.__errorNum
        
    def listAccounts(self, column):
        r = []
        r_query = self.__exeQuery(f'SELECT {column} FROM Accounts WHERE MasterId = ?', (self.__masterId,))
        if len(r_query) != 0: 
            for acc in r_query:
                r.append(acc[0]) 
        return r
            
    def count(self):
        #r = self.__exeQuery('SELECT COUNT(*) FROM Accounts WHERE MasterId = ?', (self.__masterId,))
        r = self.__exeQuery("""
                          SELECT COUNT(*) FROM(
                              SELECT * FROM Master INNER JOIN Accounts ON Master.MasterID = Accounts.MasterID
                          ) WHERE MasterId = ? LIMIT 1
                          """, (self.__masterId,))
        
        if len(r) != 0:
            return int(r[0][0])
        else:
            return -1
    
    def getAccountID(self, plat, uname):
        r = self.__exeQuery('SELECT ID FROM Accounts WHERE USER = ? AND PLATFORM = ? AND MasterId = ?', (uname, plat,self.__masterId,))
        if len(r) != 0:
            return int(r[0][0])
        else:
            return -1
    ###################################################################################################### 
    #Metodos para el master   
    def loginMaster(self, masterName, masterKey):
        listOfTupples = self.__exeQuery("SELECT MasterID FROM Master WHERE Mastername = ? AND Masterkey = ?", (masterName, masterKey,))
        if listOfTupples != []:
            self.__masterId = listOfTupples[0][0]
            return True
        else:
            return False
        
    def updateMaster(self, newMasterName, newMasterKey):
        self.__exeQuery("UPDATE Master SET Mastername = ?, MasterKey = ? WHERE id = ?", (newMasterName, newMasterKey, self.__getJoinedMasterIDSql(),))
        return self.__errorNum
   
    def signUpMaster(self, newMasterName, newMasterKey):
        r = self.__exeQuery("SELECT Mastername FROM Master WHERE Mastername = ?",(newMasterName,))
        if len(r) == 0:
            newID = f"U{self.countMaster() + 1}"
            self.__exeQuery("INSERT INTO Master (Mastername,Masterkey,MasterID) VALUES (?,?,?)", (newMasterName, newMasterKey, newID,))
        else:
            self.__errorNum = -2
        return self.__errorNum     
    
    def listMasters(self):
        r = []
        query = self.__exeQuery("SELECT Mastername FROM Master")   
        if len(query) != 0:
            for master in query:
                r.append(master[0])
        return r
    
    def getJoinedMasterID(self):
        return self.__masterId
    
    def __getJoinedMasterIDSql(self):
        r = self.__exeQuery("SELECT ID FROM Master WHERE MasterID = ?",(self.__masterId,))
        if len(r) != 0:
            return int(r[0][0])
        else:
            return -1
    
    def getJoinedMastername(self):
        r = self.__exeQuery("SELECT Mastername FROM Master WHERE MasterID = ?", (self.__masterId,))
        #r = self.__exeQuery("""
        #                  SELECT Mastername FROM(
        #                      SELECT * FROM Accounts INNER JOIN Master ON Accounts.MasterID = Master.MasterID
        #                  ) WHERE MasterID = ? LIMIT 1
        #                  """,(self.__masterId,))
        
        if len(r) != 0:
            return r[0][0]
        else:
            return ""
        
    def getJoinedMasterkey(self):
        r = self.__exeQuery("SELECT Masterkey FROM Master WHERE MasterID = ?", (self.__masterId,))
        if len(r) != 0:
            return r[0][0]
        else:
            return ""
    
    def countMaster(self):
        r = self.__exeQuery('SELECT COUNT(*) FROM Master')
        if len(r) != 0:
            return int(r[0][0])
        else:
            return -1