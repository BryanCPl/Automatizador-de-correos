import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import io
import time
from dotenv import load_dotenv
import pandas as pd
from html import escape
from basedatosManager import BD

pathHtml:str="template.html"
pathHtmlExist:bool=True



# Forzar la salida UTF-8 para caracteres en español
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Gmail normalmente requiere una contraseña de aplicación si tienes verificación en dos pasos.
# En tu archivo .env debes tener algo como:
# EMAIL=tucorreo@gmail.com
# PASSWORD=tu_contraseña_de_aplicacion

class AutomatizadorEmail:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = None

    def conectarServidor(self):
        try:
            # Gmail usa el puerto 587 para SMTP con STARTTLS
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(self.email, self.password)
            print("Correo conectado")
        except Exception as e:
            print(f"Error al conectar con Gmail: {e}")
            traceback.print_exc()

    def personalizarMensaje(self, plantilla, datosCliente):
        return plantilla.format(**datosCliente)

    def enviarEmailMasivo(self,basedataname, table_name, plantilla_html):
        clientes = BD(basedataname)
        clientes.make_table(table_name)


        for i in clientes.get_the_suscribers(table_name):
                id,name,email,empresa,descuento=i[0],i[1],i[2],i[3],i[4]
                
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = email
                msg['Subject'] = f"Hola {name} te necesitamos"

                contenido = self.personalizarMensaje(plantilla_html, {
                    'id': escape(str(id)),
                    'nombre': escape(str(name)),
                    'empresa': escape(str(empresa)),
                    'descuento': escape(str(descuento))
                })

                msg.attach(MIMEText(contenido, 'html'))
                assert self.server is not None
                self.server.send_message(msg)
                print(f"Correo enviado a {email}")
                time.sleep(2)
        
        


    def desuscripcion(self):
        pass

    def cerrar_conexion(self):
        if self.server:
            self.server.quit()
            print("conexion cerrada")

contenido=""
try:
    with open("template.html", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
except:
    print("La ruta del archivo no existe")
    pathHtmlExist=False



if __name__ == '__main__':
    if not EMAIL or not PASSWORD:
        raise ValueError("No se encontraron EMAIL y PASSWORD en el archivo .env")
    if pathHtmlExist:
        automatizador = AutomatizadorEmail(EMAIL, PASSWORD)
        automatizador.conectarServidor()
        automatizador.enviarEmailMasivo('clientes','clientes',contenido )
        automatizador.cerrar_conexion()
    


