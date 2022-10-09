from webbrowser import open_new_tab
from funcionesG import TablaF
from structsG import TablaStruct


class Modulo():
    def __init__(self, nombre, instrucciones, fila, columna):
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.mod = TablaModulos()
        self.fn = TablaF()
        self.st = TablaStruct()


class TablaModulos():
    def __init__(self):
        self.modulos = []

    def insertar(self, nombre, instrucciones, fila, columna, texto):
        
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.modulos.append(Modulo(nombre, instrucciones, fila, columnaF))
        #else:
            #aqui va el error semantico
        #    print("no se puede declarar modulo, ya existe")

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def limpiar(self):
        self.modulos = []

    def obtener(self, nombre):
        res = 0
        for modulo in self.modulos:
            if(modulo.nombre == nombre):
                res = modulo
                break
        return res

    def actualizar(self, tmodulo):
        res = 0
        for modulo in self.modulos:
            if modulo.nombre == tmodulo.nombre:
                modulo.mod = tmodulo.mod
                modulo.fn = tmodulo.fn
                modulo.st = tmodulo.st
                #print(len(modulo.mod.modulos), len(modulo.fn.funciones), len(modulo.st.structs))
                res = 1
                break
        if res == 0:
            print("los cambios fallaron")


    def llamar(self, nombre, parametros):
        res = 0
        for modulo in self.modulos:
            if(modulo.nombre == nombre):
                if(len(parametros) == 0 and len(modulo.parametros) == 0):
                    res = modulo
                else:
                    if(len(parametros) == len(modulo.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == modulo.parametros[i].tipo):
                                res =  modulo
                            else:
                                res = 0
                                break
        return res
    
    def generarHTML(self):
        if(len(self.modulos) == 0):
            print("no hay bases de datos a mostrar")
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

                    <h1>Tabla de Bases de Datos</h1>

                    <table >
                    <tr>
                        <th>No.</th>
                        <th>Nombre</th>
                        <th>No. Tablas</th>
                        <th>Linea</th>
                    </tr>'''
            
            parte2 = ""
            conteo=1
            for error in self.modulos:
                parte2+="<tr>\n";
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+error.nombre+"</td>\n";
                parte2+="<td>"+str(len(error.mod.modulos))+"</td>\n";
                parte2+="<td>"+str(error.fila)+"</td>\n";
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteDB.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteDB.html")
    
    def generarHTMLTablas(self):
        if(len(self.modulos) == 0):
            print("no hay tablas a mostrar")
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

                    <h1>Tablas en Bases de Datos</h1>

                    <table >
                    <tr>
                        <th>No.</th>
                        <th>Nombre</th>
                        <th>Base de Datos</th>
                        <th>Linea</th>
                    </tr>'''
            
            parte2 = ""
            conteo=1
            for error in self.modulos:
                db = error.nombre
                for m in error.mod.modulos:
                    parte2+="<tr>\n";
                    parte2+="<td>"+str(conteo)+"</td>\n";
                    parte2+="<td>"+m.nombre+"</td>\n";
                    parte2+="<td>"+str(db)+"</td>\n";
                    parte2+="<td>"+str(m.fila)+"</td>\n";
                    parte2+="</tr>";
                    conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteTDB.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteTDB.html")