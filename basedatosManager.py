import sqlite3

class BD:
    def __init__(self,bd_name):
        self.conexion = sqlite3.connect(f"{bd_name}.db")
        self.cursor = self.conexion.cursor()
        

    def make_table(self,table_name):
        if not table_name.isidentifier():
            raise ValueError("Nombre de tabla no válido")
        
        self.table_name=table_name
        print(self.table_name)
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            empresa TEXT NOT NULL,
            suscrito INTEGER NOT NULL DEFAULT 1,
            descuento INTEGER NOT NULL
        )
        """)

    def show_all_table(self,table):
        if self.table_name is None:
            raise RuntimeError("Primero debes crear una tabla")
        self.conexion.commit()
        self.cursor.execute(f"SELECT * FROM {table}")
        datos = self.cursor.fetchall()
        return datos

    def get_the_suscribers(self,table):
        if self.table_name is None:
            raise RuntimeError("Primero debes crear una tabla")
        self.conexion.commit()
        self.cursor.execute(f"SELECT * FROM {table} WHERE suscrito=1")
        datos = self.cursor.fetchall()
        return datos

    def set_data(self,nombre:str,email:str,empresa:str,suscrito:int,descuento:int):
        self.cursor.execute(f"""
        INSERT INTO {self.table_name}
        ( nombre, email, empresa, suscrito, descuento)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (id, nombre, email, empresa, suscrito, descuento))
        self.conexion.commit()

    def desubscribe(self,idUser):
        
        if self.table_name is None:
            raise RuntimeError("Primero debes crear una tabla")

        print("un usuario se desuscribio :(😭😭")
        self.cursor.execute(f"""
            UPDATE clientes
            SET suscrito = 0
            WHERE ID =?;
        """,(idUser,))

    def subscribe(self,idUser):
        if self.table_name is None:
            raise RuntimeError("Primero debes crear una tabla")

        self.cursor.execute(f"""
            UPDATE clientes
            SET suscrito = 1
            WHERE ID = ?;
        """,(idUser,))

    def delete_table(self,table:str):
        if table is None :
            raise RuntimeError("Error el nombre de la tabla")
        self.cursor.execute(f"DROP TABLE {table};")


    def close(self):
        self.conexion.close()


def test():
    midb=BD('clientes')
    midb.make_table('clientes')
    print(midb.get_the_suscribers('clientes'))
    midb.close()
test()