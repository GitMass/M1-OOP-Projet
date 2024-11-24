import pygame
import random
import os

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, endurence_max, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.endurence_max = endurence_max
        self.team = team  # 'player1' , 'player2' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)  
                                         


# Definitions Des Types d'unités :
class Sorceress(Unit):
    def __init__(self, x, y, team, texture_path=None):
        super().__init__(x, y, health=18, attack_power=4, endurence_max=2, team=team)

        # Ajouter la texture
        self.texture = None
        if texture_path:
            if os.path.exists(texture_path):
                self.texture = pygame.image.load(texture_path)
                self.texture = pygame.transform.scale(self.texture, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image
            else:
                print(f"{texture_path} not found")

    # affiche la texture si elle existe
    def draw(self, screen):
        if self.texture:
            screen.blit(self.texture, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Si il n ya pas de texture on utilise draw() de Unit
            super().draw(screen)


class Swordsman(Unit):
    def __init__(self, x, y, team, texture_path=None):
        super().__init__(x, y, health=22, attack_power=3, endurence_max=6, team=team)

        # Ajouter la texture
        self.texture = None
        if texture_path:

            self.texture = pygame.image.load(texture_path)
            self.texture = pygame.transform.scale(self.texture, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image

    # affiche la texture si elle existe
    def draw(self, screen):
        if self.texture:
            screen.blit(self.texture, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Si il n ya pas de texture on utilise draw() de Unit
            super().draw(screen)


class Monster(Unit):
    def __init__(self, x, y, team, texture_path=None):
        super().__init__(x, y, health=28, attack_power=2, endurence_max=4, team=team)

        # Ajouter la texture
        self.texture = None
        if texture_path:
            self.texture = pygame.image.load(texture_path)
            self.texture = pygame.transform.scale(self.texture, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image

    # affiche la texture si elle existe
    def draw(self, screen):
        if self.texture:
            screen.blit(self.texture, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Si il n ya pas de texture on utilise draw() de Unit
            super().draw(screen)


def Definir_personnages():
    personnages = []

    Yennefer = Sorceress(2, 0, 'player', 'data/yennefer.png')
    personnages.append(Yennefer)

    Sekiro = Swordsman(3, 0, 'player', 'data/sekiro.png')
    personnages.append(Sekiro)

    return personnages




