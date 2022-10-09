class Instruccion:
    '''clase abstracta'''

class Imprimir(Instruccion) :
    #clase para la instruccion imprimir

    def __init__(self,  cadena) :
        self.cadena = cadena

class Imprimire(Instruccion) :
    #clase para la instruccion imprimir con expresiones

    def __init__(self,  cadena, expresiones) :
        self.cadena = cadena
        self.expresiones = expresiones

class DeclaracionMutable1(Instruccion) :
    #clase para instruccion declaracion mutable sin tipo dato, solo recibe el id
    def __init__(self, id, expresion) :
        self.id = id
        self.expresion = expresion

class DeclaracionMutable2(Instruccion) :
    #clase para instruccion declaracion mutable con tipo dato, solo recibe el id
    def __init__(self, id, tipoDato, expresion) :
        self.id = id
        self.tipoDato = tipoDato
        self.expresion = expresion

class Declaracion1(Instruccion) :
    #clase para instruccion declaracion inmutable sin tipo dato, solo recibe el id
    def __init__(self, id, expresion) :
        self.id = id
        self.expresion = expresion

class Declaracion2(Instruccion) :
    #clase para instruccion declaracion inmutable con tipo dato, solo recibe el id
    def __init__(self, id, tipoDato, expresion) :
        self.id = id
        self.tipoDato = tipoDato
        self.expresion = expresion

class Asignacion(Instruccion) :
    #clase para la instruccion asignacion, recibe el id y el valor a asignar

    def __init__(self, id, expresion) :
        self.id = id
        self.expresion = expresion

class If(Instruccion):
    #clase para la instruccion if
    def __init__(self, condicion, instrucciones):
        self.condicion = condicion
        self.instrucciones = instrucciones

class If_Else(Instruccion):
    #clase para la instruccion if else
    def __init__(self, condicion, instrucciones, ielse):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.ielse = ielse
    
class While(Instruccion):
    #clase para la instruccion while
    def __init__(self, condicion, instrucciones):
        self.condicion = condicion
        self.instrucciones = instrucciones

class For(Instruccion):
    #clase para la instruccion while
    def __init__(self, variable, arreglo, inicio, fin, instrucciones):
        self.variable = variable
        self.arreglo = arreglo
        self.inicio = inicio
        self.fin = fin
        self.instrucciones = instrucciones

class Break(Instruccion):
    #clase para la instruccion break
    def __init__(self, expresion):
        self.expresion = expresion

class Continue(Instruccion):
    #clase para la instruccion continue
    def __init__(self):
        '''creo que este no lleva nada'''

class Loop(Instruccion):
    #clase para la instruccion loop
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
    
class Funcion(Instruccion):
    #clase para las funciones
    def __init__(self, nombre, tipo, parametros, instrucciones):
        self.nombre = nombre
        self.tipo = tipo
        self.parametros = parametros
        self.instrucciones = instrucciones
    
class Struct(Instruccion):
    #clase para los structs
    def __init__(self, nombre, campos):
        self.nombre = nombre
        self.campos = campos

class Modulo(Instruccion):
    #clase para los moduolos
    def __init__(self, nombre, instrucciones):
        self.nombre = nombre
        self.instrucciones = instrucciones

class DeclaracionArreglo(Instruccion):
    #clase para la declaracion de arreglos
    def __init__(self, nombre, tamanio, expresiones):
        self.nombre = nombre
        self.tamanio = tamanio
        self.expresiones = expresiones

class DeclaracionArregloM(Instruccion):
    #clase para la declaracion de arreglos
    def __init__(self, nombre, tamanio, expresiones):
        self.nombre = nombre
        self.tamanio = tamanio
        self.expresiones = expresiones

class DeclaracionArregloST(Instruccion):
    #clase para la declaracion de arreglos
    def __init__(self, nombre, expresiones):
        self.nombre = nombre
        self.expresiones = expresiones

class DeclaracionArregloMST(Instruccion):
    #clase para la declaracion de arreglos
    def __init__(self, nombre, expresiones):
        self.nombre = nombre
        self.expresiones = expresiones

class TamanioTipo(Instruccion):
    #clase para el tamaño tipo
    def __init__ (self, tipo, tamanio):
        self.tipo = tipo
        self.tamanio = tamanio

class DeclaracionVector(Instruccion):
    #clase para la declaracion de vectores
    def __init__(self, nombre, tipo, valor, capacidad, mutable):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.capacidad = capacidad
        self.mutable = mutable

class DeclaracionVector2(Instruccion):
    #clase para la declaracion de vectores (new, with capacity)
    def __init__(self, nombre, tipo, mutable, capacidad):
        self.nombre = nombre
        self.tipo = tipo
        self.mutable = mutable
        self.capacidad = capacidad
    
class ModificarArray(Instruccion):
    #clase para la instruccion de acceso a vector
    def __init__(self, acceso, expresion):
        self.acceso = acceso
        self.expresion = expresion

class ImprimirV(Instruccion):
    #clase para imprimir vectores y arreglos
    def __init__(self, cadena, expresion):
        self.cadena = cadena
        self.expresion = expresion

class Vpush(Instruccion):
    #clase para la operacon push con vectores
    def __init__(self, id, expresion):
        self.id = id
        self.expresion = expresion

class VpushV(Instruccion):
    #clase para la operacon push con vectores
    def __init__(self, id, arreglo):
        self.id = id
        self.arreglo = arreglo

class Vinsert(Instruccion):
    #clase para la operacion insertar con vectores
    def __init__(self, id, posicion, expresion):
        self.id = id
        self.posicion = posicion
        self.expresion = expresion

class Vremove(Instruccion):
    #clase para la operacion remover con vectores
    def __init__(self, id, posicion):
        self.id = id
        self.posicion = posicion
        
class LlamadaFuncion(Instruccion):
    #clase para la instruccion llamada a funcion
    def __init__(self, id, parametros):
        self.id = id
        self.parametros = parametros

class Return(Instruccion):
    #clase para la instruccion retorno
    def __init__(self, expresion):
        self.expresion = expresion

class DeclaracionStruct(Instruccion):
    #clase para la declaracion de struct
    def __init__(self, id, idStruct, campos, mutable):
        self.id = id
        self.idStruct = idStruct
        self.campos = campos
        self.mutable = mutable

class ModificarStruct(Instruccion):
    #clase para la modificacion de un struct
    def __init__(self, id_atributo, expresion):
        self.id_atributo = id_atributo
        self.expresion = expresion

class DeclaracionVectorT(Instruccion):
    #clase para la declaracion de una tabla Db
    def __init__(self, id, listamod):
        self.id = id
        self.listamod = listamod

class LlamadaFuncionDB(Instruccion):
    #clase para la llamada de una funcion en db
    def __init__(self, listamod, parametros):
        self.listamod = listamod
        self.parametros = parametros

class ModificacionAtributo(Instruccion):
    #clase para la modificacion de un atributo o asignacion
    def __init__(self, acceso, expresion):
        self.id = acceso[0]
        self.posicion = acceso[1]
        self.atributo = acceso[2]
        self.expresion = expresion

class AsignacionVectorDB(Instruccion):
    #clase para el inicio de la tabla
    def __init__(self, nombre, tipo, mutable, capacidad):
        self.nombre = nombre
        self.tipo = tipo
        self.mutable = mutable
        self.capacidad = capacidad



##instrucciones de mod