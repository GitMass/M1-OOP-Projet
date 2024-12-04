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

        self.current_sound = None  # Référence au son actuellement joué
        # Initialiser le mixer Pygame
        pygame.mixer.init()
        
        # Charger les sons pour chaque type de terrain
        self.sounds = {
            'magma': pygame.mixer.Sound('data/interface_graphique/Sound effect/fire.wav'),
            'mud': pygame.mixer.Sound('data/interface_graphique/Sound effect/mud.wav'),
            'lilypad': pygame.mixer.Sound('data/interface_graphique/Sound effect/water-splash.wav'),
            'healing': pygame.mixer.Sound('data/interface_graphique/Sound effect/heal-up.wav'),
            'footstep': pygame.mixer.Sound('data/interface_graphique/Sound effect/footstep.wav'),
        }

        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [
            Unit(0, 0, 10, 2, 'player',skills=[
                {'name': 'Fireball', 'damage': 5, 'range': 3},
                {'name': 'Heal', 'heal': 4, 'cost': 2}]),
            Unit(1, 0, 10, 2, 'player',skills=[{'name': 'Arrow Shot', 'damage': 3, 'range': 2}])]

        self.enemy_units = [
            Unit(6, 6, 8, 1, 'enemy',skills=[
                {'name': 'Poison Attack', 'damage': 2, 'range': 1}]),
            Unit(6, 7, 8, 1, 'enemy',skills=[
                {'name': 'Berserk Slash', 'damage': 4, 'range': 1}])]
        
        # Charger la carte des murs
        self.grass=[]
        self.walls = []
        self.magmas = []
        self.lilypads = []
        self.muds = []
        self.healing=[]
        map_data = self.read_csv('data/interface_graphique/map1.csv')
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == '0':  # Si la valeur est '1', c'est un mur
                    self.grass.append((x, y))
                if cell == '1':  # Si la valeur est '1', c'est un mur
                    self.walls.append((x, y))
                if cell == '2':  # Si la valeur est '1', c'est un mur
                    self.magmas.append((x, y))
                if cell == '3':  # Si la valeur est '1', c'est un mur
                    self.lilypads.append((x, y))
                if cell == '4':  # Si la valeur est '1', c'est un mur
                    self.muds.append((x, y))
                if cell == '5':  # Si la valeur est '1', c'est un mur
                    self.healing.append((x, y))

    # 0 : grass
    # 1 : murs
    # 2 : magma 
    # 3 : lilypad 
    # 4 : mud 
    # 5 : healing 

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

                        # Utiliser une compétence (par exemple, touche 'S' pour sélectionner une compétence)
                        if event.key==pygame.K_s:
                            # Exemple : utilisation de "Fireball" sur un ennemi proche
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x-enemy.x)<=3 and abs(selected_unit.y-enemy.y)<=3:
                                    selected_unit.use_skills('Fireball',enemy)
                                    has_acted=True
                                    selected_unit.is_selected=False
                                    break 

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

        GRASS=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/path2.png').convert_alpha()
        ROCK= pygame.image.load('data/interface_graphique/Tiles/Tiles/wall2.png').convert_alpha()
        MAGMA=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/cave magma.png').convert_alpha()
        LILYPAD=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/lilypad.png').convert_alpha()
        MUD=pygame.image.load('data/interface_graphique/Tiles/Tiles/seamless-64px-rpg-tiles-1.1.0/mud.png').convert_alpha()
        HEALING=pygame.image.load('data/interface_graphique/Tiles/Tiles/healing.png').convert_alpha()

        # Affiche la grille

        # Affiche la grille de fond avec "GRASS"
        for grass in self.grass:
        # Calculer la position où afficher l'image
            x = grass[0] * CELL_SIZE
            y = grass[1] * CELL_SIZE

        # Afficher l'image de mur à cette position
            self.screen.blit(GRASS, (x, y))

        # Affiche la grille de fond avec "ROCK"
        for wall in self.walls:
        # Calculer la position où afficher l'image
            x = wall[0] * CELL_SIZE
            y = wall[1] * CELL_SIZE

        # Afficher l'image de mur à cette position
            self.screen.blit(ROCK, (x, y))

        # Affiche la grille de fond avec "MAGMA"
        for magma in self.magmas:
        # Calculer la position où afficher l'image
            x = magma[0] * CELL_SIZE
            y = magma[1] * CELL_SIZE

        # Afficher l'image de magma à cette position
            self.screen.blit(MAGMA, (x, y))

        # Affiche la grille de fond avec "LILYPAD"
        for lilypad in self.lilypads:
        # Calculer la position où afficher l'image
            x = lilypad[0] * CELL_SIZE
            y = lilypad[1] * CELL_SIZE

        # Afficher l'image de lilypad à cette position
            self.screen.blit(LILYPAD, (x, y))

        # Affiche la grille de fond avec "MUD"
        for mud in self.muds:
        # Calculer la position où afficher l'image
            x = mud[0] * CELL_SIZE
            y = mud[1] * CELL_SIZE

        # Afficher l'image de lilypad à cette position
            self.screen.blit(MUD, (x, y))

        # Affiche la grille de fond avec "MUD"
        for healing in self.healing:
        # Calculer la position où afficher l'image
            x = healing[0] * CELL_SIZE
            y = healing[1] * CELL_SIZE

        # Afficher l'image de lilypad à cette position
            self.screen.blit(HEALING, (x, y))

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
