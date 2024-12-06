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
            Unit(0, 0, 10, 2, 'player', skills=[
                {'name': 'Fireball', 'damage': 2, 'range': 2},
                {'name': 'Dragon Blast', 'damage': 3, 'cost': 3},
                {'name': 'Inferno', 'damage': 4, 'range': 4}  # Nouvelle compétence
            ]),
            Unit(1, 0, 10, 2, 'player', skills=[
                {'name': 'Arrow Shot', 'damage': 1, 'range': 3},
                {'name': 'Stun Arrow', 'damage': 2, 'range': 4, 'effect': 'stun'},
                {'name': 'Double Shot', 'damage': 3, 'range': 5}
            ])
        ]

        self.enemy_units = [
            Unit(6, 6, 10, 2, 'enemy', skills=[
                {'name': 'Poison Attack', 'damage': 2, 'range': 1},
                {'name': 'Venom Spray', 'damage': 3, 'range': 2},
                {'name': 'Bite', 'damage': 5, 'range': 1}
            ]),
            Unit(6, 7, 10, 2, 'enemy', skills=[
                {'name': 'Roar', 'damage': 1, 'range': 3, 'effect': 'fear'},
                {'name': 'Crush', 'damage': 3, 'range': 1},
                {'name': 'Berserk Slash', 'damage': 4, 'range': 2}
            ])
        ]
        
        # Charger la carte des murs
        self.grass=[]
        self.walls = []
        self.magmas = []
        self.lilypads = []
        self.muds = []
        self.healing=[]
        map_data = self.read_csv('data/interface_graphique/map1.csv') # def read_csv(self,filename)
        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == '0':  # Si la valeur est '0', c'est un type de terrain
                    self.grass.append((x, y))
                if cell == '1':  # Si la valeur est '1', c'est un mur
                    self.walls.append((x, y))
                if cell == '2':  # Si la valeur est '2', c'est un magma
                    self.magmas.append((x, y))
                if cell == '3':  # Si la valeur est '3', c'est un lilypad
                    self.lilypads.append((x, y))
                if cell == '4':  # Si la valeur est '4', c'est un mud
                    self.muds.append((x, y))
                if cell == '5':  # Si la valeur est '5', c'est une case healing
                    self.healing.append((x, y))

    # 0 : grass
    # 1 : murs
    # 2 : magma 
    # 3 : lilypad 
    # 4 : mud 
    # 5 : healing 

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename), mode='r') as data: # mode = 'r' :read 
            data = csv.reader(data, delimiter=',') # une autre variable s'appelle 'data' qui prend data comme sa fonction / csv.reader : est utilisée pour lire des fichiers au format CSV (Comma-Separated Values, ou valeurs séparées par des virgules) et convertir leurs contenus en lignes faciles à manipuler.
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
            selected_unit.is_selected = True # dans 'unit' on a initialisé self.is_selected = Non mais ici on met True pour dire que à chaque unité à laquelle on rentre, elle est sélectonnée automatiquement 
            selected_skill=None
            selected_target=None 
            self.flip_display() # Appel de la méthode display
            
            while not has_acted: # Quand has_acted=True 

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT: # utilisé pour détecter lorsque l'utilisateur ferme la fenêtre du jeu (en cliquant sur le bouton "X" en haut de la fenêtre).
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

                        selected_unit.move(dx, dy,self) # appelle la méthode  def move(self, dx, dy,game) dans 'unit' de l'objet selected_unit. Cette méthode permet de déplacer une unité (selected_unit) dans une direction spécifique sur la grille du jeu.
                        self.flip_display()

                        # Sélection d'une compétence

                        if selected_skill is None: # si on a pas encore sélectionné une compétence
                            if event.key==pygame.K_1: # Touche 1 pour la première compétence 
                                selected_skill=selected_unit.skills[0] # appeller la première case de l'élément de 'skills' de l'objet seleted_unit 
                                self.highlight_skill_range(selected_unit,selected_skill) # Appeler la méthode 'highlight_skill_range'
                            elif event.key==pygame.K_2: # Touche 1 pour la deuxière compétence
                                if len(selected_skill)>1: # Vérifier si l'unité sélectionnée possède plus d'une compétence 
                                    selected_skill=selected_unit.skills[1]
                                    self.highlight_skill_range(selected_unit,selected_skill) # def highlight_skill_range(self,unit,skill):
                            elif event.key == pygame.K_3:  # Touche 3 pour la troisième compétence
                                if len(selected_unit.skills) > 2:
                                    selected_skill = selected_unit.skills[2]
                                    self.highlight_skill_range(selected_unit, selected_skill) 
                        
                        elif selected_skill:
                            # Valider une compétence avec Entrée
                            if event.key==pygame.K_RETURN:
                                if selected_target: # si selected_target != None
                                    selected_unit.use_skills(selected_skill['name'], selected_target) # appeller la méthode use_skills dans 'unit'  : use_skills(self,skill_name,target)
                                    if selected_target.health<=0:
                                        self.enemy_units.remove(selected_target)
                                    has_acted=True
                                    break 
                            #Annuler la sélection avec Backspace
                            elif event.key==pygame.K_SPACE :
                                selected_skill=None
                                selected_target=None 
                                self.flip_display()
                            
                        #Gestion de la sélection avec un clic de souris
                    if event.type==pygame.MOUSEBUTTONDOWN and selected_skill:
                        mouse_x,mouse_y=pygame.mouse.get_pos()
                        target_x,target_y=mouse_x // CELL_SIZE ,mouse_y // CELL_SIZE
                        for enemy in self.enemy_units:
                            if enemy.x==target_x and enemy.y==target_y :
                                if abs(selected_unit.x-enemy.x)<=selected_skill['range'] and abs(selected_unit.y-enemy.y)<=selected_skill['range']:
                                    selected_target=enemy
                                    print(f"Ennemi sélectionné : {enemy.team} à ({enemy.x},{enemy.y})")
                                    self.highlight_selected_enemy(selected_target)  # Afficher l'indicateur visuel
                                    break


            selected_unit.is_selected=False # is_selected from unit 
            self.check_end_game()
    
    def highlight_selected_enemy(self, enemy):
        """Met en surbrillance l'ennemi sélectionné."""
        rect = pygame.Rect(enemy.x * CELL_SIZE, enemy.y * CELL_SIZE, CELL_SIZE, CELL_SIZE) # Les 2 dermiers CELL_SIZE c'est la largeur et le longeur d'une unité
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)  # Dessiner un rectangle rouge : pygame.draw.rect(surface, color, rect, width=0)
        pygame.display.flip()

    def highlight_skill_range(self,unit,skill):
        for dx in range (-skill['range'],skill['range']+1): # L'instruction skill['range'] fait référence à une valeur spécifique dans un dictionnaire nommé skill, où range est une clé.
            for dy in range (-skill['range'],skill['range']+1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
                    rect = pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (255, 255, 0, 128), rect, 3) # dessiner une grille de couleur jaune semi-transparent 
        pygame.display.flip()

    def check_end_game(self):
        if not self.enemy_units:
            print("Victoire ! Tous les ennemis ont été vaincus.")
            pygame.quit()
            exit()

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
