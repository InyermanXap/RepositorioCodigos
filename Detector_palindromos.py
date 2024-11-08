import os 
from tkinter import *
from tkinter import ttk
from tkinter import Tk, messagebox
import tkinter as tk
import bcrypt
import re
from datetime import datetime
from tkinter import scrolledtext

#Rutas de las bases de datos
BD_Usuarios = "BD_Usuarios.txt"
Palindromos = "Palindromos.txt"
Historial = "Historial.txt"
# Se crean las bases de datos y sus cabecezeras para organizar la informacion
def Crear_base_de_datos():
    if not os.path.exists(BD_Usuarios):
        with open(BD_Usuarios, "w") as g:
            g.write("Usuario\tContraseña\tCorreo\n")
            print('Base de datos de usuario creada')
    if not os.path.exists(Palindromos):
        with open(Palindromos, "w") as g:
            g.write("Usuario\tCadena Original\tCadena limpia\tResultado\n")
            print('Base de datos de Palindromos creada')
    if not os.path.exists(Historial):
        with open(Historial, "w") as g:
            g.write("Usuario\tHorario de ejecucion del programa\tNombre del programa\tAutor del programa\n")
            print('Base de datos del Historial creada')

#sirve para obtener la fecha y hora de ejecucion del programa

def obtener_fecha_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#Comprobaciones para que las ventanas no se abran infinitamente
Ventana_registrar_usuario_abierta = None
Ventana_entrada_palindromo_abierta = None
Ventana_palindromo_registros_abierta = None
Ventana_historial_abierta = None
#Ventana para mostrar historial
def Ventana_historial():
    global Ventana_historial_abierta

    # Comprobar si la ventana ya está abierta
    if Ventana_historial_abierta is None:
        
        # Crear ventana y asignarla a la variable global
        Ventana_historial_abierta = tk.Tk()
        Ventana_historial_abierta.title("Historial")
        
        # Función para restablecer la variable global al cerrar la ventana
        def on_close():
            global Ventana_historial_abierta
            Ventana_historial_abierta.destroy()  # Primero destruir la ventana
            Ventana_historial_abierta = None     # Luego asignar None a la variable
        
        # Configurar el evento de cierre de ventana
        Ventana_historial_abierta.protocol("WM_DELETE_WINDOW", on_close)
        
        # Crear una caja de texto desplazable
        texto = scrolledtext.ScrolledText(Ventana_historial_abierta, wrap=tk.WORD, width=80, height=40)
        texto.pack(padx=10, pady=10)
        
        # Nombre del fichero
        fichero = Historial
        
        # Función para cargar el contenido del fichero en la caja de texto
        def cargar_contenido():
            texto.config(state=tk.NORMAL)
            texto.delete("1.0", tk.END)  # Limpiar el contenido actual
            try:
                with open(fichero, "r") as g:
                    contenido = g.read()
                    texto.insert(tk.END, contenido)
            except FileNotFoundError:
                texto.insert(tk.END, "El fichero no existe.")
            texto.config(state=tk.DISABLED)

        # Función para borrar los registros del fichero
        def borrar_registros():
            with open(fichero, "w") as g:
                g.write("Usuario\tHorario de ejecucion del programa\tNombre del programa\tAutor del programa\n")  # Escribir cabecera de nuevo
            cargar_contenido()  # Actualizar la vista

        # Cargar el contenido inicial del fichero
        cargar_contenido()

        # Botón para borrar registros
        boton_borrar = tk.Button(Ventana_historial_abierta, text="Borrar Registros", command=borrar_registros)
        boton_borrar.pack(pady=5)

