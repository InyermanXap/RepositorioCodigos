import os 
from tkinter import *
from tkinter import ttk
from tkinter import Tk, messagebox
import sys
import re
from fpdf import FPDF
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from email.message import EmailMessage

#Rutas de los archivos deben estar en la misma carpeta en caso de mover la aplicacion mover la base de datos mover las bases de datos
#Ya que si no el programa creara nuevos en blanco listos para recibir datos nuevos

BD_Admnistradores = "Administradores.txt"
BD_Taxistas = "Taxistas.txt"
BD_Taxis = "Taxis.txt"
CARPETA_FACTURAS = "facturas"
RUTA_LOGO = "C:\\Codigos769\\Parcial\\iconos\\logo.png"
#Funcion que crea las bases de datos si no estan creadas aun
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

# Definir la variable globales para evitar que se generen ventanas infinitas
Ventana_iniciar_sesion_administrador_abierta = None
Ventana_iniciar_sesion_texista_abierta = None
Ventana_registrar_taxista_abierta = None
Ventana_menu_taxi_abierta = None
Ventana_ingreso_viajes_abierta = None
Ventana_menu_administrador_abierta = None
Ventana_Ver_taxis_abierta = None
Ventana_inventario = None
ventana_asignar_abierta = None
Ventana_estado_abierta = None
Ventana_añadir_taxi = None
ventana_recuperar_abierta = None
ventana_solicitud_abierta = None
Ventana_encuesta_abierta = None
Ventana_Llenar_encuesta_abierta = None



def generar_codigo():
    ultimo_codigo = 0  # Valor inicial en caso de que no existan códigos aún

    # Verificar si el archivo ya existe
    if os.path.exists(BD_Codigos):
        with open(BD_Codigos, "r") as archivo:
            next(archivo)  # Saltar el encabezado
            for linea in archivo:
                if linea.strip():  # Asegurarse de que la línea no esté vacía
                    campos = linea.split("\t")
                    if len(campos) > 0 and campos[0].strip().isdigit():  # Verificar que haya columnas y que el primer campo sea un número
                        ultimo_codigo = int(campos[0].strip())  # Obtener el último número de código registrado
    
    nuevo_codigo = ultimo_codigo + 1  # Incrementar el código

    # Agregar el nuevo código al archivo con el estado 'Disponible'
    with open(BD_Codigos, "a") as archivo:
        # Si el archivo es nuevo, agregar el encabezado
        if os.path.getsize(BD_Codigos) == 0:
            archivo.write("No.codigo\tEstado\n")
        
        archivo.write(f"{nuevo_codigo}\tDisponible\n")

    return nuevo_codigo
#Ventana Añadir Taxi
def Añadir_taxi():
    # Ventana principal para añadir taxi
    global Ventana_añadir_taxi
    if Ventana_añadir_taxi is None or not Ventana_añadir_taxi.winfo_exists():
        ventana_taxi = Toplevel()
        ventana_taxi.title("Añadir Nuevo Taxi")
        ventana_taxi.geometry("300x200")

        Label(ventana_taxi, text="--- Añadir Nuevo Taxi al Inventario ---", font=("Arial", 12)).pack(pady=10)

        # Campo para ingresar la placa del taxi
        Label(ventana_taxi, text="Ingrese la placa del taxi:").pack(pady=5)
        entrada_placa = Entry(ventana_taxi)
        entrada_placa.pack(pady=5)

        # Botón para añadir el taxi
        Button(ventana_taxi, text="Añadir Taxi", command=lambda: añadir_nuevo_taxi(entrada_placa.get().strip(), ventana_taxi)).pack(pady=10)

        Button(ventana_taxi, text="Cerrar", command=ventana_taxi.destroy).pack(pady=5)

def añadir_nuevo_taxi(placa, ventana_taxi):
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

    # Validar que la placa no esté vacía
    if not placa:
        messagebox.showerror("Error", "La placa no puede estar vacía.")
        return
    #Validar la estrcutura de la placa
    if not re.match(r'^\d{3}[A-Za-z]{3}$', placa):
        messagebox.showerror("Error", "La placa debe tener 3 números seguidos de 3 letras (por ejemplo, 123ABC).")
        return
    # Verificar si la placa ya existe en el archivo
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            for linea in f:
                campos = linea.split("\t")
                if len(campos) > 1:  # Asegurarse de que haya al menos dos columnas (No.Taxi y Placa)
                    if campos[1].strip() == placa:  # Comparar con la placa
                        messagebox.showerror("Error", "Ya existe un taxi registrado con esta placa.")
                        return

    # Agregar el nuevo taxi a la base de datos sin asignar taxista
    with open(BD_Taxis, "a") as f:
        # Si es un archivo nuevo, agregar la cabecera
        if os.path.getsize(BD_Taxis) == 0:
            f.write("No.Taxi\tPlaca\tDPI Taxista\tNombre\tApellido\tEstado\n")

        f.write(f"{nuevo_numero_taxi}\t{placa}\tSin asignar\tSin asignar\tSin asignar\tDisponible\n")

    messagebox.showinfo("Éxito", f"El nuevo taxi ha sido añadido exitosamente con el número {nuevo_numero_taxi}.")
    ventana_taxi.destroy()

#Ventana Actualizar Estado Taxi
def Actualizar_estado_taxi():
    taxis_registrados = []

    # Verificar si el archivo de taxis existe y cargar los taxis
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")
                taxis_registrados.append(campos)

    if not taxis_registrados:
        messagebox.showinfo("Sin taxis", "No hay taxis registrados en la base de datos.")
        return

    # Crear ventana para actualizar estado de taxis
    global Ventana_estado_abierta
    if Ventana_estado_abierta is None or not Ventana_estado_abierta.winfo_exists():
        ventana_estado = Toplevel()
        ventana_estado.title("Actualizar Estado de Taxi")
        ventana_estado.geometry("400x400")

        Label(ventana_estado, text="--- Actualizar Estado de Taxi ---", font=("Arial", 14)).pack(pady=10)

        # Mostrar taxis registrados en un Listbox
        Label(ventana_estado, text="Taxis registrados:").pack(pady=5)

        listbox_taxis = Listbox(ventana_estado, width=50, height=8)
        listbox_taxis.pack(pady=5)

        for i, taxi in enumerate(taxis_registrados, start=1):
            listbox_taxis.insert(END, f"{i}. Taxi No: {taxi[0]}, Placa: {taxi[1]}, Estado actual: {taxi[5].strip()}")

        # Botón para seleccionar el taxi
        Button(ventana_estado, text="Seleccionar Taxi", command=lambda: seleccionar_taxi(listbox_taxis, taxis_registrados, ventana_estado)).pack(pady=10)

        Button(ventana_estado, text="Cerrar", command=ventana_estado.destroy).pack(pady=5)

def seleccionar_taxi(listbox_taxis, taxis_registrados, ventana_estado):
    seleccion = listbox_taxis.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Por favor seleccione un taxi.")
        return
    seleccion = seleccion[0]  # Tomar el índice seleccionado

    taxi_seleccionado = taxis_registrados[seleccion]

    # Crear nueva ventana para seleccionar el nuevo estado del taxi
    ventana_estado_nuevo = Toplevel(ventana_estado)
    ventana_estado_nuevo.title(f"Actualizar Estado del Taxi No. {taxi_seleccionado[0]}")
    ventana_estado_nuevo.geometry("300x200")

    Label(ventana_estado_nuevo, text=f"Actualizar estado del Taxi No. {taxi_seleccionado[0]}", font=("Arial", 12)).pack(pady=10)

    # Mostrar opciones de estado con botones
    Label(ventana_estado_nuevo, text="Seleccione el nuevo estado:").pack(pady=5)
    
    Button(ventana_estado_nuevo, text="Disponible", command=lambda: actualizar_estado(taxi_seleccionado, "Disponible", ventana_estado_nuevo)).pack(pady=5)
    Button(ventana_estado_nuevo, text="En uso", command=lambda: actualizar_estado(taxi_seleccionado, "En uso", ventana_estado_nuevo)).pack(pady=5)
    Button(ventana_estado_nuevo, text="En mantenimiento", command=lambda: actualizar_estado(taxi_seleccionado, "En mantenimiento", ventana_estado_nuevo)).pack(pady=5)

