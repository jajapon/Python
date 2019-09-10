'''
Created on 4 sept. 2019
@author: jajapon

Instalar el package psycopg2 y pygresql
pip install [package_name]

'''
import psycopg2

class PostgreSQL(object):
    ''' Constructor '''
    def __init__(self, hostname, database, username, password, port):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.port = port

        self.status = False
        self.mydb = ""
        self.connection = ""
        
    ''' Getters y Setters '''   
    def getHostname(self): return self.hostname
    def getDatabase(self): return self.database
    def getUsername(self): return self.username
    def getPassword(self): return self.password
    def getPort(self): return self.port
    def getConnection(self): return self.connection
    def getMyDB(self): return self.mydb
    def getStatus(self): return self.status
    
    def setHostname(self, hostname):
        self.hostname = hostname
        
    def setDatabase(self, database):
        self.database = database
    
    def setUsername(self, username):
        self.username = username
        
    def setPassword(self, password):
        self.password = password
        
    def setPort(self, port):
        self.port = port
        
    ''' Funcion que se encarga de conectarse a la base de datos usando los parametros pasados '''
    def connectDB(self):
        # Establecemos la conexion a la base de datos
        self.mydb = psycopg2.connect(
            host=self.hostname, 
            database=self.database, 
            user=self.username, 
            password=self.password,
            port=self.port
        )
        self.connection = self.mydb.cursor()

    ''' Funcion que nos reconectara a la base de datos y se ejecutara automaticamente en caso de cambiar algun dato de configuracion '''
    def reconnectDB(self):
        self.mydb.close();
        self.connectDB()
        
    
    def closeDBConnection(self):
        self.mydb.close()
        
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
            self.connectDB()
            
            self.connection.execute(query)      
            data = self.connection.fetchall()
            self.status = True
            
            self.closeDBConnection()
            
            return data
        except:
            self.status = False
            return self.status

    ''' Funcion encargada de realizar consultas que no devuelven resultados INSERT, UPDATE, DELETE '''        
    def doQuery(self, query):   
        try:  
            self.connectDB()
            
            self.connection.execute(query) 
            self.mydb.commit()
            
            self.closeDBConnection()

            self.status = True    
        except:
            self.status = False    
        
        return self.status
    