def Ventana_palindromo_registros():
    global Ventana_palindromo_registros_abierta

    # Comprobar si la ventana ya está abierta
    if Ventana_palindromo_registros_abierta is None:
        
        # Crear ventana y asignarla a la variable global
        Ventana_palindromo_registros_abierta = tk.Tk()
        Ventana_palindromo_registros_abierta.title("Contenido del Fichero")
        
        # Función para restablecer la variable global al cerrar la ventana
        def on_close():
            global Ventana_palindromo_registros_abierta
            Ventana_palindromo_registros_abierta.destroy()  # Primero destruir la ventana
            Ventana_palindromo_registros_abierta = None     # Luego asignar None a la variable
        
        # Configurar el evento de cierre de ventana
        Ventana_palindromo_registros_abierta.protocol("WM_DELETE_WINDOW", on_close)
        
        # Crear una caja de texto desplazable
        texto = scrolledtext.ScrolledText(Ventana_palindromo_registros_abierta, wrap=tk.WORD, width=80, height=40)
        texto.pack(padx=10, pady=10)
        
        # Nombre del fichero
        fichero = Palindromos
        
        # Función para cargar el contenido del fichero en la caja de texto
        def cargar_contenido():
            texto.config(state=tk.NORMAL)
            texto.delete("1.0", tk.END)  # Limpiar el contenido actual
            try:
                with open(fichero, "r") as g:
                    contenido = g.read()
                    texto.insert(tk.END, contenido)
            except FileNotFoundError:
                texto.insert(tk.END, "El fichero no existe.")
            texto.config(state=tk.DISABLED)

        # Función para borrar los registros del fichero
        def borrar_registros():
            with open(fichero, "w") as g:
                g.write("Usuario\tCadena Original\tCadena limpia\tResultado\n")  # Escribir cabecera de nuevo
            cargar_contenido()  # Actualizar la vista

        # Cargar el contenido inicial del fichero
        cargar_contenido()

        # Botón para borrar registros
        boton_borrar = tk.Button(Ventana_palindromo_registros_abierta, text="Borrar Registros", command=borrar_registros)
        boton_borrar.pack(pady=5)


#Se asegura que no se ingresen caracteres especiales en la entrada de palindromos

def validar_caracteres(texto):
    # Permite la entrada vacía o texto alfanumérico
    return texto == "" or texto.isalnum()
 # Convierte el texto a minúsculas
def convertir_minusculas(texto):
    return texto.lower()
    # Verifica si el texto es un palíndromo
def es_palindromo(texto):
    texto = convertir_minusculas(texto)  # Asegurarse de que todo esté en minúsculas
    return texto == texto[::-1]  # Compara el texto con su reverso


#Ventana para ingresar el palindromo
def Ventana_entrada_palindromo(Usuario):    
    global Ventana_entrada_palindromo_abierta
    if Ventana_entrada_palindromo_abierta is None or not Ventana_entrada_palindromo_abierta.winfo_exists():
            Ventana_entrada_palindromo = Tk()
            Ventana_entrada_palindromo.title('Ingreso de posible palindromo')
            Ventana_entrada_palindromo.geometry("800x360")
            Ventana_entrada_palindromo.config(bg = "gray")

            frame_Ventana_entrada_palindromo = Frame(Ventana_entrada_palindromo, bg="dark green", padx=20, pady=20)
            frame_Ventana_entrada_palindromo.pack(expand=True)

            label_palindromo = Label(frame_Ventana_entrada_palindromo, text="Ingrese su posible candidato a palindromo", bg="dark green")
            label_palindromo.grid(row=1, column=0, pady=10, padx=10)
             # Configuración de validación
            validate_cmd = (Ventana_entrada_palindromo.register(validar_caracteres), '%P')

            # Entrada con validación de caracteres
            texto_palindromo = Entry(frame_Ventana_entrada_palindromo, justify="center", validate="key", validatecommand=validate_cmd)
            texto_palindromo.grid(row=1, column=1, pady=10, padx=10)

            def verificar_palindromo():
            # Obtiene el texto de la entrada y verifica si es palíndromo
                texto = texto_palindromo.get()
                texto_limpio = convertir_minusculas(texto)
                if es_palindromo(texto):
                    resultado = "Es un palindromo"
                else:
                    resultado = "No es un palindromo"
                label_resultado.config(text=resultado)

                with open(Palindromos, "a") as f:
                    f.write(f"{Usuario}\t{texto}\t{texto_limpio}\t{resultado}\n")
                    messagebox.showinfo("Aviso", "Registro exitoso.")

                with open(Historial, "a") as f:
                    fecha_hora_actual = obtener_fecha_hora()
                    f.write(f"{Usuario}\t{fecha_hora_actual}\tDetector De palindromos\tInyerman Alexander Xap Chin\n")
                    messagebox.showinfo("Aviso", "Registro exitoso.")

            



        # Botón para verificar si es palíndromo
            boton_verificar = Button(frame_Ventana_entrada_palindromo, text="Verificar", command=verificar_palindromo)
            boton_verificar.grid(row=2, column=0, columnspan=2, pady=10)

            # Etiqueta para mostrar el resultado
            label_resultado = Label(frame_Ventana_entrada_palindromo, text="", bg="dark green")
            label_resultado.grid(row=3, column=0, columnspan=2, pady=10)

            


#Extraer usuarios de la base de datos
def leer_usuarios():
    usuarios = {}
    if os.path.exists(BD_Usuarios):  
        with open(BD_Usuarios, "r") as file:
            next(file)  # Saltar la cabecera
            for line in file:
                datos = line.strip().split('\t')
                if len(datos) >= 2:  # Verificar que hay suficientes datos
                    Usuario = datos[0]
                    Contraseña = datos[1]
                    Correo = datos[2]
                    usuarios[Usuario] = {'contrasena': Contraseña, 'correo': Correo}
    return usuarios
