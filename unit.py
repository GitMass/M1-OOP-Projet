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
ANOTHER_BLUE = (51, 153, 255)
GREEN = (0, 255, 0)
GREY= (128,128,128)
ANOTHER_GREY= (224,224,224)
ORANGE=(255,178,102)
YELLOW = (255, 255, 0)
PURPLE = (153, 51, 255)
CHARACTER_PER_TEAM = 3
INFO_PANEL_HEIGHT = 120
WINDOW_HEIGHT = HEIGHT + INFO_PANEL_HEIGHT




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
        self.endurence_max_init=endurence_max 
        self.endurence_max = endurence_max
        self.team = team  # 'player 1' , 'player 2' ou 'enemy'
        self.is_selected = False
        self.x_choiceButton = x_choiceButton
        self.y_choiceButton = y_choiceButton
        self.skills = []
        self.name = name
        self.is_moving = False
        self.is_attacking = False
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

        self.is_moving = True
        self.is_attacking = False


        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE_WIDTH and 0 <= new_y < GRID_SIZE_HEIGHT and not game.is_wall(new_x, new_y):
            # Verifie si il ya pas d'autre unité dans la cellule
            for unit in game.player_units + game.player2_units + game.enemy_units:
                if unit.x == new_x and unit.y == new_y:
                    return  
                
                #Vérifie si l'unité a suffisamment d'endurance pour se déplacer
                if self.endurence_max <= 0:
                    print(f"{self.name} n'a plus assez d'endurance pour se déplacer.")
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
                if isinstance(self, Swordsman):  # Shogun
                    self.health -= 3
                elif isinstance(self, Shinobi):  # Assassin
                    self.health -= 4
                elif isinstance(self, Sorceress):
                    self.health -= 5

            elif (self.x, self.y) in game.muds:
                game.current_sound=game.sounds['mud']
                game.current_sound.play()
                if isinstance(self, Swordsman):  # Shogun
                    self.endurence_max -= 5
                elif isinstance(self, Shinobi):  # Assassin
                    self.endurence_max -= 2
                elif isinstance(self, Sorceress):# Sorceress 
                    self.endurence_max -= 3
                game.turn_counter=0 # Réinitialisation du compteur

            elif (self.x, self.y) in game.water:
                game.current_sound=game.sounds['water']
                game.current_sound.play()
                if isinstance(self, Swordsman):  # Shogun
                    self.endurence_max -= 4
                elif isinstance(self, Shinobi):  # Assassin
                    self.endurence_max -= 1
                elif isinstance(self, Sorceress):# Sorceress
                    self.endurence_max -= 2
                game.turn_counter=0  # Réinitialisation du compteur

            elif (self.x, self.y) in game.healing:
                game.current_sound=game.sounds['healing']
                game.current_sound.play()
                self.health += 5  # Effet de soin commun
                # S'assure que la santé ne dépasse pas le maximum
                if self.health > self.max_health:
                    self.health = self.max_health

            elif (self.x, self.y) in game.grass:
                game.current_sound=game.sounds['footstep']
                game.current_sound.play()

            elif (self.x, self.y) in game.snow:
                game.current_sound=game.sounds['snow']
                game.current_sound.play()
                if isinstance(self, Swordsman):  # Shogun
                    self.endurence_max -= 3
                elif isinstance(self, Shinobi):  # Assassin
                    self.endurence_max -= 2
                elif isinstance(self, Sorceress):# Sorceress
                    self.endurence_max -= 1
                game.turn_counter=0  # Réinitialisation du compteur

            elif (self.x, self.y) in game.bush:
                game.current_sound=game.sounds['bush']
                game.current_sound.play()
                if isinstance(self, Swordsman):  # Shogun
                    self.health -= 0
                elif isinstance(self, Shinobi):  # Assassin
                    self.health -= 1
                elif isinstance(self, Sorceress):
                    self.health -= 1

            else:
                game.current_sound=None # Aucun son à jouer 

            # Vérifie que l'endurance ne soit pas négative
            if self.endurence_max < 0:
                self.endurence_max = 0


    def attack(self, target):
        """Attaque une unité cible."""
        self.is_moving = False
        self.is_attacking = True

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
        border_color = BLUE if self.team == "player 1" else GREEN if self.team == "player 2" else (255, 0, 0)
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
        self.skills.append(Poison_Master())
        self.skills.append(Healer())
        
