import pygame
import csv
import os
import random

from unit import *  # Assurez-vous que la classe Unit est définie dans un fichier appelé unit.py

# Paramètres de la grille et des cellules
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        
        # Charger les images
        self.player_image = pygame.image.load('player_unit.png').convert_alpha()  # Remplacez par le chemin réel de l'image
        self.enemy_image = pygame.image.load('enemy_unit.png').convert_alpha()  # Remplacez par le chemin réel de l'image
        self.wall_image = pygame.image.load('wall.png').convert_alpha()  # Remplacez par le chemin réel de l'image
        
        # Redimensionner les images pour correspondre à la taille de la cellule
        self.player_image = pygame.transform.scale(self.player_image, (CELL_SIZE, CELL_SIZE))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (CELL_SIZE, CELL_SIZE))
        self.wall_image = pygame.transform.scale(self.wall_image, (CELL_SIZE, CELL_SIZE))

        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

        self.walls = []

    def load_csv(self, filepath):
        """
        Charge une grille à partir d'un fichier CSV et initialise les murs.

        Paramètres
        ----------
        filepath : str
            Le chemin du fichier CSV.
        """
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            grid = []
            for row in reader:
                grid.append([int(cell) for cell in row])  # Convertit chaque cellule en entier

        # Convertir la grille en murs
        self.walls = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == 59:  # Supposons que "59" représente un mur
                    self.walls.append((x, y))

    def is_wall(self, x, y):
        """
        Vérifie si une cellule est un mur.
        """
        return (x, y) in self.walls

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy, self)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu avec des images au lieu de formes géométriques."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités (avec les images)
        for unit in self.player_units + self.enemy_units:
            if unit.player_or_enemy == 'player':
                self.screen.blit(self.player_image, (unit.x * CELL_SIZE, unit.y * CELL_SIZE))
            else:
                self.screen.blit(self.enemy_image, (unit.x * CELL_SIZE, unit.y * CELL_SIZE))

        # Affiche les murs (avec l'image)
        for wall in self.walls:
            self.screen.blit(self.wall_image, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE))

        # Rafraîchit l'écran
        pygame.display.flip()

def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Charger les murs depuis un fichier CSV
    game.load_csv("C:/Users/minha/OneDrive/Desktop/TP/M1/Python/projet/interface_graphique/map1.csv")  # Remplacez par le chemin réel de votre fichier CSV

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
