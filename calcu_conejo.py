import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import tkinter as tk
from tkinter import ttk


def Calcunejo(vector_tiempo, puntos_trayectoria, tipo_movimiento, descripcion_modelo):

    plt.ion()
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_aspect('equal')

    def instanciar_objeto_animado(x, y):
        componentes = []
        componentes.append(patches.Ellipse((x, y), 1.4, 0.8, color='lightgray', ec='gray', zorder=10))
        componentes.append(patches.Circle((x + 0.5, y + 0.4), 0.35, color='lightgray', ec='gray', zorder=11))
        componentes.append(patches.Ellipse((x + 0.6, y + 0.9), 0.2, 0.7, color='lightgray', ec='gray', zorder=10))
        componentes.append(patches.Ellipse((x + 0.6, y + 0.9), 0.1, 0.5, color='pink', zorder=11))
        componentes.append(patches.Circle((x + 0.65, y + 0.45), 0.05, color='black', zorder=12))
        componentes.append(patches.Circle((x - 0.7, y + 0.1), 0.15, color='white', ec='gray', zorder=11))
        return componentes


    telemetria = ax.text(
        0.05,0.92,"",
        transform=ax.transAxes,
        fontsize=10,
        fontweight='bold',
        family='monospace',
        bbox=dict(facecolor='white', alpha=0.8),
        zorder=20
    )

    instancias_anteriores=[]

    for i in range(len(vector_tiempo)):

        for item in instancias_anteriores:
            item.remove()

        pos = puntos_trayectoria[i]
        t_actual = vector_tiempo[i]

        ax.set_facecolor('#FFDAB9')
        ax.grid(True, linestyle=':', alpha=0.6)

        if tipo_movimiento == 3:

            coord_x, coord_y = 10, pos
            ax.set_ylim(pos-5,pos+10)
            ax.set_xlim(5,15)


            if pos < 10:
                ax.axhline(0,color='#A0522D',linewidth=10,zorder=4)

        else:

            coord_x, coord_y = pos, 0.5
            ax.set_xlim(pos-10,pos+20)
            ax.set_ylim(-5,10)
            ax.axhline(-0.4,color='#A0522D',linewidth=10,zorder=4)

        instancias_anteriores = instanciar_objeto_animado(coord_x,coord_y)

        for item in instancias_anteriores:
            ax.add_patch(item)

        telemetria.set_text(
            f"TIEMPO: {t_actual:.2f} s\nDesplazamiento: {pos:.2f} m\n{descripcion_modelo}"
        )

        if tipo_movimiento ==3:
            telemetria.set_text(
                f"TIEMPO: {t_actual:.2f} s\nDesplazamiento: {pos*-1:.2f} m\n{descripcion_modelo}"
            )

        plt.draw()
        plt.pause(0.02)

    plt.ioff()
    plt.show()



def iniciar_simulacion():

    tipo_movimiento = combo_movimiento.current()+1
    tiempo = float(entry_tiempo.get())

    vector_tiempo = np.linspace(0, tiempo, 120)

    if tipo_movimiento == 1:

        v = float(entry_v.get())
        puntos_trayectoria = v * vector_tiempo
        descripcion_modelo = f"MRU | V={v} m/s"

    elif tipo_movimiento == 2:

        v0 = float(entry_v0.get())
        a = float(entry_a.get())

        puntos_trayectoria = (v0*vector_tiempo)+(0.5*a*vector_tiempo**2)
        descripcion_modelo = f"MRUV | A={a}"

    else:
        puntos_trayectoria = 0.5*-9.8*vector_tiempo**2
        descripcion_modelo = f"Caída Libre | h=1/2gt^2"

    Calcunejo(vector_tiempo,puntos_trayectoria,tipo_movimiento,descripcion_modelo)

def cerrar():
    ventana.destroy()

def actualizar_campos(event=None):

    tipo = combo_movimiento.current()

    entry_v.pack_forget()
    entry_v0.pack_forget()
    entry_a.pack_forget()

    label_v.pack_forget()
    label_v0.pack_forget()
    label_a.pack_forget()

    if tipo == 0:  # MRU
        label_v.pack()
        entry_v.pack()

    elif tipo == 1:  # MRUV
        label_v0.pack()
        entry_v0.pack()
        label_a.pack()
        entry_a.pack()
    elif tipo ==2:
        pass

ventana = tk.Tk()
ventana.title("Conejo Calculadora")
ventana.geometry("500x400")


tk.Label(ventana,text="Tipo de movimiento").pack()

combo_movimiento = ttk.Combobox(
    ventana, values=["MRU","MRUV","Caída Libre"]
)

combo_movimiento.pack()
combo_movimiento.bind("<<ComboboxSelected>>", actualizar_campos)

label_v = tk.Label(ventana,text="Velocidad (MRU)")
entry_v = tk.Entry(ventana)

label_v0 = tk.Label(ventana,text="Velocidad inicial (MRUV)")
entry_v0 = tk.Entry(ventana)

label_a = tk.Label(ventana,text="Aceleración (MRUV)")
entry_a = tk.Entry(ventana)

tk.Label(ventana,text="Tiempo (s)").pack()
entry_tiempo = tk.Entry(ventana)
entry_tiempo.pack()

tk.Button(
    ventana,
    text="Iniciar Simulación",
    command=iniciar_simulacion
).place(x=200,y=300)

tk.Button(
    ventana, text="Cerrar", 
    command=cerrar
).place(x=210,y=350)

ventana.mainloop()
