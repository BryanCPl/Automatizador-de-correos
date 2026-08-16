# 📧 Automatizador de correos

Proyecto personal desarrollado en **Python** para automatizar el envío de correos electrónicos personalizados utilizando una base de datos SQLite.

El sistema permite almacenar clientes, determinar quién está suscrito a los correos, personalizar una plantilla HTML y enviar los mensajes mediante SMTP de Gmail.

Además, cuenta con un pequeño servidor Flask que permite a los usuarios **desuscribirse mediante un enlace incluido en el correo**.

> 🚧 Proyecto en desarrollo / aprendizaje

## 🚀 Características

* 📧 Envío automatizado de correos mediante SMTP.
* 🗃️ Gestión de clientes mediante SQLite.
* 👤 Almacenamiento de nombre, correo, empresa y descuento.
* ✅ Control de suscripción mediante un campo `suscrito`.
* 🎨 Plantillas HTML personalizadas.
* 🔗 Enlace de desuscripción personalizado para cada usuario.
* 🌐 Endpoint Flask para procesar las desuscripciones.
* 🔐 Variables sensibles almacenadas mediante `.env`.
* 🛡️ Escape de datos antes de insertarlos en la plantilla HTML.

## 🛠️ Tecnologías utilizadas

* **Python**
* **SQLite**
* **Flask**
* **smtplib**
* **python-dotenv**
* **HTML**
* **Jinja/format strings**

## 📁 Estructura del proyecto

```text
.
├── app.py
├── basedatosManager.py
├── servidor.py
├── template.html
├── clientes.db
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

Instalar las dependencias:

```bash
pip install flask python-dotenv pandas
```

## 🔐 Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
EMAIL=tu_correo@gmail.com
PASSWORD=tu_contraseña_de_aplicacion
```

> No subas `.env` a GitHub. Utiliza `.gitignore` para evitar publicar credenciales.

Para Gmail, normalmente se utiliza una **contraseña de aplicación** cuando la cuenta tiene habilitada la verificación en dos pasos.

## 🗃️ Base de datos

El proyecto utiliza SQLite.

La tabla de clientes contiene actualmente:

| Campo       | Tipo    | Descripción                      |
| ----------- | ------- | -------------------------------- |
| `id`        | INTEGER | Identificador único              |
| `nombre`    | TEXT    | Nombre del cliente               |
| `email`     | TEXT    | Correo electrónico               |
| `empresa`   | TEXT    | Empresa del cliente              |
| `suscrito`  | INTEGER | `1` = suscrito, `0` = desuscrito |
| `descuento` | INTEGER | Descuento asociado               |

Los clientes suscritos se obtienen mediante una consulta equivalente a:

```sql
SELECT *
FROM clientes
WHERE suscrito = 1;
```

## 📧 Envío de correos

El programa obtiene los clientes suscritos de la base de datos y genera un correo personalizado para cada uno.

La plantilla HTML puede utilizar variables como:

```html
{nombre}
{empresa}
{descuento}
{id}
```

Estas variables son reemplazadas con los datos correspondientes de cada cliente.

## 🔗 Sistema de desuscripción

Cada correo puede incluir un enlace personalizado utilizando el ID del cliente.

Ejemplo:

```html
<a href="http://127.0.0.1:5000/desuscribir/{id}">
    Desuscribirme
</a>
```

El servidor Flask recibe el ID mediante:

```text
/desuscribir/<id>
```

y actualiza el campo:

```text
suscrito = 0
```

De esta forma, el usuario deja de aparecer en la lista de destinatarios de los siguientes envíos.

## ▶️ Ejecución

Primero ejecutar el programa encargado del envío:

```bash
python app.py
```

Después iniciar el servidor Flask:

```bash
python servidor.py
```

Durante el desarrollo, Flask estará disponible normalmente en:

```text
http://127.0.0.1:5000
```

## 🔒 Seguridad

El proyecto utiliza consultas parametrizadas de SQLite para los valores introducidos en las consultas SQL:

```python
cursor.execute(
    "UPDATE clientes SET suscrito = 0 WHERE id = ?",
    (id_user,)
)
```

También se utiliza `html.escape()` para evitar que los datos almacenados sean interpretados como HTML al insertarlos en la plantilla.

Las credenciales de correo se almacenan mediante variables de entorno y no deberían incluirse directamente en el código fuente.

## 📚 Objetivo del proyecto

Este proyecto fue creado principalmente como práctica para aprender a integrar diferentes tecnologías de desarrollo:

```text
Python
   ↓
SQLite
   ↓
Backend / Flask
   ↓
HTML
   ↓
SMTP
   ↓
Correo electrónico
```

El objetivo no es solamente automatizar el envío de correos, sino practicar la comunicación entre una base de datos, una aplicación Python, un servidor web y un servicio externo de correo.

## 🚧 Próximas mejoras

* [ ] Implementar correctamente el sistema de tokens de desuscripción.
* [ ] Añadir validación de correos electrónicos.
* [ ] Registrar correos enviados.
* [ ] Registrar errores y rebotes.
* [ ] Añadir `List-Unsubscribe`.
* [ ] Mejorar el manejo de errores.
* [ ] Separar mejor las responsabilidades del proyecto.
* [ ] Crear una interfaz web para administrar los clientes.
* [ ] Añadir pruebas automatizadas.

## ⚠️ Aviso

Este proyecto está desarrollado con fines educativos y de aprendizaje.

El envío de correos debe realizarse únicamente a destinatarios que hayan aceptado recibirlos y respetando las normas aplicables de correo electrónico y protección de datos.

---

**Proyecto desarrollado como práctica de Python, bases de datos y desarrollo web.** 🐍🗃️🌐📧
