import pygame
import random
import os
import copy
import csv

# Constantes
GAME_TITLE = "Forest Gate"
CELL_SIZE = 40
GRID_SIZE_WIDTH = 30 # (1400//CELL_SIZE) - 1
GRID_SIZE_HEIGHT = 16 # int(GRID_SIZE_WIDTH*(9/16))
WIDTH = GRID_SIZE_WIDTH * CELL_SIZE
HEIGHT = GRID_SIZE_HEIGHT * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY= (128,128,128)
ORANGE=(255,178,102)
YELLOW = (255, 255, 0)
CHARACTER_PER_TEAM = 2


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

    def __init__(self, x, y, health, attack_power, endurence_max, team, texture_path, x_choiceButton, y_choiceButton, name):
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
        self.max_health = health
        self.attack_power = attack_power
        self.endurence_max = endurence_max
        self.team = team  # 'player 1' , 'player 2' ou 'enemy'
        self.is_selected = False
        self.x_choiceButton = x_choiceButton
        self.y_choiceButton = y_choiceButton
        self.skills = []
        self.name = name

        # Ajouter la texture
        self.texture = None
        if texture_path:
            if os.path.exists(texture_path):
                raw_texture = pygame.image.load(texture_path)
                self.texture = pygame.transform.scale(raw_texture, (CELL_SIZE, CELL_SIZE))  # Redimensionner l'image
                self.choice_texture = pygame.transform.scale(raw_texture, (CELL_SIZE*2, CELL_SIZE*2))
            else:
                print(f"{texture_path} not found")
                self.texture = None
                self.choice_texture = None

    def move(self, dx, dy, game):
        """Déplace l'unité de dx, dy."""

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE_WIDTH and 0 <= new_y < GRID_SIZE_HEIGHT and not game.is_wall(new_x, new_y):
            # Verifie si il ya pas d'autre unité dans la cellule
            for unit in game.player_units + game.player2_units + game.enemy_units:
                if unit.x == new_x and unit.y == new_y:
                    return  

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

        # Affiche l'unité 
        if self.texture :   # affiche la texture si elle existe
            screen.blit(self.texture, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            """Affiche l'unité sur l'écran."""
            color = BLUE if self.team == 'player' else RED
            if self.is_selected:
                pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)  
            
        # Affiche les contours pour designer l'equipe
        border_color = (0, 0, 255) if self.team == "player 1" else (0, 255, 0) if self.team == "player 2" else (255, 0, 0)
        pygame.draw.rect(screen, border_color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

        # If selected, draw a small yellow dot in the bottom-right corner of the cell
        if self.is_selected:
            dot_radius = 4  # Adjust radius as needed
            dot_x = self.x * CELL_SIZE + CELL_SIZE - dot_radius - 2
            dot_y = self.y * CELL_SIZE + CELL_SIZE - dot_radius - 2
            pygame.draw.circle(screen, YELLOW, (dot_x, dot_y), dot_radius)

        # Affiche la barre de vie
        bar_width = CELL_SIZE - 4
        bar_height = 4
        bar_x = self.x*CELL_SIZE + 2
        bar_y = self.y*CELL_SIZE + 2

        health_ratio = max(self.health/self.max_health, 0)
        current_bar_width = int(bar_width*health_ratio)

        pygame.draw.rect(screen, GREY, (bar_x, bar_y, bar_width, bar_height))
        if health_ratio>0.5:
            health_color=GREEN
        elif health_ratio<=0.5 and health_ratio>0.2 :
            health_color=ORANGE
        else:
            health_color=RED 
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_bar_width, bar_height))
     
    # affichage libre
    def choiceButton_draw(self, screen):
        if self.texture:
            # Agrandir la texture 
            

            # Affiche la texture a l'interieur du rectangle :
            self.button = pygame.Rect(self.x_choiceButton*CELL_SIZE, self.y_choiceButton*CELL_SIZE, CELL_SIZE*2, CELL_SIZE*2)
            screen.blit(self.choice_texture, (self.button.x,self.button.y))
            pygame.draw.rect(screen, WHITE, self.button, 2)

            # Affiche le nom du personnage :
            font = pygame.font.Font(None, 16)
            text = font.render(f"{str(self)} : {str(self.__class__.__name__)}", True, WHITE)
            # screen.blit(text, (self.button.x, self.button.y+int(CELL_SIZE*1.5)))

    
    def Unit_target_button(self):
        return pygame.Rect(self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)

                                         


# Definitions Des Types d'unités :
class Sorceress(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton, name):
        super().__init__(x, y, health=18, attack_power=4, endurence_max=4, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton, name=name)
        self.skills.append(PurpleChaos_Skill())
        
class Swordsman(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton, name):
        super().__init__(x, y, health=22, attack_power=3, endurence_max=6, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton, name=name)
        self.skills.append(Ichimonji_Skill())

class Monster(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton, name):
        super().__init__(x, y, health=28, attack_power=2, endurence_max=4, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton, name=name)


