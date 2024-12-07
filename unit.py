import pygame
import random
import os

# Constantes
GRID_SIZE = 18
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CHARACTER_PER_TEAM = 3
PLAYER_TURN_COLOR=BLUE
ENEMY_TURN_COLOR=RED



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

    def __init__(self, x, y, health, attack_power, endurence_max, team, texture_path, x_choiceButton, y_choiceButton):
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
        self.x_choiceButton = x_choiceButton
        self.y_choiceButton = y_choiceButton

        # Ajouter la texture
        self.texture = None
        if texture_path:
            if os.path.exists(texture_path):
                self.texture = pygame.image.load(texture_path)
                self.texture = pygame.transform.scale(self.texture, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image
            else:
                print(f"{texture_path} not found")
                self.texture = None

       

    
    
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
        if self.texture :   # affiche la texture si elle existe
            screen.blit(self.texture, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        # affichage d'un rectangle vert autour du joueur pendant son tour
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
            self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),width=3)
   
    

    def choiceButton_draw(self, screen):
        if self.texture:
            #Affiche la texture a l'interieur du rectangle :
            self.button = pygame.Rect(self.x_choiceButton*CELL_SIZE, self.y_choiceButton*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(self.texture, (self.button.x,self.button.y))
            pygame.draw.rect(screen, WHITE, self.button, 2)
           
            # Affiche le nom et les caractéristiques du personnage
            font = pygame.font.Font(None, 20)  # Police de taille 20
            name_text = font.render(f"{self.__class__.__name__}", True, WHITE)  # Nom du personnage
            health_text = font.render(f"HP: {self.health}", True, WHITE)  # Santé
            attack_text = font.render(f"AP: {self.attack_power}", True, WHITE)  # Attaque
            endurence_max_text = font.render(f"EN_MAX: {self.endurence_max }", True, WHITE)
            screen.blit(name_text, (self.button.x, self.button.y + CELL_SIZE + 5))
            screen.blit(health_text, (self.button.x, self.button.y + CELL_SIZE + 20))
            screen.blit(attack_text, (self.button.x , self.button.y + CELL_SIZE + 35))  
            screen.blit(endurence_max_text, (self.button.x , self.button.y + CELL_SIZE + 50))              
              
  

# Definitions Des Types d'unités :
class Sorceress(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton):
        super().__init__(x, y, health=18, attack_power=4, endurence_max=2, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton)

class Swordsman(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton):
        super().__init__(x, y, health=22, attack_power=3, endurence_max=6, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton)

class Monster(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton):
        super().__init__(x, y, health=28, attack_power=2, endurence_max=4, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton)


class Archer(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton):
        super().__init__(x, y, health=9, attack_power=2, endurence_max=3, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton)
class Guerrier (Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton):
        super().__init__(x, y, health=44, attack_power=5, endurence_max=3, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton)



# Création des personnages :
Personnages = {
        "Yennefer": Sorceress(2, 0, 'player', 'data/yennefer.png', 3, 3),
        "Sekiro": Swordsman(3, 0, 'player', 'data/sekiro.png', 6, 3),
        
}
Enemy={
       "Archer":  Archer(8,6,'enemy', 'data/Archer.png',3,3),
       "Guerriere": Guerrier(9,6,'enemy','data/guerriere.jpg',6,3),


}
   






