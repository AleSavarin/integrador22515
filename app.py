from flask import Flask                 # para utilizar el FrameWork
from flask import render_template       # renderizar los templates
from flaskext.mysql import MySQL        # para ejecutar consultas SQL

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
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Alejandro', 'savaing@hotmail.com', 'fotoAlejandro.jpg');"
    conn = mysql.connect()      # abro la conexión con la BBDD
    cursor = conn.cursor()      # para que vaya sobre la BBDD
    cursor.execute(sql)         # le paso la consulta SQL
    conn.commit()               # finaliza la acción y actualiza 

    return render_template('empleados/index.html')      # renderizo index.html




# al final hago el punto de entrada a la app
if __name__ == '__main__':
    app.run(debug=True)			    # para iniciar en depuración x ahora para probar
