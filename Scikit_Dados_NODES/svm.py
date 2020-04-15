import pandas as pd


base_source = pd.read_csv('/home/matt/Documents/Wifi_Sniffer-master/kNN_Dados_NODES/database.csv')

base = base_source.replace(['sala01-1', 'sala01-2', 'sala01-3', 'sala01-4', 'sala01-5',
                      'sala01-6', 'sala01-7', 'sala01-8', 'sala01-9', 'sala02-1',
                      'sala02-2', 'sala02-3', 'sala02-4', 'sala02-5', 'sala02-6',
                      'sala02-7', 'sala02-8', 'sala02-9', 'corredor1', 'corredor2',
                      'corredor3', 'corredor4', 'corredor5', 'corredor6', 
                      'corredor7', 'corredor8', 'forasala1', 'forasala2'],

                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 
                     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])

"""
base_source = pd.read_csv('/home/matt/Documents/Wifi_Sniffer-master/kNN_Dados_NODES/database2.csv')

base = base_source.replace(['sala01', 'sala02', 'corredor1', 'corredor2',
                      'corredor3', 'corredor4', 'corredor5', 'corredor6', 
                      'corredor7', 'corredor8', 'forasala1', 'forasala2'],

                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
"""

#separa atributos previsores
previsores = base.iloc[:,0:4].values
#separa atributos classe
classe = base.iloc[:,4].values

#preprocessamento dos dados para modelo padrão caso seja preciso
#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#previsores = scaler.fit_transform(previsores)

#divisão da base de treinamento e teste
from sklearn.model_selection import train_test_split
previsores_treinamento, previsores_teste, classe_treinamento, classe_test = train_test_split(previsores, classe, test_size=0.20, random_state=0)

from sklearn.svm import SVC
classificador = SVC(kernel = 'linear', random_state = 1)

#Fit the model using X as training data and y as target values
classificador.fit(previsores_treinamento, classe_treinamento)
#o algoritmo prevê o resultado para comparar com a classe teste(já sabemos)
previsoes = classificador.predict(previsores_teste)

from sklearn.metrics import confusion_matrix, accuracy_score
#precisão de acertos
precisao = accuracy_score(classe_test, previsoes)
#registro x classe
matriz = confusion_matrix(classe_test, previsoes)

import collections
collections.Counter(classe_test)