def actualizar_estado(taxi_seleccionado, nuevo_estado, ventana_estado_nuevo):
    # Leer todo el archivo de taxis
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            lineas = f.readlines()

        # Actualizar la línea del taxi seleccionado con el nuevo estado
        with open(BD_Taxis, "w") as f:
            for linea in lineas:
                campos = linea.strip().split("\t")
                if campos[0].strip() == taxi_seleccionado[0].strip():  # Verificar si coincide el número de taxi
                    # Reescribir la línea del taxi seleccionado con el nuevo estado
                    nueva_linea = f"{campos[0]}\t{campos[1]}\t{campos[2]}\t{campos[3]}\t{campos[4]}\t{nuevo_estado}\n"
                    f.write(nueva_linea)
                else:
                    f.write(linea)

        # Confirmar la actualización
        messagebox.showinfo("Éxito", f"El estado del Taxi No. {taxi_seleccionado[0]} ha sido actualizado a '{nuevo_estado}'.")
        ventana_estado_nuevo.destroy()

    else:
        messagebox.showerror("Error", "La base de datos de taxis no existe.")


#Ventana Asignar Taxis
def Asignar_taxis():
    taxis_disponibles = []
    
    # Verificar si el archivo de taxis existe y cargar los taxis sin asignar
    if os.path.exists(BD_Taxis):
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            for linea in f:
                campos = linea.split("\t")
                if campos[2].strip() == "Sin asignar":  # Si el taxi no tiene taxista asignado
                    taxis_disponibles.append(campos)
    
    if not taxis_disponibles:
        messagebox.showinfo("Sin taxis", "No hay taxis disponibles para asignar.")
        return
    
    # Crear ventana para asignar taxis
    global ventana_asignar_abierta
    if ventana_asignar_abierta is None or not ventana_asignar_abierta.winfo_exists():
        ventana_asignar = Toplevel()
        ventana_asignar.title("Asignar Taxi a Taxista")
        ventana_asignar.geometry("400x400")

        Label(ventana_asignar, text="--- Asignar Taxi a Taxista ---", font=("Arial", 14)).pack(pady=10)

        # Mostrar taxis disponibles en un Listbox
        Label(ventana_asignar, text="Taxis disponibles:").pack(pady=5)
        
        listbox_taxis = Listbox(ventana_asignar, width=50, height=8)
        listbox_taxis.pack(pady=5)
        
        for i, taxi in enumerate(taxis_disponibles, start=1):
            listbox_taxis.insert(END, f"{i}. Taxi No: {taxi[0]}, Placa: {taxi[1]}")
        
        # Campo de entrada para el DPI del taxista
        Label(ventana_asignar, text="Ingrese el DPI del taxista:").pack(pady=5)
        entry_dpi = Entry(ventana_asignar)
        entry_dpi.pack(pady=5)

        # Botón para asignar taxi
        Button(ventana_asignar, text="Asignar Taxi", command=lambda: confirmar_asignacion(listbox_taxis, entry_dpi, taxis_disponibles, ventana_asignar)).pack(pady=10)

        Button(ventana_asignar, text="Cerrar", command=ventana_asignar.destroy).pack(pady=5)

def confirmar_asignacion(listbox_taxis, entry_dpi, taxis_disponibles, ventana_asignar):
    # Obtener el índice seleccionado del Listbox
    seleccion = listbox_taxis.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Por favor seleccione un taxi.")
        return
    seleccion = seleccion[0]  # Tomar el índice seleccionado
    
    taxi_seleccionado = taxis_disponibles[seleccion]
    
    # Obtener el DPI del taxista
    DPI_taxista = entry_dpi.get().strip()
    
    if not DPI_taxista:
        messagebox.showerror("Error", "Por favor ingrese un DPI válido.")
        return
    
    # Verificar si el taxista está registrado
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
        messagebox.showerror("Error", "El taxista con ese DPI no está registrado.")
        return
    
    # Actualizar el taxi con el taxista seleccionado
    actualizar_taxis(taxi_seleccionado, taxista_encontrado)
    
    # Confirmar asignación
    messagebox.showinfo("Éxito", f"Taxi No. {taxi_seleccionado[0]} con placa {taxi_seleccionado[1]} ha sido asignado al taxista {taxista_encontrado[2]} {taxista_encontrado[3]}.")
    ventana_asignar.destroy()

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
        messagebox.showinfo("Éxito","El taxi ha sido actualizado correctamente.")
    else:
        messagebox.showerror("Error","La base de datos de taxis no existe.")
    if os.path.exists(BD_Taxistas):
        with open(BD_Taxistas, "r") as f:
            lineas = f.readlines()

        # Actualizar la línea del taxi seleccionado con los datos del taxista
        with open(BD_Taxistas, "w") as f:
            for linea in lineas:
                campos = linea.strip().split("\t")
                if campos[4].strip() == taxista_encontrado[4].strip():  # Verificar si coincide el número de taxi
                    # Actualizar con los datos del taxista
                    nueva_linea = f"{campos[0]}\t{campos[1]}\t{campos[2]}\\t{campos[3]}\\t{campos[4]}\t{campos[5]}\t{campos[6]}\t{taxi_seleccionado[1]}\n"
                    f.write(nueva_linea)
                else:
                    f.write(linea)
        messagebox.showinfo("Éxito","El archivo del taxista ha sido actualizado correctamente.")
    else:
        messagebox.showerror("Error","La base de datos de taxista no existe.")

#Ventana inventario Taxis
def Inventario_taxis():
    global Ventana_inventario
    if Ventana_inventario is None or not Ventana_inventario.winfo_exists():

        if not os.path.exists(BD_Taxis):
            messagebox.showerror("Error", "La base de datos de taxis no existe.")
            return
        
        # Crear una nueva ventana de Tkinter para mostrar el inventario
        ventana_inventario = Toplevel()
        ventana_inventario.title("Inventario de Taxis")
        ventana_inventario.geometry("600x400")
        
        # Encabezado del inventario
        encabezado = Label(ventana_inventario, text="--- Inventario de Taxis ---", font=("Arial", 14, "bold"))
        encabezado.pack(pady=10)
        
        # Crear un Frame para contener el inventario
        frame_inventario = Frame(ventana_inventario)
        frame_inventario.pack(pady=10)

        # Crear un Text widget para mostrar los datos
        text_area = Text(frame_inventario, wrap="none", width=70, height=15, font=("Courier", 10))
        text_area.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Agregar un Scrollbar para desplazarse si hay muchos datos
        scroll_bar = Scrollbar(frame_inventario, orient=VERTICAL, command=text_area.yview)
        scroll_bar.pack(side=RIGHT, fill=Y)
        text_area.config(yscrollcommand=scroll_bar.set)
        
        # Leer el archivo de taxis y mostrar los datos
        with open(BD_Taxis, "r") as f:
            next(f)  # Saltar la cabecera
            taxis = f.readlines()

            if not taxis:
                text_area.insert(END, "No hay taxis registrados en la base de datos.")
            else:
                # Insertar los encabezados en la Text widget
                text_area.insert(END, "No.Taxi\tPlaca\tDPI Taxista\tNombre\tApellido\tEstado\n")
                text_area.insert(END, "-"*70 + "\n")

                # Insertar los datos de los taxis
                for linea in taxis:
                    text_area.insert(END, linea.strip() + "\n")
        
        # Deshabilitar la edición del widget de texto
        text_area.config(state=DISABLED)

        # Agregar un botón para cerrar la ventana
        boton_cerrar = Button(ventana_inventario, text="Cerrar", command=ventana_inventario.destroy)
        boton_cerrar.pack(pady=10)

