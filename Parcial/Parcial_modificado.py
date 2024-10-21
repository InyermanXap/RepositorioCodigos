import os 
import smtplib
from email.message import EmailMessage
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    print("3. Solicitar Taxi")
    print("4. Salir")

    opcion =input("Ingrese su opcion:   ")

    if opcion == "1":
        Iniciar_sesion_administrador()
   
    elif opcion == "2":
        main()
    
    elif opcion == "3":
        Solicitar_taxi()

    elif opcion == "4":
        return
    else:
        print("Opcion Invalida, Por favor seleccione una opcion valida")

def Solicitar_taxi():
    print("Bienvenido querido cliente")
    print("Por favor ingrese sus datos y seleccione al taxista de su preferencia")
    texto_nombre_cliente = input("Ingrese su nombre: ")
    texto_NIT_cliente = input("Ingrese su NIT: ")
    texto_direccion_cliente= input("Ingrese el lugar donde sera recogido: ")
    texto_correo_cliente= input("Ingrese su correo electrónico para que le llegue su factura: ")
    texto_numero_cliente = input ("Ingrese su número para contactar con usted: ")
    
    print("Seleccione su taxista")
    taxistas_disponibles = []
    
    # Verificamos si la base de datos de taxistas existe
    if os.path.exists(BD_Taxistas):
        with open(BD_Taxistas, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.strip().split("\t")
                if len(campos) >= 7:  # Asegurarse de que hay suficientes campos
                    taxistas_disponibles.append({
                        'DPI': campos[4],  # DPI del taxista
                        'nombre': campos[2],  # Nombre del taxista
                        'apellido': campos[3],  # Apellido del taxista
                        'correo': campos[6],  # Correo del taxista
                        'automovil': campos[7] if len(campos) > 7 else "Sin asignar"  # Automóvil (si existe)
                    })

    # Si no hay taxistas disponibles, mostramos un mensaje
    if not taxistas_disponibles:
        print("No hay taxistas disponibles en este momento.")
        return
    
    # Mostrar la lista de taxistas disponibles
    for i, taxista in enumerate(taxistas_disponibles, start=1):
        print(f"{i}. {taxista['nombre']} {taxista['apellido']} - Automóvil: {taxista['automovil']}")

    # Selección de taxista
    seleccion = int(input("\nSeleccione el número del taxista: ")) - 1
    if seleccion < 0 or seleccion >= len(taxistas_disponibles):
        print("Selección inválida. Intente de nuevo.")
        return
    
    taxista_seleccionado = taxistas_disponibles[seleccion]
    
    print(f"Ha seleccionado al taxista {taxista_seleccionado['nombre']} {taxista_seleccionado['apellido']} con el automóvil {taxista_seleccionado['automovil']}.")

    Solicitud_cliente(texto_correo_cliente, texto_numero_cliente, texto_NIT_cliente, texto_nombre_cliente, texto_direccion_cliente, taxista_seleccionado)



def enviar_correo_taxista(correo_destinatario_cliente, asunto, mensaje):
    # Configuracion del servidor SMTP
    servidor = 'smtp.gmail.com'
    puerto = 587
    remitente = 'vegachanito09@gmail.com'
    contrasena = 'erxs hyqv rvoi wrel'

    # Crear el mensaje
    email_msg = MIMEMultipart()
    email_msg['From'] = remitente
    email_msg['To'] = correo_destinatario_cliente
    email_msg['Subject'] = asunto
    email_msg.attach(MIMEText(mensaje, 'plain'))

    # Conectar al servidor y enviar el correo
    try:
        server = smtplib.SMTP(servidor, puerto)
        server.starttls()
        server.login(remitente, contrasena)
        server.sendmail(remitente, correo_destinatario_cliente, email_msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")

def Solicitud_cliente(texto_correo_cliente, texto_numero_cliente, texto_NIT_cliente, texto_nombre_cliente, texto_direccion_cliente, taxista_seleccionado):
    # Obtener el correo del taxista seleccionado
    correo_destinatario_cliente = taxista_seleccionado['correo']
    asunto = "Nueva Solicitud de Viaje"

    # Crear el mensaje para el taxista
    mensaje = f"""Buen día. Le informamos que tiene una solicitud de viaje. Por favor, póngase en contacto con el cliente.
    Nombre del cliente: {texto_nombre_cliente}
    NIT del cliente: {texto_NIT_cliente}
    Lugar para recoger al cliente: {texto_direccion_cliente}
    Correo del cliente: {texto_correo_cliente}
    Número del cliente: {texto_numero_cliente}
    """
    
    # Llamar a la función para enviar el correo
    enviar_correo(correo_destinatario_cliente, asunto, mensaje)
    print(f"Correo enviado a {correo_destinatario_cliente}.")

    

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
    
    print("1. Ver Taxistas ")
    print("2. Taxis")
    print("3. Salir")

    opcion =input("Ingrese su opcion:   ")

    
    if opcion == "1":
        crear_taxista()
    
    elif opcion == "2":
        Ver_taxis()
    elif opcion == "3":
        return

    else:
       print("Opcion Invalida, Por Favor intentelo de nuevo")

    
def Ingresar_nuevo_taxista():
    Nombre_taxista = input("Ingrese el Nombre del taxista:   ")

    Apellido_taxista = input("Ingrese el Apellido del taxista:  ")

    DPI_taxista = input("Ingrese el DPI del taxista:  ")

    Tel_taxista = input("Ingrese el Telefono del taxista:  ")

    Correo_taxista = input("Ingrese el correo del taxista:   ")

    Contraseña_taxista = input("Contrasena (minimo 8 caracteres, 1 mayuscula, 1 numero, 1 caracter especial")

    Confirmacion_contraseña_taxista = input("Ingrese su contraseña nuevamente:   ")

    if Contraseña_taxista != Confirmacion_contraseña_taxista:
        print("Las contraseñas no coinciden. Por favor, intentelo de nuevo.")
        return
    else:
        while True:
        
                if validar_contrasena(Contraseña_taxista):
                    break
                else:
                    print("Contraseña no cumple los requisitos. Intentalo de nuevo.")
   
        with open(BD_Taxistas, "r") as f:
            for linea in f:
                campos = linea.strip().split("\t")  # Elimina espacios en blanco o saltos de línea
                if len(campos) > 4 and campos[4] == DPI_taxista:  # Verifica que haya al menos 5 campos
                    print("El DPI ya existe. Este taxista ya se encuentra registrado.")
                    return

        with open(BD_Taxistas, "a") as f:
            f.write(f"Taxista\t{Contraseña_taxista}\t{Nombre_taxista}\t{Apellido_taxista}\t{DPI_taxista}\t{Tel_taxista}\t{Correo_taxista}\t{Auto_taxista}\n")
        with open(BD_Taxis, "a") as f:
            f.write(f"\tsin asignar\t{DPI_taxista}\t{Nombre_taxista}\t{Apellido_taxista}\n")
            generar_archivo_taxista(DPI_taxista)
        print("Registro exitoso.")


def generar_archivo_taxista(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'
    
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            f.write("No.Viajes\tKilometros\tSalario\tGanancia empresa\tGanancia Taxista\n")
        print(f"Archivo {nombre_archivo} creado correctamente.")
    else:
        print(f"El archivo {nombre_archivo} ya existe.")

def ver_taxistas(taxistas, viajes):
    if not taxistas:
        print("No hay taxistas registrados.")
        return

    print("\n--- Lista de Taxistas ---")
    for taxista in taxistas:
        dpi_taxista = taxista["dpi"]
        nombre = taxista["nombre"]
        apellido = taxista["apellido"]
        sueldo = taxista["sueldo_mensual"]
        taxi_asignado = taxista["taxi_asignado"]
        
        # Contar el número de viajes realizados por este taxista
        numero_viajes = sum(1 for viaje in viajes if viaje["dpi_taxista"] == dpi_taxista)
        
        # Calcular la ganancia total para la empresa asociada a este taxista
        ganancia_total_empresa = sum(viaje["ganancia_empresa"] for viaje in viajes if viaje["dpi_taxista"] == dpi_taxista)
        
        # Mostrar la información del taxista
        print(f"DPI: {dpi_taxista}, Nombre: {nombre}, Apellido: {apellido}, Taxi Asignado: {taxi_asignado}, "
              f"Número de Viajes: {numero_viajes}, Sueldo del Mes: {sueldo}, Ganancia Total para la Empresa: {ganancia_total_empresa}")


def crear_taxista(taxistas, dpi, nombre, apellido, sueldo_mensual, taxi_asignado):
    taxista = {
        "dpi": dpi,
        "nombre": nombre,
        "apellido": apellido,
        "sueldo_mensual": sueldo_mensual,
        "taxi_asignado": taxi_asignado
    }
    taxistas.append(taxista)
    crear_viaje(taxistas)

def crear_viaje(viajes, id_viaje, dpi_taxista, ganancia_empresa,taxistas):
    viaje = {
        "id_viaje": id_viaje,
        "dpi_taxista": dpi_taxista,
        "ganancia_empresa": ganancia_empresa
    }
    viajes.append(viaje)
    ver_taxistas(taxistas,viajes)




def obtener_numero_viajes(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'
    
    if not os.path.exists(nombre_archivo):
        return 0  # Si no existe el archivo, el número de viajes es 0
    
    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()
        return len(lineas) - 1
    

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

    elif opcion == "5":
        return
    
    else:
        print("Por favor seleccione una opcion valida")

    
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
                    if len(campos) > 0 and campos[0].strip().isdigit():  # Verificar que haya columnas y que campos[0] sea un número
                        ultimo_numero_taxi = int(campos[0].strip())  # Obtener el número de taxi

    nuevo_numero_taxi = ultimo_numero_taxi + 1  # Incrementar el número del taxi

    # Ingresar la placa del taxi
    Placa = input("Ingrese la placa del taxi:   ").strip()

    # Validar que la placa no esté vacía
    if not Placa:
        print("Error: La placa no puede estar vacía.")
        return

    # Verificar si la placa ya existe en el archivo
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            for linea in f:
                campos = linea.split("\t")
                if len(campos) > 1:  # Asegurarse de que haya al menos dos columnas (No.Taxi y Placa)
                    if campos[1].strip() == Placa:  # Comparar con la placa
                        print("Error: Ya existe un taxi registrado con esta placa.")
                        return

    # Agregar el nuevo taxi a la base de datos sin asignar taxista
    with open(BD_Taxis, "a") as f:
        # Si es un archivo nuevo, agregar la cabecera
        if os.path.getsize(BD_Taxis) == 0:
            f.write("No.Taxi\tPlaca\tDPI Taxista\tNombre\tApellido\tEstado\n")

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
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            lineas = f.readlines()

        # Actualizar la línea del taxi seleccionado con los datos del taxista
        with open(BD_Taxis, "w") as f:
            for linea in lineas:
                campos = linea.strip().split("\t")
                if campos[0].strip() == taxi_seleccionado[0].strip():  # Verificar si coincide el número de taxi
                    # Actualizar con los datos del taxista
                    nueva_linea = f"{campos[0]}\t{campos[1]}\t{taxista_encontrado[4]}\t{taxista_encontrado[2]}\t{taxista_encontrado[3]}\tEn uso\n"
                    f.write(nueva_linea)
                else:
                    f.write(linea)
        print("El taxi ha sido actualizado correctamente.")
    else:
        print("La base de datos de taxis no existe.")



def Actualizar_estado_taxi():
    print("\n--- Actualizar Estado de Taxi ---")
    
    # Verificar si hay taxis registrados
    taxis_registrados = []
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")
                taxis_registrados.append(campos)

    if not taxis_registrados:
        print("No hay taxis registrados en la base de datos.")
        return

    # Mostrar lista de taxis registrados
    print("\nTaxis registrados:")
    for i, taxi in enumerate(taxis_registrados, start=1):
        print(f"{i}. Taxi No: {taxi[0]}, Placa: {taxi[1]}, Estado actual: {taxi[5].strip()}")

    # Seleccionar taxi
    seleccion = int(input("\nSeleccione el número del taxi que desea actualizar: ")) - 1
    if seleccion < 0 or seleccion >= len(taxis_registrados):
        print("Selección inválida. Intente de nuevo.")
        return
    taxi_seleccionado = taxis_registrados[seleccion]

    # Mostrar posibles estados
    print("\nSeleccione el nuevo estado del taxi:")
    print("1. Disponible")
    print("2. En uso")
    print("3. En mantenimiento")
    
    estado_opcion = input("Ingrese el número correspondiente al estado: ")

    if estado_opcion == "1":
        nuevo_estado = "Disponible"
    elif estado_opcion == "2":
        nuevo_estado = "En uso"
    elif estado_opcion == "3":
        nuevo_estado = "En mantenimiento"
    else:
        print("Opción inválida. Intente de nuevo.")
        return

    # Actualizar el estado del taxi seleccionado
    with open(BD_Taxis, "w") as f:
        for i, linea in enumerate(taxis_registrados):
            if i == seleccion:
                # Reescribir la línea del taxi seleccionado con el nuevo estado
                f.write(f"{taxi_seleccionado[0]}\t{taxi_seleccionado[1]}\t{taxi_seleccionado[2]}\t{taxi_seleccionado[3]}\t{taxi_seleccionado[4]}\t{nuevo_estado}\n")
            else:
                f.write("\t".join(linea))  # Reescribir las otras líneas sin cambios

    print(f"El estado del Taxi No. {taxi_seleccionado[0]} ha sido actualizado a '{nuevo_estado}'.")


def validar_contrasena(Contraseña_taxista):
    if (len(Contraseña_taxista) >= 8 and 
        re.search(r'[A-Z]', Contraseña_taxista) and 
        re.search(r'[0-9]', Contraseña_taxista) and 
        re.search(r'[!@#$%^&*(),.?":{}|<>]', Contraseña_taxista)):
        return True
    return False

def leer_usuarios():
    usuarios = {}
    if os.path.exists(BD_Taxistas):  
        with open(BD_Taxistas, "r") as file:
            next(file)  # Saltar la cabecera
            for line in file:
                datos = line.strip().split('\t')
                if len(datos) >= 7:  # Verificar que hay suficientes datos
                    DPI_taxista = datos[4]
                    Contraseña_taxista = datos[1]
                    Correo_taxista = datos[6]
                    usuarios[DPI_taxista] = {'contrasena': Contraseña_taxista, 'correo': Correo_taxista}
    return usuarios




def iniciar_sesion(usuarios):
    usuarios = leer_usuarios()
    
    DPI_taxista = input("DPI de taxista: ")
    Contraseña_taxista = input("Contraseña: ")
    
    if DPI_taxista in usuarios and usuarios[DPI_taxista]['contrasena'] == Contraseña_taxista:
        print("Inicio de sesión exitoso.")
        mostrar_submenu(DPI_taxista)
    else:
        print("DPI o contraseña incorrectos.")
        return False


def recuperar_contrasena():
    usuarios = leer_usuarios()
    
    DPI_taxista = input("DPI de taxista: ")
    
    if DPI_taxista in usuarios:
        correo_destinatario = usuarios[DPI_taxista]['correo']
        asunto = "Recuperación de contraseña"
        Contraseña_taxista = usuarios[DPI_taxista]['contrasena']
        mensaje = f"Hola {DPI_taxista}, tu contraseña es {Contraseña_taxista}."
        
        enviar_correo(correo_destinatario, asunto, mensaje)
        print(f"Correo enviado a {correo_destinatario}.")
    else:
        print("Usuario no encontrado.")



def enviar_correo(correo_destinatario, asunto, mensaje):
    # Configuracion del servidor SMTP
    servidor = 'smtp.gmail.com'
    puerto = 587
    remitente = 'vegachanito09@gmail.com'
    contrasena = 'erxs hyqv rvoi wrel'

    # Crear el mensaje
    email_msg = MIMEMultipart()
    email_msg['From'] = remitente
    email_msg['To'] = correo_destinatario
    email_msg['Subject'] = asunto
    email_msg.attach(MIMEText(mensaje, 'plain'))

    # Conectar al servidor y enviar el correo
    try:
        server = smtplib.SMTP(servidor, puerto)
        server.starttls()
        server.login(remitente, contrasena)
        server.sendmail(remitente, correo_destinatario, email_msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")

def ingresar_viajes(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'

    # Verificar si el archivo del taxista existe
    if not os.path.exists(nombre_archivo):
        print(f"El archivo del taxista {DPI_taxista} no existe. Primero, genera su archivo.")
        return

    try:
        km_recorridos = float(input("Ingresa los kilómetros recorridos: "))
        if km_recorridos <= 0:
            print("Los kilómetros recorridos deben ser un número positivo.")
            return
    except ValueError:
        print("Por favor, ingresa un número válido para los kilómetros.")
        return

    # Calcular los valores
    monto_total_viaje = km_recorridos * 5
    salario_taxista = 0.60 * monto_total_viaje
    ganancia_empresa = 0.40 * monto_total_viaje

    # Obtener el número de viajes actuales
    num_viajes = obtener_numero_viajes(DPI_taxista) + 1

    # Guardar la información en el archivo del taxista
    with open(nombre_archivo, "a") as file:
        file.write(f"{num_viajes}\t{km_recorridos}\t{salario_taxista}\t{ganancia_empresa}\t{salario_taxista}\n")

    print(f"\nDatos guardados en {nombre_archivo}")

def mostrar_menu():
    print("MENU DEL TAXISTA")
    print("1. Inicio de sesion")
    print("2. Registro de nuevo usuario")
    print("3. Recuperar contrasena")
    print("4. Salir")

def mostrar_submenu(DPI_taxista):
    print("1. Ingreso de viajes")
    print("   Calculo de salario del mes")
    print("   Calculo de los kilometros recorridos")
    print("   Ganancias de la empresa\n")
    print("2. Ver Sueldo del mes")

    print("3. Salir")

    opcion = input("Seleccione una opcion:  ")

    if opcion == "1":
        ingresar_viajes(DPI_taxista)

    elif opcion == "2":
        Ver_sueldo_mes(DPI_taxista)

def Ver_sueldo_mes(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'

    if not os.path.exists(nombre_archivo):
        print(f"El archivo del taxista {DPI_taxista} no existe. Primero, genera su archivo.")
        return

    total_salario = 0
    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()[1:]  # Omitir la cabecera
        for linea in lineas:
            datos = linea.strip().split("\t")
            total_salario += float(datos[2])  # Salario Taxista está en la columna 3 (índice 2)

    print(f"El salario total del mes es: Q{total_salario:.2f}")


def main():
    usuarios = leer_usuarios()
    
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ")
        
        if opcion == '1':
            iniciar_sesion(usuarios)
        elif opcion == '2':
            Ingresar_nuevo_taxista()
        elif opcion == '3':
            recuperar_contrasena()
        elif opcion == '4':
            print("Gracias por usar el sistema.")
            break

Menu_principal()

