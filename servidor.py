from flask import Flask
from basedatosManager import BD
app=Flask(__name__)


@app.route("/desuscribir/<int:id_user>")
def desuscribir(id_user):
    print("Hollaalalallaalalalalal")
    bd = BD("clientes")
    bd.make_table('clientes')
    print(bd.show_all_table('clientes'))
    bd.desubscribe(id_user)
    print(bd.get_the_suscribers('clientes'))
    bd.close()

    return "Te has desuscrito correctamente."

if __name__=="__main__":
    app.run(debug=True)