from instrucciones.instrucciones import TamanioTipo
from ts import Simbolo
from expresiones.operacion import *


#estas funciones seran para la tabla de simbolos, mas adelante hare la separacion
#donde comenzaran las funciones para la traduccion, mejor en otro archivo :v
def procesar_funcion_global(nombre, tipo, parametros, instrucciones, data):
    data.pStack = 0
    tipo_dato = ""
    if tipo == None:
        tipo_dato = "Void"
        columna = find_column(data.texto, nombre.lexpos)
        simbolo_temporal = Simbolo(nombre.value, tipo_dato, "Funcion",0, data.ts.nombre_entorno(), False, nombre.lineno, columna, -1, data.pHeap)
        simbolo_temporal.instrucciones = instrucciones
        data.ts.ingresar(simbolo_temporal)
        data.ts.nombre.append(nombre.value)
        data.pHeap+=1
        
    else:
        tipo_simbolo = "Funcion"
        if isinstance(tipo, list):
            tipo_dato += "Vector:"
            if tipo[1].type == "ID":
                tipo_dato += tipo[1].value
            else:
                tipo_dato += tipoDato(tipo[1].value)
            
        elif tipo.type == "ID":
            tipo_dato = tipo.value
        else:
            tipo_dato = tipoDato(tipo.value)
        
        columna = find_column(data.texto, nombre.lexpos)
        data.ts.ingresar(Simbolo(nombre.value, tipo_dato, tipo_simbolo, 0, data.ts.nombre_entorno(), False, nombre.lineno, columna, -1, data.pHeap))
        data.ts.nombre.append(nombre.value)
        data.pHeap += 1

    columna = find_column(data.texto, nombre.lexpos)
    tipo_simbolo = "Variable"
    data.ts.ingresar(Simbolo("return", tipo_dato, tipo_simbolo, 1, data.ts.nombre_entorno(), True, nombre.lineno, columna, data.pStack, -1))
    data.pStack += 1
    #aqui vemos si hay parametros
    if parametros != None:
        procesar_parametros(parametros, data)

    from interprete import procesar_instrucciones_ts
    procesar_instrucciones_ts(instrucciones, data)

    simbolo_temporal.tamanio = data.pStack
    data.ts.modificar_tamanio(simbolo_temporal)

#Simbolo(nombre.value, tipo_dato, tipo_simbolo, 0, data.ts.nombre_entorno(), False, nombre.lineno, columna, -1, data.pHeap)
def procesar_parametros(parametros, data):
    for i in range(len(parametros)):
        tipo_dato = parametros[i].tipo
        if parametros[i].isReferencia == "A":
            tipo_simbolo = "Arreglo"
        elif parametros[i].isReferencia == "V":
            tipo_simbolo = "Vector"
        else:
            tipo_simbolo = "Variable"
        columna = find_column(data.texto, parametros[i].id.lexpos)
        simbolo_temporal = Simbolo(parametros[i].id, tipo_dato, tipo_simbolo, 1, data.ts.nombre_entorno(), True, parametros[i].id.lineno, columna, data.pStack, -1)
        data.ts.ingresar(simbolo_temporal)
        data.pStack += 1

