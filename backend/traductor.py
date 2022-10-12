from expresiones.operacion import *
from expresiones.eTraduccion import *

def procesar_imprimir(inst, data):
    op = Operacion()
    dato = op.ejecutar(inst, data)

    if dato.tipo == "CADENA":
        for caracter in dato.valor:
            ascii_char = str(ord(caracter))
            data.consola.concatenar(f"printf(\"%c\", {ascii_char}); ")
            data.consola.concatenar("\n")
        data.consola.concatenar("printf(\"%c\", 10); ")
        data.consola.concatenar("\n")
    else:
        temp_ambito = data.ts.nombre_entorno()
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    
def procesar_imprimire(cadena, expresiones, data):
    op = Operacion()
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA":
        if "{:?}" in dato.valor:
            procesar_imprimirV(cadena, expresiones[0], data)
        else:
            temp = dato.valor.split("{}")
            if len(temp)-1 == len(expresiones):
                cadena_temp = "\n"
                tipo_impresion = ""
                casteo = ""
                hubo_error = False
                for i in range(len(expresiones)):
                    cadena_temp += "\n"
                    for caracter in temp[i]:
                        ascii_char = str(ord(caracter))
                        cadena_temp += "\n"
                        cadena_temp += f"printf(\"%c\", {ascii_char}); "

                    exp_temp = op.ejecutar(expresiones[i], data)
                    #print(exp_temp.tipo)
                    if(exp_temp.valor == "error"):
                        hubo_error = True
                        break
                    elif exp_temp.tipo == "ENTERO":
                        tipo_impresion = "d"
                        casteo = "(int)"
                    elif exp_temp.tipo == "DECIMAL":
                        tipo_impresion = "f"
                    elif exp_temp.tipo == "CARACTER":
                        tipo_impresion = "c"
                        casteo = "(int)"
                    elif exp_temp.tipo == "CADENA":
                        tipo_impresion = "c"
                        casteo = "(int)"
                    elif exp_temp.tipo == "BOOL":
                        tipo_impresion = "d"
                        casteo = "(int)"

                    if exp_temp.tipo == "CADENA":
                        cadena_temp += "\n"
                        tr = TraductorExp()
                        traduccion = tr.traducir_expresion(expresiones[i], data)
                        cadena_temp += traduccion.codigo
                        cadena_temp += "\n"
                        
                        etiqueta1 = data.obtenerEtiqueta()
                        etiqueta2 = data.obtenerEtiqueta()

                        temporal1 = traduccion.direccion
                        temporal2 = data.obtenerTemporal()
                        temporal3 = data.obtenerTemporal()
                        cadena_temp += temporal2+" = "
                        cadena_temp += f"heap[(int){temporal1}];"
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = 0;"
                        cadena_temp += "\n"
                        cadena_temp += temporal1+" = "+temporal1+" + 1;"
                        cadena_temp += "\n"
                        cadena_temp += temporal2+" = "+temporal2+" + "+temporal1+";"
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = "+temporal3+" + "+temporal1+";"
                        cadena_temp += "\n"

                        #aqui va el if
                        cadena_temp += etiqueta1+":\n"
                        cadena_temp += "if("+temporal2+"=="+temporal3+") goto "+etiqueta2+";\n"
                        cadena_temp += temporal1+" = heap[(int)"+temporal3+"];\n"
                        cadena_temp += f"printf(\"%{tipo_impresion}\", {casteo}{temporal1}); "
                        cadena_temp += "\n"
                        cadena_temp += temporal3+" = "+temporal3+" + 1;\n"
                        cadena_temp += "goto "+etiqueta1+";\n"
                        cadena_temp += etiqueta2+":\n"

                    else:
                        tr = TraductorExp()
                        traduccion = tr.traducir_expresion(expresiones[i], data)
                        cadena_temp += "\n"
                        cadena_temp += traduccion.codigo
                        cadena_temp += "\n"
                        cadena_temp += f"printf(\"%{tipo_impresion}\", {casteo}{traduccion.direccion}); "

                for i in range(len(temp)-1, len(temp)):
                    ascii_char = str(ord(caracter))
                    
                    cadena_temp += "\n"
                    cadena_temp += f"printf(\"%c\", {ascii_char}); "
                    cadena_temp += "\n"
                    cadena_temp += "printf(\"%c\", 10);"

                if hubo_error:
                    data.errores.insertar("la expresion a mostrar no es valida", "", dato.linea, dato.columna, data.texto)
                else:
                    data.consola.concatenar(cadena_temp)
            else:
                data.errores.insertar("la cantidad de expresiones no es valida para imprimir en cadena", "", dato.linea, dato.columna, data.texto)
    else:
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", "", dato.linea, dato.columna, data.texto)
    