#Ventana Menu taxis
def Ventana_Ver_taxis():    
    global Ventana_Ver_taxis_abierta
    if Ventana_Ver_taxis_abierta is None or not Ventana_Ver_taxis_abierta.winfo_exists():
            Ventana_Ver_taxis = Tk()
            Ventana_Ver_taxis.title('Taxi Fasty Gestion De Taxis')
            Ventana_Ver_taxis.geometry("800x360")
            Ventana_Ver_taxis.config(bg = "gray")
           

            frame_Ventana_Ver_taxis = Frame(Ventana_Ver_taxis, bg="dark green", padx=20, pady=20)
            frame_Ventana_Ver_taxis.pack(expand=True)

                    # Título de la ventana
            label_titulo = Label(frame_Ventana_Ver_taxis, text=f"Gestion De Taxis ", font=("Arial", 26), bg="sky blue")
            label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

                            # Botón de inicio de sesión
            boton_Inventario_taxis = Button(frame_Ventana_Ver_taxis, text="Gestion de Taxis",command=Inventario_taxis)
            boton_Inventario_taxis.grid(row=1, column=0, columnspan=2, pady=20)

                            # Botón de inicio de sesión
            boton_asignar_taxi = Button(frame_Ventana_Ver_taxis, text="Asignar Taxi",command=Asignar_taxis)
            boton_asignar_taxi.grid(row=2, column=0, columnspan=2, pady=20)

            boton_actualizar_estado_taxi = Button(frame_Ventana_Ver_taxis, text="Actualizar Estado De Taxi",command=Actualizar_estado_taxi)
            boton_actualizar_estado_taxi.grid(row=3, column=0, columnspan=2, pady=20)

            boton_Añadir_taxi = Button(frame_Ventana_Ver_taxis, text="Añadir_taxi",command=Añadir_taxi)
            boton_Añadir_taxi.grid(row=4, column=0, columnspan=2, pady=20)


#Menu Administrador
def Ventana_menu_administrador():    
    global Ventana_menu_administrador_abierta
    if Ventana_menu_administrador_abierta is None or not Ventana_menu_administrador_abierta.winfo_exists():
            Ventana_menu_administrador = Tk()
            Ventana_menu_administrador.title('Taxi Fasty Menu Administrador')
            Ventana_menu_administrador.geometry("800x360")
            Ventana_menu_administrador.config(bg = "gray")
           

            frame_Ventana_menu_administrador = Frame(Ventana_menu_administrador, bg="dark green", padx=20, pady=20)
            frame_Ventana_menu_administrador.pack(expand=True)

                    # Título de la ventana
            label_titulo = Label(frame_Ventana_menu_administrador, text=f"Bienvenido Administrador ", font=("Arial", 26), bg="sky blue")
            label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

                            # Botón de inicio de sesión
            boton_Taxis = Button(frame_Ventana_menu_administrador, text="Gestion de Taxis",command=Ventana_Ver_taxis)
            boton_Taxis.grid(row=1, column=0, columnspan=2, pady=20)

                            # Botón de inicio de sesión
            boton_taxistas = Button(frame_Ventana_menu_administrador, text="Gestion Taxistas")#,command=crear_taxista)
            boton_taxistas.grid(row=2, column=0, columnspan=2, pady=20)


def enviar_factura_por_correo(correo_cliente, nombre_pdf):
    # Configuración del servidor SMTP
    servidor = 'smtp.gmail.com'
    puerto = 587
    remitente = 'vegachanito09@gmail.com'  # Cambia esto por tu correo
    contrasena = 'erxs hyqv rvoi wrel'  # Contraseña o clave de aplicación

    # Crear el mensaje
    email_msg = MIMEMultipart()
    email_msg['From'] = remitente
    email_msg['To'] = correo_cliente
    email_msg['Subject'] = 'Factura de su viaje con Taxi Fasty'
    cuerpo = 'Gracias por utilizar nuestros servicios. Adjunto encontrará la factura de su reciente viaje.'
    email_msg.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar la factura en PDF
    try:
        with open(nombre_pdf, 'rb') as adjunto:
            parte_adjunto = MIMEBase('application', 'octet-stream')
            parte_adjunto.set_payload(adjunto.read())
            # Codificar en base64
            import email.encoders as encoders
            encoders.encode_base64(parte_adjunto)
            parte_adjunto.add_header('Content-Disposition', f"attachment; filename={os.path.basename(nombre_pdf)}")
            email_msg.attach(parte_adjunto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo adjuntar la factura. Error: {str(e)}")
        return

    # Conectar al servidor y enviar el correo
    try:
        server = smtplib.SMTP(servidor, puerto)
        server.starttls()  # Iniciar la conexión TLS (segura)
        server.login(remitente, contrasena)  # Iniciar sesión en el servidor SMTP
        server.sendmail(remitente, correo_cliente, email_msg.as_string())  # Enviar el correo
        server.quit()  # Cerrar la conexión
        print("Correo enviado exitosamente.")
        messagebox.showinfo("Éxito", "La factura ha sido enviada correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        messagebox.showerror("Error", f"No se pudo enviar el correo. Error: {str(e)}")

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


#ventana y funcion recuperar contraseña
def recuperar_contrasena():
    # Crear ventana para recuperación de contraseña
    global ventana_recuperar_abierta
    if ventana_recuperar_abierta is None or not ventana_recuperar_abierta.winfo_exists():
        ventana_recuperar = Toplevel()
        ventana_recuperar.title("Recuperar Contraseña")
        ventana_recuperar.geometry("300x200")

        Label(ventana_recuperar, text="Recuperación de Contraseña", font=("Arial", 12)).pack(pady=10)

        Label(ventana_recuperar, text="Ingrese el DPI del taxista:").pack(pady=5)

        dpi_entry = Entry(ventana_recuperar)
        dpi_entry.pack(pady=5)

        Button(ventana_recuperar, text="Recuperar", command=lambda: procesar_recuperacion(dpi_entry.get(), ventana_recuperar)).pack(pady=10)
        
        Button(ventana_recuperar, text="Cerrar", command=ventana_recuperar.destroy).pack(pady=5)

def procesar_recuperacion(DPI_taxista, ventana_recuperar):
    usuarios = leer_usuarios()
    
    if DPI_taxista in usuarios:
        correo_destinatario = usuarios[DPI_taxista]['correo']
        asunto = "Recuperación de contraseña"
        Contraseña_taxista = usuarios[DPI_taxista]['contrasena']
        mensaje = f"Hola {DPI_taxista}, tu contraseña es {Contraseña_taxista}."

        # Enviar el correo con la contraseña
        enviar_correo(correo_destinatario, asunto, mensaje)

        messagebox.showinfo("Éxito", f"Correo enviado a {correo_destinatario}.")
        ventana_recuperar.destroy()
    else:
        messagebox.showerror("Error", "Usuario no encontrado.")

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

    messagebox.showinfo("Info",f"El salario total del mes es: Q{total_salario:.2f}")

def incrementar_numero_factura():
    archivo_num_factura = "numero_factura.txt"
    
    # Obtener el número actual
    numero_factura = obtener_numero_factura()
    nuevo_numero = numero_factura + 1
    
    # Guardar el nuevo número de factura en el archivo
    with open(archivo_num_factura, "w") as archivo:
        archivo.write(str(nuevo_numero))
    
    return nuevo_numero


def obtener_numero_factura():
    archivo_num_factura = "numero_factura.txt"
    
    # Si el archivo no existe, crearlo y comenzar desde la factura 1
    if not os.path.exists(archivo_num_factura):
        with open(archivo_num_factura, "w") as archivo:
            archivo.write("1")
        return 1
    
    # Leer el número de factura actual desde el archivo
    with open(archivo_num_factura, "r") as archivo:
        numero_factura = int(archivo.read())
    
    return numero_factura


def manejar_viaje_con_factura(DPI_taxista, Texto_kilometro_recorrido, Texto_NIT_cliente, Texto_correo_cliente):
    # Ingresar los datos del viaje
    total_viaje = ingresar_viajes(DPI_taxista, Texto_kilometro_recorrido, Texto_NIT_cliente, Texto_correo_cliente)
    
    # Generar la factura si se requiere
    nombre_pdf = generar_factura(DPI_taxista, Texto_kilometro_recorrido, Texto_NIT_cliente, Texto_correo_cliente)

    # Puedes enviar la factura si lo deseas
    enviar_factura_por_correo(Texto_correo_cliente.get(), nombre_pdf)


#Calcula el precio total del viaje dependiendo de los kilometros recorridos
def generar_factura(DPI_taxista, Texto_kilometro_recorrido, Texto_NIT_cliente, Texto_correo_cliente,Texto_Direccion_cliente,Texto_Nombre_cliente):
    # Asegurarse de que la carpeta de facturas existe
    if not os.path.exists(CARPETA_FACTURAS):
        os.makedirs(CARPETA_FACTURAS)

    # Información de la factura
    km_recorridos = float(Texto_kilometro_recorrido.get())
    monto_total_viaje = km_recorridos * 5
    NIT_cliente = Texto_NIT_cliente.get()
    correo_cliente = Texto_correo_cliente.get()
    nombre_cliente = Texto_Nombre_cliente.get()
    Direccion_cliente = Texto_Direccion_cliente.get()
    nuevo_codigo = generar_codigo()
    print(f"Se ha generado el nuevo código: {nuevo_codigo}")
    # Obtener y actualizar el número de factura
    numero_factura = incrementar_numero_factura()

    # Crear un objeto PDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar el logotipo en la parte superior izquierda
    if os.path.exists(RUTA_LOGO):
        pdf.image(RUTA_LOGO, x=10, y=8, w=33)  # Ajustar la posición y tamaño del logo

    # Mover el cursor del PDF hacia abajo después del logo
    pdf.set_y(50)

        # Título de la factura
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f'Factura #{numero_factura}', ln=True, align='C')

    # Datos del cliente
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, 'Taxi Fasty', ln=True)
    pdf.cell(200, 10, 'Dirección: Ciudad de Guatemala', ln=True)
    pdf.cell(200, 10, 'NIT 123456789', ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f'NIT del Cliente: {NIT_cliente}', ln=True)
    pdf.cell(200, 10, f'Nombre del Cliente: {nombre_cliente}', ln=True)
    pdf.cell(200, 10, f'Dirección del Cliente: {Direccion_cliente}', ln=True)
    pdf.cell(200, 10, f'Codigo de Viaje: {nuevo_codigo}', ln=True)

    # Línea separadora
    pdf.ln(10)
    pdf.cell(0, 10, '--------------------------------------------', 0, 1, 'C')
    pdf.ln(5)

    # Información del viaje
    pdf.cell(200, 10, f'Kilómetros Recorridos: {km_recorridos} km', ln=True)
    pdf.cell(200, 10, f'Monto Total del Viaje: Q{monto_total_viaje:.2f}', ln=True)

    # Total a pagar
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, f'Total a Pagar: Q{monto_total_viaje:.2f}', ln=True, align='R')

    # Guardar el PDF en la carpeta de facturas con el número de factura
    nombre_pdf = os.path.join(CARPETA_FACTURAS, f'Factura_{numero_factura}.pdf')
    pdf.output(nombre_pdf)

    print(f"Factura #{numero_factura} generada correctamente en {nombre_pdf}")
    enviar_factura_por_correo(correo_cliente, nombre_pdf)
    