#Iniciar sesion
def Iniciar_sesion_taxista(Texto_usuario_taxista, Texto_contraseña_taxista):
    usuarios = leer_usuarios()  # Esta función debe leer los datos de taxistas con las contraseñas hasheadas

    Usuario = Texto_usuario_taxista.get()
    Contraseña = Texto_contraseña_taxista.get().encode('utf-8')  # Convertir a bytes para bcrypt
    
    # Verificar si el DPI está registrado
    if Usuario in usuarios:
        # Extraer el hash de la contraseña
        hash_contraseña = usuarios[Usuario]['contrasena'].encode('utf-8')  # Convertir el hash guardado a bytes
        
        # Comparar la contraseña ingresada con el hash almacenado
        if bcrypt.checkpw(Contraseña, hash_contraseña):
            Ventana_entrada_palindromo(Usuario)  # Abrir el menú si las credenciales son correctas
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

#validaciones para registro
def validar_nombre_apellido(nombre):
    """Valida que el nombre o apellido solo contenga letras"""
    return bool(re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nombre))

def validar_correo(correo):
    """Valida el formato de correo electrónico"""
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo))

def validar_contrasena(Contraseña_taxista):

    if (len(Contraseña_taxista) >= 8 and 
        re.search(r'[A-Z]', Contraseña_taxista) and 
        re.search(r'[0-9]', Contraseña_taxista) and 
        re.search(r'[!@#$%^&*(),.?":{}|<>]', Contraseña_taxista)):
        return True
    return False

def hashear_contrasena(contrasena):
    contrasena_bytes = contrasena.encode('utf-8')  # Convertir a bytes
    sal = bcrypt.gensalt()  # Generar una sal segura
    hash_contrasena = bcrypt.hashpw(contrasena_bytes, sal)  # Hashear la contraseña
    return hash_contrasena.decode('utf-8')  # Devolver como cadena para almacenar

#Registro de usuario en la base de datos de usuario
def Registrar_taxista(texto_Nombre_taxista,texto_Correo_taxista,texto_Contraseña_taxista,texto_Confirmacion_contraseña_taxista):
    # Obtener valores de los campos
    Nombre_taxista = texto_Nombre_taxista.get()
    Correo_taxista = texto_Correo_taxista.get()
    Contraseña_taxista = texto_Contraseña_taxista.get()
    Confirmacion_contraseña_taxista = texto_Confirmacion_contraseña_taxista.get()
    
     # Cargar usuarios existentes
    usuarios = leer_usuarios()
    
    # Validaciones
    if Nombre_taxista in usuarios:
        messagebox.showerror("Error", "El nombre de usuario ya está registrado. Por favor, elige otro nombre.")
        return

    if not validar_nombre_apellido(Nombre_taxista):
        messagebox.showerror("Error", "El nombre solo debe contener letras. Por favor, revisa el formato.")
        return

    if not validar_correo(Correo_taxista):
        messagebox.showerror("Error", "El formato del correo no es válido. Debe ser: ejemplo@dominio.com")
        return

    if Contraseña_taxista != Confirmacion_contraseña_taxista:
        messagebox.showerror("Error", "Las contraseñas no coinciden. Por favor, revisa los campos.")
        return

    if not validar_contrasena(Contraseña_taxista):  
        messagebox.showerror("Error", "La contraseña no cumple con los requisitos.")
        return
    
       # Encriptar la contraseña antes de almacenarla
    contrasena_hasheada = hashear_contrasena(Contraseña_taxista)
    
    # Registrar los datos en el archivo con la contraseña encriptada
    with open(BD_Usuarios, "a") as f:
        f.write(f"{Nombre_taxista}\t{contrasena_hasheada}\t{Correo_taxista}\n")
        messagebox.showinfo("Aviso", "Registro exitoso.")


