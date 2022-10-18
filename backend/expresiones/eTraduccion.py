from instrucciones.instrucciones import Loop, If, If_Else, TamanioTipo
from expresiones.expresiones import *
from expresiones.aritmetica import *
from expresiones.logica import *
from expresiones.relacional import *



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
                               
            elif expresion.expresion.type == "CADENA":
                temporal = data.obtenerTemporal()
                data.consola.concatenar("\n")
                data.consola.concatenar("heap[(int)H] = "+ str(len(expresion.expresion.value))+";")
                data.consola.concatenar("\n")
                data.consola.concatenar("H = H + 1;")
                for caracter in expresion.expresion.value:
                    ascii_char = str(ord(caracter))
                    data.consola.concatenar("\n")
                    data.consola.concatenar("heap[(int)H] = "+ ascii_char+";")
                    data.consola.concatenar("\n")
                    data.consola.concatenar("H = H + 1;")
                return
                
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
        '''
        elif isinstance(expresion, ExpresionRaiz):
            resultado = Retorno()
            dato = self.traducir_expresion(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == 0 or dato.tipo == "error":
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, dato.linea, dato.columna, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else: 
                if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                    resultado.tipo = "DECIMAL"
                    resultado.valor = pow(dato.valor, 0.5)
                else:
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("no es posible calcular la raiz, la expresion no es numerica", temp_ambito, dato.linea, dato.columna, data.texto)
                    resultado.tipo = "error"
                    resultado.valor = "error"
            return resultado

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
        
        elif isinstance(expresion, ExpresionAcceso): 
            resultado = Retorno()
            simbol = data.ts.obtener(expresion.id.value)
            if simbol == 0:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    try:
                        temp1 = simbol.valor
                        for i in expresion.acceso:
                            dato = self.traducir_expresion(i, data)
                            if dato.tipo == "ENTERO":
                                temp1 = temp1[dato.valor]
                            
                        resultado.valor = temp1
                        resultado.tipo = simbol.tipoDato
                    except:
                        resultado.tipo = "error"
                        resultado.valor = "error"
                        temp_ambito = data.ts.nombre_entorno()
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
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
        
        elif isinstance(expresion, ExpresionCasteo):
            resultado = Retorno()
            dato = self.traducir_expresion(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                if expresion.tipo.type == "FLOAT":
                    resultado.valor = float(dato.valor)
                    resultado.tipo = "DECIMAL"
                elif expresion.tipo.type == "INT":
                    resultado.valor = int(dato.valor)
                    resultado.tipo = "ENTERO"
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ts.nombre_entorno()
                    data.errores.insertar("el valor no se puede castear a un tipo que no sea decimal o entero", temp_ambito, expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
            else:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ts.nombre_entorno()
                data.errores.insertar("el valor a castear no es entero o decimal", temp_ambito, expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
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

        