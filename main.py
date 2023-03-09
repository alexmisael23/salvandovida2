from flask import Flask, session, render_template, request, url_for, redirect
import pyrebase
import json
from Modelo.usuario import usuario
from Modelo.UsuarioSistema import UsuarioSistema

app = Flask(__name__)

# Variable de configuración
config = {
    "apiKey": "AIzaSyBXPZq0iXyIcrb18x5WjVE2r7XA9fgpP18",
    "authDomain": "salvandovida-10b02.firebaseapp.com",
    "databaseURL": "https://salvandovida-10b02-default-rtdb.firebaseio.com",
    "projectId": "salvandovida-10b02",
    "storageBucket": "salvandovida-10b02.appspot.com",
    "messagingSenderId": "935386215564",
    "appId": "1:935386215564:web:f92e396909ea2df84877a9"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

# Option
app.secret_key = 'secret'


# user = auth.create_user_with_email_and_password(email,password)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email

            return redirect(url_for('prueba'))
        except:
            return 'Error'
    return render_template('inicio.html')

#@app.route('/prueba')
@app.route('/prueba')
def prueba():
    if 'user' in session:
        lista_Comida = db.child("clientes").get().val()
        return render_template("pedidos.html", elementos_Comida=lista_Comida.values())
    else:
        return render_template('inicio.html')

# Ruta para observar la información de los sensores#

@app.route('/sensores')
def sensores():
    lista_Sensores = db.child("Cafeteria").get().val()
    return render_template("info_sensores.html", elementos_sensores=lista_Sensores.values())


# ruta para mostrar formulario de registro
@app.route('/add')
def add():
    return render_template('alta_personas.html')


# ---------------------------------------------------------------------------------------------
# Capturar los datos del formulario y guardarlos en FB

# ---------------------------Mostrar el formulario de registro--------------------------------------#
@app.route('/actualizar_persona/<id>')
def actualizar_persona(id):
    lista = db.child("Registro").child(str(id)).get().val()
    return render_template("formulario_actualizar.html", lista=lista, id_persona=id)


# -----------------------Ruta para obtener los datos del formularaio y despuesactualizar-------------------------------#
@app.route('/update', methods=["POST"])
def update_persona():
    # ----------Variables para obtener información del formualrio---------#
    idpersona = request.form.get('id')
    email = request.form.get('email')
    contraseña = request.form.get('contraseña')

    modificar_persona = usuario(email, contraseña)

    objeto_enviar = json.dumps(modificar_persona.__dict__)
    datos_completo = json.loads(objeto_enviar)
    db.child("Registro").child(str(idpersona)).update(datos_completo)
    return redirect(url_for('hello_word'))


# -------------Formulario de registro de usuarios del sistema------------------#
@app.route('/altausuarios')
def altausuarios():
    return render_template("alta_usuarios_sistema.html")


# -------------------- Ruta para obtener los datos del formulario y crear el usuario ----------------------------#
@app.route('/guardarusuariosistema', methods=['POST'])
def guardarusuariosistema():
    if request.method == 'POST':
        usuario_sistema = request.form.get('usuario')
        password = request.form.get('password')

        try:
            usuario_sistema_nuevo = UsuarioSistema(usuario_sistema, password)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y = json.loads(objeto_enviar)
            db.child("usuarios").push(y)

        except:
            print("error")

    return render_template("alta_usuarios_sistema.html")


# -------------------Tabla donde se registraran los pedidos---------------------------#
# @app.route('/pedidousuario',)
# def pedidousuario():
#   lista_pedido = db.child("pedidos").get().val()

#  return render_template("pedidos.html", elementos_pedidos=lista_pedido.values())


# ----eliminar un registro de la tabla-----#
@app.route('/eliminar_persona', methods=["GET"])
def eliminar_persona():
    id = request.args.get("id")
    db.child("clientes").child(str(id)).remove()
    return redirect(url_for('prueba'))
    # ------return "usuario eliminado correctamente------#


@app.route('/alta/<nombre>')
def registrar(nombre):
    db.child("personas").push({"nombre": nombre})
    return "dato guardado exitosamente"


@app.route('/eliminar')
def eliminar():
    db.child("personas").child("-MxCQaEgMBu5xDfAzOWP").remove()
    return "usuario eliminado correctamente"


@app.route('/modificar')
def modificar():
    db.child("personas").child("-MxCRMB6ex31I-Qsnbjy").update({"nombre": "Maria Dosantos Aveiro"})
    return "Datos modificados correctamente"


if __name__ == '__main__':
    app.run(debug=True)
