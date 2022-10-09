from webbrowser import open_new_tab


class Funcion():
    def __init__(self, nombre, tipo, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.tipo = tipo
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.isFuncion = False

class Parametro():
    def __init__(self, id, tipo):
        self.tipo = tipo
        self.id = id
        self.valor = 0
        self.isReferencia = False

class TablaF():
    def __init__(self):
        self.funciones = []

    def insertar(self, nombre, tipo, parametros, instrucciones, fila, columna, texto):
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.funciones.append(Funcion(nombre, tipo, parametros, instrucciones, fila, columnaF))
        else:
            #aqui va el error semantico
            print("no se puede declarar funcion, ya existe")

    def limpiar(self):
        self.funciones = []

    def obtener(self, nombre):
        res = 0
        for funcion in self.funciones:
            if(funcion.nombre == nombre):
                res = funcion
                break
        return res

    def llamar(self, nombre, parametros):
        res = 0
        for funcion in self.funciones:
            if(funcion.nombre == nombre):
                if(len(parametros) == 0 and len(funcion.parametros) == 0):
                    res = funcion
                else:
                    if(len(parametros) == len(funcion.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == funcion.parametros[i].tipo):
                                res =  funcion
                            else:
                                res = 0
                                break
        return res
    
    def generarHTML(self):
        if(len(self.funciones) == 0):
            print("no hay funciones a mostrar")
        else:
            parte1 = '''<!DOCTYPE html>
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

                    <h1>Funciones Globales</h1>

                    <table >
                    <tr>
                        <th>No.</th>
                        <th>Nombre</th>
                        <th>Tipo</th>
                        <th>Linea</th>
                        <th>Columna</th>
                    </tr>'''
            
            parte2 = ""
            conteo=1
            for error in self.funciones:
                if error.tipo == None:
                    tipo = "None"
                else:
                    tipo = error.tipo
                parte2+="<tr>\n";
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+error.nombre+"</td>\n";
                parte2+="<td>"+tipo+"</td>\n";
                parte2+="<td>"+str(error.fila)+"</td>\n";
                parte2+="<td>"+str(error.columna)+"</td>\n";
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteFunciones.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteFunciones.html")

    