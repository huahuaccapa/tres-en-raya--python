import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import math
import random

class TresEnRaya:
    def __init__(self):
        self.tablero = np.zeros((3, 3))  
        self.jugador_actual = 1  
    
    def hacer_movimiento(self, fila, columna):
        if self.tablero[fila][columna] == 0:
            self.tablero[fila][columna] = self.jugador_actual
            self.jugador_actual = 3 - self.jugador_actual  # Cambia de jugador
            return True
        return False
    
    def movimientos_disponibles(self):
        return [(i, j) for i in range(3) for j in range(3) if self.tablero[i][j] == 0]
    
    def ganador(self):
        # Verificar filas y columnas
        for i in range(3):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != 0:
                return self.tablero[i][0]
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != 0:
                return self.tablero[0][i]
        
        # Verificar diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != 0:
            return self.tablero[0][0]
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != 0:
            return self.tablero[0][2]
        
        # Empate o juego no terminado
        return 0 if len(self.movimientos_disponibles()) == 0 else -1
    
    def es_terminado(self):
        return self.ganador() != -1

class JuegoTresEnRayaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya con Dificultades")
        self.juego = TresEnRaya()
        self.dificultad = "difícil"  # Por defecto
        self.botones = [[None for _ in range(3)] for _ in range(3)]
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Selector de dificultad
        tk.Label(frame_controles, text="Dificultad:").pack(side=tk.LEFT, padx=5)
        self.dificultad_var = tk.StringVar(value="difícil")
        dificultades = ttk.Combobox(frame_controles, 
                                  textvariable=self.dificultad_var,
                                  values=["fácil", "medio", "difícil"],
                                  state="readonly")
        dificultades.pack(side=tk.LEFT, padx=5)
        
        # Botón reiniciar
        tk.Button(frame_controles, 
                text="Reiniciar", 
                command=self.reiniciar_juego).pack(side=tk.LEFT, padx=5)
        
        # Frame para el tablero
        frame_tablero = tk.Frame(self.root)
        frame_tablero.pack(pady=10)
        
        # Configurar botones del tablero
        btn_width = 6
        btn_height = 3
        font = ('Arial', 20, 'bold')
        
        for i in range(3):
            for j in range(3):
                self.botones[i][j] = tk.Button(
                    frame_tablero, 
                    text='', 
                    width=btn_width, 
                    height=btn_height,
                    font=font,
                    command=lambda fila=i, columna=j: self.manejar_click(fila, columna))
                self.botones[i][j].grid(row=i, column=j, padx=5, pady=5)
    
    def manejar_click(self, fila, columna):
        if self.juego.jugador_actual == 1 and self.juego.tablero[fila][columna] == 0:
            self.actualizar_boton(fila, columna, 'X')
            self.juego.hacer_movimiento(fila, columna)
            
            if not self.juego.es_terminado():
                self.root.after(500, self.turno_computadora)
            else:
                self.mostrar_resultado()
    
    def turno_computadora(self):
        if self.juego.jugador_actual == 2:
            fila, columna = self.obtener_movimiento_computadora()
            self.actualizar_boton(fila, columna, 'O')
            self.juego.hacer_movimiento(fila, columna)
            
            if self.juego.es_terminado():
                self.mostrar_resultado()
    
    def obtener_movimiento_computadora(self):
        dificultad = self.dificultad_var.get().lower()
        
        if dificultad == "fácil":
            return self.movimiento_aleatorio()
        elif dificultad == "medio":
            return self.movimiento_medio()
        else:  # difícil
            return self.mejor_movimiento()
    
    def movimiento_aleatorio(self):
        movimientos = self.juego.movimientos_disponibles()
        return random.choice(movimientos)
    
    def movimiento_medio(self):
        # Minimax con profundidad limitada para hacerlo más "humano"
        if random.random() < 0.3:  # 30% de probabilidad de mover aleatoriamente
            return self.movimiento_aleatorio()
        
        mejor_valor = math.inf
        mejor_mov = (-1, -1)
        movimientos = self.juego.movimientos_disponibles()
        
        # Evaluar solo 2 niveles de profundidad para hacerlo más rápido
        for (i, j) in movimientos:
            self.juego.hacer_movimiento(i, j)
            valor = self.minimax(self.juego, 2, True, -math.inf, math.inf)
            self.juego.tablero[i][j] = 0
            self.juego.jugador_actual = 2
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_mov = (i, j)
        
        return mejor_mov if mejor_mov != (-1, -1) else self.movimiento_aleatorio()
    
    def mejor_movimiento(self):
        mejor_valor = math.inf
        mejor_mov = (-1, -1)
        
        for (i, j) in self.juego.movimientos_disponibles():
            self.juego.hacer_movimiento(i, j)
            valor = self.minimax(self.juego, 0, True, -math.inf, math.inf)
            self.juego.tablero[i][j] = 0
            self.juego.jugador_actual = 2
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_mov = (i, j)
        
        return mejor_mov
    
    def minimax(self, tablero, profundidad, es_maximizando, alfa, beta):
        resultado = tablero.ganador()
        
        if resultado != -1:
            if resultado == 1: return 1
            elif resultado == 2: return -1
            else: return 0
        
        if es_maximizando:
            mejor_valor = -math.inf
            for (i, j) in tablero.movimientos_disponibles():
                tablero.hacer_movimiento(i, j)
                valor = self.minimax(tablero, profundidad+1, False, alfa, beta)
                tablero.tablero[i][j] = 0
                tablero.jugador_actual = 1
                mejor_valor = max(mejor_valor, valor)
                alfa = max(alfa, mejor_valor)
                if beta <= alfa: break
            return mejor_valor
        else:
            mejor_valor = math.inf
            for (i, j) in tablero.movimientos_disponibles():
                tablero.hacer_movimiento(i, j)
                valor = self.minimax(tablero, profundidad+1, True, alfa, beta)
                tablero.tablero[i][j] = 0
                tablero.jugador_actual = 2
                mejor_valor = min(mejor_valor, valor)
                beta = min(beta, mejor_valor)
                if beta <= alfa: break
            return mejor_valor
    
    def actualizar_boton(self, fila, columna, texto):
        self.botones[fila][columna].config(text=texto, state='disabled')
    
    def mostrar_resultado(self):
        ganador = self.juego.ganador()
        if ganador == 1:
            messagebox.showinfo("Fin del juego", "¡Ganaste!")
        elif ganador == 2:
            messagebox.showinfo("Fin del juego", "¡La computadora ganó!")
        else:
            messagebox.showinfo("Fin del juego", "¡Empate!")
    
    def reiniciar_juego(self):
        self.juego = TresEnRaya()
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text='', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    juego_gui = JuegoTresEnRayaGUI(root)
    root.mainloop()