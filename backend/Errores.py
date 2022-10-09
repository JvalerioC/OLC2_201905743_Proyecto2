from datetime import datetime
from webbrowser import open_new_tab

class Error0():
    def __init__(self, descripcion, ambito, fila, columna):
        self.descripcion=descripcion
        self.ambito = ambito
        self.fila=fila
        self.columna=columna
        self.fecha = datetime.today().strftime('%Y/%m/%d %H:%M')

class TablaErrores():
    def __init__(self):
        self.errores = []
    
    def insertar(self, descripcion, ambito, fila, columna, texto):
        columnaF = self.find_column(texto, columna)
        self.errores.append(Error0(descripcion, ambito, fila, columnaF))

    def limpiar(self):
        self.errores = []
    
    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def generarHTML(self):
        if(len(self.errores) == 0):
            print("no se ha analizado el archivo o no hay variables a mostrar")
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

                    <h1>Tabla de Errores</h1>

                    <table >
                    <tr>
                        <th>No.</th>
                        <th>Descripcion</th>
                        <th>Ambito</th>
                        <th>Linea</th>
                        <th>Columna</th>
                        <th>Fecha</th>
                    </tr>'''
            
            parte2 = ""
            conteo=1
            for error in self.errores:
                parte2+="<tr>\n";
                parte2+="<td>"+str(conteo)+"</td>\n";
                parte2+="<td>"+error.descripcion+"</td>\n";
                parte2+="<td>"+error.ambito+"</td>\n";
                parte2+="<td>"+str(error.fila)+"</td>\n";
                parte2+="<td>"+str(error.columna)+"</td>\n";
                parte2+="<td>"+error.fecha+"</td>\n"
                parte2+="</tr>";
                conteo+=1

            parte3="</table>\n</body>\n</html>";

            file = open("reporteErrores.html", "w")
            file.write(parte1+parte2+parte3)
            file.close()
            open_new_tab("reporteErrores.html")

