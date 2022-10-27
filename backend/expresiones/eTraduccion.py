from instrucciones.instrucciones import Loop, If, If_Else, TamanioTipo
from expresiones.expresiones import *
from expresiones.aritmetica import *
from expresiones.logica import *
from expresiones.relacional import *
from expresiones.operacion import Operacion


class TraductorExp():
    def __init__(self):
        '''se hara una copia casi de operacion pero en vez de operar, traducira'''
    
    def traducir_expresion(self, expresion, data):
        
        if isinstance(expresion, ExpresionAritmetica):
            exp1 = self.traducir_expresion(expresion.expresion1, data)
            exp2 = self.traducir_expresion(expresion.expresion2, data)
            return t_aritmetica(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionLogica):
            exp1 = self.traducir_expresion(expresion.expresion1, data)
            exp2 = self.traducir_expresion(expresion.expresion2, data)
            return t_logica(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionRelacional):
            exp1 = self.traducir_expresion(expresion.expresion1, data)
            exp2 = self.traducir_expresion(expresion.expresion2, data)
            return t_relacional(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)
        
        elif isinstance(expresion, ExpresionUnaria):
            exp1 = self.traducir_expresion(expresion.expresion, data)
            return t_unaria(exp1, expresion.operador, exp1.linea, exp1.columna, data)
        
        elif isinstance(expresion, ExpresionPotencia):
            exp1 = self.traducir_expresion(expresion.expresion1, data)
            exp2 = self.traducir_expresion(expresion.expresion2, data)
            return potencia(exp1, exp2, expresion.tipo, expresion.tipoP, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionInicial):
            if expresion.expresion.type == "TRUE" or expresion.expresion.type == "FALSE":
                if expresion.expresion.value.upper() == "TRUE":
                    te =  Texp(str(1), "",expresion.expresion.lineno,0)
                    te.tipo = "BOOL"
                elif expresion.expresion.value.upper() == "FALSE":
                    te =  Texp(str(0), "",expresion.expresion.lineno,0)
                    te.tipo = "BOOL"
            elif expresion.expresion.type == "ID":
                simbol = data.ts.obtener(expresion.expresion.value, data.pStack, data.pHeap)
                if simbol == 0:
                    te = "error"
                    data.errores.insertar("la variable a acceder no existe", 0, expresion.expresion.lineno, expresion.expresion.lexpos, data.texto)
                else:
                    te =  Texp(str(expresion.expresion.value), "",expresion.expresion.lineno,0) 
                    puntero = data.ts.obtener_puntero_stack(expresion.expresion.value, data.pStack, data.pHeap)
                    temporal = data.obtenerTemporal()
                    te.codigo = te.codigo + "\n"
                    te.codigo = te.codigo + temporal+" = P + "+str(puntero)+";"
                    te.codigo = te.codigo +"\n"
                    temporal = data.obtenerTemporal()
                    te.codigo = te.codigo + temporal+" = stack[(int)"+ data.obtenerTemporalAnterior()+"];"
                    te.direccion = temporal
                    te.tipo = simbol.tipoDato
                    te.valor = simbol.valor
                               
            elif expresion.expresion.type == "CADENA":
                te =  Texp(None, None,expresion.expresion.lineno,0)
                te.tipo = "CADENA"
                te.valor = expresion.expresion.value
                return te
                
            elif expresion.expresion.type == "CARACTER":
                ascii_char = str(ord(expresion.expresion.value))
                te = Texp(ascii_char, "",expresion.expresion.lineno,0)
            elif expresion.expresion.type == "ENTERO":
                te =  Texp(str(expresion.expresion.value), "",expresion.expresion.lineno,0)
                te.tipo = "ENTERO"
            elif expresion.expresion.type == "DECIMAL":
                te =  Texp(str(expresion.expresion.value), "",expresion.expresion.lineno,0)
                te.tipo = "DECIMAL"
            return te

        elif isinstance(expresion, ExpresionAbsoluto):
            dato = self.traducir_expresion(expresion.expresion, data)
            
            if dato == "error":
                data.errores.insertar("el id al que se intenta accesar no existe", "", dato.linea, dato.columna, data.texto)
                dato = "error"
            else:
                if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                    dato.tipo = dato.tipo
                    etiquetaV = data.obtenerEtiqueta()
                    etiquetaF = data.obtenerEtiqueta()
                    cadena_temp = dato.codigo
                    cadena_temp += "\nif("+dato.direccion+" < 0) goto "+etiquetaV+";"
                    cadena_temp += "\n"
                    cadena_temp += "goto "+etiquetaF+";"
                    cadena_temp += "\n"
                    cadena_temp += etiquetaV +": "
                    cadena_temp += "\n"
                    cadena_temp += dato.direccion +" = 0-"+dato.direccion +";"
                    cadena_temp += "\n"
                    cadena_temp += etiquetaF+": "
                    dato.codigo = cadena_temp
                else:
                    data.errores.insertar("no es posible calcular el valor absoluto, la expresion no es numerica", "", dato.linea, dato.columna, data.texto)
                    dato.tipo = "error"
            return dato

        elif isinstance(expresion, ExpresionAcceso): 
            te = Texp("","", expresion.id.lineno, 0)
            error_comprobacion = False
            simbol = data.ts.obtener(expresion.id.value, 0, len(data.ts.simbolos))
            if simbol == 0:
                    te = "error"
                    data.errores.insertar("el id al que se intenta accesar no existe", "", expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    
                    if len(simbol.dimensiones) == len(expresion.acceso):
                        te.tipo = simbol.tipoDato
                        posicion = acceso_posicion(expresion.acceso,simbol.dimensiones, data)
                        if posicion == "error":
                            error_comprobacion = True
                        temporal = data.obtenerTemporal()
                        cadena_temp = "\n"
                        te.direccion = temporal
                        traductor = self.traducir_expresion(ExpresionInicial(expresion.id), data)
                        cadena_temp += traductor.codigo
                        cadena_temp += "\n"
                        cadena_temp += traductor.direccion+" = "+traductor.direccion+" + 1;"
                        cadena_temp += "\n"
                        cadena_temp += traductor.direccion+" = "+traductor.direccion+" + "+str(posicion)+";"
                        cadena_temp += "\n"
                        cadena_temp += temporal+" = heap[(int)"+traductor.direccion+"];"
                        te.codigo = cadena_temp
                    #este de aqui solo aplica para la impresion
                    elif len(simbol.dimensiones) > len(expresion.acceso):
                        te.tipo = simbol.tipoDato
                        te.tipoS = "Arreglo"
                        from tipoDato import ParaLex
                        a = ParaLex()
                        a.value = 0
                        a.type = "ENTERO"
                        expresion.acceso.append(ExpresionInicial(a))
                        posicion = acceso_posicion(expresion.acceso,simbol.dimensiones, data)
                        if posicion == "error":
                            error_comprobacion = True
                        cadena_temp = "\n"
                        traductor = self.traducir_expresion(ExpresionInicial(expresion.id), data)
                        cadena_temp += traductor.codigo
                        cadena_temp += "\n"
                        cadena_temp += traductor.direccion+" = "+traductor.direccion+" + 1;"
                        cadena_temp += "\n"
                        cadena_temp += traductor.direccion+" = "+traductor.direccion+" + "+str(posicion)+";"
                        te.codigo = cadena_temp
                        te.direccion = traductor.direccion
                        te.dimension = simbol.dimensiones[len(simbol.dimensiones)-1]
                    
                else:
                    te = "error"
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", "", expresion.id.lineno, expresion.id.lexpos, data.texto)
            if error_comprobacion:
                te = "error"
                print("hay que hacer la comprobacion")
            return te
        
        elif isinstance(expresion, ExpresionCasteo):
            
            dato = self.traducir_expresion(expresion.expresion, data)
            te = Texp("", "", dato.linea, dato.columna)
            if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                te.codigo = dato.codigo
                if expresion.tipo.type == "FLOAT":
                    te.direccion = dato.direccion
                    te.tipo = "DECIMAL"
                    te.valor = dato.valor
                elif expresion.tipo.type == "INT":
                    te.direccion = dato.direccion
                    te.valor = dato.valor
                    te.tipo = "ENTERO"
                else:
                    te = "error"
                    data.errores.insertar("el valor no se puede castear a un tipo que no sea decimal o entero", "", expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
            else:
                te = "error"
                data.errores.insertar("el valor a castear no es entero o decimal", "", expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
            return te
        
        
        elif isinstance(expresion, ExpresionRaiz):
            dato = self.traducir_expresion(expresion.expresion, data)
            te = Texp("", "", dato.linea, dato.columna)
            if dato.tipo == 0 or dato.tipo == "error":
                data.errores.insertar("el id al que se intenta accesar no existe", "", dato.linea, dato.columna, data.texto)
                te = "error"
            else: 
                if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                    te.tipo = "DECIMAL"
                    te.codigo = dato.codigo
                    temporal = data.obtenerTemporal()
                    te.valor = pow(dato.valor, 0.5)
                    te.codigo += "\n"+temporal+" = "+str(te.valor)+";"
                    te.direccion = temporal
                    
                else:
                    data.errores.insertar("no es posible calcular la raiz, la expresion no es numerica", "", dato.linea, dato.columna, data.texto)
                    te = "error"
            return te        
        
        '''
        elif isinstance(expresion, ExpresionClone):
            resultado = Retorno()
            resultado.linea = expresion.id.lineno
            resultado.columna = expresion.id.lexpos
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                resultado.tipo = simbol.tipoDato
                resultado.valor = simbol.valor
            return resultado
        
        

        

        elif isinstance(expresion, ExpresionToString):
            resultado = Retorno()
            dato = self.traducir_expresion(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == 0 or dato.tipo == "error":
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("la expreson no es valida", temp_ambito, dato.linea, dato.columna, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                resultado.tipo = 'CADENA'
                resultado.valor = str(dato.valor)
            return resultado'''

        '''
        elif isinstance(expresion, ExpresionInstruccion):
            resultado = Retorno()
            if isinstance(expresion.instruccion, Loop):  resultado = expresion_loop(expresion.instruccion.instrucciones, data)
            elif isinstance(expresion.instruccion, If):  resultado = expresion_if(expresion.instruccion.condicion, expresion.instruccion.instrucciones, data)
            elif isinstance(expresion.instruccion, If_Else): resultado = expresion_elif(expresion.instruccion.condicion, expresion.instruccion.instrucciones, expresion.instruccion.ielse, data)
            else: print("la expresion instruccion a buscar no es valida")
            return resultado
        
        

        elif isinstance(expresion, ExpresionRemove):
            resultado = Retorno()
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Vector" and simbol.mutable:
                    temp = simbol.valor
                    resultado.tipo = simbol.tipoDato
                    posicion = self.traducir_expresion(expresion.posicion, data)
                    resultado.valor = temp.pop(posicion.valor)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector o el vector no es mutable", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

        elif isinstance(expresion, ExpresionContains):
            resultado = Retorno()
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    dato = self.traducir_expresion(expresion.expresion, data)
                    if dato.tipo == simbol.tipoDato:
                        resultado.tipo = "BOOL"
                        resultado.valor = dato.valor in simbol.valor
                    else:
                        resultado.tipo = "error"
                        resultado.valor = "error"
                        temp_ambito = data.ts.nombre_entorno()
                        data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado
        
        
        
        

        elif isinstance(expresion, ExpresionCapacity):
            resultado = Retorno()
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Vector":
                    resultado.tipo = "ENTERO"
                    if simbol.capacidad == None:
                        resultado.valor = len(simbol.valor)+1
                    else:
                        resultado.valor = encontrar_capacidad(simbol.valor, simbol.capacidad)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

        elif isinstance(expresion, ExpresionLen):
            resultado = Retorno()
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    resultado.tipo = "ENTERO"
                    resultado.valor = len(simbol.valor)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado
        
        elif isinstance(expresion, ExpresionLlamada):
            resultado = expresion_llamada(expresion.id, expresion.parametros, data)
            return resultado
        
        

        elif isinstance(expresion, ExpresionAccesoStruct):
            buscar = self.traducir_expresion(ExpresionInicial(expresion.id), data)
            resultado = devolver_struct(buscar.valor, expresion.atributo)
            return resultado
        
        elif isinstance(expresion, ExpresionLlamadaDB):
            id = expresion.listamod[len(expresion.listamod)-1]
            listamod = expresion.listamod[:len(expresion.listamod)-1]
            buscar = 0
            temp = data.modulos
            for mod in listamod:
                buscar = temp.obtener(mod.value)
                if buscar != 0:
                    temp = buscar.mod
            resultado = expresion_llamadaDB(id, expresion.parametros, buscar.fn, data)
            return resultado

        elif isinstance(expresion, ExpresionAccesoAtributoDB):
            resultado = expresion_acceso_atributo(expresion.id, expresion.posicion, expresion.atributo, data)
            return resultado
        else:
            print(expresion, "error expresion desconocida")'''

def acceso_posicion(acceso, dimensiones, data): #este retorna la posicion (row major) del arreglo siempre y cuando cumpla con las dimensiones
    hubo_error = False
    op = Operacion()
    posicion = 1
    value = []
    if len(acceso) == 1:
        dato = op.ejecutar(acceso[0], data)
        if dato.tipo == "ENTERO":
            if dato.valor < dimensiones[0] and dato.valor > -1:
                posicion = dato.valor
            else:
                posicion = "error"
        else:
            data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
    elif len(acceso) == 2:
        for i in range(len(acceso)):
            dato = op.ejecutar(acceso[i], data)
            if dato.tipo == "ENTERO":
                if dato.valor < dimensiones[i]:
                    hubo_error = False
                    value.append(dato.valor)
                else:
                    hubo_error = True
                    break
            else:
                data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
        if hubo_error != True:
            posicion = dimensiones[1]*value[0]+value[1]
        else:
            posicion = "error"


    elif len(acceso) == 3:
        for i in range(len(acceso)):
            dato = op.ejecutar(acceso[i], data)
            if dato.tipo == "ENTERO":
                if dato.valor < dimensiones[i]:
                    hubo_error = False
                    value.append(dato.valor)
                else:
                    hubo_error = True
                    break
            else:
                data.errores.insertar("no se utilizo un entero para el acceso al arreglo", "", acceso[0].lineno, acceso[0].lexpos, data.texto)
        if hubo_error != True:
            posicion = dimensiones[2]*dimensiones[1]*value[0]
            posicion += dimensiones[2]*value[1]+value[2]
        else:
            posicion = "error"
    return posicion

