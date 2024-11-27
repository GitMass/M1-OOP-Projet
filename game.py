import pygame,csv,os 
import random

from unit import *

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
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(6, 7, 8, 1, 'enemy')]
        
        # Charger la carte des murs
        self.walls = []
        self.magmas = []
        self.lilypads = []
        self.muds = []
        map_data = self.read_csv('data/interface_graphique/map1.csv')
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == '1':  # Si la valeur est '1', c'est un mur
                    self.walls.append((x, y))
                if cell == '2':  # Si la valeur est '1', c'est un mur
                    self.magmas.append((x, y))
                if cell == '3':  # Si la valeur est '1', c'est un mur
                    self.lilypads.append((x, y))
                if cell == '4':  # Si la valeur est '1', c'est un mur
                    self.muds.append((x, y))

    # 0 : grass
    # 1 : murs
    # 2 : magma 
    # 3 : lilypad 
    # 4 : mud 

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename), mode='r') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

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

                        selected_unit.move(dx, dy,self)
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
        """Affiche le jeu."""

        GRASS=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/monsoongrass.png').convert_alpha()
        ROCK= pygame.image.load('data/interface_graphique/Tiles/Tiles/wall2.png').convert_alpha()
        MAGMA=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/cave magma.png').convert_alpha()
        LILYPAD=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/lilypad.png').convert_alpha()
        MUD=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/mud.png').convert_alpha()
        # Affiche la grille

        # Affiche la grille de fond avec "GRASS"
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                self.screen.blit(GRASS, (x, y))


        for wall in self.walls:
        # Calculer la position où afficher l'image
            x = wall[0] * CELL_SIZE
            y = wall[1] * CELL_SIZE

        # Afficher l'image de mur à cette position
            self.screen.blit(ROCK, (x, y))

        for magma in self.magmas:
        # Calculer la position où afficher l'image
            x = magma[0] * CELL_SIZE
            y = magma[1] * CELL_SIZE

        # Afficher l'image de magma à cette position
            self.screen.blit(MAGMA, (x, y))

        for lilypad in self.lilypads:
        # Calculer la position où afficher l'image
            x = lilypad[0] * CELL_SIZE
            y = lilypad[1] * CELL_SIZE

        # Afficher l'image de lilypad à cette position
            self.screen.blit(LILYPAD, (x, y))

        for mud in self.muds:
        # Calculer la position où afficher l'image
            x = mud[0] * CELL_SIZE
            y = mud[1] * CELL_SIZE

        # Afficher l'image de lilypad à cette position
            self.screen.blit(MUD, (x, y))

        # Affiche les contours de la grille (optionnel si vous voulez une bordure blanche)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()

def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
