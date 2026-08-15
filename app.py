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

    def enviarEmailMasivo(self, archivo_csv, plantilla_html):
        try:
            clientes = pd.read_csv(archivo_csv, encoding="utf-8")
        except FileNotFoundError as e:
            print(f"No se encontró el archivo CSV: {e}")
            return
        except Exception as e:
            print(f"Error leyendo el archivo CSV: {e}")
            traceback.print_exc()
            return

        columnas_requeridas = {"nombre", "email", "empresa", "descuento"}
        columnas_faltantes = columnas_requeridas - set(clientes.columns)
        if columnas_faltantes:
            print(f"Faltan columnas en el CSV: {sorted(columnas_faltantes)}")
            return

        for i, cliente in clientes.iterrows():
            try:
                email_destino = str(cliente['email']).strip()
                if not email_destino:
                    raise ValueError("El correo del cliente está vacío")

                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = email_destino
                msg['Subject'] = f"Hola {cliente['nombre']} te necesitamos"

                contenido = self.personalizarMensaje(plantilla_html, {
                    'nombre': cliente['nombre'],
                    'empresa': cliente['empresa'],
                    'descuento': cliente['descuento']
                })

                msg.attach(MIMEText(contenido, 'html'))
                assert self.server is not None
                self.server.send_message(msg)
                print(f"Correo enviado a {email_destino}")
                time.sleep(2)
            except Exception as e:
                print(f"Error en el cliente {i} ({cliente.get('email', 'desconocido')}): {e}")
                traceback.print_exc()

    def desuscripcion(self,idUser):
        pass

    def cerrar_conexion(self):
        if self.server:
            self.server.quit()
            print("conexion cerrada")

contenido=""
with open("template.html", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

if __name__ == '__main__':
    if not EMAIL or not PASSWORD:
        raise ValueError("No se encontraron EMAIL y PASSWORD en el archivo .env")

    automatizador = AutomatizadorEmail(EMAIL, PASSWORD)
    automatizador.conectarServidor()
    automatizador.enviarEmailMasivo('clientes.csv',contenido )
    automatizador.cerrar_conexion()