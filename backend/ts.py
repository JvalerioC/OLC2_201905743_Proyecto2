from webbrowser import open_new_tab


class Simbolo():

    def __init__(self, id, tipoDato, tipoSimbolo, tamanio, ambito, mutable, linea, columna, pr, ps):
        self.id = id
        self.tipoDato = tipoDato
        self.tipoSimbolo = tipoSimbolo
        self.tamanio = tamanio
        self.ambito = ambito
        self.mutable = mutable
        self.linea = linea
        self.columna = columna
        self.posicionStack = pr
        self.posicionHeap = ps
        self.capacidad = None
        self.modulo = []
        self.valor = 0
        self.instrucciones = None

class TablaSimbolos():
    def __init__(self):
        self.simbolos = []
        self.nombre = []
        self.contadorNombre = 0
        self.nombre.append("Global")

    def nombre_entorno(self):
        name = ""
        if len(self.nombre) == 1:
            name = "Global"
        else:
            name += self.nombre[0]
            for i in range(1, len(self.nombre)):
                name += ", "
                name += self.nombre[i]
        return name


    def ingresar(self, simbolo):
        self.simbolos.append(simbolo)

    def limpiar(self):
        self.simbolos = []

    def modificar(self, tsimbolo):
        res = 0
        for simbolo in self.simbolos:
            if(simbolo.id == tsimbolo.id):
                simbolo.valor = tsimbolo.valor
                res = True
        return res

    def modificar_tamanio(self, tsimbolo):
        for simbolo in self.simbolos:
            if simbolo.id == tsimbolo.id:
                simbolo.tamanio = tsimbolo.tamanio


    def obtener(self, id):
        res = 0
        if len(self.simbolos) == 0:
            return res
        else:
            for simbolo in self.simbolos:
                if(simbolo.id == id):
                    res=simbolo
            return res

    def obtenerTamanioSimbolo(self, id):
        res = 0
        if len(self.simbolos == 0):
            return res
        else:
            for simbolo in self.simbolos:
                if(simbolo.id == id):
                    res = simbolo.tamanio
                    break
            return res                      
    
    def longitud(self):
        return len(self.simbolos)
    
    def eliminar(self, id):
        for i in range(len(self.simbolos)):
            if(self.simbolos[i].id == id):
                self.simbolos.pop(i)
    
    def generarHTML(self):
        if(len(self.simbolos) == 0):
            print("no se ha analizado el archivo o no hay variables a mostrar")
        else:
            parte1 ='''<!DOCTYPE html>
                <html>
                <head>
                <style>
                body {
                background-image: url('https://www.wallpapertip.com/wmimgs/40-405583_high-resolution-white-background-hd.jpg');
                background-repeat: no-repeat;
                background-attachment: fixed;  
                background-size: cover;
                }
                .footer {
                position: absolute;
                left: 0;
                bottom: 1;
                width: 100%;
                background-color: #D0D0D0;
                color: black;
                text-align: left ;
                }
                table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 40%;
                margin: auto;
                }
                h2 {
                    text-align: center;
                }
                h1 {
                    text-align: center;
                }

                td, th {
                border: 1px solid #dddddd;
                text-align: center;
                padding: 8px;
                }

                tr:nth-child(even) {
                background-color: #dddddd;
                }
                </style>
                </head>
                <body>

                <h1>Tabla de Simbolos</h1>

                <table >
                <tr>
                    <th>No.</th>
                    <th>Identificador</th>
                    <th>Tipo Simbolo</th>
                    <th>Tipo Dato</th>
                    <th>Ambito</th>
                    <th>Tamaño</th>
                    <th>Posicion Stack</th>
                    <th>Posicion Heap</th>
                    <th>Linea</th>
                    <th>Columna</th>
                </tr>'''
            parte2 = ""
            conteo=1;

            for simbolo in self.simbolos:
                parte2+="<tr>\n"
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+simbolo.id+"</td>\n";
                parte2+="<td>"+simbolo.tipoSimbolo+"</td>\n";
                parte2+="<td>"+str(simbolo.tipoDato)+"</td>\n";
                parte2+="<td>"+simbolo.ambito+"</td>\n";
                parte2+="<td>"+str(simbolo.tamanio)+"</td>\n";
                parte2+="<td>"+str(simbolo.posicionStack)+"</td>\n";
                parte2+="<td>"+str(simbolo.posicionHeap)+"</td>\n";
                parte2+="<td>"+str(simbolo.linea)+"</td>\n";
                parte2+="<td>"+str(simbolo.columna)+"</td>\n";
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteTS.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteTS.html")

