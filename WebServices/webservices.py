'''
Created on 9 sept. 2019

@author: inercodevops
'''
import requests as req

class webservices(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def get(self, url):
        data = ""
        mensaje = "Error"
        scode = -1
        
        try:
            response = req.get(url)
            
            if response.status_code == 200:
                scode = response.status_code
                data = response.json()
                mensaje = "OK"
            else:
                scode = response.status_code
        
        except:
            mensaje = "Server error: was not found"
            
        return data, scode, mensaje
    

        