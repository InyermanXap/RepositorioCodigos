import os 
import smtplib
from email.message import EmailMessage

#Bases de datos y rutas de archivos

BD_Admnistradores = "Administradores.txt"
BD_Taxistas = "Taxistas.txt"
BD_Taxis = "Taxis.txt"

def Crear_base_de_datos():
    if not os.path.exists(BD_Admnistradores):
        with open(BD_Admnistradores, "w") as g:
            g.write("Cargo\tContraseña\tNombre\tApellido\tDPI\tTelefono\tCorreo\nAdministrador\tGoku360\tInyerman\tXap\t3000305680101\t49925704\tinyermanxap@gmail.com\n ")
            print('base de datos de administradores creada')
    if not os.path.exists(BD_Taxistas):
        with open(BD_Taxistas, "w") as h:
            h.write("Cargo\tContraseña\tNombre\tApellido\tDPI\tTelefono\tCorreo\tAutomovil\n ")
            print('base de datos de taxistas creada')
    if not os.path.exists(BD_Taxis):
        with open(BD_Taxis, "w") as h:
            h.write("No.Taxi\tPlaca\tDPI Taxista\tNombre\tApellido\tEstado\n ")
            print('base de datos de taxis creada')


def Menu_principal():
    Crear_base_de_datos()
    print("Bienvenido, Por favor seleccione una opcion")
    print("1. Iniciar Sesion Administrador")
    print("2. Iniciar Sesion Taxista")
    print("3. Salir")

    opcion =input("Ingrese su opcion:   ")

    if opcion == "1":
        Iniciar_sesion_administrador()
   
    elif opcion == "2":
        #Iniciar_sesion_taxista()
        print("funcion pendiente")
        Menu_principal()
    elif opcion == "3":
        return
    else:
        print("Opcion Invalida, Por favor seleccione una opcion valida")

