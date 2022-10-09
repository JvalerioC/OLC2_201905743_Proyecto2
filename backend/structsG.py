from webbrowser import open_new_tab


class Struct():
    def __init__(self, nombre, campos, fila, columna):
        self.nombre = nombre
        self.campos = campos
        self.fila = fila
        self.columna = columna

class Campo():
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = None

class Campo2():
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.tipo = None
        self.valor = valor


class TablaStruct():
    def __init__(self):
        self.structs = []

    def insertar(self, nombre, campos, fila, columna, texto):
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.structs.append(Struct(nombre, campos, fila, columnaF))
        else:
            #aqui va el error semantico
            print("no se puede declarar struct, ya existe")

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def limpiar(self):
        self.structs = []

    def obtener(self, nombre):
        res = 0
        for struct in self.structs:
            if(struct.nombre == nombre):
                res = struct
                break
        return res

    def llamar(self, nombre, parametros):
        res = 0
        for struct in self.structs:
            if(struct.nombre == nombre):
                if(len(parametros) == 0 and len(struct.parametros) == 0):
                    res = struct
                else:
                    if(len(parametros) == len(struct.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == struct.parametros[i].tipo):
                                res =  struct
                            else:
                                res = 0
                                break
        return res

    def generarHTML(self):
        if(len(self.structs) == 0):
            print("no hay structs a mostrar")
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

                    <h1>Structs Globales</h1>

                    <table >
                    <tr>
                        <th>No.</th>
                        <th>Nombre</th>
                        <th>Linea</th>
                        <th>Columna</th>
                    </tr>'''
            
            parte2 = ""
            conteo=1
            for error in self.structs:
                parte2+="<tr>\n";
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+error.nombre+"</td>\n";
                parte2+="<td>"+str(error.fila)+"</td>\n";
                parte2+="<td>"+str(error.columna)+"</td>\n";
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteStruct.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteStruct.html")