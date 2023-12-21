import numpy as np
import math
from random import randrange
import logging, os
from tensorflow import keras
import time

N_FEATURES = 28*28

class DecisionStump:
    def __init__(self, n_features):
        # Seleccionar al azar una caracteri­stica, un umbral y una polaridad.
        self.caracteristica = np.random.randint(N_FEATURES)
        self.umbral = randrange(256)
        self.polaridad = 1 if randrange(2) == 1 else -1 

    def predict(self, X):
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        caracteristicas = X[:, self.caracteristica]
        predictions = np.ones(len(X))
        predictions[caracteristicas < self.umbral if self.polaridad == 1 else caracteristicas > self.umbral] = -1

        return predictions

class Adaboost:
    def __init__(self, T=5, A=20):
        self.T = T
        self.A = A
        self.listaClasificadores = []

    def fit(self, X, Y, verbose = False):
        #Inicializamos el vector
        D = np.ones(len(X), dtype=float) / len(X)
        
        for t in range(self.T):
            errorMin = np.inf
            mejorClasificador = None
            mejorPrediccion = None

            # Probamos los clasificadores
            for _ in range(self.A):
                clasificadorDebil = DecisionStump(N_FEATURES)
                predicciones = clasificadorDebil.predict(X)
                error = np.sum(D[Y != predicciones])

                # Si hay un error menor, entonces tenemos un clasificador mejor
                if error < errorMin:
                    mejorClasificador = clasificadorDebil
                    mejorPrediccion = predicciones
                    errorMin = error

            alfa = 0.5 * np.log((1 - errorMin) / (errorMin + 1e-10))
            D *= np.exp(-alfa * Y * mejorPrediccion)
            D /= np.sum(D)  # Normalizar D para que sume a 1

            self.listaClasificadores.append((alfa, mejorClasificador))
    
    def predict(self, X):
        final_predictions = np.zeros(len(X))

        for alfa, clasificador in self.listaClasificadores:
            predictions = np.zeros(len(X))
            for i, x in enumerate(X):
                prediction = clasificador.predict(x.reshape(1, -1))
                # Extraer el valor escalar de la predicción
                predictions[i] = prediction[0] if isinstance(prediction, np.ndarray) else prediction

            final_predictions += alfa * predictions

        return np.sign(final_predictions)
    
def evaluate(digit, T=5, A=20, verbose=False):
    # Cargar el conjunto de datos MNIST
    (X_train, Y_train), (X_test, Y_test) = keras.datasets.mnist.load_data()

    # Aplanar las imágenes y normalizar
    X_train = X_train.reshape((X_train.shape[0], -1)) / 255.0
    X_test = X_test.reshape((X_test.shape[0], -1)) / 255.0
    Y_train = np.where(Y_train == digit, 1, -1)
    Y_test = np.where(Y_test == digit, 1, -1)

    #Entrenar el clasificador Adaboost
    adaboost = Adaboost(T=T, A=A)
    start_time = time.time()
    adaboost.fit(X_train, Y_train, verbose=verbose)
    training_time = time.time() - start_time
    
    # Calcular la precisión
    train_accuracy = np.mean(adaboost.predict(X_train) == Y_train)
    test_accuracy = np.mean(adaboost.predict(X_test) == Y_test)

    # Imprimir resultados
    print(f"Entrenando clasificador Adaboost para el dígito {digit}, T={T}, A={A}")
    if verbose:
        for i, (alfa, clasificador) in enumerate(adaboost.listaClasificadores, 1):
            print(f"Añadido clasificador {i}: {clasificador.caracteristica}, {clasificador.umbral:.8f}, {'+' if clasificador.polaridad == 1 else '-'}, {alfa:.8f}")
    print(f"Tasas acierto (train, test) y tiempo: {train_accuracy*100:.2f}%, {test_accuracy*100:.2f}%, {training_time:.3f} s.")

# Ejemplo de uso de la función
evaluate(digit=7, T=20, A=10, verbose=True)