def procesar_declaracion1_ts(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    columna = find_column(data.texto, id.lexpos)
    #id.value, dato.valor, dato.tipoS, dato.tipo, temp_ambito, False, id.lineno, id.lexpos, data.texto
    simbolo_temporal = Simbolo(id.value, dato.tipo, dato.tipoS, 1, data.ts.nombre_entorno(), False, id.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion2_ts(id, tipo, expresion, data):
    tipo_dato = tipoDato(tipo.value)
    columna = find_column(data.texto, id.lexpos)
    simbolo_temporal = Simbolo(id.value, tipo_dato, "Variable", 1, data.ts.nombre_entorno(), False, id.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracionM1_ts(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    columna = find_column(data.texto, id.lexpos)
    simbolo_temporal = Simbolo(id.value, dato.tipo, dato.tipoS, 1, data.ts.nombre_entorno(), True, id.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracionM2_ts(id, tipo, expresion, data):
    tipo_dato = tipoDato(tipo.value)
    columna = find_column(data.texto, id.lexpos)
    simbolo_temporal = Simbolo(id.value, tipo_dato, "Variable", 1, data.ts.nombre_entorno(), True, id.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_arreglo_ts(nombre, tamanio, expresiones, data):
    tipo_simbolo = "Arreglo"
    columna = find_column(data.texto, nombre.lexpos)
    longitud = []
    tt = tamanio_tipo(longitud, tamanio)
    simbolo_temporal = Simbolo(nombre.value, tt[1], tipo_simbolo, 1, data.ts.nombre_entorno(), False, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_arreglo_mutable_ts(nombre, tamanio, expresiones, data):
    tipo_simbolo = "Arreglo"
    columna = find_column(data.texto, nombre.lexpos)
    longitud = []
    tt = tamanio_tipo(longitud, tamanio)
    simbolo_temporal = Simbolo(nombre.value, tt[1], tipo_simbolo, 1, data.ts.nombre_entorno(), True, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_arreglo_mutable_st_ts(nombre, expresiones, data):
    tt = calcular_tipo_array(expresiones, data)
    tipo_simbolo = "Arreglo"
    columna = find_column(data.texto, nombre.lexpos)
    simbolo_temporal = Simbolo(nombre.value, tt, tipo_simbolo, 1, data.ts.nombre_entorno(), True, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_arreglo_st_ts(nombre, expresiones, data):
    tt = calcular_tipo_array(expresiones, data)
    tipo_simbolo = "Arreglo"
    columna = find_column(data.texto, nombre.lexpos)
    simbolo_temporal = Simbolo(nombre.value, tt, tipo_simbolo, 1, data.ts.nombre_entorno(), False, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_vector_ts(nombre, tipo, valor, capacidad, mutable, data):
    tipo_simbolo = "Vector"
    is_vector = False
    columna = find_column(data.texto, nombre.lexpos)
    op = Operacion()
    if isinstance(valor[0], list):
        is_vector = True
    else:
        dato = op.ejecutar(valor[0], data)
        tipo1 = dato.tipo
    tt = None
    if is_vector:
        dato = op.ejecutar(valor[0][0])
        tt = dato.tipo
    else:
        dato = op.ejecutar(valor[0])
        tt = dato.tipo
    simbolo_temporal = Simbolo(nombre.value, tt, tipo_simbolo, 1, data.ts.nombre_entorno(), mutable, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_declaracion_vector2_ts(nombre, tipo, mutable, capacidad, data):
    tipo_simbolo = "Vector"
    columna = find_column(data.texto, nombre.lexpos)
    tipo_dato = None
    if tipo.type == "ID":
        tipo_dato = tipo.value
    else:
        tipo_dato = tipoDato(tipo.value)
    simbolo_temporal = Simbolo(nombre.value, tipo_dato, tipo_simbolo, 1, data.ts.nombre_entorno(), mutable, nombre.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1

def procesar_if_ts(condicion, instrucciones, data):
    from interprete import procesar_instrucciones_ts
    data.ts.nombre.append("if")
    procesar_instrucciones_ts(instrucciones, data)
    data.ts.nombre.pop()

def procesar_if_else_ts(condicion, instrucciones, ielse, data):
    from interprete import procesar_instrucciones_ts
    data.ts.nombre.append("if")
    procesar_instrucciones_ts(instrucciones, data)
    data.ts.nombre.pop()

    from instrucciones.instrucciones import If_Else
    from instrucciones.instrucciones import If
    if isinstance(ielse, If_Else) : procesar_if_else_ts(ielse.condicion, ielse.instrucciones, ielse.ielse, data)
    elif isinstance(ielse, If) : procesar_if_ts(ielse.condicion, ielse.instrucciones, data)
    else:
        data.ts.nombre.append("else")
        procesar_instrucciones_ts(instrucciones, data)
        data.ts.nombre.pop()

def procesar_while_ts(condicion, instrucciones, data):
    from interprete import procesar_instrucciones_ts
    data.ts.nombre.append("while")
    procesar_instrucciones_ts(instrucciones, data)
    data.ts.nombre.pop()

def procesar_for_ts(variable, arreglo, inicio, fin, instrucciones, data):
    from interprete import procesar_instrucciones_ts
    data.ts.nombre.append("for")
    columna = find_column(data.texto, variable.lexpos)
    simbolo_temporal = Simbolo(variable.value, None, "Variable", 1, data.ts.nombre_entorno(), True, variable.lineno, columna, data.pStack, -1)
    data.ts.ingresar(simbolo_temporal)
    data.pStack += 1
    procesar_instrucciones_ts(instrucciones, data)
    data.ts.nombre.pop()

def procesar_loop_ts(instrucciones, data):
    from interprete import procesar_instrucciones_ts
    data.ts.nombre.append("loop")
    procesar_instrucciones_ts(instrucciones, data)
    data.ts.nombre.pop()

#estas funciones son para encontrar posiciones, tipos de dato para la ts
def find_column(input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "usize": return "ENTERO"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"
    else: return dato

def tamanio_tipo(longitud, tt):
    longitud.append(tt.tamanio.value)
    if isinstance(tt.tipo, TamanioTipo):
        return tamanio_tipo(longitud, tt.tipo)
    else:
        temp = []
        temp.append(longitud)
        temp.append(tipoDato(tt.tipo.value))
        return temp

def calcular_tipo_array(expresiones, data):
    if isinstance(expresiones, ExpresionInicial):
        op = Operacion()
        dato = op.ejecutar(expresiones, data)
        return dato.tipo
    else:
        for i in expresiones:
            temp = calcular_tipo_array(i, data)
            
        return temp