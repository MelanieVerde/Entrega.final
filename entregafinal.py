import dataset
miBase = dataset.connect("sqlite:///base.db")
tabla = miBase["Productos"]

# Si la tabla está vacía, cargamos los productos iniciales
if len(tabla) == 0:
    tabla.insert({"nombre": "Shampoo", "categoria": "Capilar", "precio": 5500})
    tabla.insert({"nombre": "Crema de enjuague", "categoria": "Capilar", "precio": 5600})
    tabla.insert({"nombre": "Dentifrico", "categoria": "Cuidado Oral", "precio": 3000})
    tabla.insert({"nombre": "Crema facial", "categoria": "Skin Care", "precio": 7500})
    tabla.insert({"nombre": "Crema de cuerpo", "categoria": "Cuidado Personal", "precio": 7000})
    tabla.insert({"nombre": "Labial", "categoria": "Make Up", "precio": 7500})
    tabla.insert({"nombre": "Labial waterproof", "categoria": "Make Up", "precio": 8500})
    tabla.insert({"nombre": "Jabon de manos", "categoria": "Cuidado Personal", "precio": 1500})
    tabla.insert({"nombre": "Jabon corporal", "categoria": "Cuidado Personal", "precio": 5000})

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Opción no válida. Por favor, ingrese un número.")

while True:
 # Opciones del menú
    opciones = input("\nMenú Principal\nR - Remover\nA - Agregar\nAC - Actualizar por ID\nBN - Buscar por Nombre\nBC - Buscar por Categoría\nL - Listar\nS - Salir\n------------\n").strip().upper()
    
    
 # Comienza menu de opciones    
    match opciones:

#Opción remover producto
        case "R":
            remover = input("\nIngrese el producto a remover: ").strip().title()
            for producto in tabla:
                if producto["nombre"].title() == remover:
                    tabla.delete(id=producto["id"])
                    print(f"\n{producto['nombre']} removido con éxito.\n")
                    break
            else:
                print(f"\nProducto {remover} no encontrado.\n")

#Opción agregar producto
        case "A":
            agregar = input("\nProducto a agregar: ").strip().title()
            categoria = input("Categoría: ").strip().title()
            precio = pedir_entero("Precio: ")
            tabla.insert({"nombre": agregar, "categoria": categoria, "precio": precio})
            print(f"\n{agregar} agregado con éxito.\n")

        case "AC":
            idBuscar = pedir_entero("\nID a actualizar: ")
            producto_actual = tabla.find_one(id=idBuscar)

            if producto_actual:
                print(f"\nProducto seleccionado: {producto_actual['nombre']} | {producto_actual['categoria']} | ${producto_actual['precio']}")

                # Solicita al usuario los nuevos valores, si desea cambiarlos
                nombreActualizar = producto_actual["nombre"]
                catActualizar = producto_actual["categoria"]
                precioActualizar = producto_actual["precio"]

                # Pregunta al usuario si desea cambiar cada campo
                if input("\n¿Quiere cambiar el nombre? (SI/NO): ").upper() == "SI":
                    nombreActualizar = input("Nombre nuevo: ").strip().title()

                if input("¿Quiere cambiar la categoría? (SI/NO): ").upper() == "SI":
                    catActualizar = input("Categoría nueva: ").strip().title()

                if input("¿Quiere cambiar el precio? (SI/NO): ").upper() == "SI":
                    precioActualizar = pedir_entero("Precio nuevo: ")

                actualizar = {
                    "id": idBuscar,
                    "nombre": nombreActualizar,
                    "categoria": catActualizar,
                    "precio": precioActualizar
                }
                tabla.upsert(actualizar, ["id"])
                print("\nProducto actualizado con éxito.\n")
            else:
                print(f"\nNo se encontró ningún producto con ID {idBuscar}.\n")

#Opción listar productos, categoria y precio
        case "L":
            print("\n---Lista de productos---")
            for producto in tabla:
                print(f"ID: {producto['id']} | {producto['nombre']} | {producto['categoria']} | ${producto['precio']}")
    

        case "BN":
            buscarNombre = input("\nNombre del producto a buscar: ").strip()
            encontrados = list(tabla.find(nombre={"ilike": f"%{buscarNombre}%"}))
            cantidad = len(encontrados)

            if cantidad > 0:
                print(f"\nSe encontraron {cantidad} coincidencia(s):\n")
                for encontrado in encontrados:
                    print(f"ID: {encontrado['id']} | {encontrado['nombre']} | Categoría: {encontrado['categoria']} | Precio: ${encontrado['precio']}")
            else:
                print("\nNo se encontraron coincidencias.\n")

        case "BC":
            buscarCategoria = input("\nCategoría a buscar: ").strip()
            encontrados = list(tabla.find(categoria={"ilike": f"%{buscarCategoria}%"}))
            cantidad = len(encontrados)

            if cantidad > 0:
                print(f"\nSe encontraron {cantidad} producto(s) en esa categoría:\n")
                for encontrado in encontrados:
                    print(f"ID: {encontrado['id']} | {encontrado['nombre']} | Categoría: {encontrado['categoria']} | Precio: ${encontrado['precio']}")
            else:
                print("\nNo se encontraron productos en esa categoría.\n")

#Opción salir del menú
        case "S": 
            print("\nMuchas gracias por usar nuestro sistema.\n")
            break

#Opción por defecto (si escriben cualquier otra letra)
        case _:
            print("\nOpción incorrecta, intente nuevamente.\n")