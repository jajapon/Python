'''
Created on 9 ago. 2019

@author: jajapon
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from astropy.time.utils import split

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor

class Regresion(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    # Modelo de regresion
    def generarModelo(self, num_parametros, num_neuronas_capas, tipo_kernel, tactivaciones):
        # create model
        model = Sequential()
        
        kernels = tipo_kernel.split(":")
        capasn = num_neuronas_capas.split(":")
        activaciones = tactivaciones.split(":")
        
        for i in range(len(capasn)):
            # Declaramos las variables que vayamos a utilizar
            neuronas = int(capasn[i])
            kernel = kernels[i]
            activacion = activaciones[i]
            
            # Comprobamos  Si es la primera capa para actuar de forma diferente
            if (i == 0):
                if (activacion != ""):
                    model.add(Dense(neuronas, input_dim=num_parametros, kernel_initializer=kernel, activation=activacion))
                else:                    
                    model.add(Dense(neuronas, input_dim=num_parametros, kernel_initializer=kernel))
            else:
                if (activacion != ""):
                    model.add(Dense(neuronas, kernel_initializer=kernel, activation=activacion))
                else:                    
                    model.add(Dense(neuronas, kernel_initializer=kernel))
                                   
        # Compilamos el modelo 
        model.compile(loss='mean_squared_error', optimizer='adam')
        
        # devolvemos el modelo ya preparado para su uso '''
        return model
    
    
    ''' Metodo utilizado para entrenar nuestro modelo de red neuronal con un set de datos ''' 
    def entrenarRed(self, modelo, x_train, y_train, nepocas, batchSize):
        print()
        modelo.summary()
        print()
        modelo.compile(loss='mse', optimizer='adam', metrics=['mse','mae'])
        
        historico = modelo.fit(x_train, y_train, epochs=nepocas, batch_size=batchSize,  verbose=1, validation_split=0.2)
        print(historico.history.keys())
        return historico
    
    
    def generarDatos(self, fichero, tamanio):    
        #Variables
        dataframe = pd.read_csv(fichero, delim_whitespace=True, header=None)
        dataset = dataframe.values
        x=dataset[:,0:tamanio]
        y=dataset[:,tamanio]
        y=np.reshape(y, (-1,1))
        return x, y
    
    def generarDatosEntrenoYTest(self, x, y, scaler_x, scaler_y): 
        print()
        print(scaler_x.fit(x))
        xscale=scaler_x.transform(x)
        print(scaler_y.fit(y))
        yscale=scaler_y.transform(y)
        
        x_train, x_test, y_train, y_test = train_test_split(xscale, yscale)
        return x_train, x_test, y_train, y_test

    ''' Metodo que se encarga de mostrar la los resultados de entreno de la red neuronal en una grafica '''
    def mostrarGraficaEntreno(self, historico):
        # "Loss"
        plt.plot(historico.history['loss'])
        plt.plot(historico.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
        
    
    def showGraphic(self, prediction, Y_test):
        Y = []
        X = []
        
        for i in range(len(prediction)):
            Y.append(prediction[i])
            X.append(Y_test[i][0])
            
        time = len(prediction)
        times = []
        for i in range(time): times.append(i)
        
        mins = int(Y_test[:,0].min()) 
        maxs = int(Y_test[:,0].max()) + 100
        
        linex, liney = [], []
        for i in range(maxs):
            linex.append(i)
            liney.append(i)
            
    
        #showGraphics
        plt.plot(X , Y, "ro")
        plt.plot(linex , liney, "blue")
        plt.title("Salida real / Prediccion")
        plt.ylabel("Prediccion")
        plt.xlabel("Salida real")
        plt.show()
        
        plt.title("Salida real / Prediccion  en tiempo")
        plt.ylabel("Salida Real \ Prediccion")
        plt.xlabel("tiempo")
        plt.plot(times , X)
        plt.plot(times , Y)
        plt.legend(["salida real", "prediccion"], loc="upper left")
        plt.show()

    
        