def obtener_numero_viajes(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'
    
    # Si el archivo no existe, el número de viajes es 0
    if not os.path.exists(nombre_archivo):
        return 0  
    
    # Contar el número de líneas (viajes), restando la cabecera
    with open(nombre_archivo, "r") as file:
        lineas = file.readlines()
        return len(lineas) - 1  # Restar 1 para omitir la cabecera


# Modificar la función ingresar_viajes para devolver el número de la factura generada
def ingresar_viajes(DPI_taxista, Texto_kilometro_recorrido,):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'

    if not os.path.exists(nombre_archivo):
        messagebox.showerror("Error", f"El archivo del taxista {DPI_taxista} no existe. Primero, genera su archivo.")
        return

    try:
        km_recorridos = float(Texto_kilometro_recorrido.get())
        if km_recorridos <= 0:
            messagebox.showerror("Error", "Los kilómetros recorridos deben ser un número positivo.")
            return
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para los kilómetros.")
        return

    monto_total_viaje = km_recorridos * 5
    salario_taxista = 0.60 * monto_total_viaje
    ganancia_empresa = 0.40 * monto_total_viaje
    num_viajes = obtener_numero_viajes(DPI_taxista) + 1

    with open(nombre_archivo, "a") as file:
        file.write(f"{num_viajes}\t{km_recorridos}\t{salario_taxista}\t{ganancia_empresa}\t{salario_taxista}\n")
        messagebox.showinfo("Aviso", f"El total es de Q{monto_total_viaje}")

    return monto_total_viaje  # Solo retornamos el monto total del viaje


def Ventana_ingreso_viajes(DPI_taxista):
    global Ventana_ingreso_viajes_abierta

    if Ventana_ingreso_viajes_abierta is None or not Ventana_ingreso_viajes_abierta.winfo_exists():
        Ventana_ingreso_viajes_abierta = Toplevel()
        Ventana_ingreso_viajes_abierta.title("USAC Administrador")
        Ventana_ingreso_viajes_abierta.geometry("500x400")
        Ventana_ingreso_viajes_abierta.config(bg="dark green")

        frame_ingreso_viajes = Frame(Ventana_ingreso_viajes_abierta, bg="dark green", padx=20, pady=20)
        frame_ingreso_viajes.pack(expand=True)

        label_titulo = Label(frame_ingreso_viajes, text="Calcular el viaje", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        label_kilometro_recorrido = Label(frame_ingreso_viajes, text="Ingrese la cantidad de kilómetros recorridos", bg="dark green")
        label_kilometro_recorrido.grid(row=1, column=0, pady=10, padx=10)

        Texto_kilometro_recorrido = Entry(frame_ingreso_viajes, justify="center")
        Texto_kilometro_recorrido.grid(row=1, column=1, pady=10, padx=10)

        label_NIT_cliente = Label(frame_ingreso_viajes, text="Ingrese el NIT del Cliente", bg="dark green")
        label_NIT_cliente.grid(row=2, column=0, pady=10, padx=10)

        Texto_NIT_cliente = Entry(frame_ingreso_viajes, justify="center")
        Texto_NIT_cliente.grid(row=2, column=1, pady=10, padx=10)

        label_Nombre_cliente = Label(frame_ingreso_viajes, text="Ingrese el Nombre del cliente", bg="dark green")
        label_Nombre_cliente.grid(row=3, column=0, pady=10, padx=10)

        Texto_Nombre_cliente = Entry(frame_ingreso_viajes, justify="center")
        Texto_Nombre_cliente.grid(row=3, column=1, pady=10, padx=10)

        label_Direccion_cliente = Label(frame_ingreso_viajes, text="Ingrese Direccion", bg="dark green")
        label_Direccion_cliente.grid(row=4, column=0, pady=10, padx=10)

        Texto_Direccion_cliente = Entry(frame_ingreso_viajes, justify="center")
        Texto_Direccion_cliente.grid(row=4, column=1, pady=10, padx=10)

        label_correo_cliente = Label(frame_ingreso_viajes, text="Ingrese el correo del cliente para mandar la factura", bg="dark green")
        label_correo_cliente.grid(row=5, column=0, pady=10, padx=10)

        Texto_correo_cliente = Entry(frame_ingreso_viajes, justify="center")
        Texto_correo_cliente.grid(row=5, column=1, pady=10, padx=10)

        # Variable para almacenar el número de factura generada
        numero_factura_generada = None

        # Botón para calcular y generar la factura
        boton_calcular_viaje = Button(frame_ingreso_viajes, text="Calcular Viaje", 
                                      command=lambda: ingresar_viajes(DPI_taxista, Texto_kilometro_recorrido))
        boton_calcular_viaje.grid(row=6, column=0, columnspan=2, pady=20)

        # Botón para enviar la factura después de que se ha generado
        boton_enviar_factura = Button(frame_ingreso_viajes, text="Enviar Factura", 
                                      command=lambda:generar_factura(DPI_taxista, Texto_kilometro_recorrido, Texto_NIT_cliente, Texto_correo_cliente,Texto_Direccion_cliente,Texto_Nombre_cliente) )
        boton_enviar_factura.grid(row=7, column=0, columnspan=2, pady=20)

    
def Ventana_menu_taxi(DPI_taxista):    
    global Ventana_menu_taxi_abierta
    if Ventana_menu_taxi_abierta is None or not Ventana_menu_taxi_abierta.winfo_exists():
            Ventana_menu_taxista = Tk()
            Ventana_menu_taxista.title('Taxi Fasty Menu Taxista')
            Ventana_menu_taxista.geometry("800x360")
            Ventana_menu_taxista.config(bg = "gray")
           

            frame_Ventana_menu_taxista = Frame(Ventana_menu_taxista, bg="dark green", padx=20, pady=20)
            frame_Ventana_menu_taxista.pack(expand=True)

                    # Título de la ventana
            label_titulo = Label(frame_Ventana_menu_taxista, text=f"Bienvenido{DPI_taxista} ", font=("Arial", 26), bg="sky blue")
            label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

                            # Botón de inicio de sesión
            boton_ingreso_viajes = Button(frame_Ventana_menu_taxista, text="Ingreso de viajes\n Creacion de facturas",command=lambda:Ventana_ingreso_viajes(DPI_taxista))
            boton_ingreso_viajes.grid(row=1, column=0, columnspan=2, pady=20)

                            # Botón de inicio de sesión
            boton_ver_sueldo = Button(frame_Ventana_menu_taxista, text="Ver sueldo del mes",command=lambda:Ver_sueldo_mes(DPI_taxista))
            boton_ver_sueldo.grid(row=2, column=0, columnspan=2, pady=20)

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

def Iniciar_sesion_taxista(Texto_usuario_taxista, Texto_contraseña_taxista):
    usuarios = leer_usuarios()
    
    DPI_taxista = Texto_usuario_taxista.get()
    Contraseña_taxista = Texto_contraseña_taxista.get()
    
    if DPI_taxista in usuarios and usuarios[DPI_taxista]['contrasena'] == Contraseña_taxista:
        Ventana_menu_taxi(DPI_taxista)
    else:
        messagebox.showerror("Error","DPI o contraseña incorrectos.")
    

def generar_archivo_taxista(DPI_taxista):
    nombre_archivo = f'{DPI_taxista.replace(" ", "_")}.txt'
    
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w') as f:
            f.write("No.Viajes\tKilometros\tSalario\tGanancia empresa\tGanancia Taxista\n")
        messagebox.showinfo("Aviso",f"Archivo {nombre_archivo} creado correctamente.")
    else:
        messagebox.showerror("Error",f"El archivo {nombre_archivo} ya existe.")

def validar_nombre_apellido(nombre):
    """Valida que el nombre o apellido solo contenga letras"""
    return bool(re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nombre))

def validar_correo(correo):
    """Valida el formato de correo electrónico"""
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo))

