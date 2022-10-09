from ast import Expr
from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    MODULO = 5
    POTENCIA = 6

class OPERACION_RELACIONAL(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    MAYOR_IGUAL = 3
    MENOR_IGUAL = 4
    IGUAL = 5
    DIFERENTE = 6

class OPERACION_LOGICA(Enum) :
    OR = 1
    AND = 2
    NOT = 3

class Expresion:
    'clase abstracta para las expresiones'

class ExpresionAritmetica(Expresion) :
    #clase para las expresiones binarias

    def __init__(self, expresion1, expresion2, operador) :
        self.expresion1 = expresion1
        self.expresion2 = expresion2
        self.operador = operador

class ExpresionRelacional(Expresion):
    def __init__(self, expresion1, expresion2, operador):
        self.expresion1 = expresion1
        self.expresion2 = expresion2
        self.operador = operador

class ExpresionLogica(Expresion):

    def __init__(self, expresion1, expresion2, operador):
        self.expresion1 = expresion1
        self.expresion2 = expresion2
        self.operador = operador

class ExpresionUnaria(Expresion) :
    #CLASE PARA LA EXPRESION UNARIA
    def __init__(self, operador, expresion) :
        self.operador = operador
        self.expresion = expresion

class ExpresionPotencia(Expresion):
    #clase para la expresion potencia
    def __init__(self, tipo, tipoP, expresion1, expresion2):
        self.tipo = tipo
        self.tipoP = tipoP.value
        self.expresion1 = expresion1
        self.expresion2 = expresion2

class ExpresionInicial(Expresion):
    #clase para las expresiones que son valores
    def __init__(self, expresion):
        self.expresion = expresion

class ExpresionInstruccion(Expresion):
    #clase para la expresion if
    def __init__(self, instruccion):
        self.instruccion = instruccion

class ExpresionAcceso(Expresion):
    #clase para la expresion de acceso a arreglo o vector
    def __init__(self, acceso):
        self.id = acceso[0]
        self.acceso = acceso[1]

class ExpresionAccesoStruct(Expresion):
    #clase para la expresion de acceso a struct
    def __init__(self, acceso):
        self.id = acceso[0]
        self.atributo = acceso[1:]
class ExpresionRemove(Expresion):
    #clase para la expresion remove (vector)
    def __init__(self, id, posicion):
        self.id = id
        self.posicion = posicion

class ExpresionContains(Expresion):
    #clase para la expresion contains (vector)
    def __init__(self, id, expresion):
        self.id = id
        self.expresion = expresion

class ExpresionLen(Expresion):
    #clase para la expresion contains (vector)
    def __init__(self, id):
        self.id = id

class ExpresionCapacity(Expresion):
    #clase para la expresion contains (vector)
    def __init__(self, id):
        self.id = id

class ExpresionLlamada(Expresion):
    #clase para la expresion llamada a funcion
    def __init__(self, id, parametros):
        self.id = id
        self.parametros = parametros

class ExpresionAbsoluto(Expresion):
    #clase para la expresion de valor absoluto
    def __init__(self, expresion):
        self.expresion = expresion

class ExpresionRaiz(Expresion):
    #clase para la expresion de valor absoluto
    def __init__(self, expresion):
        self.expresion = expresion

class ExpresionToString(Expresion):
    #clase para la expresion de valor absoluto
    def __init__(self, expresion):
        self.expresion = expresion

class ExpresionClone(Expresion):
    #clase para la expresion de valor absoluto
    def __init__(self, id):
        self.id = id

class ExpresionCasteo(Expresion):
    #clase para la expresion casteo
    def __init__(self, expresion, tipo):
        self.expresion = expresion
        self.tipo = tipo

class ExpresionLlamadaDB(Expresion):
    #clase para la llamada a funcion de DB
    def __init__(self, listamod, parametros):
        self.listamod = listamod
        self.parametros = parametros

class ExpresionAccesoAtributoDB(Expresion):
    #clase para el acceso a un atributo de una tabla
    def __init__(self, acceso):
        self.id = acceso[0]
        self.posicion = acceso[1]
        self.atributo = acceso[2]
