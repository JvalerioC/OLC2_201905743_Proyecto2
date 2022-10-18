def tipoDato(dato):
    if dato.valor == "i64": return 0
    if dato.valor == "usize": return 0
    if dato.valor == "f64": return 0.0
    if dato.valor == "bool": return False
    if dato.valor == "char": return '0'
    if (dato.valor == "String" or dato.valor == "&str"): return ""

class Retorno():
    def __init__(self):
        self.tipo = 0
        self.valor = None
        self.linea = 0
        self.columna = 0
        self.tipoS = "Variable"
        self.capacidad = None

class Texp():
    def __init__(self, direccion, codigo, linea, columna):
        self.direccion = direccion
        self.codigo = codigo
        self.linea = linea
        self.columna = columna
        self.tipo = ""
        self.etiquetaV = None
        self.etiquetaF = None
    
    def obtenerV(self):
        tempV = self.etiquetaV.split(",")
        tempV2 = ""
        for temp in tempV:
            tempV2 += temp+": "
        return  tempV2

    def obtenerF(self):
        tempF = self.etiquetaF.split(",")
        tempF2 = ""
        for temp in tempF:
            tempF2 += temp+": "
        return  tempF2
    
class Impresion():
    def __init__(self):
        self.cadena = ""
    
    def concatenar(self, texto):
        self.cadena += texto
    
    def imprimir(self):
        print(self.cadena)

#esta clase es para los datos que se manejaran en la aplicacion
class Datos():
    def __init__(self, consola, errores, ts, texto):
        self.consola = consola
        self.errores = errores
        self.ts = ts
        self.texto = texto
        self.temporal = 0
        self.etiqueta = 0
        self.pStack = 0
        self.pHeap = 0
        self.encabezado = "#include <stdio.h>\n"
        self.encabezado += "float stack[100000]; // Stack\n"
        self.encabezado += "float heap[100000]; // Heap\n"
        self.encabezado += "float P; // Puntero Stack\n"
        self.encabezado += "float H; // Puntero Heap\n"
        #estos datos me serviran para llevar control del flujo
        self.isWhile = False
        self.isFor = False
        self.isLoop = False
        self.huboLlamada = False
        self.etiquetaSalidaCiclo = None
        self.etiquetaRegresoCiclo = None


    def generar_etiquetas(self):
        cadena = "\nfloat t0"
        for i in range(1,self.temporal):
            cadena += ", t"+str(i)
        cadena += ";\n"
        return cadena
    
    def obtenerTemporal(self):
        numero = self.temporal
        self.temporal = self.temporal+1
        return "t"+str(numero)

    def obtenerTemporalAnterior(self):
        numero = self.temporal-2
        return "t"+str(numero)

    def obtenerEtiqueta(self):
        numero = self.etiqueta
        self.etiqueta = self.etiqueta+1
        return "L"+str(numero)

    def obtenerEtiquetaAnterior(self):
        numero = self.etiqueta-2
        return "L"+str(numero)




