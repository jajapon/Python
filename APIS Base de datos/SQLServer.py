'''
Created on 30 ago. 2019

@author: jajapon
'''
import pyodbc

class SQLServer:
    ''' Constructor '''
    def __init__(self, hostname, database, username, password ):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.status = False
        self.mydb = ""
        self.connection = ""
        
        self.connectDB()
        
    ''' Getters y Setters '''   
    def getHostname(self): return self.hostname
    def getDatabase(self): return self.database
    def getUsername(self): return self.username
    def getPassword(self): return self.password
    def getMyDB(self): return self.mydb
    def getConnection(self): return self.connection
    def getStatus(self): return self.status
    
    def setHostname(self, hostname):
        self.hostname = hostname
        self.connectDB()
        
    def setDatabase(self, database):
        self.database = database
        self.connectDB()
    
    def setUsername(self, username):
        self.username = username
        self.connectDB()
        
    def setPassword(self, password):
        self.password = password
        self.connectDB()
        
    ''' Funcion que se encarga de conectarse a la base de datos usando los parametros pasados '''
    def connectDB(self):
        # Establecemos la conexion a la base de datos
        self.mydb = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + self.hostname + ';'
                      'Database=' + self.database + ';'
                      'UID=' + self.username + ';'
                      'PWD=' + self.password + ';')
        
        self.connection = self.mydb.cursor()

    ''' Funcion que se encarga de ejecutar la consulta SQL y devolver el resultado '''    
    def executeQuery(self, query):
        q = query.upper()
        
        if q.find("SELECT") != -1:
            return self.doSelect(query)
        elif q.find("DELETE") != -1  or q.find("UPDATE") != -1 or q.find("INSERT") != -1:
            return self.doQuery(query)
        else:
            return False
        
    ''' Funcion encargada de realizar consultas SELECT y devolver su resultado '''    
    def doSelect(self, query):         
        try:  
            self.connection.execute(query)      
            data = self.connection.fetchall()
            self.status = True
            return data
        except:
            self.status = False
            return self.status

    ''' Funcion encargada de realizar consultas que no devuelven resultados INSERT, UPDATE, DELETE '''        
    def doQuery(self, query):   
        try:  
            self.connection.execute(query) 
            self.status = True     
        except:
            self.status = False    
        
        return self.status

    