def validar_telefono(telefono):
    """Valida que el teléfono contenga solo números y tenga solo 8 dígitos)"""
    return bool(re.match(r'^\d{8}$', telefono))

def validar_auto_taxista(placa):
    # Si la placa está vacía, retorna True (permitir)
    if not placa:
        return True
    # Si la placa no está vacía, realiza la validación
    return bool(re.match(r'^\d{3}[A-Za-z]{3}$', placa))

def validar_dpi(dpi):
    """Valida que el DPI tenga exactamente 13 dígitos"""
    return bool(re.match(r'^\d{13}$', dpi))

def validar_contrasena(Contraseña_taxista):

    if (len(Contraseña_taxista) >= 8 and 
        re.search(r'[A-Z]', Contraseña_taxista) and 
        re.search(r'[0-9]', Contraseña_taxista) and 
        re.search(r'[!@#$%^&*(),.?":{}|<>]', Contraseña_taxista)):
        return True
    return False

def Registrar_taxista(texto_Nombre_taxista, texto_Apellido_taxista, texto_DPI_taxista, texto_Tel_taxista, texto_Correo_taxista, texto_Auto_taxista, texto_Contraseña_taxista, texto_Confirmacion_contraseña_taxista):
    # Obtener valores de los campos
    Nombre_taxista = texto_Nombre_taxista.get()
    Apellido_taxista = texto_Apellido_taxista.get()
    DPI_taxista = texto_DPI_taxista.get()
    Tel_taxista = texto_Tel_taxista.get()
    Correo_taxista = texto_Correo_taxista.get()
    Auto_taxista = texto_Auto_taxista.get()
    Contraseña_taxista = texto_Contraseña_taxista.get()
    Confirmacion_contraseña_taxista = texto_Confirmacion_contraseña_taxista.get()
    
    # Validaciones
    if not validar_nombre_apellido(Nombre_taxista):
        messagebox.showerror("Error", "El nombre solo debe contener letras. Por favor, revisa el formato.")
        return

    if not validar_nombre_apellido(Apellido_taxista):
        messagebox.showerror("Error", "El apellido solo debe contener letras. Por favor, revisa el formato.")
        return

    if not validar_dpi(DPI_taxista):
        messagebox.showerror("Error", "El DPI debe tener exactamente 13 dígitos.")
        return

    if not validar_telefono(Tel_taxista):
        messagebox.showerror("Error", "El número de teléfono debe contener entre 8 dígitos.")
        return

    if not validar_correo(Correo_taxista):
        messagebox.showerror("Error", "El formato del correo no es válido. Debe ser: ejemplo@dominio.com")
        return

    if not validar_auto_taxista(Auto_taxista):
        messagebox.showerror("Error", "La placa debe tener 3 números seguidos de 3 letras (por ejemplo, 123ABC).")
        return
    
    if Contraseña_taxista != Confirmacion_contraseña_taxista:
        messagebox.showerror("Error", "Las contraseñas no coinciden. Por favor, revisa los campos.")
        return

    if not validar_contrasena(Contraseña_taxista):  # Asumimos que esta función ya está implementada
        messagebox.showerror("Error", "La contraseña no cumple con los requisitos.")
        return
    
    # Si todas las validaciones pasan, se procede con el registro (similar al código original)
    with open(BD_Taxistas, "a") as f:
        f.write(f"Taxista\t{Contraseña_taxista}\t{Nombre_taxista}\t{Apellido_taxista}\t{DPI_taxista}\t{Tel_taxista}\t{Correo_taxista}\t{Auto_taxista}\n")
    

    
    generar_archivo_taxista(DPI_taxista)  # Asumimos que esta función ya está implementada
    messagebox.showinfo("Aviso", "Registro exitoso.")


            #Verifica las credenciales del administrador
def Iniciar_sesion_administrador(Texto_usuario_admni,Texto_contraseña_admni):
    Usuario_admni = Texto_usuario_admni.get()
    Contraseña_admni = Texto_contraseña_admni.get()
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
                        Ventana_menu_administrador()
                        return
                else:
                    messagebox.showerror("Error","Credenciales incorrectas. Por favor, intentelo de nuevo.")
                    return       
                
                
                #Ventana para ingresar datos para registrar taxista