# Definition des compétances :
class Ichimonji_Skill:
    def __init__(self):
        self.name = "Ichimonji"
        self.damage = 10
        self.range = 1
        self.sound_effect = "data/skills/ichimonji.mp3"
        self.animation_frames = ["data/skills/ichimonji.png"]

    def use_skill(self, owner_unit, game):
        target = None  # Initialize the target
        # Check all potential targets
        for potential_target in game.player_units + game.player2_units + game.enemy_units:
            if (owner_unit.team != potential_target.team and
                    (abs(owner_unit.x - potential_target.x) <= self.range and abs(owner_unit.y - potential_target.y) <= self.range)):
                # validate target
                target = potential_target

                # Apply skill effects to the target
                target.health -= self.damage

                # Play the sound effect
                if self.sound_effect:
                    sound = pygame.mixer.Sound(self.sound_effect)
                    sound.play()

                # Play the animation
                for frame in self.animation_frames:
                    animation_image = pygame.image.load(frame).convert_alpha()
                    animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
                    game.screen.blit(animation_image, (target.x * CELL_SIZE, target.y * CELL_SIZE))
                    pygame.display.flip()
                    pygame.time.delay(100)  # Delay between frames

                if target.team == "player 1" and target.health<=0 :
                            game.player_units.remove(target)
                elif target.team == "player 2" and target.health<=0 :
                            game.player2_units.remove(target)
                elif target.team == "enemy" and target.health<=0 :
                            game.enemy_units.remove(target)

                self.used = True
                break

        if target == None :
            print("No valid target in range, Skill canceled.")
            self.used = True

class PurpleChaos_Skill:
    def __init__(self):
        self.name = "Purple Chaos"
        self.damage = 6
        self.range = 6
        self.sound_effect = "data/skills/magicblast.mp3"
        self.animation_frames = ["data/skills/purple.png"]

    def use_skill(self, owner_unit, game):
        target_x, target_y = owner_unit.x, owner_unit.y  # Start with the owner's position
        new_target_x, new_target_y = owner_unit.x, owner_unit.y

        # Initial target zone draw
        game.draw_map_units()
        highlight_rect = pygame.Rect((target_x-1) * CELL_SIZE, (target_y-1) * CELL_SIZE, CELL_SIZE*3, CELL_SIZE*3)
        pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
        pygame.display.flip()

        # Target selection phase
        selecting_target = True
        while selecting_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Move the highlight with arrow keys
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_target_x = max(0, target_x - 1)
                        new_target_y = target_y
                    elif event.key == pygame.K_RIGHT:
                        new_target_x = min(GRID_SIZE_WIDTH - 1, target_x + 1)
                        new_target_y = target_y
                    elif event.key == pygame.K_UP:
                        new_target_x = target_x
                        new_target_y = max(0, target_y - 1)
                    elif event.key == pygame.K_DOWN:
                        new_target_x = target_x
                        new_target_y = min(GRID_SIZE_HEIGHT - 1, target_y + 1)

                    # validate the new target if whithin range 
                    if abs(owner_unit.x - new_target_x) <= self.range and abs(owner_unit.y - new_target_y) <= self.range:
                        target_x = new_target_x
                        target_y = new_target_y
                        
                    # Redraw the map with the highlight
                    game.draw_map_units()
                    highlight_rect = pygame.Rect((target_x-1) * CELL_SIZE, (target_y-1) * CELL_SIZE, CELL_SIZE*3, CELL_SIZE*3)
                    pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
                    pygame.display.flip()

                    # Validate the target with the space key
                    if event.key == pygame.K_SPACE:
                        print("Launching Purple Chaos !")
                        selecting_target = False  # Exit the selection phase
                        break

                    # annuler le skill
                    elif event.key == pygame.K_1:
                        print("Skill canceled.")
                        return
                        

        # Explosion phase
        game.draw_map_units()
        pygame.display.flip()

        # Play sound effect
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound.play()

        # play animations and apply damage
        for dx in range(-1, 2):  # -1, 0, 1 for 3x3 area
            for dy in range(-1, 2):
                cell_x = target_x + dx
                cell_y = target_y + dy

                # Skip cells out of bounds
                if cell_x < 0 or cell_x >= GRID_SIZE_WIDTH or cell_y < 0 or cell_y >= GRID_SIZE_HEIGHT:
                    continue

                # Damage units in the 3x3 area
                for potential_target in game.player_units + game.player2_units + game.enemy_units:
                    if potential_target.x == cell_x and potential_target.y == cell_y:
                        potential_target.health -= self.damage

                        # Remove units with 0 or less health
                        if potential_target.health <= 0:
                            if potential_target.team == "player 1":
                                game.player_units.remove(potential_target)
                            elif potential_target.team == "player 2":
                                game.player2_units.remove(potential_target)
                            elif potential_target.team == "enemy":
                                game.enemy_units.remove(potential_target)

                # Play animation for the cell
                for frame in self.animation_frames:
                    animation_image = pygame.image.load(frame).convert_alpha()
                    animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
                    game.screen.blit(animation_image, (cell_x * CELL_SIZE, cell_y * CELL_SIZE))
                    pygame.display.flip()
                    pygame.time.delay(50)  # Delay between frames

        


        


        


# Création des personnages :
Personnages = {
        "Yennefer": Sorceress(2, 0, 'player', 'data/characters/yennefer.png', 3, 3, "Yennefer"),
        "Sekiro": Swordsman(3, 0, 'player', 'data/characters/samurai.png', 6, 3, "Sekiro"),
    }