def procesar_imprimirV(cadena, expresion, data):
    print()

def procesar_declaracion1(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    if dato.tipo == "CADENA":
        puntero = data.ts.obtener_puntero_stack(id.value, data.pStack)
        temporal = data.obtenerTemporal()
        data.consola.concatenar("\n")
        data.consola.concatenar(temporal+ " = H;")
        data.consola.concatenar("\n")
        data.consola.concatenar("stack["+str(puntero)+"] = "+temporal+";")
        tr = TraductorExp()
        tr.traducir_expresion(expresion, data)
    else:
        #aqui traduzco la expresion
        tr = TraductorExp()
        traduccion = tr.traducir_expresion(expresion, data)
        if traduccion == "error":
            return
        data.consola.concatenar(traduccion.codigo)
        if traduccion.direccion[0] != "t":
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+" = "+traduccion.direccion+";")
            traduccion.direccion = temporal
        
        puntero = data.ts.obtener_puntero_stack(id.value, data.pStack)
        temporal = data.obtenerTemporal()
        data.consola.concatenar("\n")
        data.consola.concatenar(temporal+ " = P + "+str(puntero)+";")
        data.consola.concatenar("\n")
        data.consola.concatenar("stack[(int)"+temporal+"] = "+traduccion.direccion+";")

    
def procesar_declaracion2(id, tipo, expresion, data):
    
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    if dato.tipo == tipoDato(tipo.value):
        if dato.tipo == "CADENA":
            puntero = data.ts.obtener_puntero_stack(id.value, data.pStack)
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+ " = H;")
            data.consola.concatenar("\n")
            data.consola.concatenar("stack["+str(puntero)+"] = "+temporal+";")
            tr = TraductorExp()
            tr.traducir_expresion(expresion, data)
        else:
            #aqui traduzco la expresion
            tr = TraductorExp()
            traduccion = tr.traducir_expresion(expresion, data)
            if traduccion == "error":
                return
            data.consola.concatenar(traduccion.codigo)
            if traduccion.direccion[0] != "t":
                temporal = data.obtenerTemporal()
                data.consola.concatenar("\n")
                data.consola.concatenar(temporal+" = "+traduccion.direccion+";")
                traduccion.direccion = temporal
            
            puntero = data.ts.obtener_puntero_stack(id.value, data.pStack)
            temporal = data.obtenerTemporal()
            data.consola.concatenar("\n")
            data.consola.concatenar(temporal+ " = P + "+str(puntero)+";")
            data.consola.concatenar("\n")
            data.consola.concatenar("stack[(int)"+temporal+"] = "+traduccion.direccion+";")

    else:
        temp_ambito = ""
        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_declaracionM1(id, expresion, data):
    print("Soy una declaracion sin tipo, mutable")

def procesar_declaracionM2(id, tipo, expresion, data):
    print("soy una declaracion con tipo, mutable")

def procesar_funcion(nombre, tipo, parametros, instrucciones, data):
    #me voy directo a las instrucciones, regresare para los parametros
    data.consola.concatenar("\n")
    data.consola.concatenar("void "+ nombre.value + "() { \n" )
    from interprete import procesar_instrucciones
    procesar_instrucciones(instrucciones, data)
    data.consola.concatenar("\n}")

def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"
    else: return dato