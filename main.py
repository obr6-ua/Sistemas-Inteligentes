import pygame
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from pygame.locals import *
from variable import *


GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=5 # número de filas del crucigrama
COLS=6 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

def variablesHorizontales(tablero):
    var = []
    for i in range(tablero.getAlto()):
        tam = 0
        inicio = 0
        palabra_actual = []
        for j in range(tablero.getAncho()):
            celda_actual = tablero.getCelda(i, j)
            if celda_actual == '*' and tam > 0:
                variable = Variable(tam, i, inicio, 'H')
                variable.setPalabra(palabra_actual)
                var.append(variable)
                palabra_actual = []
                tam = 0
            elif celda_actual != '*':
                if tam == 0:
                    inicio = j
                palabra_actual.append(celda_actual)
                tam += 1
        if tam > 0:  # Para el caso donde llegamos al final sin encontrar una celda llena
            variable = Variable(tam, i, inicio, 'H')
            variable.setPalabra(palabra_actual)
            var.append(variable)
    return var

def variablesVerticales(tablero):
    var = []
    for j in range(tablero.getAncho()):
        tam = 0
        inicio = 0
        palabra_actual = []
        for i in range(tablero.getAlto()):
            celda_actual = tablero.getCelda(i, j)
            if celda_actual == '*' and tam > 0:
                variable = Variable(tam, inicio, j, 'V')
                variable.setPalabra(palabra_actual)
                var.append(variable)
                palabra_actual = []
                tam = 0
            elif celda_actual != '*':
                if tam == 0:
                    inicio = i
                palabra_actual.append(celda_actual)
                tam += 1
        if tam > 0:  # Para el caso donde llegamos al final sin encontrar una celda llena
            variable = Variable(tam, inicio, j, 'V')
            variable.setPalabra(palabra_actual)
            var.append(variable)
    return var



def imprimir_dominios(variables):
    for var in variables:
        print(f"Variable {var.getDireccion()}{var.getFila() if var.getDireccion() == 'H' else var.getColumna()}:")
        print(f" Posición: ({var.getFila()}, {var.getColumna()})")
        print(f" Longitud: {var.getTam()}")
        print(f" Orientación: {var.getDireccion()}")
        print(f" Palabra actual: {''.join(var.palabra)}")
        print(f" Dominio: {var.dominio}")
        print() 

def dominiosBase(variables, almacen):
    for variable in variables:
        tam_var = variable.getTam()  # Obtiene el tamaño de la variable
        dominio_variable = []  # Inicia una lista vacía para el dominio de esta variable
        pos_almacen = busca(almacen, tam_var)  #Busca en el almacén si hay un dominio con el mismo tamaño
        if pos_almacen != -1:  # Si se encuentra un dominio con el tamaño adecuado
            for palabra in almacen[pos_almacen].getLista():
                if esCompatible(palabra, variable):
                    dominio_variable.append(palabra)
        variable.dominio = dominio_variable  # Actualiza el dominio de la variable

def esCompatible(palabra, variable):
    if len(palabra) != len(variable.palabra):
        return False
    for i, letra in enumerate(variable.palabra):
        if letra != '-' and letra.upper() != palabra[i].upper():
            return False
    return True

def actualizarDominios(variables, var_asignada, palabra_asignada):
    # Primero eliminamos la palabra de todos los dominios
    for var in variables:
        if palabra_asignada in var.dominio:
            var.dominio.remove(palabra_asignada)
    
    # Ahora, para cada variable vertical que se cruce con la variable horizontal,
    # actualizamos su dominio para mantener solo las palabras compatibles.
    if var_asignada.getDireccion() == 'H':
        fila_asignada = var_asignada.getFila()
        for i, letra in enumerate(palabra_asignada):
            columna_cruce = var_asignada.getColumna() + i
            for var_vertical in [v for v in variables if v.getDireccion() == 'V' and v.getColumna() == columna_cruce]:
                # Calculamos la posición relativa de la intersección en la palabra vertical
                indice_interseccion = fila_asignada - var_vertical.getFila()
                if 0 <= indice_interseccion < var_vertical.getTam():
                    # Mantenemos solo las palabras que coinciden en la letra de la intersección
                    var_vertical.dominio = [
                        pal for pal in var_vertical.dominio
                        if indice_interseccion < len(pal) and pal[indice_interseccion].upper() == letra.upper()
                    ]
                    if not var_vertical.dominio:
                        return False
                    
