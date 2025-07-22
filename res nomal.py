import tkinter as tk
import math
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tres en Raya - Minimax")
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        
        # Configuración de colores
        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff"
        self.text_color = "#333333"
        self.win_color = "#4caf50"
        
        self.create_board()
        
    def create_board(self):
        self.root.configure(bg=self.bg_color)
        for i in range(9):
            button = tk.Button(
                self.root,
                text=" ",
                font=('Helvetica', 20),
                width=6,
                height=3,
                bg=self.button_color,
                fg=self.text_color,
                command=lambda idx=i: self.make_move(idx)
            )
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)
            
        reset_button = tk.Button(
            self.root,
            text="Reiniciar",
            font=('Helvetica', 12),
            bg="#ff5722",
            fg="white",
            command=self.reset_game
        )
        reset_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
    
    def make_move(self, position):
        if self.board[position] == " " and self.current_player == "X":
            self.board[position] = "X"
            self.buttons[position].config(text="X", state="disabled")
            
            if self.check_winner("X"):
                self.highlight_winning_combinations()
                messagebox.showinfo("Fin del juego", "¡Has ganado!")
                self.disable_all_buttons()
                return
            
            if self.is_board_full():
                messagebox.showinfo("Fin del juego", "¡Empate!")
                return
            
            self.current_player = "O"
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        best_move = self.best_move()
        self.board[best_move] = "O"
        self.buttons[best_move].config(text="O", state="disabled")
        
        if self.check_winner("O"):
            self.highlight_winning_combinations()
            messagebox.showinfo("Fin del juego", "La IA ha ganado")
            self.disable_all_buttons()
            return
        
        if self.is_board_full():
            messagebox.showinfo("Fin del juego", "¡Empate!")
            return
        
        self.current_player = "X"
    
    def minimax(self, depth, is_maximizing):
        scores = {"X": -1, "O": 1, "tie": 0}
        
        winner = self.check_winner("O" if is_maximizing else "X")
        if winner:
            return scores["O"] if is_maximizing else scores["X"]
        
        if self.is_board_full():
            return scores["tie"]
        
        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(depth + 1, False)
                    self.board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "X"
                    score = self.minimax(depth + 1, True)
                    self.board[i] = " "
                    best_score = min(score, best_score)
            return best_score
    
    def best_move(self):
        best_score = -math.inf
        move = -1
        
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(0, False)
                self.board[i] = " "
                
                if score > best_score:
                    best_score = score
                    move = i
        return move
    
    def check_winner(self, player):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)              # Diagonales
        ]
        
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return True
        return False
    
    def highlight_winning_combinations(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)              # Diagonales
        ]
        
        for a, b, c in winning_combinations:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                self.buttons[a].config(bg=self.win_color)
                self.buttons[b].config(bg=self.win_color)
                self.buttons[c].config(bg=self.win_color)
                return
    
    def is_board_full(self):
        return " " not in self.board
    
    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")
    
    def reset_game(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", state="normal", bg=self.button_color)
    
    def run(self):
        self.root.mainloop()

# Iniciar el juego
game = TicTacToe()
game.run()
