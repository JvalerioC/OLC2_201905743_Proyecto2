class Nodo_AST():
    def __init__(self, etiqueta, valor, tipo, fila, columna):
        self.etiqueta = etiqueta
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.referencia = ""
        self.expresion = ""
        self.hijos = []

    def agregarHijo(self, *args):
        for arg in args:
            self.hijos.append(arg)

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1



class Grafo():
    def __init__(self, raiz):
        self.texto = ""
        self.contador = 1
        self.raiz = raiz
  
        self.texto+="digraph G{"
        self.texto+="Node0[label=\"" + self.escapar(self.raiz.etiqueta) + "\"];\n";

        self.recorrido("Node0",self.raiz)

        self.texto+= "}"
        print(self.texto)
        return self.texto

    def recorrido(self, padre, hijos):
        if(hijos == None): return

        for hijo in hijos:
            nombrehijo="Node"+str(contador)
            self.texto+=nombrehijo+"[label=\"" + self.escapar(hijo.etiqueta) + "\"];\n";
            self.texto+=padre+"->"+nombrehijo+";\n"
            contador=contador+1
            self.recorrido(nombrehijo,hijo)

    def escapar(self, cadena):
        cadena = cadena.replace("\\", " ")
        cadena = cadena.replace("\"", " ")
        cadena = cadena.replace("\n", " ")
        cadena = cadena.replace("\t", " ")
        cadena = cadena.replace("\r", " ")
        return cadena
    
