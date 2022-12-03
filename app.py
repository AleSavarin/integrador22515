from flask import Flask                 # para utilizar el FrameWork
from flask import render_template       # renderizar los templates
from flask import request               # para que se pueda ejecutar el submit del formulario
from flaskext.mysql import MySQL        # para ejecutar consultas SQL
from datetime import datetime           # para manejar "timestamp"

app = Flask(__name__)                   # mi app va a ser de Flask y por costumbre se utiliza __name__

# Conexión a la BBDD
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'       # podría ser un host remoto (IP o URL) 
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''            # Creo que no puse contraseña
app.config['MYSQL_DATABASE_DB']='sistema22515'      # Nombre de la BBDD

mysql.init_app(app)             # Para iniciar la conexión.


@app.route('/')                 # Cuando voy al puerto ####/ hago
def index():
    return render_template('empleados/index.html')      # renderizo index.html

@app.route('/create')
def create():
    return render_template('empleados/create.html')     # Voy al formulario de Create

@app.route('/store', methods=['POST'])
def storage():
    # Levanto los datos del formulario
    _nombre = request.form['txtNombre']         # por convención el _ es para variables de BBDD
    _correo = request.form['txtCorreo']         #
    _foto   = request.files['txtFoto']        # es .files porque son archivos

    # Hago la consulta SQL
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos =(_nombre, _correo, _foto.filename)   # creo una tupla con los datos
    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD
    cursor.execute(sql, datos)  # le paso la consulta SQL y los datos que se copiarán en el %s
    conn.commit()               # finaliza la acción y actualiza 

    return render_template('empleados/index.html')     # Lo redirijo al index


# al final hago el punto de entrada a la app
if __name__ == '__main__':
    app.run(debug=True)			    # para iniciar en depuración x ahora para probar