#Ventana de Registro de Usuario
def Ventana_taxedratico_registro():
        # Verificar si la ventana ya existe o no
    global Ventana_registrar_usuario_abierta
    if Ventana_registrar_usuario_abierta is None or not Ventana_registrar_usuario_abierta.winfo_exists():
            # Crear la ventana del menú del administrador
        Ventana_registrar_usuario = Toplevel()
        Ventana_registrar_usuario.title("Registro de usuario de Detector de Palindromo")
        Ventana_registrar_usuario.geometry("700x700")
        Ventana_registrar_usuario.config(bg="dark green")

            # Crear el frame dentro de la nueva ventana
        frame_registrar_taxista = Frame(Ventana_registrar_usuario, bg="dark green", padx=20, pady=20)
        frame_registrar_taxista.pack(expand=True)

        # Título de la ventana
        label_titulo = Label(frame_registrar_taxista, text="Registrar Nuevo Ususario", font=("Arial", 16), bg="dark green")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiqueta y entrada para el nombre del taxedrático
        label_nombre_tax = Label(frame_registrar_taxista, text="Ingrese el Nombre del Usuario", bg="dark green")
        label_nombre_tax.grid(row=1, column=0, pady=10, padx=10)
        texto_Nombre_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Nombre_taxista.grid(row=1, column=1, pady=10, padx=10)

        # Etiqueta y entrada para el DPI del taxedrático
        label_correo_tax = Label(frame_registrar_taxista, text="Ingrese el correo del usuario", bg="dark green")
        label_correo_tax.grid(row=5, column=0, pady=10, padx=10)
        texto_Correo_taxista = Entry(frame_registrar_taxista, justify="center")
        texto_Correo_taxista.grid(row=5, column=1, pady=10, padx=10)

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
        boton_registrar_tax = Button(frame_registrar_taxista, text="Registrar",command=lambda: Registrar_taxista(texto_Nombre_taxista,texto_Correo_taxista,texto_Contraseña_taxista,texto_Confirmacion_contraseña_taxista))
        boton_registrar_tax.grid(row=10, column=0, columnspan=2, pady=20)

    else:
        # Si la ventana ya está abierta, simplemente traerla al frente
        Ventana_registrar_usuario_abierta.lift()


#Pagina inicial
if __name__ =='__main__':
    ventana_principal = Tk()
    ventana_principal.title('Detector de Palindromos')
    ventana_principal.geometry("800x360")
    ventana_principal.config(bg = "gray")
    Crear_base_de_datos()

    frame_ventana_principal = Frame(ventana_principal, bg="dark green", padx=20, pady=20)
    frame_ventana_principal.pack(expand=True)

            # Título de la ventana
    label_administrador = Label(frame_ventana_principal, text="Bienvenido", font=("Arial", 26), bg="sky blue")
    label_administrador.grid(row=0, column=0, columnspan=2, pady=10)

    label_titulo = Label(frame_ventana_principal, text="Iniciar Sesion ", font=("Arial", 16), bg="dark green")
    label_titulo.grid(row=1, column=0, columnspan=3, pady=10)

        # Etiqueta y entrada para usuario
    label_usuario = Label(frame_ventana_principal, text="Ingrese su usuario", bg="dark green")
    label_usuario.grid(row=2, column=0, pady=10, padx=10)

    Texto_usuario_taxista = Entry(frame_ventana_principal, justify="center")
    Texto_usuario_taxista.grid(row=2, column=1, pady=10, padx=10)

        # Etiqueta y entrada para contraseña
    label_contraseña = Label(frame_ventana_principal, text="Ingrese su contraseña", bg="dark green")
    label_contraseña.grid(row=3, column=0, pady=10, padx=10)

    Texto_contraseña_taxista = Entry(frame_ventana_principal, justify="center", show="*")  # El `show="*"` oculta el texto de la contraseña
    Texto_contraseña_taxista.grid(row=3, column=1, pady=10, padx=10)

        # Botón de inicio de sesión
    boton_iniciar_sesion = Button(frame_ventana_principal, text="Iniciar Sesión",command=lambda: Iniciar_sesion_taxista(Texto_usuario_taxista, Texto_contraseña_taxista))
    boton_iniciar_sesion.grid(row=4, column=0, columnspan=2, pady=10)

    boton_registrar_taxista = Button(frame_ventana_principal, text="Registrar Usuario",command=Ventana_taxedratico_registro)
    boton_registrar_taxista.grid(row=5, column=0, columnspan=2, pady=10)

    #Boton para ver registros de palindromos
    boton_mostrar_palindromo = Button(frame_ventana_principal, text="Ver registro de palindromos", command=Ventana_palindromo_registros)
    boton_mostrar_palindromo.grid(row=6, column=0, columnspan=2, pady=10)

    #Boton para ver Historial
    boton_historial = Button(frame_ventana_principal, text="Ver Historial", command=Ventana_historial)
    boton_historial.grid(row=7, column=0, columnspan=2, pady=10)

    #boton_recuperar_contraseña = Button(frame_ventana_principal, text="Recuperar Contraseña",command=recuperar_contrasena)
    #boton_recuperar_contraseña.grid(row=6, column=0, columnspan=2, pady=10)
        

ventana_principal.mainloop()


            