def Ventana_taxedratico_registro():
        # Verificar si la ventana ya existe o no
    global Ventana_registrar_taxista_abierta
    if Ventana_registrar_taxista_abierta is None or not Ventana_registrar_taxista_abierta.winfo_exists():
            # Crear la ventana del menú del administrador
        Ventana_registrar_taxista = Toplevel()
        Ventana_registrar_taxista.title("Taxi Fasti Registrar taxistas")
        Ventana_registrar_taxista.geometry("700x700")
        Ventana_registrar_taxista.config(bg="dark green")

            # Crear el frame dentro de la nueva ventana
        frame_registrar_taxista = Frame(Ventana_registrar_taxista, bg="dark green", padx=20, pady=20)
        frame_registrar_taxista.pack(expand=True)

        # Título de la ventana
        label_titulo = Label(frame_registrar_taxista, text="Registrar Nuevo Taxista", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiqueta y entrada para el nombre del taxedrático
        label_nombre_tax = Label(frame_registrar_taxista, text="Ingrese el Nombre del taxista", bg="dark green")
        label_nombre_tax.grid(row=1, column=0, pady=10, padx=10)
        texto_Nombre_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Nombre_taxista.grid(row=1, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el apellido del taxedrático
        label_apellido_tax = Label(frame_registrar_taxista, text="Ingrese el Apellido del taxista", bg="dark green")
        label_apellido_tax.grid(row=2, column=0, pady=10, padx=10)
        texto_Apellido_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Apellido_taxista.grid(row=2, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el DPI del taxedrático
        label_dpi_tax = Label(frame_registrar_taxista, text="Ingrese el DPI del taxista", bg="dark green")
        label_dpi_tax.grid(row=3, column=0, pady=10, padx=10)
        texto_DPI_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_DPI_taxista.grid(row=3, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el DPI del taxedrático
        label_tel_tax = Label(frame_registrar_taxista, text="Ingrese el Telefono del taxista", bg="dark green")
        label_tel_tax.grid(row=4, column=0, pady=10, padx=10)
        texto_Tel_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Tel_taxista.grid(row=4, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el DPI del taxedrático
        label_correo_tax = Label(frame_registrar_taxista, text="Ingrese el correo del taxista", bg="dark green")
        label_correo_tax.grid(row=5, column=0, pady=10, padx=10)
        texto_Correo_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Correo_taxista.grid(row=5, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el DPI del taxedrático
        label_taxi_tax = Label(frame_registrar_taxista, text="Ingrese la placa del taxi que se le asignara al taxista", bg="dark green")
        label_taxi_tax.grid(row=6, column=0, pady=10, padx=10)
        texto_Auto_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Auto_taxista.grid(row=6, column=1, pady=10, padx=10)

        # Etiqueta y entrada para la contraseña
        label_contrasena_tax = Label(frame_registrar_taxista, text="Contrasena (minimo 8 caracteres, 1 mayuscula, 1 numero, 1 caracter especial", bg="dark green")
        label_contrasena_tax.grid(row=8, column=0, pady=10, padx=10)
        texto_Contraseña_taxista = Entry(frame_registrar_taxista, justify="center", show="*")
        texto_Contraseña_taxista.grid(row=8, column=1, pady=10, padx=10)

        label_confirmacion_tax = Label(frame_registrar_taxista, text="Confirme la Contraseña", bg="dark green")
        label_confirmacion_tax.grid(row=9, column=0, pady=10, padx=10)
        texto_Confirmacion_contraseña_taxista = Entry(frame_registrar_taxista, justify="center", show="*")
        texto_Confirmacion_contraseña_taxista.grid(row=9, column=1, pady=10, padx=10)
        

        # Botón para registrar
        boton_registrar_tax = Button(frame_registrar_taxista, text="Registrar",command=lambda: Registrar_taxista(texto_Nombre_taxista,texto_Apellido_taxista,texto_DPI_taxista,texto_Tel_taxista,texto_Correo_taxista,texto_Auto_taxista,texto_Contraseña_taxista,texto_Confirmacion_contraseña_taxista))
        boton_registrar_tax.grid(row=10, column=0, columnspan=2, pady=20)

    else:
        # Si la ventana ya está abierta, simplemente traerla al frente
        Ventana_registrar_taxista_abierta.lift()

#Ventana para solicitar viaje
def Solicitar_taxi():
    # Crear la ventana principal
    global ventana_solicitud_abierta
    if ventana_solicitud_abierta is None or not ventana_solicitud_abierta.winfo_exists():
        ventana_solicitud = Toplevel()
        ventana_solicitud.title("Solicitud de Taxi")
        ventana_solicitud.geometry("400x500")
        
        Label(ventana_solicitud, text="Bienvenido querido cliente", font=("Arial", 12)).pack(pady=10)
        Label(ventana_solicitud, text="Ingrese sus datos y seleccione un taxista").pack(pady=5)

        # Entrada de datos del cliente
        Label(ventana_solicitud, text="Nombre:").pack(pady=5)
        nombre_cliente = Entry(ventana_solicitud)
        nombre_cliente.pack(pady=5)

        Label(ventana_solicitud, text="Dirección de recogida:").pack(pady=5)
        direccion_cliente = Entry(ventana_solicitud)
        direccion_cliente.pack(pady=5)

        Label(ventana_solicitud, text="Correo electrónico:").pack(pady=5)
        correo_cliente = Entry(ventana_solicitud)
        correo_cliente.pack(pady=5)

        Label(ventana_solicitud, text="Número de contacto:").pack(pady=5)
        numero_cliente = Entry(ventana_solicitud)
        numero_cliente.pack(pady=5)

        # Mostrar taxistas disponibles
        Label(ventana_solicitud, text="Seleccione su taxista:").pack(pady=5)
        lista_taxistas = Listbox(ventana_solicitud)
        lista_taxistas.pack(pady=5, fill=BOTH, expand=True)

        taxistas_disponibles = []

        # Verificamos si la base de datos de taxistas existe
        if os.path.exists(BD_Taxistas):
            with open(BD_Taxistas, "r") as f:
                next(f)  # Saltar la cabecera
                for linea in f:
                    campos = linea.strip().split("\t")
                    if len(campos) >= 7:  # Asegurarse de que hay suficientes campos
                        taxista = {
                            'DPI': campos[4],  # DPI del taxista
                            'nombre': campos[2],  # Nombre del taxista
                            'apellido': campos[3],  # Apellido del taxista
                            'correo': campos[6],  # Correo del taxista
                            'automovil': campos[7] if len(campos) > 7 else "Sin asignar"  # Automóvil (si existe)
                        }
                        taxistas_disponibles.append(taxista)
                        lista_taxistas.insert(END, f"{taxista['nombre']} {taxista['apellido']} - Automóvil: {taxista['automovil']}")

        if not taxistas_disponibles:
            messagebox.showinfo("Sin taxistas", "No hay taxistas disponibles en este momento.")
            return
    
    # Función para procesar la selección del taxista y enviar los datos
    def seleccionar_taxista():
        seleccion = lista_taxistas.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un taxista.")
            return

        taxista_seleccionado = taxistas_disponibles[seleccion[0]]
        
        # Recopilar datos del cliente
        texto_nombre_cliente = nombre_cliente.get()
        texto_direccion_cliente = direccion_cliente.get()
        texto_correo_cliente = correo_cliente.get()
        texto_numero_cliente = numero_cliente.get()

        if not texto_nombre_cliente or not texto_direccion_cliente or not texto_correo_cliente or not texto_numero_cliente:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Mostrar selección al usuario
        messagebox.showinfo("Taxista seleccionado", f"Ha seleccionado al taxista {taxista_seleccionado['nombre']} {taxista_seleccionado['apellido']} con el automóvil {taxista_seleccionado['automovil']}.")

        # Llamar a la función Solicitud_cliente con los datos
        Solicitud_cliente(texto_correo_cliente, texto_numero_cliente, texto_nombre_cliente, texto_direccion_cliente, taxista_seleccionado)

    # Botón para confirmar la selección del taxista
    Button(ventana_solicitud, text="Confirmar y Solicitar Taxi", command=seleccionar_taxista).pack(pady=10)

    # Botón para cerrar la ventana
    Button(ventana_solicitud, text="Cancelar", command=ventana_solicitud.destroy).pack(pady=5)

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
    enviar_correo_taxista(correo_destinatario_cliente, asunto, mensaje)
    messagebox.showinfo("Aviso",f"Su taxista ha sido informado")

def guardar_datos_encuesta_txt(calificacion_1, calificacion_2, calificacion_3, calificacion_4, recomendacion, comentarios):
    nombre_archivo = "encuestas.txt"
    
    with open(nombre_archivo, mode='a', encoding='utf-8') as archivo_txt:
        archivo_txt.write("Encuesta de Satisfacción:\n")
        archivo_txt.write(f"1. Actitud del taxista: {calificacion_1}\n")
        archivo_txt.write(f"2. Condiciones del taxi: {calificacion_2}\n")
        archivo_txt.write(f"3. Limpieza del taxi: {calificacion_3}\n")
        archivo_txt.write(f"4. Rapidez del taxista en llegar: {calificacion_4}\n")
        archivo_txt.write(f"5. Recomendación: {recomendacion}\n")
        archivo_txt.write(f"6. Comentarios adicionales: {comentarios}\n")
        archivo_txt.write("-" * 40 + "\n")  # Separador entre encuestas
    
    print("Respuestas guardadas exitosamente en un archivo de texto.")

# Función para mostrar la ventana de la encuesta de satisfacción
def Ventana_Llenar_encuesta(Texto_codigo):
    codigo_viaje = Texto_codigo.get()

    # Simulación de verificación del código
    if not verificar_codigo_disponible(codigo_viaje):
        messagebox.showerror("Error", "El código ingresado no está disponible o ya ha sido utilizado.")
        return

    # Crear la ventana para la encuesta
    Ventana_Llenar_encuesta_abierta = tk.Toplevel()
    Ventana_Llenar_encuesta_abierta.title("Encuesta de Satisfacción")
    Ventana_Llenar_encuesta_abierta.geometry("400x600")

    # Pregunta 1: Actitud del taxista
    label_pregunta_1 = tk.Label(Ventana_Llenar_encuesta_abierta, text="¿Cómo calificaría la actitud del taxista?")
    label_pregunta_1.pack(pady=5)
    respuesta_1 = tk.StringVar()  
    opciones_pregunta_1 = ["Excelente", "Bueno", "Regular", "Malo"]
    for opcion in opciones_pregunta_1:
        tk.Radiobutton(Ventana_Llenar_encuesta_abierta, text=opcion, variable=respuesta_1, value=opcion).pack()

    # Pregunta 2: Condiciones del taxi
    label_pregunta_2 = tk.Label(Ventana_Llenar_encuesta_abierta, text="¿Cómo calificaría las condiciones del taxi?")
    label_pregunta_2.pack(pady=5)
    respuesta_2 = tk.StringVar()  
    opciones_pregunta_2 = ["Excelente", "Bueno", "Regular", "Malo"]
    for opcion in opciones_pregunta_2:
        tk.Radiobutton(Ventana_Llenar_encuesta_abierta, text=opcion, variable=respuesta_2, value=opcion).pack()

    # Pregunta 3: Limpieza del taxi
    label_pregunta_3 = tk.Label(Ventana_Llenar_encuesta_abierta, text="¿Cómo calificaría la limpieza del taxi?")
    label_pregunta_3.pack(pady=5)
    respuesta_3 = tk.StringVar()  
    opciones_pregunta_3 = ["Excelente", "Bueno", "Regular", "Malo"]
    for opcion in opciones_pregunta_3:
        tk.Radiobutton(Ventana_Llenar_encuesta_abierta, text=opcion, variable=respuesta_3, value=opcion).pack()

    # Pregunta 4: Rapidez del taxista en llegar
    label_pregunta_4 = tk.Label(Ventana_Llenar_encuesta_abierta, text="¿Cómo calificaría la rapidez del taxista en llegar?")
    label_pregunta_4.pack(pady=5)
    respuesta_4 = tk.StringVar()  
    opciones_pregunta_4 = ["Excelente", "Bueno", "Regular", "Malo"]
    for opcion in opciones_pregunta_4:
        tk.Radiobutton(Ventana_Llenar_encuesta_abierta, text=opcion, variable=respuesta_4, value=opcion).pack()

    # Pregunta 5: Recomendación
    label_pregunta_5 = tk.Label(Ventana_Llenar_encuesta_abierta, text="¿Recomendaría nuestro servicio a otras personas?")
    label_pregunta_5.pack(pady=5)
    respuesta_5 = tk.StringVar()  
    opciones_pregunta_5 = ["Sí", "No"]
    for opcion in opciones_pregunta_5:
        tk.Radiobutton(Ventana_Llenar_encuesta_abierta, text=opcion, variable=respuesta_5, value=opcion).pack()

    # Pregunta 6: Comentarios adicionales
    label_pregunta_6 = tk.Label(Ventana_Llenar_encuesta_abierta, text="Comentarios adicionales:")
    label_pregunta_6.pack(pady=5)
    texto_comentarios = tk.Text(Ventana_Llenar_encuesta_abierta, height=4, width=40)
    texto_comentarios.pack(pady=5)

    # Función para enviar las respuestas
    def enviar_respuestas():
        calificacion_1 = respuesta_1.get()
        calificacion_2 = respuesta_2.get()
        calificacion_3 = respuesta_3.get()
        calificacion_4 = respuesta_4.get()
        recomendacion = respuesta_5.get()
        comentarios = texto_comentarios.get("1.0", tk.END).strip()

        # Validar que todas las preguntas se respondan (excepto comentarios)
        if not (calificacion_1 and calificacion_2 and calificacion_3 and calificacion_4 and recomendacion):
            messagebox.showerror("Error", "Por favor, responde todas las preguntas.")
            return

        # Guardar las respuestas en el archivo de texto
        guardar_datos_encuesta_txt(calificacion_1, calificacion_2, calificacion_3, calificacion_4, recomendacion, comentarios)

        # Mostrar mensaje de éxito y cerrar la ventana
        messagebox.showinfo("Gracias", "Gracias por completar la encuesta.")
        Ventana_Llenar_encuesta_abierta.destroy()

    # Botón para enviar las respuestas
    boton_enviar = tk.Button(Ventana_Llenar_encuesta_abierta, text="Enviar", command=enviar_respuestas)
    boton_enviar.pack(pady=20)

def actualizar_estado_codigo(codigo_viaje):
    if os.path.exists(BD_Codigos):
        with open(BD_Codigos, "r") as f:
            lineas = f.readlines()

        with open(BD_Codigos, "w") as f:
            for linea in lineas:
                campos = linea.strip().split("\t")
                if campos[0] == codigo_viaje and campos[1] == "Disponible":  # Buscar el código y su estado
                    nueva_linea = f"{campos[0]}\tUtilizado\n"  # Cambiar estado a "Utilizado"
                else:
                    nueva_linea = linea  # Mantener los demás datos sin cambios
                f.write(nueva_linea)

def verificar_codigo_disponible(codigo_viaje):
    """
    Verifica si el código de viaje está disponible.
    Retorna True si está disponible, de lo contrario False.
    """
    if os.path.exists(BD_Codigos):
        with open(BD_Codigos, "r") as f:
            for linea in f:
                campos = linea.strip().split("\t")
                if campos[0] == codigo_viaje and campos[1] == "Disponible":  # Comparar código y estado
                    return True  # El código está disponible
    return False  # El código no está disponible o no existe

def Ventana_encuesta():

    global Ventana_encuesta_abierta

    if Ventana_encuesta_abierta is None or not Ventana_encuesta_abierta.winfo_exists():
        # Solo crear la ventana si no existe o si se ha cerrado
        Ventana_encuesta_abierta = tk.Toplevel()
        Ventana_encuesta_abierta.title("Encuesta de Satisfacción")
        Ventana_encuesta_abierta.geometry("500x400")
        Ventana_encuesta_abierta.config(bg="dark green")

        # Crear el frame dentro de la nueva ventana
        frame_encuesta = tk.Frame(Ventana_encuesta_abierta, bg="dark green", padx=20, pady=20)
        frame_encuesta.pack(expand=True)

        # Título de la ventana
        label_titulo = tk.Label(frame_encuesta, text="Encuesta de Satisfacción", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiqueta y entrada para usuario
        label_codigo = tk.Label(frame_encuesta, text="Ingrese su código de viaje:", bg="dark green")
        label_codigo.grid(row=1, column=0, pady=10, padx=10)

        Texto_codigo = tk.Entry(frame_encuesta, justify="center")
        Texto_codigo.grid(row=1, column=1, pady=10, padx=10)
        codigo_viaje =Texto_codigo.get()
        # Botón para verificar el código e iniciar la encuesta
        boton_verificar_codigo = tk.Button(frame_encuesta, text="Verificar Código", command=lambda:Ventana_Llenar_encuesta(Texto_codigo))
        boton_verificar_codigo.grid(row=2, column=0, columnspan=2, pady=10)

                
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
        messagebox.showinfo("Aviso","Correo enviado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error",f"Error al enviar correo: {str(e)}")

                #Ventana para ingresar datos de inicio de sesion de taxista
def Ventana_iniciar_sesion_texista():

    global Ventana_iniciar_sesion_texista_abierta

    if Ventana_iniciar_sesion_texista_abierta is None or not Ventana_iniciar_sesion_texista_abierta.winfo_exists():
        # Solo crear la ventana si no existe o si se ha cerrado
        Ventana_iniciar_sesion_texista_abierta = Toplevel()
        Ventana_iniciar_sesion_texista_abierta.title("Iniciar Sesion Taxista")
        Ventana_iniciar_sesion_texista_abierta.geometry("500x400")
        Ventana_iniciar_sesion_texista_abierta.config(bg="dark green")

            # Crear el frame dentro de la nueva ventana
        frame_inicio_taxista = Frame(Ventana_iniciar_sesion_texista_abierta, bg="dark green", padx=20, pady=20)
        frame_inicio_taxista.pack(expand=True)

            # Título de la ventana
        label_titulo = Label(frame_inicio_taxista, text="Iniciar Sesion Taxista", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

            # Etiqueta y entrada para usuario
        label_usuario = Label(frame_inicio_taxista, text="Ingrese su usuario", bg="dark green")
        label_usuario.grid(row=1, column=0, pady=10, padx=10)

        Texto_usuario_taxista = Entry(frame_inicio_taxista, justify="center")
        Texto_usuario_taxista.grid(row=1, column=1, pady=10, padx=10)

            # Etiqueta y entrada para contraseña
        label_contraseña = Label(frame_inicio_taxista, text="Ingrese su contraseña", bg="dark green")
        label_contraseña.grid(row=2, column=0, pady=10, padx=10)

        Texto_contraseña_taxista = Entry(frame_inicio_taxista, justify="center", show="*")  # El `show="*"` oculta el texto de la contraseña
        Texto_contraseña_taxista.grid(row=2, column=1, pady=10, padx=10)

            # Botón de inicio de sesión
        boton_iniciar_sesion = Button(frame_inicio_taxista, text="Iniciar Sesión",command=lambda: Iniciar_sesion_taxista(Texto_usuario_taxista, Texto_contraseña_taxista))
        boton_iniciar_sesion.grid(row=3, column=0, columnspan=2, pady=10)

        boton_registrar_taxista = Button(frame_inicio_taxista, text="Registrar Taxista",command=Ventana_taxedratico_registro)
        boton_registrar_taxista.grid(row=4, column=0, columnspan=2, pady=10)

        boton_recuperar_contraseña = Button(frame_inicio_taxista, text="Recuperar Contraseña",command=recuperar_contrasena)
        boton_recuperar_contraseña.grid(row=5, column=0, columnspan=2, pady=10)

    else:
            # Si la ventana ya está abierta, simplemente enfócala
        Ventana_iniciar_sesion_texista_abierta.lift()
    
                        
            
                      #Ventana donde se llena la informacion para el inicio de sesion del administrador
def Ventana_iniciar_sesion_administrador():

    global Ventana_iniciar_sesion_administrador_abierta

    if Ventana_iniciar_sesion_administrador_abierta is None or not Ventana_iniciar_sesion_administrador_abierta.winfo_exists():
        # Solo crear la ventana si no existe o si se ha cerrado
        Ventana_iniciar_sesion_administrador_abierta = Toplevel()
        Ventana_iniciar_sesion_administrador_abierta.title("USAC Administrador")
        Ventana_iniciar_sesion_administrador_abierta.geometry("400x300")
        Ventana_iniciar_sesion_administrador_abierta.config(bg="dark green")

            # Crear el frame dentro de la nueva ventana
        frame_inicio_admni = Frame(Ventana_iniciar_sesion_administrador_abierta, bg="dark green", padx=20, pady=20)
        frame_inicio_admni.pack(expand=True)

            # Título de la ventana
        label_titulo = Label(frame_inicio_admni, text="Iniciar Sesion Administrador", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

            # Etiqueta y entrada para usuario
        label_usuario = Label(frame_inicio_admni, text="Ingrese su usuario", bg="dark green")
        label_usuario.grid(row=1, column=0, pady=10, padx=10)

        Texto_usuario_admni = Entry(frame_inicio_admni, justify="center")
        Texto_usuario_admni.grid(row=1, column=1, pady=10, padx=10)

            # Etiqueta y entrada para contraseña
        label_contraseña = Label(frame_inicio_admni, text="Ingrese su contraseña", bg="dark green")
        label_contraseña.grid(row=2, column=0, pady=10, padx=10)

        Texto_contraseña_admni = Entry(frame_inicio_admni, justify="center", show="*")  # El `show="*"` oculta el texto de la contraseña
        Texto_contraseña_admni.grid(row=2, column=1, pady=10, padx=10)

            # Botón de inicio de sesión
        boton_iniciar_sesion = Button(frame_inicio_admni, text="Iniciar Sesión",command=lambda: Iniciar_sesion_administrador(Texto_usuario_admni, Texto_contraseña_admni))
        boton_iniciar_sesion.grid(row=3, column=0, columnspan=2, pady=20)

    else:
            # Si la ventana ya está abierta, simplemente enfócala
        Ventana_iniciar_sesion_administrador_abierta.lift()


#Pagina principal
if __name__ =='__main__':
    ventana_principal = Tk()
    ventana_principal.title('USAC')
    ventana_principal.geometry("800x360")
    ventana_principal.config(bg = "gray")
    Ventana_iniciar_sesion_administrador_abierta = None
    Crear_base_de_datos()

    frame_ventana_principal = Frame(ventana_principal, bg="dark green", padx=20, pady=20)
    frame_ventana_principal.pack(expand=True)

            # Título de la ventana
    label_administrador = Label(frame_ventana_principal, text="Bienvenido", font=("Arial", 26), bg="sky blue")
    label_administrador.grid(row=0, column=0, columnspan=2, pady=10)

                    # Botón de inicio de sesión
    boton_administrador = Button(frame_ventana_principal, text="Iniciar Sesión Admisitrador",command=Ventana_iniciar_sesion_administrador)
    boton_administrador.grid(row=1, column=0, columnspan=2, pady=20)

                    # Botón de inicio de sesión
    boton_taxista = Button(frame_ventana_principal, text="Iniciar Sesión Taxista",command=Ventana_iniciar_sesion_texista)
    boton_taxista.grid(row=2, column=0, columnspan=2, pady=20)

                    # Botón de inicio de sesión
    boton_cliente = Button(frame_ventana_principal, text="Solicitar Viaje",command=Solicitar_taxi)
    boton_cliente.grid(row=3, column=0, columnspan=2, pady=20)

    boton_encuesta = Button(frame_ventana_principal, text="Llenar Encuesta de Satisfaccion",command=Ventana_encuesta)
    boton_encuesta.grid(row=4, column=0, columnspan=2, pady=20)
    


        

ventana_principal.mainloop()