def Iniciar_sesion_administrador():
    Usuario_admni = input("Ingrese su DPI:   ")
    Contraseña_admni = input("Ingrese su contraseña:   ")

    if os.path.exists(BD_Admnistradores):
        with open(BD_Admnistradores, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")

                # Eliminar espacios en blanco y saltos de línea
                cargo = campos[0].strip()
                nombre_usuario = campos[4].strip()
                password = campos[1].strip()


                if nombre_usuario == Usuario_admni and password == Contraseña_admni:
                    if cargo == "Administrador":
                        print("Bienvenido, admin.")
                        Menu_administrador()
                        return
    print("Credenciales incorrectas. Por favor, intentelo de nuevo.")


def Menu_administrador():
    print("Menu Administrador")
    print("1. Ingresar Nuevo Taxista")
    print("2. Ver Taxistas ")
    print("3. Taxis")
    print("4. Salir")

    opcion =input("Ingrese su opcion:   ")

    if opcion == "1":
       Ingresar_nuevo_taxista()
    
    elif opcion == "2":
        Ver_taxistas()
    
    elif opcion == "3":
        Ver_taxis()
    elif opcion == "4":
        return

    else:
       print("Opcion Invalida, Por Favor intentelo de nuevo")
       Menu_administrador()
    
def Ingresar_nuevo_taxista():
    Nombre_taxista = input("Ingrese el Nombre del taxista:   ")

    Apellido_taxista = input("Ingrese el Apellido del taxista:  ")

    DPI_taxista = input("Ingrese el DPI del taxista:  ")

    Tel_taxista = input("Ingrese el Telefono del taxista:  ")

    Correo_taxista = input("Ingrese el correo del taxista:   ")

    Auto_taxista = input("Ingrese la placa del taxi que se le asignara al taxista:   ")

    Contraseña_taxista = input("Ingrese la contraseña del taxista:   ")

    Confirmacion_contraseña_taxista = input("Ingrese su contraseña nuevamente:   ")

    if Contraseña_taxista != Confirmacion_contraseña_taxista:
        print("Las contraseñas no coinciden. Por favor, intentelo de nuevo.")
        Ingresar_nuevo_taxista()
    else:
        with open(BD_Taxistas, "r") as f:
            for linea in f:
                campos = linea.split("\t")
                if campos[4] == DPI_taxista:  # Verificamos por DPI si el taxista ya esta reggistrado
                    print("El DPI ya existe. Este taxista ya se encuentra registrado.")
                    return

        with open(BD_Taxistas, "a") as f:
            f.write(f"Taxista\t{Contraseña_taxista}\t{Nombre_taxista}\t{Apellido_taxista}\t{DPI_taxista}\t{Tel_taxista}\t{Correo_taxista}\t{Auto_taxista}\n")
        with open(BD_Taxis,"a") as f:
            f.write(f"\t{Auto_taxista}\t{DPI_taxista}\t{Nombre_taxista}\t{Apellido_taxista}\n")
            generar_archivo_taxista(DPI_taxista)
        print("Registro exitoso.")

def generar_archivo_taxista(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'
    
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            f.write("No.Viajes\tTaxista\tGanancia empresa\Ganacia Taxista\n")
        print(f"Archivo {nombre_archivo} creado correctamente.")
    else:
        print(f"El archivo {nombre_archivo} ya existe.")

def Ver_taxis():
    print("1. Ver taxis en inventario y su estado")
    print("2. Asignar Taxis")
    print("3. Actualizar estado de taxi")
    print("4.Añadir taxi")
    print("5. Salir")

    opcion = input("Por favor seleccione una de las opciones: ")

    if opcion == "1":
        Inventario_taxis()
    
    elif opcion == "2":
        Asignar_taxis()

    elif opcion == "3":
        Actualizar_estado_taxi()

    elif opcion == "4":
        Añadir_taxi()

    elif input == "5":
        return
    
    else:
        print("Por favor seleccione una opcion valida")
        Ver_taxis()
    
def Inventario_taxis():
    if os.path.exists(BD_Taxis):
        print("\n--- Inventario de Taxis ---")
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            taxis = f.readlines()

            if not taxis:
                print("No hay taxis registrados en la base de datos.")
            else:
                print("No.Taxi\tPlaca\tDPI Taxista\tNombre\tApellido")
                for linea in taxis:
                    print(linea.strip())  # Imprimir cada línea quitando espacios y saltos de línea
    else:
        print("La base de datos de taxis no existe.")
    
def Añadir_taxi():
    print("\n--- Añadir Nuevo Taxi al Inventario ---")

    # Determinar el último número de taxi
    ultimo_numero_taxi = 0
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                if linea.strip():  # Asegurarse de que la línea no esté vacía
                    campos = linea.split("\t")
                    ultimo_numero_taxi = int(campos[0].strip())  # Obtener el número de taxi

    nuevo_numero_taxi = ultimo_numero_taxi + 1  # Incrementar el número del taxi

    Placa = input("Ingrese la placa del taxi:   ")

    # Verificar si la placa ya existe en el archivo
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            for linea in f:
                campos = linea.split("\t")
                if campos[1].strip() == Placa:
                    print("Error: Ya existe un taxi registrado con esta placa.")
                    return

    # Agregar el nuevo taxi a la base de datos sin asignar taxista
    with open(BD_Taxis, "a") as f:
        f.write(f"{nuevo_numero_taxi}\t{Placa}\tSin asignar\tSin asignar\tSin asignar\tDisponible\n")

    print(f"El nuevo taxi ha sido añadido exitosamente con el número {nuevo_numero_taxi}.")

def Asignar_taxis():
    print("\n--- Asignar Taxi a Taxista ---")
    
    # Verificar que hay taxis sin asignar
    taxis_disponibles = []
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")
                if campos[2].strip() == "Sin asignar":  # Si el taxi no tiene taxista asignado
                    taxis_disponibles.append(campos)

    if not taxis_disponibles:
        print("No hay taxis disponibles para asignar.")
        return

    # Mostrar taxis disponibles
    print("\nTaxis disponibles:")
    for i, taxi in enumerate(taxis_disponibles, start=1):
        print(f"{i}. Taxi No: {taxi[0]}, Placa: {taxi[1]}")

    # Seleccionar taxi
    seleccion = int(input("\nSeleccione el número del taxi que desea asignar: ")) - 1
    if seleccion < 0 or seleccion >= len(taxis_disponibles):
        print("Selección inválida. Intente de nuevo.")
        return
    taxi_seleccionado = taxis_disponibles[seleccion]

    # Solicitar el DPI del taxista
    DPI_taxista = input("Ingrese el DPI del taxista:   ")

    # Verificar que el taxista esté registrado
    taxista_encontrado = None
    if os.path.exists(BD_Taxistas):
        with open(BD_Taxistas, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")
                if campos[4].strip() == DPI_taxista:
                    taxista_encontrado = campos
                    break

    if not taxista_encontrado:
        print("El taxista con ese DPI no está registrado.")
        return

    # Asignar taxi al taxista en el archivo de taxis
    actualizar_taxis(taxi_seleccionado, taxista_encontrado)

    # Confirmar la asignación
    print(f"Taxi No. {taxi_seleccionado[0]} con placa {taxi_seleccionado[1]} ha sido asignado al taxista {taxista_encontrado[2]} {taxista_encontrado[3]}.")

def actualizar_taxis(taxi_seleccionado, taxista_encontrado):
    # Leer todo el archivo de taxis
    with open(BD_Taxis, "r") as f:
        lineas = f.readlines()

    # Actualizar la línea del taxi seleccionado con los datos del taxista
    with open(BD_Taxis, "w") as f:
        for linea in lineas:
            campos = linea.split("\t")
            if campos[0].strip() == taxi_seleccionado[0]:  # Si coincide el número de taxi
                f.write(f"{campos[0]}\t{campos[1]}\t{taxista_encontrado[4]}\t{taxista_encontrado[2]}\t{taxista_encontrado[3]}\tEn uso\n")
            else:
                f.write(linea)


Menu_principal()
