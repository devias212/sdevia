class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_nombre(self):
        print(f"Nombre del empleado: {self.nombre}")


class Salario:
    def __init__(self, salario):
        self.salario = salario

    def mostrar_salario(self):
        print(f"Salario del empleado: {self.salario}")

class Designacion(Empleado, Salario):
    def __init__(self, nombre, salario, cargo):
        Empleado.__init__(self, nombre)
        Salario.__init__(self, salario)
        self.cargo = cargo

    def mostrar_cargo(self):
        print(f"Cargo del empleado: {self.cargo}")

    def mostrar_informacion(self):
        self.mostrar_nombre()
        self.mostrar_salario()
        self.mostrar_cargo()

nombre = input("Ingrese el nombre del empleado: ")
salario = float(input("Ingrese el salario del empleado: "))
cargo = input("Ingrese el cargo del empleado: ")

empleado = Designacion(nombre, salario, cargo)

# Se comprueba si el objeto tiene el atributo 'nombre'
if hasattr(empleado, "nombre"):
    print("El objeto tiene el atributo 'nombre'")
else:
    print("El objeto no tiene el atributo 'nombre'")

# Se comprueba si el objeto tiene el atributo 'salario'
if hasattr(empleado, "salario"):
    print("El objeto tiene el atributo 'salario'")
else:
    print("El objeto no tiene el atributo 'salario'")

empleado.mostrar_informacion()