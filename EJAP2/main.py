import customtkinter as ctk
import csv
import os
import numpy as np
import pandas as pd
import matplotlib
import requests
matplotlib.use('TkAgg') # necesario para usar matplotlib con tkinter, se debe configurar antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # sin esto no se pueden mostrar las gráficas dentro de la app, se necesita para integrar matplotlib con tkinter
from crear_csv import crear_csv

# La api se toma de https://developer.riotgames.com/
api_key = "" # Queria hacerlo de valo, pero riot no deja
csv_cuentas = "cuentas.csv"

# Cambiar para usar api (crear/reescribir csv) o no (precargado)
usar_api = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def cargar_cuentas():
    cuentas = {}
    if os.path.exists(csv_cuentas):
        with open(csv_cuentas, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cuentas[row['usuario']] = {
                    'contraseña': row['contraseña'],
                    'riot_id': row['riot_id'],
                    'tagline': row['tagline'],
                    'region': row['region'],
                }
    return cuentas


def cargar_matches():
    if os.path.exists("match_data.csv"):
        return pd.read_csv("match_data.csv")
    return None


def crear_df():
    df = cargar_matches()
    if df is None:
        return None
    df['deaths'] = df['deaths'].replace(0, 1) # (x/0) no se puede, se reemplaza (:pensive:)
    # tecnicamente la api si da el kda, pero 1. hay apartados que ocupan solo 1 de los 3 datos, 2. lo queria calcular y 3. se me olvido sacarlo
    df['kda'] = (df['kills'] + df['assists']) / df['deaths']     # kda es kills + assists / deaths, se calcula para cada fila del dataframe y se agrega como nueva columna
    return df

# Frame de las graficas. Muestra la grafica dentro del frame dado, se reutiliza para todas las graficas
def mostrar_grafica(frame, fig):
    fig.set_size_inches(8.5, 4.5)

    # ajusta margenes
    # profa estube 3 horas teniendo problemas con el layout (porfa no)
    fig.subplots_adjust(
        left=0.08,
        right=0.97,
        top=0.90,
        bottom=0.20
    )

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()

    widget = canvas.get_tk_widget()
    widget.pack(expand=True)

# Graficas (y consultas)

# kda por campeon
def grafica_kda(frame):
    df = crear_df()
    fig, ax = plt.subplots()
    df.groupby('champion')['kda'].mean().plot(kind='bar', ax=ax)
    ax.set_title("KDA por campeon")
    ax.set_xlabel("Campeón")
    ax.set_ylabel("KDA Promedio")
    mostrar_grafica(frame, fig)

# kda respecto al nivel
def grafica_kda_level(frame):
    df = crear_df()
    fig, ax = plt.subplots()
    ax.scatter(df['level'], df['kda'])
    ax.set_title("KDA vs Level")
    ax.set_xlabel("Nivel")
    ax.set_ylabel("KDA")
    mostrar_grafica(frame, fig)

# kda por tipo de kill
def grafica_tipo_kill(frame):
    df = crear_df()
    df['tipo'] = np.select(
        [df['penta_kills']>0, df['quadra_kills']>0, df['triple_kills']>0, df['double_kills']>0],
        ['Penta','Quadra','Triple','Double'],
        default='Single'
    )
    fig, ax = plt.subplots()
    df.boxplot(column='kda', by='tipo', ax=ax)
    ax.set_title("KDA por tipo de kill")
    ax.set_xlabel("Tipo de Kill")
    ax.set_ylabel("KDA")
    fig.suptitle("")  # quitar titulo automático feo
    mostrar_grafica(frame, fig)

# winrate por campeon
def grafica_winrate(frame):
    df = crear_df()
    fig, ax = plt.subplots()
    df.groupby('champion')['win'].mean().plot(kind='bar', ax=ax)
    ax.set_title("Winrate")
    ax.set_xlabel("Campeón")
    ax.set_ylabel("Winrate")
    mostrar_grafica(frame, fig)

# spells por campeon
def grafica_spells(frame):
    df = crear_df()
    fig, ax = plt.subplots()
    df.groupby('champion')[['spell1_casts','spell2_casts','spell3_casts','spell4_casts']].mean().plot(kind='bar', ax=ax)
    ax.set_title("Spells")
    ax.set_xlabel("Campeón")
    ax.set_ylabel("Casteos Promedio")
    mostrar_grafica(frame, fig)

# daño hecho y recibido
def grafica_damage(frame):
    df = crear_df()
    fig, ax = plt.subplots()
    data = df[['total_damage','damage_taken']].mean()
    data.index = ['Daño Hecho', 'Daño Recibido']
    data.plot(kind='bar', ax=ax)
    ax.set_title("Daño")
    ax.set_xlabel("Tipo de Daño")
    ax.set_ylabel("Promedio")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    mostrar_grafica(frame, fig)

# oro
def grafica_gold(frame): 
    df = crear_df()
    fig, ax = plt.subplots()
    data = df[['gold_earned','gold_spent','gold_per_minute','bounty_gold']].mean()
    data.index = ['Oro Ganado', 'Oro Gastado', 'Oro por Minuto', 'Bounty']
    data.plot(kind='bar', ax=ax)
    ax.set_title("Oro")
    ax.set_xlabel("Métrica de Oro")
    ax.set_ylabel("Promedio")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    mostrar_grafica(frame, fig)

# vision
def grafica_vision(frame):
    df = crear_df()
    fig, ax = plt.subplots()

    ax.scatter(df['wards_placed'], df['vision_score'], label="Placed")
    ax.scatter(df['wards_killed'], df['vision_score'], label="Killed")

    z = np.polyfit(df['wards_placed'], df['vision_score'], 1)
    p = np.poly1d(z)
    ax.plot(df['wards_placed'], p(df['wards_placed']))

    corr_placed = df['wards_placed'].corr(df['vision_score'])
    corr_killed = df['wards_killed'].corr(df['vision_score'])

    ax.set_title(f"Vision Score vs Wards\nplaced={corr_placed:.2f}, killed={corr_killed:.2f}")
    ax.set_xlabel("Wards")
    ax.set_ylabel("Vision Score")
    ax.legend()

    mostrar_grafica(frame, fig)

def grafica_objetivos(frame):
    df = crear_df()
    fig, ax = plt.subplots()

    labels = ['Turrets', 'Inhibitors', 'Nexus']
    
    kills = [
        df['turret_kills'].mean(),
        df['inhibitor_kills'].mean(),
        df['nexus_kills'].mean()
    ]
    
    lost = [
        df['turret_lost'].mean(),
        df['inhibitor_lost'].mean(),
        df['nexus_lost'].mean()
    ]

    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width/2, kills, width, label='Destruidos')
    ax.bar(x + width/2, lost, width, label='Perdidos')

    ax.set_title("Objetivos")
    ax.set_ylabel("Promedio")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.legend()

    mostrar_grafica(frame, fig)

