from omar_bouaouda_ruiz import *

class AdaboostMultiClass:
    def __init__(self, n_classes, T=5, A=20):
        self.n_classes = n_classes
        self.T = T
        self.A = A
        self.clasificadores = []  # Lista de clasificadores AdaBoost, uno por clase

    def fit(self, X, Y):
        # Entrenar un clasificador AdaBoost para cada clase
        for i in range(self.n_classes):
            print(f"Entrenando para la clase {i}")
            Y_binaria = np.where(Y == i, 1, -1)  # Convertir a etiquetas binarias
            adaboost = Adaboost(self.T, self.A)
            adaboost.fit(X, Y_binaria)
            self.clasificadores.append(adaboost)

    def predict(self, X):
        # Recolectar las predicciones de cada clasificador AdaBoost
        predicciones = np.array([clasificador.predict(X) for clasificador in self.clasificadores])
        # Elegir la clase con la mayor confianza (suma ponderada de alfas) para cada muestra
        return np.argmax(predicciones, axis=0)

def evaluate_multiclass(T=5, A=20, verbose=False):
    # Cargar el conjunto de datos MNIST
    (X_train, Y_train), (X_test, Y_test) = keras.datasets.mnist.load_data()

    # Aplanar las imágenes y normalizar
    X_train = X_train.reshape((X_train.shape[0], -1)) / 255.0
    X_test = X_test.reshape((X_test.shape[0], -1)) / 255.0

    n_classes = len(np.unique(Y_train))

    # Entrenar el clasificador Adaboost multiclase
    adaboost_mc = AdaboostMultiClass(n_classes, T=T, A=A)
    adaboost_mc.fit(X_train, Y_train)

    # Calcular la precisión
    train_accuracy = np.mean(adaboost_mc.predict(X_train) == Y_train)
    test_accuracy = np.mean(adaboost_mc.predict(X_test) == Y_test)

    # Imprimir resultados
    print(f"Tasas de acierto en entrenamiento y prueba: {train_accuracy*100:.2f}%, {test_accuracy*100:.2f}%")
