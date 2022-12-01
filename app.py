from flask import Flask                 # para utilizar el FrameWork
from flask import render_template       # renderizar los templates

app = Flask(__name__)                   # mi app va a ser de Flask y por costumbre se utiliza __name__

# Acá todo el código que necesito!

@app.route('/')             # Cuando voy al puerto ####/ hago
def index():
    return render_template('empleados/index.html')      # renderizo index.html

'''
@app.route('/juanca')      
def juanca():
    return render_template('empleados/juanca.html')
'''


# al final hago el punto de entrada a la app
if __name__ == '__main__':
    app.run(debug=True)			    # para iniciar en depuración x ahora para probar