# roles
def grafica_roles(frame):
    df = crear_df()
    fig, ax = plt.subplots()

    ax.plot(df['lane'], label='lane', marker='o')
    ax.plot(df['individual_position'], label='posicion individual', marker='s')

    ax.set_title("Comparación por partida")
    ax.set_xlabel("Partida")
    ax.set_ylabel("Posición")
    ax.legend()

    mostrar_grafica(frame, fig)

# App

class App(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.usuario_actual = None

        self.label = ctk.CTkLabel(self, text="Login")
        self.label.pack(pady=10)

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.user_entry.pack(pady=5)

        self.cont_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.cont_entry.pack(pady=5)

        self.login_btn = ctk.CTkButton(self, text="Iniciar sesión", command=self.validar_login)
        self.login_btn.pack(pady=10)

        self.message = ctk.CTkLabel(self, text="")
        self.message.pack()

    def validar_login(self):
        usuario = self.user_entry.get()
        contraseña = self.cont_entry.get()

        cuentas = cargar_cuentas()

        if usuario in cuentas and cuentas[usuario]['contraseña'] == contraseña:
            self.usuario_actual = cuentas[usuario]

            if usar_api:
                try:
                    region = self.usuario_actual['region']
                    riot_id = self.usuario_actual['riot_id']
                    tagline = self.usuario_actual['tagline']

                    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tagline}?api_key={api_key}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        puuid = response.json().get("puuid")

                        if puuid:
                            print("Actualizando CSV desde API...")
                            crear_csv(puuid, region, api_key)
                        else:
                            print("No se obtuvo PUUID")
                    else:
                        print("Error en API:", response.status_code)

                except Exception as e:
                    print("Error API:", e)

            self.mmenu_principal()
        else:
            self.message.configure(text="Credenciales incorrectas")

    def mmenu_principal(self):
        plt.close('all')
        
        for widget in self.winfo_children():
            widget.destroy()

        titulo = ctk.CTkLabel(self, text=f'Cuenta: {self.usuario_actual["riot_id"]}#{self.usuario_actual["tagline"]} - Region: {self.usuario_actual["region"]}')
        titulo.pack(pady=10)

        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(expand=True)

        self.botones_config = [
            ("KDA", grafica_kda),
            ("KDA-Level", grafica_kda_level),
            ("Tipo Kill", grafica_tipo_kill),
            ("Winrate", grafica_winrate),
            ("Spells", grafica_spells),
            ("Daño", grafica_damage),
            ("Oro", grafica_gold),
            ("Vision", grafica_vision),
            ("Objetivos", grafica_objetivos),
            ("Roles", grafica_roles),
        ]

        index = 0
        for row in range(2):
            for col in range(5):
                text, func = self.botones_config[index]
                btn = ctk.CTkButton(
                    grid_frame,
                    text=text,
                    command=lambda f=func: self.abrir_frame(f)
                )
                btn.grid(row=row, column=col, padx=10, pady=10)
                index += 1

    def abrir_frame(self, funcion):
        for widget in self.winfo_children():
            widget.destroy()

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        volver = ctk.CTkButton(top_frame, text="Volver", command=self.mmenu_principal)
        volver.pack(side="left")

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        try:
            plt.close('all')
            funcion(frame)
        except Exception as e:
            print(f"Error en gráfica: {e}")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("900x600")

    root.tk.call('tk', 'scaling', 2.0)
    root.tk.call('proc', 'bgerror', 'msg', '{return}')

    app = App(master=root)
    app.pack(expand=True, fill="both")

    root.mainloop()
