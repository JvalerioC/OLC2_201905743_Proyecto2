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
        self.valor = 0
        self.linea = 0
        self.columna = 0
        self.tipoS = "Variable"
        self.capacidad = None
    
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
        self.encabezado = """#include <stdio.h>
                            float stack[100000]; // Stack
                            float heap[100000]; // Heap
                            float P; // Puntero Stack
                            float H; // Puntero Heap
                            """
    def generar_etiquetas(self):
        cadena = "\nfloat t0"
        for i in range(1,self.temporal):
            cadena += ", t"+str(self.temporal)
        cadena += "\n"
        return cadena
    
    def obtenerTemporal(self):
        numero = self.temporal
        self.temporal = self.temporal+1
        return "t"+str(numero)

    def obtenerEtiqueta(self):
        numero = self.etiqueta
        self.etiqueta = self.etiqueta+1
        return "L"+str(numero)