def es_consistente(palabra, variable, asignacion):
    # Verifica que la palabra no haya sido ya asignada a otra variable
    if palabra in asignacion.values():
        return False

    # Para cada intersección con otras variables asignadas, verificar que la letra coincida
    for var in asignacion:
        interseccion = variable.intersecta_con(var)
        if interseccion:
            # Comprobamos que las letras en la intersección coincidan
            if palabra[interseccion[0]] != asignacion[var][interseccion[1]]:
                return False

    return True


def dominio_vacio(variables):
    for var in variables:
        if not var.dominio:  # Si el dominio está vacío
            return True
    return False

def borrarPalabraAlmacen(variables, palabra , almacen):
    tam_palabra = len(palabra)
    for var in variables:
        if var.getTam() == tam_palabra and palabra in var.dominio:
            var.dominio.remove(palabra)

def meterVariable(variablesAsignadas , variablesSinAsignar):
    variablesSinAsignar.append(variablesAsignadas[0])
    variablesAsignadas.pop(0)
    
def quitarVariable(variablesAsignadas , variablesSinAsignar):
    variablesAsignadas.append(variablesSinAsignar[0])
    variablesSinAsignar.pop(0)

def insertarEnTablero(variable , tablero):
    for v in variable:
        for i in range(v.tam):
            if v.direccion == 'H':
                tablero.setCelda(v.fila , v.columna + i , v.palabra[i])
            
            
def introducir_palabra(variable , palabra ,  tablero):
    variable.setPalabra(palabra)
    insertarEnTablero(variable , tablero)

def guardarDominioAnterior(variables, historial_dominios):
    historial_dominios.append([var.dominio[:] for var in variables])

def restaurarDominioAnterior(variables, historial_dominios):
    if historial_dominios:
        ultimo_dominio = historial_dominios.pop()
        for var, dom in zip(variables, ultimo_dominio):
            var.dominio = dom


def FC(almacen, tablero):
    varH = variablesHorizontales(tablero)
    varV = variablesVerticales(tablero)
    variables = varH + varV
    dominiosBase(variables, almacen)
    asignacion = {}
    variables_asignadas = set()
    historial_dominios = []  # Este será el historial de los dominios a restaurar

    if forward_checking(variables, asignacion,almacen, tablero, historial_dominios, variables_asignadas):
        insertarEnTablero(variables , tablero)
        return True
        # Aquí imprime el tablero o la asignación de palabras como prefieras
    else:
        return False
        
