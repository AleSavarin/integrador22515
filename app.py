from flask import Flask                 # para utilizar el FrameWork
from flask import render_template, redirect       # renderizar los templates y recargar la ruta
from flask import request               # para que se pueda ejecutar el submit del formulario
from flaskext.mysql import MySQL        # para ejecutar consultas SQL
from datetime import datetime           # para manejar "timestamp"
import os                               # para manejar archivos
from flask import send_from_directory   # para acceder a archivos

app = Flask(__name__)                   # mi app va a ser de Flask y por costumbre se utiliza __name__

# Conexión a la BBDD
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'       # podría ser un host remoto (IP o URL) 
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''            # Creo que no puse contraseña
app.config['MYSQL_DATABASE_DB']='sistema22515'      # Nombre de la BBDD

mysql.init_app(app)             # Para iniciar la conexión.

CARPETA = os.path.join('uploads')                   # Elijo la ubicación
app.config['CARPETA']=CARPETA


# FUNCIONES
def queryMySQL(query, data=()):            #  Por si no paso datos, toma tupla nula por defecto
    conn=mysql.connect()
    cursor=conn.cursor()
    if len(data) > 0:
        cursor.execute(query,data)         # Para INSERT y UPDATE
    else:
        cursor.execute(query)

    conn.commit()


@app.route('/')                 # Cuando voy al puerto ####/ hago
def index():
    sql = "SELECT * FROM `empleados`;"      #hago un filtro trayendo todo
    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD
    cursor.execute(sql)         # le paso la consulta SQL
    empleados = cursor.fetchall()       # guardo la consulta en una tupla
    #print(empleados)            # imprimo los datos en consola
    conn.commit()               # finaliza la acción y actualiza 

    return render_template('empleados/index.html', empleados=empleados)     # Lo renderizo al index

@app.route('/create')
def create():
    return render_template('empleados/create.html')     # Voy al formulario de Create

@app.route('/store', methods=['POST'])
def storage():
    # Levanto los datos del formulario
    _nombre = request.form['txtNombre']         # por convención el _ es para variables de BBDD
    _correo = request.form['txtCorreo']         #
    _foto   = request.files['txtFoto']          # es .files porque son archivos

    now = datetime.now()                        # tomo el tiempo actual
    tiempo = now.strftime("%Y%m%d%H%M%S")       # le doy formato año/mes/dia/hora/minuto/segundo
    # https://www.geeksforgeeks.org/python-strftime-function/
    
    nuevoNombreFoto = ''
    if _foto.filename != '':                        # si subió archivo
        nuevoNombreFoto = tiempo + _foto.filename   # le agrego el timestamp al nombre de la foto
        _foto.save("uploads/"+nuevoNombreFoto)      # lo guardo en la carpeta uploads

    # Hago la consulta SQL
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos =(_nombre, _correo, nuevoNombreFoto)   # creo una tupla con los datos

    queryMySQL(sql,datos)

    return redirect('/')        # Lo redirijo al index

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD

    # Borrar foto actual
    cursor.execute("SELECT foto FROM empleados WHERE id =%s", id)
    fila = cursor.fetchone()                    # devuelve una tupla 
    try:
        os.remove(os.path.join(CARPETA, fila[0]))              # elimino la foto
    except:
        pass                    # Ejecutar en caso que falle

    # Borrar el registro
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))  # le paso la consulta SQL y los datos que se copiarán en el %s
    conn.commit()
    
    return redirect('/')     # Voy al inicio

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD
    cursor.execute("SELECT * FROM `empleados` WHERE id=%s;",(id))         # le paso la consulta SQL
    empleados = cursor.fetchall()       # guardo la consulta en una tupla
    conn.commit()               # finaliza la acción y actualiza 

    return render_template('empleados/edit.html', empleados=empleados)     # Voy al inicio

@app.route('/update', methods=['POST'])
def update():
    _id = request.form['txtID']
    _nombre = request.form['txtNombre']         
    _correo = request.form['txtCorreo']         
    _foto   = request.files['txtFoto']
    #print((_nombre, _correo, _id))

    sql = "UPDATE `empleados` SET nombre=%s, correo=%s WHERE id=%s;"

    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD
    if _foto.filename != '':
        now = datetime.now()                        # tomo el tiempo actual
        tiempo = now.strftime("%Y%m%d%H%M%S")       # le doy formato año/mes/dia/hora/minuto/segundo
        nuevoNombreFoto = tiempo + _foto.filename   # le agrego el timestamp al nombre de la foto
        _foto.save("uploads/"+nuevoNombreFoto)      # lo guardo en la carpeta uploads

        # Para borrar la foto actual
        cursor.execute("SELECT foto FROM empleados WHERE id =%s", _id)
        fila = cursor.fetchone()                    # devuelve una tupla 
        try:
            os.remove(os.path.join(CARPETA, fila[0]))              # elimino la foto
        except:
            pass                # Ejecutar algo si la foto no existe
        cursor.execute("UPDATE `empleados` SET foto=%s WHERE id=%s;",(nuevoNombreFoto, _id))
        conn.commit()

    cursor.execute(sql, (_nombre, _correo, _id))         # le paso la consulta SQL
    conn.commit()               # finaliza la acción y actualiza 

    return redirect('/')     # Voy al inicio

@app.route('/uploads/<nombreFoto>')
def muestraFoto(nombreFoto):
    return send_from_directory(CARPETA, nombreFoto)


# al final hago el punto de entrada a la app
if __name__ == '__main__':
    app.run(debug=True)			    # para iniciar en depuración x ahora para probar
