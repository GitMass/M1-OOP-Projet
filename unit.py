import pygame
import random

# Constantes
GRID_SIZE = 12
CELL_SIZE = 64
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN=(51,102,0)
GREY= (128,128,128)
ORANGE=(255,178,102)


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

    def __init__(self, x, y, health, attack_power, team,skills=None):
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
        self.health = health # Points de vie actuels
        self.max_health= health # Santé maximale
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.skills=skills if skills else []


    """
    skills : list[dict]
        Une liste de compétences de l'unité. Par exemple :
        [{'name': 'Fireball', 'damage': 5, 'range': 3}, {'name': 'Heal', 'heal': 4, 'cost': 2}]
    """

    def use_skills(self,skill_name,target):
        """
        Utilise une compétence sur une cible.

        Paramètres
        ----------
        skill_name : str
            Le nom de la compétence à utiliser.
        target : Unit
            L'unité cible de la compétence.
        """
        for skill in self.skills :
            if skill['name']==skill_name:
                if 'damage' in skill:
                    if abs(self.x-target.x)<=skill.get('range',1) and abs(self.y-target.y)<=skill.get('range',1):
                        target.health -= skill['damage']
                        if target.health<0:
                            target.health=0 # Éviter les points de vie négatifs 
                        print(f"{self.team} utilse {skill_name} sur {target.team}. Dégât : {skill['damage']}")
                if 'heal' in skill:
                    target.health +=skill['heal']
                    print(f"{self.team} utilse {skill_name} sur {target.team}. Soin : {skill['heal']}")
                break 

    def move(self, dx, dy,game):
        #"""Déplace l'unité de dx, dy."""
        #if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
        #    self.x += dx
        #    self.y += dy
        """
        Déplace l'unité de dx, dy si la nouvelle cellule n'est pas un mur.
        """
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and not game.is_wall(new_x, new_y):
            if hasattr(game, 'current_sound') and game.current_sound:  # Vérifie l'existence de current_sound
                game.current_sound.stop()
                
            # Met à jour la position     
            self.x = new_x
            self.y = new_y

        # Détection du type de terrain
        if (self.x, self.y) in game.magmas:
            game.current_sound=game.sounds['magma']
            game.current_sound.play()
        elif (self.x, self.y) in game.muds:
            game.current_sound=game.sounds['mud']
            game.current_sound.play()
        elif (self.x, self.y) in game.lilypads:
            game.current_sound=game.sounds['lilypad']
            game.current_sound.play()
        elif (self.x, self.y) in game.healing:
            game.current_sound=game.sounds['healing']
            game.current_sound.play()
        elif (self.x, self.y) in game.grass:
            game.current_sound=game.sounds['footstep']
            game.current_sound.play()
        else:
            game.current_sound=None # Aucun son à jouer 


    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, DARK_GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Calcul de la position de la barre de point de vie 
        bar_width=9  # Largeur de la barre de vie
        bar_height=CELL_SIZE-2         # Hauteur de la barre de vie
        bar_x=self.x*CELL_SIZE+54 # Position x de la barre 
        bar_y=self.y*CELL_SIZE # Position y

        # Calculer la largeur de la barre de vie en fonction des points de vie restant
        health_ratio=max(self.health/self.max_health,0) # Ratio de santé (entre 0 et 1)
        current_health_height=int(bar_height*health_ratio)

        # Dessiner le fond de la barre (gris)
        pygame.draw.rect(screen,GREY,(bar_x,bar_y,bar_width,bar_height))
        # Dessiner la barre de santé (verte si >50%, orange si 20<v<=50%, sinon rouge)
        if health_ratio>0.5:
            health_color=GREEN
        elif health_ratio<=0.5 and health_ratio>0.2 :
            health_color=ORANGE
        else:
            health_color=RED 
        pygame.draw.rect(screen,health_color,(bar_x,bar_y+ (bar_height - current_health_height), bar_width, current_health_height))