def forward_checking(variables, asignacion, almacen, tablero, historial_dominios, variables_asignadas):
    if len(asignacion) == len(variables):
        print("Todas las variables han sido asignadas.")
        return True

    # Seleccionamos la siguiente variable que no está asignada y no está en el conjunto de asignadas
    variable = next((v for v in variables if v.getDireccion() == 'H' and v not in asignacion and v not in variables_asignadas), None)
    if not variable:
        print("No hay más variables para asignar.")
        return True

    print(f"Variable actual: {variable.getDireccion()} ({variable.getFila()}, {variable.getColumna()}) con dominio {variable.dominio}")
    
    for palabra in variable.dominio:
        print(f"Probando palabra '{palabra}' para la variable {variable.getDireccion()}({variable.getFila()}, {variable.getColumna()}).")
        guardarDominioAnterior(variables, historial_dominios)

        if es_consistente(palabra, variable, asignacion, tablero):
            asignacion[variable] = palabra
            variable.setPalabra(palabra)
            variables_asignadas.add(variable)
            actualizarDominios(variables, variable, palabra)
            imprimir_dominios(variables)
            print(f"Palabra '{palabra}' asignada. Dominios actualizados.")

            if dominio_vacio(variables):
                print(f"El dominio de alguna variable se vació. Retrocediendo...")
                restaurarDominioAnterior(variables, historial_dominios)
                variable.dominio.remove(palabra)  # Eliminamos la palabra que causó el problema
                print(f"Palabra '{palabra}' eliminada del dominio de la variable tras retroceso.")
                del asignacion[variable]
                variables_asignadas.remove(variable)
                variable.setPalabra(['-'] * variable.getTam())
            else:
                if forward_checking(variables, asignacion, almacen, tablero, historial_dominios, variables_asignadas):
                    return True
                print(f"Retrocediendo de la profundidad con la palabra '{palabra}' debido a un fallo en la asignación.")
                restaurarDominioAnterior(variables, historial_dominios)
                del asignacion[variable]
                variables_asignadas.remove(variable)
                variable.setPalabra(['-'] * variable.getTam())
        else:
            print(f"La palabra '{palabra}' no es consistente con la asignación actual. Probando la siguiente palabra.")

    print(f"No se encontraron palabras válidas para la variable {variable.getDireccion()}({variable.getFila()}, {variable.getColumna()}). Retrocediendo...")
    restaurarDominioAnterior(variables, historial_dominios)
    return False

           
def ac3(almacen, tablero):
    # Inicializar variables y dominios
    varH=variablesHorizontales(tablero)
    varV=variablesVerticales(tablero)
    variables = varH + varV
    dominiosBase(variables, almacen)
    historial_dominios = []
    variablesSinAsignar = variables[:]
    asignacion = {}

    # Función recursiva para intentar asignar palabras a las variables
    def intentar_asignar():
        if not variablesSinAsignar:
            return True  # Todas las variables han sido asignadas

        variable = variablesSinAsignar.pop(0)
        guardarDominioAnterior(variables, historial_dominios)

        for palabra in variable.dominio:
            if es_consistente(palabra, variable, asignacion):
                asignacion[variable] = palabra
                actualizarDominios(variables, variable, palabra)
                
                if not dominio_vacio(variables):
                    if intentar_asignar():
                        return True

                # Si no funciona, deshacemos los cambios y probamos con la siguiente palabra
                asignacion.pop(variable, None)
                restaurarDominioAnterior(variables, historial_dominios)
                borrarPalabraAlmacen(variables, palabra, almacen)

        # No se encontró una palabra válida, restaurar y devolver falso
        variablesSinAsignar.insert(0, variable)
        restaurarDominioAnterior(variables, historial_dominios)
        return False

    if intentar_asignar():
        for var, palabra in asignacion.items():
            introducir_palabra(var, palabra, tablero)
        return tablero
    else:
        return "No se encontró una solución"

# Ejemplo de uso
# Crear el tablero, almacen, y las variables aquí...
# Luego llamar a resolver_crucigrama(variables, almacen, tablero)

        


#########################################################################
# Detecta si se pulsa el botón de FC
######################################################################### 
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    f= open('d0.txt', 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen=[]
   
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1: #no existen palabras de esa longitud
            dom=Dominio(len(pal))
            dom.addPal(pal.upper())            
            almacen.append(dom)
        elif pal.upper() not in almacen[pos].lista: #añade la palabra si no está duplicada        
            almacen[pos].addPal(pal.upper())           
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for dom in almacen:
        print (dom.tam)
        lista=dom.getLista()
        for pal in lista:
            print (pal, end=" ")
        print()
        
#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    almacen=creaAlmacen()
    game_over=False
    tablero=Tablero(FILS, COLS)    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    res=FC(tablero , almacen) #aquí llamar al forward checking
                    if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")                                  
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):
                     res=ac3(almacen , tablero) #aquí llamar al forward checking            
                     print("AC3")
                     if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])             
        #pintar botones        
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
 
#hay un dominio para cada variable. Cada variable serian las palabras que se pueden meter
#El dominio de una variable , serán todas las palabras menos aquellas que ya estan completas 
