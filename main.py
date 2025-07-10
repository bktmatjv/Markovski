#PYTHON 3.12
import numpy as np
import pandas as pd
import chains as ch
import customtkinter as ctk


# ----------------- INTERFAZ (MULTIPANTALLA) -----------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MARKOSVKI")
        self.geometry("400x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.pantalla_inicio = PantallaInicio(self)
        self.pantalla_markov = PantallaMarkov(self)
        self.pantalla_creditos = PantallaCreditos(self)
        self.mostrar_inicio()

    def mostrar_inicio(self):
        self.pantalla_markov.pack_forget()
        self.pantalla_creditos .pack_forget()
        self.pantalla_inicio.pack(expand=True, fill="both")

    def mostrar_simulador(self):
        self.pantalla_inicio.pack_forget()
        self.pantalla_creditos.pack_forget()
        self.pantalla_markov.pack(expand=True, fill="both")

    def mostrar_creditos(self):
        self.pantalla_inicio.pack_forget()
        self.pantalla_markov.pack_forget()
        self.pantalla_creditos.pack(expand=True, fill="both")

class PantallaInicio(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2b2b2b")  # Fondo principal

        # -------------------- TÍTULO CON SOMBRA --------------------
        label_sombra = ctk.CTkLabel(
            self,
            text="Markovski",
            font=("Trebuchet MS", 60, "bold"),
            text_color="black",
            fg_color="transparent"
        )
        label_sombra.place(relx=0.5, y=102, anchor="center")

        label_principal = ctk.CTkLabel(
            self,
            text="Markovski",
            font=("Trebuchet MS", 60, "bold"),
            text_color="skyblue",
            fg_color="transparent"
        )
        label_principal.place(relx=0.5, y=100, anchor="center")

        # -------------------- BOTONES --------------------
        button_width = 200
        button_height = 40
        button_spacing = 50
        start_y = 250

        btn_entrar = ctk.CTkButton(
            self,
            text="Ir al simulador",
            command=master.mostrar_simulador,
            width=button_width,
            height=button_height,
            font=("Trebuchet MS", 16),
            corner_radius=10
        )
        btn_entrar.place(relx=0.5, y=start_y, anchor="center")

        btn_creditos = ctk.CTkButton(
            self,
            text="Créditos",
            command=master.mostrar_creditos,
            width=button_width,
            height=button_height,
            font=("Trebuchet MS", 16),
            corner_radius=10
        )
        btn_creditos.place(relx=0.5, y=start_y + 1  * button_spacing, anchor="center")

        btn_salir = ctk.CTkButton(
            self,
            text="Salir",
            command=master.destroy,
            width=button_width,
            height=button_height,
            font=("Trebuchet MS", 16),
            corner_radius=10,
            fg_color="#E74C3C",         # rojo suave
            hover_color="#C0392B",      # rojo más oscuro al pasar el mouse
            text_color="white"
        )
        btn_salir.place(relx=0.5, y=start_y + 2 * button_spacing, anchor="center")


#creditos
class PantallaCreditos(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        # Configuración de la pantalla
        self.configure(bg_color="black")  # Fondo oscuro

        # Título
        self.titulo = ctk.CTkLabel(self, text="¡Créditos!", font=("Trebuchet MS", 50), text_color="skyblue")
        self.titulo.pack(pady=20)

        # Lista de nombres
        creditos = [
            "   Salvador Arturo Diaz   ",
            "   Vivianne Rios Hasegawa   ",
            "   Vanessa Barrientos   ",
            "   Matias Del Castillo   ",
            "   Martin Asmat    "
        ]

        colores = [
            "skyblue",
            "pink",
            "yellow",
            "green",
            "red"
        ]

        button_width = 200
        button_height = 40
        button_spacing = 50
        start_y = 250

        btn_regresar = ctk.CTkButton(
            self,
            text="Regresar al inicio",
            command=master.mostrar_inicio,
            width=button_width,
            height=button_height,
            font=("Trebuchet MS", 16),
            corner_radius=10,
            fg_color="#E74C3C",  # rojo suave
            hover_color="#C0392B",  # rojo más oscuro al pasar el mouse
            text_color="white"
        )
        btn_regresar.place(relx=0.5, y=start_y + 2 * button_spacing, anchor="center")

        # Mostrar cada nombre en un label
        i = 0
        for nombre in creditos:
            label = ctk.CTkLabel(self, text=nombre, font=("Trebuchet MS", 18), fg_color= colores[i], bg_color="transparent", text_color="black")
            i+=1
            label.pack(pady=5)




class PantallaMarkov(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Datos
        self.num_empresas = 5
        self.num_dias = 80
        self.nombres_empresas = ["Credicorp", "Amazon", "Apple", "Tesla", "Microsoft"]
        self.tickers = ["BAP", "AMZN", "AAPL", "TSLA", "MSFT"]

        try:
            self.df_retornos, self.dias = ch.generar_datos_reales(self.nombres_empresas, self.tickers, self.num_dias)



            self.df_transiciones_normalizada, self.vector_inicial = ch.calcular_transiciones(
                self.df_retornos, self.nombres_empresas, self.dias)
        except Exception as e:
            self.df_transiciones_normalizada = pd.DataFrame()
            self.vector_inicial = np.array([])
            print("Error al obtener datos:", e)

        # Título
        label_title = ctk.CTkLabel(self, text="Simulador de Matriz de Markov", font=("Trebuchet MS", 24))
        label_title.pack(pady=20)

        # Textbox para resultados
        self.text_output = ctk.CTkTextbox(self, width=700, height=300)
        self.text_output.pack(pady=10)

        # Botón matriz
        btn_mostrar_matriz = ctk.CTkButton(
            self, text="Mostrar Matriz de Transiciones y Vector Inicial",
            command=self.mostrar_matriz_transiciones)
        btn_mostrar_matriz.pack(pady=10)

        # Entrada de días
        frame_N = ctk.CTkFrame(self)
        frame_N.pack(pady=10)

        label_N = ctk.CTkLabel(frame_N, text="Número de días (N):")
        label_N.pack(side="left", padx=5)

        self.entry_N = ctk.CTkEntry(frame_N, width=100)
        self.entry_N.pack(side="left", padx=5)

        btn_mostrar_probabilidades = ctk.CTkButton(
            frame_N, text="Mostrar Vector de Probabilidades",
            command=self.mostrar_probabilidades_N_dias)
        btn_mostrar_probabilidades.pack(side="left", padx=5)

        # Botón volver
        btn_volver = ctk.CTkButton(self, text="Volver al inicio", command=master.mostrar_inicio)
        btn_volver.pack(pady=20)

    def mostrar_matriz_transiciones(self):
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", "\nMatriz de transiciones normalizada:\n")
        self.text_output.insert("end", self.df_transiciones_normalizada.to_string())
        self.text_output.insert("end", "\n\nVector inicial:\n")
        self.text_output.insert("end", str(self.vector_inicial))

    def mostrar_probabilidades_N_dias(self):
        try:
            N = int(self.entry_N.get())
            vector_probabilidades = self.vector_inicial.copy()
            for _ in range(N):
                vector_probabilidades = np.dot(vector_probabilidades, self.df_transiciones_normalizada)

            self.text_output.delete("1.0", "end")
            self.text_output.insert("end", f"\nVector de probabilidades después de {N} días:\n")
            self.text_output.insert("end", str(vector_probabilidades))
        except ValueError:
            self.text_output.delete("1.0", "end")
            self.text_output.insert("end", "Por favor ingrese un número válido para N.")


# ----------------- EJECUCIÓN -----------------

if __name__ == "__main__":
    app = App()
    app.mainloop()