class Swordsman(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton, name):
        super().__init__(x, y, health=22, attack_power=3, endurence_max=6, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton, name=name)
        self.skills.append(Ichimonji_Skill())
        self.skills.append(Sky_Clear())
        self.skills.append(Samurai_Grave())

class Shinobi(Unit):
    def __init__(self, x, y, team, texture_path, x_choiceButton, y_choiceButton, name):
        super().__init__(x, y, health=22, attack_power=3, endurence_max=6, team=team, texture_path=texture_path, x_choiceButton=x_choiceButton, y_choiceButton=y_choiceButton, name=name)
        self.skills.append(Shuriken())
        self.skills.append(Assasin_Flicker())
        self.skills.append(Allies())

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




class Sky_Clear:
    def __init__(self):
        self.name = "Sky Clear"
        self.damage = 12 
        self.range = 3 
        self.sound_effect = "data/skills/ichimonji.mp3"
        self.animation_frames = ["data/skills/ichimonji.png"]

    def use_skill(self, owner_unit, game):
        target_x, target_y = owner_unit.x, owner_unit.y  # Start with the owner's position

        # Initial target zone draw
        game.draw_map_units()
        highlight_rect = pygame.Rect((target_x) * CELL_SIZE, (target_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
        pygame.display.flip()

        direction=None 

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
                        direction="left"
                    elif event.key == pygame.K_RIGHT:
                        direction="right"                      
                    elif event.key == pygame.K_UP:                        
                        direction="up"                        
                    elif event.key == pygame.K_DOWN:                        
                        direction="down"
                        

                    # Déterminer les 3 cases consécutives basées sur la direction
                    target_positions=[]
                    if direction=="up":
                        target_positions=[(owner_unit.x,owner_unit.y-i) for i in range(1,4)]
                    if direction=="down":
                        target_positions=[(owner_unit.x,owner_unit.y+i) for i in range(1,4)]
                    if direction=="left":
                        target_positions=[(owner_unit.x-i,owner_unit.y) for i in range(1,4)]
                    if direction=="right":
                        target_positions=[(owner_unit.x+i,owner_unit.y) for i in range(1,4)]

                    # Ensure the effect zone does not include the caster
                    target_positions = [(x, y) for x, y in target_positions if (x, y) != (owner_unit.x, owner_unit.y)]

                    # Redraw the map with the highlight
                    game.draw_map_units()
                    for new_target_x,new_target_y in target_positions:
                        if 0 <= new_target_x < GRID_SIZE_WIDTH and 0 <= new_target_y < GRID_SIZE_HEIGHT:
                            highlight_rect = pygame.Rect((new_target_x) * CELL_SIZE, (new_target_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                            pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
                    pygame.display.flip()

                    # Validate the target with the space key
                    if event.key == pygame.K_SPACE:
                        print("Launching SKY CLEAR !!!")
                        selecting_target = False  # Exit the selection phase
                        break

                    # annuler le skill
                    elif event.key == pygame.K_x:
                        print("Skill canceled.")
                        return
                        

        # Explosion phase
        game.draw_map_units()
        pygame.display.flip()

        # Play sound effect
        if self.sound_effect:
            sound2 = pygame.mixer.Sound("data/skills/sword_throw.mp3")
            sound3 = pygame.mixer.Sound("data/skills/crack.mp3")
            sound2.play()
            sound3.play()

        # Damage units in the picked area
        for new_target_x,new_target_y in target_positions:
            if 0 <= new_target_x < GRID_SIZE_WIDTH and 0 <= new_target_y < GRID_SIZE_HEIGHT:
                for potential_target in game.player_units + game.player2_units + game.enemy_units:
                    if potential_target == owner_unit:
                        continue
                    if potential_target.x == new_target_x and potential_target.y == new_target_y:
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
                    # Load and display the cracked ground frame
                    for cracked_frame in self.animation_frames:
                        cracked_image = pygame.image.load(cracked_frame).convert_alpha()
                        cracked_image = pygame.transform.scale(cracked_image, (CELL_SIZE, CELL_SIZE)) 

                        # Draw the cracked ground image first (background)
                        game.screen.blit(cracked_image, (new_target_x * CELL_SIZE, new_target_y * CELL_SIZE))
                        # Draw the ichimonji image on top
                        game.screen.blit(animation_image, (new_target_x * CELL_SIZE, new_target_y * CELL_SIZE))

                        # Update the display
                        pygame.display.flip()
                        pygame.time.delay(50)  # Delay between frames


class Samurai_Grave:
    def __init__(self):
        self.name = "Samurai Grave"
        self.damage = 15 
        self.range = 6
        self.sound_effect = "data/skills/ichimonji.mp3"
        self.animation_frames = ["data/skills/samurai_grave.png"]
        self.animation_frames_2 = ["data/skills/gris.png"]

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
                        print("Launching SAMURAI GRAVE !")
                        selecting_target = False  # Exit the selection phase
                        break

                    # annuler le skill
                    elif event.key == pygame.K_x:
                        print("Skill canceled.")
                        return
                        

        # Explosion phase
        game.draw_map_units()
        pygame.display.flip()

        # Play sound effect
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound2=pygame.mixer.Sound("data/skills/die.mp3")
            sound.play()
            sound2.play()
            

        # play animations and apply damage
        affected_cells = []
        for dx in range(-1, 2):  # -1, 0, 1 for 3x3 area
            for dy in range(-1, 2):
                cell_x = target_x + dx
                cell_y = target_y + dy

                # Skip cells out of bounds
                if cell_x < 0 or cell_x >= GRID_SIZE_WIDTH or cell_y < 0 or cell_y >= GRID_SIZE_HEIGHT:
                    continue

                affected_cells.append((cell_x, cell_y))

        # Play animations and apply damage simultaneously
        for frame1 in self.animation_frames:
            # Draw the "samurai_grave" animation
            for cell_x, cell_y in affected_cells:
                animation_image1 = pygame.image.load(frame1).convert_alpha()
                animation_image1 = pygame.transform.scale(animation_image1, (CELL_SIZE, CELL_SIZE))
                game.screen.blit(animation_image1, (cell_x * CELL_SIZE, cell_y * CELL_SIZE))

            pygame.display.flip()
            pygame.time.delay(500)  # Delay between frames
        
        sound3 = pygame.mixer.Sound("data/skills/dagger-slash-sound.mp3")
        sound3.play()
        pygame.time.delay(int(sound3.get_length() * 100))  # Attendre la fin du deuxième son
        sound4=pygame.mixer.Sound("data/skills/sword-blade-slash-fx.mp3")
        sound4.play()
        pygame.time.delay(int(sound4.get_length() * 100))  # Attendre la fin du deuxième son
        sound5 = pygame.mixer.Sound("data/skills/sword-clash.mp3")
        sound5.play()
        pygame.time.delay(int(sound5.get_length() * 100))  # Attendre la fin du deuxième son
        sound6=pygame.mixer.Sound("data/skills/sword-blade-slash-metallic.mp3")
        sound6.play()
        pygame.time.delay(int(sound6.get_length() * 100))  # Attendre la fin du deuxième son

        # Apply damage to units in affected cells
        for cell_x, cell_y in affected_cells:
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

class PurpleChaos_Skill:
    def __init__(self):
        self.name = "Purple Chaos"
        self.damage = 10 
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
                    elif event.key == pygame.K_x:
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

class Poison_Master:
    def __init__(self):
        self.name = "Poison Master"
        self.damage = 6
        self.range = 6
        self.sound_effect = "data/skills/poison_master.mp3"
        self.animation_frames = ["data/skills/poison_cell.png"]
        self.maps = ["data/maps/map_poison_1.csv", "data/maps/map_poison_2.csv", "data/maps/map_poison_3.csv"]
        self.current_map_index = 0
        self.poison_zones = self.load_poison_zones(self.maps[self.current_map_index])
        
        # Variables graphiques
        self.temp_surface = None
        self.animation_image = None
    
    def initialize_graphics(self):
        """Initialise les graphismes et les surfaces après l'initialisation de Pygame."""
        if self.animation_image is None:
            self.animation_image = pygame.image.load(self.animation_frames[0]).convert_alpha()
            self.animation_image = pygame.transform.scale(self.animation_image, (CELL_SIZE, CELL_SIZE))
    
    def load_poison_zones(self, filename):
        """Charge les zones de poison depuis un fichier CSV."""
        zones = []
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for y, row in enumerate(reader):
                for x, cell in enumerate(row):
                    if cell == '*':
                        zones.append((x, y))  # Ajouter la position du flacon (x, y)
        return zones

        
    def use_skill(self, owner_unit, game):
        # S'assurer que les graphismes sont initialisés
        if self.animation_image is None:
            self.initialize_graphics()
        
        selecting_target = True
        # Préparer une surface temporaire de la taille de l'écran
        if self.temp_surface is None:
            self.temp_surface = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        
        while selecting_target:
            # Dessiner sur la surface temporaire
            self.temp_surface.fill((0, 0, 0, 0))  # Effacer la surface temporaire (transparent)
            
            for x, y in self.poison_zones:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.temp_surface, (0,0,0, 128), rect)  # Dessiner les zones de poison
            
            # Blitter la surface temporaire sur l'écran principal
            game.draw_map_units()  # Dessiner l'état de la carte
            game.screen.blit(self.temp_surface, (0, 0))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    # Changer de carte avec les flèches directionnelles
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.current_map_index = (self.current_map_index + 1) % len(self.maps)
                        self.poison_zones = self.load_poison_zones(self.maps[self.current_map_index])
                        break
                    # Valider avec K_SPACE
                    elif event.key == pygame.K_SPACE:
                        print("Lancement du flacon de poison avec la carte sélectionnée !")
                        selecting_target = False
                        break
                    # Annuler avec K_X
                    elif event.key == pygame.K_x:
                        print("Skill annulé.")
                        return
        # Play sound effect
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound.play()
            
        # Phase d'explosion
        game.draw_map_units()
        self.temp_surface.fill((0, 0, 0, 0))  # Effacer la surface temporaire
        for x, y in self.poison_zones:
            self.temp_surface.blit(self.animation_image, (x * CELL_SIZE, y * CELL_SIZE))  # Dessiner l'image d'animation
        # Afficher la surface avec toutes les animations sur l'écran
        game.screen.blit(self.temp_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)  # Réduire le délai pour un affichage fluide
        
        
        # Appliquer les dégâts
        for cell_x, cell_y in self.poison_zones:
            for potential_target in game.player_units + game.player2_units + game.enemy_units:
                if potential_target == owner_unit:
                    continue
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


class Healer:
    def __init__(self):
        self.name = "Healer"
        self.heal_amount = 5  # Montant de soin par unité
        self.range = 3  # Portée de la compétence
        self.sound_effect = "data/skills/magic.mp3"  # Effet sonore
        self.animation_frames = ["data/skills/healer.png"]  # Animation de soin

    def use_skill(self, owner_unit, game):
        target_x, target_y = owner_unit.x, owner_unit.y  # Position du propriétaire

        # Afficher la zone grise de la portée
        game.draw_map_units()
        highlight_rect = pygame.Rect((target_x-2) * CELL_SIZE, (target_y-2) * CELL_SIZE, CELL_SIZE*5, CELL_SIZE*5)
        pygame.draw.rect(game.screen, (GREEN), highlight_rect, 3)  # Bord gris
        pygame.display.flip()

        # Attendre que l'utilisateur appuie sur la barre d'espace pour lancer la compétence
        selecting_target = True
        while selecting_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Vérifier si l'utilisateur appuie sur la barre d'espace pour lancer la compétence
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Lancement du soin !")
                        selecting_target = False  # Quitter la phase de sélection
                        break

                    # Annuler la compétence si l'utilisateur appuie sur la touche X
                    elif event.key == pygame.K_x:
                        print("Compétence annulée.")
                        return

        # Phase d'activation de la compétence
        game.draw_map_units()
        pygame.display.flip()

        # Jouer l'effet sonore
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound.play()
        affected_cells=[]
        # Appliquer les soins aux alliés dans la zone d'effet
        for dx in range(-self.range, self.range-1):  # -range, ..., +range pour une zone carrée
            for dy in range(-self.range, self.range -1):
                cell_x = target_x+1 + dx
                cell_y = target_y+1 + dy

                # Vérifier si la cellule est dans les limites du terrain
                if cell_x < 0 or cell_x >= GRID_SIZE_WIDTH or cell_y < 0 or cell_y >= GRID_SIZE_HEIGHT:
                    continue

                # Soigner les unités alliées dans la zone d'effet
                for potential_target in game.player_units + game.player2_units:  # Allié dans les deux équipes
                    if potential_target.x == cell_x and potential_target.y == cell_y:
                        potential_target.health += self.heal_amount  # Augmenter les PV de l'unité

                        # Assurer que les PV ne dépassent pas la capacité maximale de l'unité
                        if potential_target.health > potential_target.max_health:
                            potential_target.health = potential_target.max_health

                affected_cells.append((cell_x,cell_y))
        # Jouer l'animation de soin pour la cellule
        for frame in self.animation_frames:
            game.draw_map_units()

            # Draw the "samurai_grave" animation
            for cell_x, cell_y in affected_cells:
                animation_image = pygame.image.load(frame).convert_alpha()
                animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
                game.screen.blit(animation_image, (cell_x * CELL_SIZE, cell_y * CELL_SIZE))

            pygame.display.flip()
            pygame.time.delay(1000)  # Delay between frames

        
class Shuriken:
    def __init__(self):
        self.name = "Shuriken"
        self.damage = 8 
        self.range = 4  
        self.sound_effect = "data/skills/shuriken_sound_1.mp3"
        self.animation_frames = ["data/skills/shuriken.png"]
        self.animation_frames_2 = ["data/skills/green_magma.png"]

    def use_skill(self, owner_unit, game):
        target_x, target_y = owner_unit.x, owner_unit.y  # Start with the owner's position

        # Initial target zone draw
        game.draw_map_units()
        highlight_rect = pygame.Rect((target_x) * CELL_SIZE, (target_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
        pygame.display.flip()

        direction=None 

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
                        direction="left"
                    elif event.key == pygame.K_RIGHT:
                        direction="right"                      
                    elif event.key == pygame.K_UP:                        
                        direction="up"                        
                    elif event.key == pygame.K_DOWN:                        
                        direction="down"
                        

                    # Déterminer les 3 cases consécutives basées sur la direction
                    target_positions=[]
                    if direction=="up":
                        target_positions=[(owner_unit.x,owner_unit.y-i) for i in range(1,5)]
                    if direction=="down":
                        target_positions=[(owner_unit.x,owner_unit.y+i) for i in range(1,5)]
                    if direction=="left":
                        target_positions=[(owner_unit.x-i,owner_unit.y) for i in range(1,5)]
                    if direction=="right":
                        target_positions=[(owner_unit.x+i,owner_unit.y) for i in range(1,5)]

                    # Ensure the effect zone does not include the caster
                    target_positions = [(x, y) for x, y in target_positions if (x, y) != (owner_unit.x, owner_unit.y)]

                    # Redraw the map with the highlight
                    game.draw_map_units()
                    for new_target_x,new_target_y in target_positions:
                        if 0 <= new_target_x < GRID_SIZE_WIDTH and 0 <= new_target_y < GRID_SIZE_HEIGHT:
                            highlight_rect = pygame.Rect((new_target_x) * CELL_SIZE, (new_target_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                            pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)  # Gray border
                    pygame.display.flip()

                    # Validate the target with the space key
                    if event.key == pygame.K_SPACE:
                        print("Launching SHURIKEN !!!")
                        selecting_target = False  # Exit the selection phase
                        break

                    # annuler le skill
                    elif event.key == pygame.K_x:
                        print("Skill canceled.")
                        return
                        

        # Explosion phase
        game.draw_map_units()
        pygame.display.flip()

        # Play sound effect
        if self.sound_effect:
            sound1 = pygame.mixer.Sound(self.sound_effect)
            sound1.play()
            pygame.time.delay(50)  # Attendre la fin du premier son

            # Jouer un deuxième son
            sound2 = pygame.mixer.Sound("data/skills/shuriken_sound_2.mp3")
            sound3 = pygame.mixer.Sound("data/skills/sword-blade-slash-metallic.mp3")
            sound2.play()
            sound3.play()

        # Damage units in the picked area
        for new_target_x,new_target_y in target_positions:
            if 0 <= new_target_x < GRID_SIZE_WIDTH and 0 <= new_target_y < GRID_SIZE_HEIGHT:
                for potential_target in game.player_units + game.player2_units + game.enemy_units:
                    if potential_target == owner_unit:
                        continue
                    if potential_target.x == new_target_x and potential_target.y == new_target_y:
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
                    # Load and display the cracked ground frame
                    for cracked_frame in self.animation_frames_2:
                        cracked_image = pygame.image.load(cracked_frame).convert_alpha()
                        cracked_image = pygame.transform.scale(cracked_image, (CELL_SIZE, CELL_SIZE)) 

                        # Draw the cracked ground image first (background)
                        game.screen.blit(cracked_image, (new_target_x * CELL_SIZE, new_target_y * CELL_SIZE))
                        # Draw the ichimonji image on top
                        game.screen.blit(animation_image, (new_target_x * CELL_SIZE, new_target_y * CELL_SIZE))

                        # Update the display
                        pygame.display.flip()
                        pygame.time.delay(100)  # Delay between frames
        


class Assasin_Flicker :
    def __init__(self):
        self.name = "Ichimonji"
        self.damage = 10
        self.range = 5
        self.sound_effect = "data/skills/ichimonji.mp3"
        self.animation_frames = ["data/skills/ichimonji.png"]

    def use_skill(self, owner_unit, game):
        target = None

        # Draw the initial range area
        game.draw_map_units()
        for dx in range(-self.range, self.range + 1):
            for dy in range(-self.range, self.range + 1):
                x, y = owner_unit.x + dx, owner_unit.y + dy
                if 0 <= x < GRID_SIZE_WIDTH and 0 <= y < GRID_SIZE_HEIGHT:
                    highlight_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)
        pygame.display.flip()

        selecting_target = True
        while selecting_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse clicks for target selection
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_x, clicked_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                    # Check if the clicked position is within range and has an enemy
                    if abs(owner_unit.x - clicked_x) <= self.range and abs(owner_unit.y - clicked_y) <= self.range:
                        for potential_target in game.player_units + game.player2_units + game.enemy_units:
                            if potential_target.x == clicked_x and potential_target.y == clicked_y:
                                target = potential_target
                                selecting_target = False
                                break

                # Cancel skill
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    print("Skill canceled.")
                    return

        if not target:
            print("No valid target selected.")
            return

        # Highlight the area around the target
        adjacent_units = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_x, adj_y = target.x + dx, target.y + dy
            if 0 <= adj_x < GRID_SIZE_WIDTH and 0 <= adj_y < GRID_SIZE_HEIGHT:
                adjacent_units.append((adj_x, adj_y))

        direction_selection = True
        selected_position = None
        while direction_selection:
            game.draw_map_units()
            for adj_x, adj_y in adjacent_units:
                highlight_rect = pygame.Rect(adj_x * CELL_SIZE, adj_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(game.screen, (153, 51, 255, 128), highlight_rect, 3)  # Purple border
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_position = (target.x - 1, target.y)
                        highlight_rect = pygame.Rect( (target.x - 1)* CELL_SIZE, target.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(game.screen, (255, 255, 0, 128), highlight_rect, 3)  # Yellow border
                        pygame.display.flip()
                        pygame.time.delay(100) 
                    elif event.key == pygame.K_RIGHT:
                        selected_position = (target.x + 1, target.y)
                        highlight_rect = pygame.Rect( (target.x + 1)* CELL_SIZE, target.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(game.screen, (255, 255, 0, 128), highlight_rect, 3)  # Yellow border
                        pygame.display.flip()
                        pygame.time.delay(100)
                    elif event.key == pygame.K_UP:
                        selected_position = (target.x, target.y - 1)
                        highlight_rect = pygame.Rect( (target.x)* CELL_SIZE, (target.y-1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(game.screen, (255, 255, 0, 128), highlight_rect, 3)  # Yellow border
                        pygame.display.flip()
                        pygame.time.delay(100)
                    elif event.key == pygame.K_DOWN:
                        selected_position = (target.x, target.y + 1)
                        highlight_rect = pygame.Rect( (target.x)* CELL_SIZE, (target.y+1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(game.screen, (255, 255, 0, 128), highlight_rect, 3)  # Yellow border
                        pygame.display.flip()
                        pygame.time.delay(100)

                    # Confirm selection with space key
                    if event.key == pygame.K_SPACE and selected_position in adjacent_units:
                        direction_selection = False
                        break

                    # Cancel skill
                    elif event.key == pygame.K_x:
                        print("Skill canceled.")
                        return

        # Teleport behind the target and apply damage
        owner_unit.x, owner_unit.y = selected_position

        # Play sound effect
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound.play()

        # Apply damage
        target.health -= self.damage
        if target.health <= 0:
            if target in game.player_units:
                game.player_units.remove(target)
            elif target in game.player2_units:
                game.player2_units.remove(target)
            elif target in game.enemy_units:
                game.enemy_units.remove(target)


    
        # Play animation
        animation_image = pygame.image.load(self.animation_frames[0]).convert_alpha()
        animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
        game.screen.blit(animation_image, (target.x * CELL_SIZE, target.y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(100)


class Shadow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_frames = ["data/skills/shadow.png"]
class Allies:
    def __init__(self):
        self.name = "Allies"
        self.damage = 10
        self.range = 3 
        self.sound_effect = "data/skills/ichimonji.mp3"
        self.animation_frames = ["data/skills/ichimonji.png"]
    def use_skill(self, owner_unit, game):
        # Calculate the zone of effect
        zone_of_effect = []
        for dx in range(-self.range, self.range ):
            for dy in range(-self.range, self.range ):
                x, y = owner_unit.x + dx, owner_unit.y + dy
                if 0 <= x < GRID_SIZE_WIDTH and 0 <= y < GRID_SIZE_HEIGHT:
                    zone_of_effect.append((x, y))
        # Draw the zone of effect
        game.draw_map_units()
        for x, y in zone_of_effect:
            highlight_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(game.screen, (128, 128, 128, 128), highlight_rect, 3)
        pygame.display.flip()
        selecting_target = True
        while selecting_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Validate the skill activation with space
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        selecting_target = False
                        break
                    # Cancel the skill
                    elif event.key == pygame.K_x:
                        print("Skill canceled.")
                        return
        # Find all enemies in the zone of effect
        enemies_in_zone = [
            unit for unit in game.player_units + game.player2_units + game.enemy_units
            if (unit.x, unit.y) in zone_of_effect and unit !=owner_unit 
        ]
        if not enemies_in_zone:
            print("No enemies in the zone of effect.")
            return
        # Crée des shadows et les positionne près des ennemis
        shadows = []
        shadows_next=[]
        adjacent_positions = [
            (owner_unit.x + dx, owner_unit.y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= owner_unit.x + dx < GRID_SIZE_WIDTH and 0 <= owner_unit.y + dy < GRID_SIZE_HEIGHT
        ]
        for pos in adjacent_positions:
            shadow_next = Shadow(*pos)
            shadows_next.append(shadow_next)
        # Affiche les shadows autour du personnage
        for shadow_next in shadows_next:
            animation_image = pygame.image.load(shadow_next.animation_frames[0]).convert_alpha()
            animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
            game.screen.blit(animation_image, (shadow_next.x * CELL_SIZE, shadow_next.y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(500)
        for enemy in enemies_in_zone:
            # Trouver une position adjacente disponible pour le shadow
            shadow_position = self.get_adjacent_position(enemy, game)
            if shadow_position:
                shadow = Shadow(*shadow_position)
                shadows.append((shadow, enemy))  # Associer le shadow à son ennemi
        # Affiche les shadows sur la carte
        for shadow_enemy_pair in shadows:
            shadow, enemy = shadow_enemy_pair  # Extraire shadow et enemy explicitement
            animation_image = pygame.image.load(shadow.animation_frames[0]).convert_alpha()
            animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
            game.screen.blit(animation_image, (shadow.x * CELL_SIZE, shadow.y * CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(1000)
        # Les shadows attaquent leurs ennemis associés
        for shadow, enemy in shadows:
            # Téléportation du shadow près de l'ennemi
            shadow.x, shadow.y = self.get_adjacent_position(enemy, game)
            # Animation d'attaque
            animation_image = pygame.image.load(self.animation_frames[0]).convert_alpha()
            animation_image = pygame.transform.scale(animation_image, (CELL_SIZE, CELL_SIZE))
            game.screen.blit(animation_image, (enemy.x * CELL_SIZE, enemy.y * CELL_SIZE))
            pygame.display.flip()
            pygame.time.delay(500)
            # Appliquer les dégâts à l'ennemi
            enemy.health -= self.damage
            if enemy.health <= 0:
                if enemy in game.player_units:
                    game.player_units.remove(enemy)
                elif enemy in game.player2_units:
                    game.player2_units.remove(enemy)
                elif enemy in game.enemy_units:
                    game.enemy_units.remove(enemy)
        # Jouer l'effet sonore
        if self.sound_effect:
            sound = pygame.mixer.Sound(self.sound_effect)
            sound.play()
    def get_adjacent_position(self, target, game):
        """
        Trouve une position libre adjacente à une cible (target).
        Retourne une position (x, y) ou None si aucune position n'est disponible.
        """
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_x, adj_y = target.x + dx, target.y + dy
            if 0 <= adj_x < GRID_SIZE_WIDTH and 0 <= adj_y < GRID_SIZE_HEIGHT:
                # Vérifie qu'aucune autre unité n'est sur cette position
                if not any(
                    unit.x == adj_x and unit.y == adj_y
                    for unit in game.player_units + game.player2_units + game.enemy_units
                ):
                    return adj_x, adj_y
        return None  # Aucune position disponible



# Création des personnages :
Personnages = {
        "Yennefer": Sorceress(2, 0, 'player', 'data/characters/yennefer.png', 8, 8, "Yennefer"),
        "Shogun": Swordsman(3, 0, 'player', 'data/characters/samurai.png', 14, 8, "Shogun"),
        "Sekiro": Shinobi(4, 0, 'player', 'data/characters/sekiro.png', 20, 8, "Sekiro"),
    }






