from unit import *

# VERSION
X = 1
Y = 0
Z = 0
print(f" =========== {GAME_TITLE} Version {X}.{Y}.{Z} =========== \n")


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



    # init game
    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """

        # screen
        self.screen = screen

        # units
        self.player_units = []
        self.player2_units = []
        self.enemy_units = []

        # game mode
        self.GameMode = ""
        
        # Compteur de tours
        self.turn_counter = 0  

        # maps
        self.maps = {
           "map1": {"name": "Novigrad Meadows", "fichier": "data/maps/map1.csv", "photo": "data/maps/map1.png"},
           "map2": {"name": "Skellige Mountains", "fichier": "data/maps/map2.csv", "photo": "data/maps/map2.png"},
        }
        # map choice
        self.selected_map_file = []
        # map textures
        self.grass=[]
        self.walls = []
        self.magmas = []
        self.water = []
        self.muds = []
        self.healing=[]
        self.snow=[]
        self.bush=[]

        # Load background image
        self.info_panel_background_image = pygame.image.load("data\splash_images\info_panel_background.png").convert()
        self.info_panel_background_image = pygame.transform.scale(self.info_panel_background_image, (WIDTH, INFO_PANEL_HEIGHT))




    # Charger les textures et sons
    def load_textures_sounds(self):
        # Sound effects
        pygame.mixer.init()
        self.current_sound = None
        self.sounds = {
            'footstep': pygame.mixer.Sound('data/map_sound_effects/grass_footstep.wav'),
            'magma': pygame.mixer.Sound('data/map_sound_effects/fire.wav'),
            'mud': pygame.mixer.Sound('data/map_sound_effects/mud.wav'),
            'water': pygame.mixer.Sound('data/map_sound_effects/swimming.mp3'),
            'healing': pygame.mixer.Sound('data/map_sound_effects/apple.wav'),
            'snow': pygame.mixer.Sound('data/map_sound_effects/snow.mp3'),
            'bush': pygame.mixer.Sound('data/map_sound_effects/bush.mp3'),

        }

        # Map textures
        # charger les textures de la map
        self.GRASS=pygame.image.load('data/tiles/simplegrass.png').convert_alpha()
        self.WALL= pygame.image.load('data/tiles/cartoon_wall.png').convert_alpha()
        self.MAGMA=pygame.image.load('data/tiles/magma.png').convert_alpha()
        self.WATER=pygame.image.load('data/tiles/lilypad.png').convert_alpha()
        self.MUD=pygame.image.load('data/tiles/mud.png').convert_alpha()
        self.APPLE_TREE=pygame.image.load('data/tiles/appletree2.png').convert_alpha()
        self.SNOW=pygame.image.load('data/tiles/snow.jpg').convert_alpha()
        self.BUSH=pygame.image.load('data/tiles/bush.png').convert_alpha()
       
        # Redimensionner les textures
        self.GRASS = pygame.transform.scale(self.GRASS, (CELL_SIZE, CELL_SIZE))
        self.WALL = pygame.transform.scale(self.WALL, (CELL_SIZE, CELL_SIZE))
        self.MAGMA = pygame.transform.scale(self.MAGMA, (CELL_SIZE, CELL_SIZE))
        self.WATER = pygame.transform.scale(self.WATER, (CELL_SIZE, CELL_SIZE))
        self.MUD = pygame.transform.scale(self.MUD, (CELL_SIZE, CELL_SIZE))
        self.APPLE_TREE = pygame.transform.scale(self.APPLE_TREE, (CELL_SIZE, CELL_SIZE))
        self.SNOW=pygame.transform.scale(self.SNOW, (CELL_SIZE, CELL_SIZE))
        self.BUSH=pygame.transform.scale(self.BUSH, (CELL_SIZE, CELL_SIZE))
        


    # bouton retourner
    def draw_back_button(self):
       
       back_button_width = 200
       back_button_height = 50
       back_button_rect = pygame.Rect(WIDTH // 2 - back_button_width // 2, HEIGHT - 100, back_button_width, back_button_height)

       # Dessiner le bouton
       pygame.draw.rect(self.screen, WHITE, back_button_rect)  
       back_button_font = pygame.font.Font(None, 40)
       back_button_text = back_button_font.render("Retour", True, BLACK ) 
       self.screen.blit(back_button_text, (back_button_rect.centerx - back_button_text.get_width() // 2, back_button_rect.centery - back_button_text.get_height() // 2))

       return back_button_rect
    



    # Display and Map
    def read_map_from_csv(self, filename):
        """
        input :
            filename : string
                the path of the csv containing the map matrix
                    0 : grass
                    1 : murs 
                    2 : magma -> -3 Shogun | -4 Assasin | -5 Sorceress (point de vie)
                    3 : water -> -4 Shogun | -1 Assasin | -2 Sorceress (endurence)
                    4 : mud   -> -5 Shogun | -2 Assasin | -3 Sorceress (endurence)
                    5 : healing -> +5 Shogun | +5 Assasin | +5 Sorceress (point de vie)
                    6 : snow -> -3 Shogun | -2 Assasin | -1 Sorceress (endurence)
                    7 : Bush -> -0 Shogun | -1 Assasin | -1 Sorceress (point de vie)
        
        """

        # Charger la map du csv
        map = []
        with open(os.path.join(filename), mode='r') as data: # mode = 'r' :read 
            data = csv.reader(data, delimiter=',') # une autre variable s'appelle 'data' qui prend data comme sa fonction / csv.reader : est utilisée pour lire des fichiers au format CSV (Comma-Separated Values, ou valeurs séparées par des virgules) et convertir leurs contenus en lignes faciles à manipuler.
            for row in data:
                map.append(list(row))
        
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == '0':  # Si la valeur est '0', c'est un type de terrain
                    self.grass.append((x, y))
                if cell == '1':  # Si la valeur est '1', c'est un mur
                    self.walls.append((x, y))
                if cell == '2':  # Si la valeur est '2', c'est un magma
                    self.magmas.append((x, y))
                if cell == '3':  # Si la valeur est '3', c'est un lilypad
                    self.water.append((x, y))
                if cell == '4':  # Si la valeur est '4', c'est un mud
                    self.muds.append((x, y))
                if cell == '5':  # Si la valeur est '5', c'est une case healing
                    self.healing.append((x, y))
                if cell == '6':   # Si la valeur est '6', c'est un type de terrain 
                    self.snow.append((x,y))
                if cell == '7':   # Si la valeur est '7', c'est un buisson
                    self.bush.append((x,y))
                



    # verifie si c'est un mur
    def is_wall(self, x, y):
        """
        Vérifie si une cellule est un mur.
        """
        return (x, y) in self.walls




    # determiner les blocks visibles :
    def get_visible_cells(self, unit):

        def est_visible(x1, y1, x2, y2):
            # tester si le aucun obstacle est entre le block 2 et 1 grace a l'algorithme de Bresenham
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                # If the current cell is a wall, the line of sight is blocked
                if (x1, y1) in self.walls:
                    return False

                # If we've reached the target cell, the line of sight is clear
                if (x1, y1) == (x2, y2):
                    return True

                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        # retourne un set de tuples representant les cellules visibles (x, y)
        # we use set() to avoid overlap, cheking if a cell is in the set is also very fast (complexity of O(1))
        # cells must store immutable objects, thats why we chose to use tuples for a cell coordinate

        
        max_range = 6
        visible_cells = set()
        
        for dx in range(-max_range, max_range + 1):
            for dy in range(-max_range, max_range + 1):
                x, y = unit.x + dx, unit.y + dy

                # Skip cells outside the grid
                if not (0 <= x < GRID_SIZE_WIDTH and 0 <= y < GRID_SIZE_HEIGHT):
                    continue

                # tester si aucun obstacle est entre le block et l'unité
                if est_visible(unit.x, unit.y, x, y):
                    visible_cells.add((x, y))

        return visible_cells




    # ecran de choix de la carte
    def choose_map(self):
    
        # Charger l'image de fond
        splash_menu_image_1 = pygame.image.load("data/splash_images/pic_avatar.png") 
        splash_menu_image_1 = pygame.transform.scale(splash_menu_image_1, (WIDTH,WINDOW_HEIGHT))
        
        # affiche l'image de fond
        self.screen.blit(splash_menu_image_1, (0,0))

        # Charger la musique de fond
        # pygame.mixer.music.load("data/musics/cinematic_music.mp3")
        # pygame.mixer.music.play(loops=0) # joue en boucle

        # rafraichir l'écran
        pygame.display.flip()

        # Charger les cartes 
        map_previews = {
            name: {
             "image": pygame.image.load(info["photo"]).convert_alpha(),
             "fichier": info["fichier"],
        }
        for name, info in self.maps.items()
        }

        # Redimensionner les map pour qu'elles tiennent dans la fenêtre
        card_width, card_height = 180, 140
        positions = {
           "map1": pygame.Rect(WIDTH // 3 - card_width // 2, HEIGHT // 2 - card_height // 2, card_width, card_height),
           "map2": pygame.Rect(2 * WIDTH // 3 - card_width // 2, HEIGHT // 2 - card_height // 2, card_width, card_height),
        }

        for name, info in map_previews.items():
            map_previews[name]["image"] = pygame.transform.scale(info["image"], (card_width, card_height))

        # Texte pour le titre
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Choose Your Map:", True, WHITE)

        # boucle pour le choix de la carte
        while True:
           
            # Afficher le titre
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 8))

            # Afficher les cartes avec leurs noms
            for name, rect in positions.items():
                # Dessiner la carte 
                self.screen.blit(map_previews[name]["image"], rect.topleft)
                # Ajouter une bordure blanche autour
                pygame.draw.rect(self.screen, WHITE, rect, 3)
                # Dessiner le nom de la carte
                map_name_font = pygame.font.Font(None, 40)
                map_name_text = map_name_font.render(self.maps[name]["name"], True, WHITE)
                self.screen.blit( map_name_text,(rect.centerx - map_name_text.get_width() // 2, rect.bottom + 10))
               
            back_button_rect = self.draw_back_button()
            # Rafraîchir l'écran
            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    mouse_pos = event.pos
                    for name, rect in positions.items():
                        if rect.collidepoint(mouse_pos):
                            self.selected_map_file = self.maps[name]["fichier"]
                            return self.selected_map_file
                    
                    if back_button_rect.collidepoint(mouse_pos):
                        # Action lorsque le bouton Retour est cliqué (par exemple, retourner au menu principal)
                    
                        pygame.event.clear()  # Nettoyer les événements restants
                        self.lunch_game()
                        return None
          
          


    # Affichage de la carte et les unites pendent le jeux 
    def draw_map_units(self, team="player 1", ShowGrille=False):
        """Affiche le jeu."""

        if len(self.selected_map_file)==0:
            print("No map selected!")
            return

        # Pour effacer ce qui étai affiché precedement
        rect_to_fill = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.screen.fill(BLACK, rect_to_fill)

        # Affiche les blocs : "GRASS"
        for grass in self.grass:    
            x = grass[0] * CELL_SIZE
            y = grass[1] * CELL_SIZE
            self.screen.blit(self.GRASS, (x, y))

        # Affiche les blocs : "WALL"
        for wall in self.walls:
            x = wall[0] * CELL_SIZE
            y = wall[1] * CELL_SIZE
            self.screen.blit(self.WALL, (x, y))

        # Affiche les blocs : "MAGMA"
        for magma in self.magmas:
            x = magma[0] * CELL_SIZE
            y = magma[1] * CELL_SIZE
            self.screen.blit(self.MAGMA, (x, y))

        # Affiche les blocs : "LILYPAD"
        for water in self.water:
            x = water[0] * CELL_SIZE
            y = water[1] * CELL_SIZE
            self.screen.blit(self.WATER, (x, y))

        # Affiche les blocs : "MUD"
        for mud in self.muds:
            x = mud[0] * CELL_SIZE
            y = mud[1] * CELL_SIZE
            self.screen.blit(self.MUD, (x, y))

        # Affiche les blocs : "HEALING"
        for healing in self.healing:
            x = healing[0] * CELL_SIZE
            y = healing[1] * CELL_SIZE
            self.screen.blit(self.APPLE_TREE, (x, y))        

        # Affiche les blocs : "SNOW"
        for grasse_ocr in self.snow:
            x = grasse_ocr[0] * CELL_SIZE
            y = grasse_ocr[1] * CELL_SIZE
            self.screen.blit(self.SNOW, (x, y))     

        # Affiche les blocs : "BUSH"
        for bush in self.bush:
            x = bush[0] * CELL_SIZE
            y = bush[1] * CELL_SIZE
            self.screen.blit(self.BUSH, (x, y))     

        # Affiche les contours de la grille (optionnel si vous voulez une bordure blanche)
        if ShowGrille == True :
            for x in range(0, WIDTH, CELL_SIZE):
                for y in range(0, HEIGHT, CELL_SIZE):
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Calculer les cellules visibles pour les unités de l'équipe
        all_visible_cells = set()
        if team == "player 1":
            units = self.player_units
        elif team == "player 2":
            units = self.player2_units
        elif team == "enemy":
            units = self.enemy_units

        for unit in units:
            all_visible_cells.update(self.get_visible_cells(unit))

        # Afficher les unités
        for unit in self.player_units + self.enemy_units + self.player2_units:
            if (((unit.x, unit.y) in all_visible_cells) and ((unit.x, unit.y) not in self.bush)) or unit.team == team:
                unit.draw(self.screen)

        # Ajouter un overlay gris pour les zones non visibles
        for x in range(GRID_SIZE_WIDTH):
            for y in range(GRID_SIZE_HEIGHT):
                if (x, y) not in all_visible_cells:
                    overlay_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    # Dessiner une couleur grise transparente (alpha blending)
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))  # Surface temporaire
                    s.set_alpha(100)  # Niveau de transparence (0-255)
                    s.fill((50, 50, 50))  # Couleur grise
                    self.screen.blit(s, overlay_rect.topleft)

        # Rafraîchit l'écran
        pygame.display.flip()




    # Main menu
    def Main_menu(self, GameName):
        """
        Affiche le menu principale
        Output : 
            - str : "PvE" pour jouer contre l'ordinateur, "PVP" pour jouer contre un autre utilisateur
        """
        
        # Charger l'image de fond
        splash_menu_image = pygame.image.load("data/splash_images/menu_image.png")
        splash_menu_image = pygame.transform.scale(splash_menu_image, (WIDTH,WINDOW_HEIGHT))

        # Charger la musique de fond
        pygame.mixer.music.load("data/musics/Dark Souls - A moment's peace.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) # joue en boucle

        # Texte du titre
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render(GameName, True, WHITE)

        # Buttons 
        button_font = pygame.font.Font(None, 36)
        buttons = {
            "Solo Deathmatch" : {"rect" : pygame.Rect(WIDTH//3, HEIGHT//2, WIDTH//3, 50), "mode": "PvE"},
            "Multiplayer Deathmatch" : {"rect" : pygame.Rect(WIDTH//3, HEIGHT//2+70, WIDTH//3, 50), "mode" : "PvP"}
        }

        while True :
            # affiche l'image de fond
            self.screen.blit(splash_menu_image, (0,0))

            # affiche le titre
            self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))

            # affiche les bouttons
            for text, info in buttons.items():
                pygame.draw.rect(self.screen, WHITE, info["rect"], border_radius=5)
                button_text = button_font.render(text, True, BLACK)
                self.screen.blit(button_text, (info["rect"].x + (info["rect"].width-button_text.get_width())//2,
                                               info["rect"].y + (info["rect"].height-button_text.get_height())//2))
                
            # rafraichir l'écran
            pygame.display.flip()

            # si la souris a été cliqué
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1) : # clic gauche
                    mouse_pos = event.pos
                    for info in buttons.values():
                        if info["rect"].collidepoint(mouse_pos):
                            # pygame.mixer.music.stop() # Arréte la musique de fond
                            self.GameMode = info["mode"]
                            return info["mode"]

              


    # Character choice menu
    def Characters_choice(self, player, NumberOfCharacters):
        """
        input :
            - player : string : "player 1" or "player 2" or "enemy"
        output : 
            append chosen list 
        """

        # Charger l'image de fond
        splash_menu_image_1 = pygame.image.load("data/splash_images/pic_avatar.png") 
        splash_menu_image_1 = pygame.transform.scale(splash_menu_image_1, (WIDTH,WINDOW_HEIGHT))

        # affiche l'image de fond
        self.screen.blit(splash_menu_image_1, (0,0))

        # Charger la musique de fond
        # pygame.mixer.music.load("data/musics/cinematic_music.mp3")
        # pygame.mixer.music.play(loops=0) # joue en boucle

        # rafraichir l'écran
        pygame.display.flip()

        selected_units = []
        while len(selected_units) < NumberOfCharacters:

            # Afficher l'instruction de choix :
            font = pygame.font.Font(None, 60)
            text = font.render(f"{player} : Choose your characters ({len(selected_units) + 1}/{NumberOfCharacters})", True, ANOTHER_GREY)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4))

            # Affiche les personnages disponibles :
            for key in Personnages:
                Personnages[key].choiceButton_draw(self.screen)
           
            # update screen :
            pygame.display.flip()

            # Gestion des evennements :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for key in Personnages:
                        if Personnages[key].button.collidepoint(mouse_pos):
                            selected_units.append(copy.copy(Personnages[key]))

        
        if player == "player 1":
            self.player_units = selected_units
            # position initiale des personnages :
            for i in range(len(self.player_units)):
                self.player_units[i].team = "player 1"
                self.player_units[i].x = 0
                self.player_units[i].y = 2 + i

        elif player == "player 2":
            self.player2_units = selected_units
            # position initiale des personnages :
            for i in range(len(self.player2_units)):
                self.player2_units[i].team = "player 2"
                self.player2_units[i].x = GRID_SIZE_WIDTH - 1
                self.player2_units[i].y = GRID_SIZE_HEIGHT - 3 - i

        elif player == "enemy" :
            self.enemy_units = selected_units
            # position initiale des personnages :
            for i in range(len(self.enemy_units)):
                self.enemy_units[i].team = "enemy"
                self.enemy_units[i].x = GRID_SIZE_WIDTH - 1
                self.enemy_units[i].y = GRID_SIZE_HEIGHT - 3 - i

        return selected_units

      
        

    def play_game_music(self):
        # Lancer la musique de jeu
        pygame.mixer.music.load("data/musics/The Witcher 3 - The Hunt Begins.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1) # joue en boucle
        return                  

    


    def draw_info_panel(self, team=None, unit=None, mode=None):

        # afficher l'image de fond 
        self.screen.blit(self.info_panel_background_image, (0, HEIGHT))

        # initialiser le rectangle de la bordure
        info_panel_rect = pygame.Rect(0, HEIGHT, WIDTH, INFO_PANEL_HEIGHT)

        # Determine border color based on the team
        if team == "player 1":
            border_color = BLUE
        elif team == "player 2":
            border_color = GREEN
        elif team == "enemy":
            border_color = RED
        else:
            border_color = WHITE  # Default color

        # Draw border around the panel
        pygame.draw.rect(self.screen, border_color, info_panel_rect, 4)

        # Font for text
        font = pygame.font.Font(None, 20)  

        # Draw columns
        column_width = WIDTH // 3

        # --- First Column: Unit Info ---
        if unit:
            # Display Unit Picture
            if unit.texture:
                profile_picture_x = 20
                profile_picture_y = HEIGHT + 20
                profile_picture_width = 60
                profile_picture__height = 60

                picture_rect = pygame.Rect(profile_picture_x, profile_picture_y, profile_picture_width, profile_picture__height)
                self.screen.blit(pygame.transform.scale(unit.raw_texture, (profile_picture_width, profile_picture__height)), (profile_picture_x, profile_picture_y))
                pygame.draw.rect(self.screen, border_color, picture_rect, 2)

            # Display Name Below Picture
            name_text = font.render(unit.name, True, WHITE)
            self.screen.blit(name_text, (profile_picture_x + (profile_picture_width - name_text.get_width()) // 2, profile_picture_y + profile_picture__height + 5))

            # Display Health Bar
            health_ratio = unit.health / unit.max_health
            health_bar_width = 200
            health_bar_x = profile_picture_x + profile_picture_width + 20
            health_bar_y = HEIGHT + 20

            health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, 10)
            pygame.draw.rect(self.screen, GREY, health_bar_rect)  # Background bar
            pygame.draw.rect(self.screen, RED, (health_bar_x, health_bar_y, int(health_ratio * health_bar_width), 10))  # Health bar

            health_text = font.render(f"HP: {unit.health}/{unit.max_health}", True, WHITE)
            self.screen.blit(health_text, (health_bar_x, health_bar_y + 15))

            # Display Endurance Bar
            endurance_ratio = unit.endurence / unit.endurence_max
            endurence_bar_width = health_bar_width
            endurence_bar_x = health_bar_x
            endurence_bar_y = health_bar_y + 35

            endurance_bar_rect = pygame.Rect(endurence_bar_x, endurence_bar_y, endurence_bar_width, 10)
            pygame.draw.rect(self.screen, GREY, endurance_bar_rect)  # Background bar
            pygame.draw.rect(self.screen, GREEN, (endurence_bar_x, endurence_bar_y, int(endurance_ratio * health_bar_width), 10))  # Endurance bar

            endurance_text = font.render(f"Endurance: {unit.endurence}/{unit.endurence_max}", True, WHITE)
            self.screen.blit(endurance_text, (endurence_bar_x, endurence_bar_y + 15))

        # --- Second Column: Skills ---
        if unit and unit.skills:
            for i, skill in enumerate(unit.skills[:3]):
                
                # Skill Icon Rectangle
                skill_picture_width = 50
                skill_x = column_width + 60 + (i * (skill_picture_width + 60))  # Position squares with spacing
                skill_y = HEIGHT + 20
                skill_rect = pygame.Rect(skill_x, skill_y, skill_picture_width, skill_picture_width)

                # Display Skill Icon
                if skill.skill_logo:
                    skill_icon = pygame.transform.scale(skill.skill_logo, (skill_picture_width, skill_picture_width))
                    self.screen.blit(skill_icon, (skill_x, skill_y))

                pygame.draw.rect(self.screen, WHITE, skill_rect, 2)  # Border for skill icon

                # Display Skill Number (1, 2, 3)
                number_font = pygame.font.Font(None, 20)
                number_text = number_font.render(str(i + 1), True, WHITE)
                self.screen.blit(number_text, (skill_x + 5, skill_y + 5))

                # Display Skill Name Below Icon
                skill_name_text = font.render(skill.name, True, WHITE)
                self.screen.blit(skill_name_text, (skill_x + (skill_picture_width - skill_name_text.get_width()) // 2, skill_y + skill_picture_width + 5))

        # --- Third Column: Instructions ---
        instructions = []

        if unit and (mode == "moving"):
            instructions = [
                "Move : Arrow keys",
                "Skill 1, 2, 3 : Key 1, 2, 3",
                "Skip Turn : Space",
                "Cancel Skill : X"
            ]

        elif unit and (mode == "skill 1"):
            instructions = unit.skills[0].instructions

        elif unit and (mode == "skill 2"):
            instructions = unit.skills[1].instructions

        elif unit and (mode == "skill 3"):
            instructions = unit.skills[2].instructions

        else:
            instructions = [
                "Move : Arrow keys",
                "Skill 1, 2, 3 : Key 1, 2, 3",
                "Skip Turn : Space",
                "Cancel Skill : X"
            ]

        instruction_y = HEIGHT + 10
        for instruction in instructions:
            instruction_text = font.render(instruction, True, WHITE)
            self.screen.blit(instruction_text, (2 * column_width + 10, instruction_y))
            instruction_y += 20

        # Draw Borders Between Columns
        pygame.draw.line(self.screen, border_color, (column_width, HEIGHT), (column_width, HEIGHT + INFO_PANEL_HEIGHT), 2)
        pygame.draw.line(self.screen, border_color, (2 * column_width, HEIGHT), (2 * column_width, HEIGHT + INFO_PANEL_HEIGHT), 2)


    def reset_endurance(self):
        """Réinitialise l'endurance de toutes les unités (alliées et ennemies)."""
        for unit in self.player_units + self.player2_units + self.enemy_units:
            unit.endurence_max = unit.endurence_max_init  # Réinitialisation à la valeur initiale
        print("Endurance réinitialisée pour tous les personnages !")


    # Tour des joueurs 1 et 2
    def handle_player_turn(self, team):
        """
            input : 
                - team : "player 1" ou "player 2"
        
        """
        if team == "player 1" :
            for selected_unit in self.player_units:

                # Tant que l'unité n'a pas terminé son tour
                has_acted = False
                selected_unit.is_selected = True
                selected_unit.endurence = selected_unit.endurence_max
                self.draw_map_units(team)
                self.draw_info_panel(team, selected_unit, "moving")
                pygame.display.flip() 
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
                                if selected_unit.endurence > 0:
                                    dx = -1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_RIGHT:
                                if selected_unit.endurence > 0:
                                    dx = 1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_UP:
                                if selected_unit.endurence > 0:
                                    dy = -1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_DOWN:
                                if selected_unit.endurence > 0:
                                    dy = 1
                                    selected_unit.endurence = selected_unit.endurence - 1

                            selected_unit.move(dx, dy, self)
                            self.draw_map_units(team)
                            self.draw_info_panel(team, selected_unit, "moving")
                            pygame.display.flip()

                            # Use skills : skill 1, 2 or 3
                            if event.key == pygame.K_1:
                                if len(selected_unit.skills) > 0:
                                    self.draw_info_panel(team, selected_unit, "skill 1")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[0]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)   
                                else:
                                    print(f"{selected_unit.name} has no skill 1.")
                            elif event.key == pygame.K_2:
                                if len(selected_unit.skills) > 1:
                                    self.draw_info_panel(team, selected_unit, "skill 2")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[1]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)
                                    pygame.display.flip()

                                else:
                                    print(f"{selected_unit.name} has no skill 2.")
                            elif event.key == pygame.K_3:
                                if len(selected_unit.skills) > 2:
                                    self.draw_info_panel(team, selected_unit, "skill 3")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[2]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)
                                    pygame.display.flip()
                                else:
                                    print(f"{selected_unit.name} has no skill 3.")

                            # Attaque (touche espace) met fin au tour
                            if event.key == pygame.K_SPACE:
                                for enemy in self.enemy_units:
                                    if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                        selected_unit.attack(enemy)
                                        if enemy.health <= 0:
                                            self.enemy_units.remove(enemy)

                                has_acted = True
                                selected_unit.is_selected = False

            if self.GameMode == "PvE" :
                if len(self.enemy_units) == 0 :
                    self.game_end("enemy")
            elif self.GameMode == "PvP" :
                if len(self.player2_units) == 0 :
                    self.game_end("player 2")

        elif team == "player 2" :
            for selected_unit in self.player2_units:

                # Tant que l'unité n'a pas terminé son tour
                has_acted = False
                selected_unit.is_selected = True
                selected_unit.endurence = selected_unit.endurence_max
                self.draw_map_units(team)
                self.draw_info_panel(team, selected_unit, "moving")
                pygame.display.flip()

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
                                if selected_unit.endurence > 0:
                                    dx = -1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_RIGHT:
                                if selected_unit.endurence > 0:
                                    dx = 1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_UP:
                                if selected_unit.endurence > 0:
                                    dy = -1
                                    selected_unit.endurence = selected_unit.endurence - 1
                            elif event.key == pygame.K_DOWN:
                                if selected_unit.endurence > 0:
                                    dy = 1
                                    selected_unit.endurence = selected_unit.endurence - 1

                            selected_unit.move(dx, dy, self)
                            self.draw_map_units(team)
                            self.draw_info_panel(team, selected_unit, "moving")
                            pygame.display.flip()

                            # Use skills : skill 1, 2 or 3
                            if event.key == pygame.K_1:
                                if len(selected_unit.skills) > 0:
                                    self.draw_info_panel(team, selected_unit, "skill 1")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[0]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)
                                    pygame.display.flip()
                                else:
                                    print(f"{selected_unit.name} has no skill 1.")
                            elif event.key == pygame.K_2:
                                if len(selected_unit.skills) > 1:
                                    self.draw_info_panel(team, selected_unit, "skill 2")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[1]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)
                                    pygame.display.flip()
                                else:
                                    print(f"{selected_unit.name} has no skill 2.")
                            elif event.key == pygame.K_3:
                                if len(selected_unit.skills) > 2:
                                    self.draw_info_panel(team, selected_unit, "skill 3")
                                    pygame.display.flip()
                                    skill = selected_unit.skills[2]
                                    skill.use_skill(selected_unit, self)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                    self.draw_map_units(team)
                                    pygame.display.flip()
                                else:
                                    print(f"{selected_unit.name} has no skill 3.")

                            # Attaque (touche espace) met fin au tour
                            if event.key == pygame.K_SPACE:
                                for enemy in self.enemy_units:
                                    if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                        selected_unit.attack(enemy)
                                        if enemy.health <= 0:
                                            self.enemy_units.remove(enemy)

                                has_acted = True
                                selected_unit.is_selected = False

            if self.GameMode == "PvE" :
                if len(self.enemy_units) == 0 :
                    self.game_end("enemy")
            elif self.GameMode == "PvP" :
                if len(self.player2_units) == 0 :
                    self.game_end("player 2")

        # Incrémenter le compteur de tours **à la fin du tour**
        self.turn_counter += 1
        print(f"Tour {self.turn_counter} terminé.")

        # Réinitialisation de l’endurance après 3 tours
        if self.turn_counter >= 5:
            self.reset_endurance()
            self.turn_counter = 0  # Réinitialiser le compteur après réinitialisation
        



    # IA de enemy
    def handle_enemy_turn(self):

        # tester si tous les adversaires sont morts
        if len(self.player_units) == 0 :
            self.game_end("player 1")

        # faire le tour de chaque unité de enemy
        for enemy in self.enemy_units:
            
            # attente pour rendre le tour des ennemies plus realistique
            pygame.time.delay(500)

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy, self)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

            # Met à jour le panneau d'information avec les détails de l'ennemi
            self.draw_map_units("enemy")
            self.draw_info_panel("enemy", enemy)
            pygame.display.flip()

            # attente pour rendre le tour des ennemies plus realistique
            pygame.time.delay(100) 

        # tester si tous les adversaires sont morts
        if len(self.player_units) == 0 :
            self.game_end("player 1")






    def enemy_AI_turn(self):
                
                # tester si tous les adversaires sont morts
                if len(self.player_units) == 0 :
                    self.game_end("player 1")

                # tour de chaque unité de enemy
                for enemy in self.enemy_units:

                    # attente pour rendre le tour des ennemies plus realistique
                    pygame.time.delay(500)

                    # Movement decision
                    best_move = self.AI_find_best_move(enemy)
                    if best_move:
                        enemy.move(best_move[0], best_move[1], self)

                    # Skill usage
                    best_skill = self.AI_evaluate_skills(enemy)
                    if best_skill:
                        best_skill.use_skill(enemy, self)

                    # Attack decision if no skill is ai compatible
                    target = self.AI_find_best_target(enemy)
                    if target:
                        enemy.attack(target)

                    # tester si tous les adversaires sont morts
                    if len(self.player_units) == 0 :
                        self.game_end("player 1")

                    # Update the game state after enemy's action
                    self.draw_map_units("enemy")
                    pygame.display.flip()

                    # attente pour rendre le tour des ennemies plus realistique
                    pygame.time.delay(500)




    def AI_find_best_move(self, enemy):
        # Evaluate potential moves and return the best one
        best_move = None
        best_score = -500

        for dx in range(-enemy.endurence_max, enemy.endurence_max + 1):  # Example range, adjust for movement rules
            for dy in range(-enemy.endurence_max, enemy.endurence_max + 1):
                new_x = enemy.x + dx
                new_y = enemy.y + dy
                if not self.is_wall(new_x, new_y) and (0 <= new_x < GRID_SIZE_WIDTH and 0 <= new_y < GRID_SIZE_HEIGHT):
                    score = self.AI_evaluate_position(new_x, new_y, enemy)
                    if score > best_score:
                        best_score = score
                        best_move = (dx, dy)

        # alterer best_move legerement de facon aleatoire
        potential_alteration = [-2, -1, 0, 1, 2]
        probabilities = [0.1, 0.1, 0.6, 0.1, 0.1]
        ax = random.choices(potential_alteration, weights=probabilities, k=1)[0]
        ay = random.choices(potential_alteration, weights=probabilities, k=1)[0]
        a_new_x = best_move[0] + ax
        a_new_y = best_move[0] + ay
        if not self.is_wall(a_new_x, a_new_y) and (0 <= a_new_x < GRID_SIZE_WIDTH and 0 <= a_new_y < GRID_SIZE_HEIGHT):
            best_move = (a_new_x, a_new_y)

        return best_move
    



    def AI_evaluate_position(self, x, y, unit):
            # Return a score based on strategic factors (e.g., proximity to player units, terrain)
            score = 0
            for player in self.player_units:
                distance = abs(player.x - x) + abs(player.y - y)
                score -= (distance * 2)  # Prefer closer positions
            if (x == player.x) and (x == player.x):
                score -= 500 # to avoid moving into player block
            if (x, y) in self.healing:
                score += 5  # Bonus for healing zones
            if (x, y) in self.magmas:
                score -= 10  # Penalty for harmful terrain
            return score
    



    def AI_find_best_target(self, enemy):
        # Return the best target for the given enemy
        best_target = None
        best_score = -500
        for player in self.player_units:
            distance = abs(player.x - enemy.x) + abs(player.y - enemy.y)
            if distance <= 10:
                score = player.health * -1  # Prefer low-health targets
                if score > best_score:
                    best_score = score
                    best_target = player
        return best_target





    def AI_evaluate_skills(self, enemy):
        # Evaluate the effectiveness of each skill and return the best one
        best_skill = None
        best_effectiveness = -100
        for skill in enemy.skills:
            effectiveness = self.AI_simulate_skill_use(skill, enemy)
            if effectiveness > best_effectiveness:
                best_effectiveness = effectiveness
                best_skill = skill
        
        # si best_effectiveness == -100 alors aucun skill n'est compatible avec l'IA
        if best_effectiveness == -100 :
            return None

        return best_skill





    def AI_simulate_skill_use(self, skill, enemy):
        # Simulate the skill's effect and return an effectiveness score
        effectiveness = 0

        # test if skill is AI compatible
        if skill.AI_compatible == False :
            effectiveness = -100
            return effectiveness

        # test effectiveness for all player units
        for player in self.player_units:
            if skill.range >= abs(player.x - enemy.x) + abs(player.y - enemy.y):
                effectiveness += skill.damage  # Adjust based on skill properties
        return effectiveness




    
    # ecran de fin de jeu
    def game_end(self, loser):
        """
        Displays the end game screen with the loser's message.

        Parameters:
        loser (str): The team that survived or was decimated.
        """
        # Stop background music
        pygame.mixer.music.stop()

        # Set the end game message
        if loser == "player 1":
            title = "GAME OVER"
            message = "Player 1 was Decimated..."
        elif loser == "player 2":
            title = "GAME OVER"
            message = "Player 1 Defeated player 2 !"
        elif loser == "enemy":
            # Font settings
            title_font = pygame.font.Font(None, 72)
            message_font = pygame.font.Font(None, 36)

            # Button settings
            button_font = pygame.font.Font(None, 36)
            button_text = "Go to Title Screen"
            button_rect = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 100, WIDTH // 3, 50)

            # Charger l'image de fond
            splash_menu_image_1 = pygame.image.load("data/splash_images/you_win.png") 
            splash_menu_image_1 = pygame.transform.scale(splash_menu_image_1, (WIDTH,HEIGHT))

            # affiche l'image de fond
            self.screen.blit(splash_menu_image_1, (0,0))

            # Charger la musique de fond
            pygame.mixer.music.load("data/musics/end_victory.mp3")
            pygame.mixer.music.play(loops=0) # joue en boucle

            # rafraichir l'écran
            pygame.display.flip()
            title = "GAME WIN"
            message = "Player 1 Survived !"


        # Font settings
        title_font = pygame.font.Font(None, 72)
        message_font = pygame.font.Font(None, 36)
        # Button settings
        button_font = pygame.font.Font(None, 36)
        button_text = "Go to Title Screen"
        button_rect = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 100, WIDTH // 3, 50)

        while True:

            # Render the end game message
            title_text = title_font.render(title, True, WHITE)
            message_text = message_font.render(message, True, WHITE)

            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
            self.screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - 50))

            # Draw the "Go to Title Screen" button
            pygame.draw.rect(self.screen, ANOTHER_BLUE, button_rect, border_radius=5)
            button_text_render = button_font.render(button_text, True, WHITE)
            self.screen.blit(button_text_render, (
                button_rect.x + (button_rect.width - button_text_render.get_width()) // 2,
                button_rect.y + (button_rect.height - button_text_render.get_height()) // 2
            ))

            # Update the display
            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):
                        self.lunch_game()  # Go to title screen
                        return
                    



    # Pipeline complete du jeu
    def lunch_game(self):
        """
        Restarts the game by returning to the title screen.
        """
        # charger les textures et sons
        self.load_textures_sounds()

        # Clear the current game state
        self.player_units = []
        self.player2_units = []
        self.enemy_units = []
        self.selected_map_file = []

        # Afficher le menu principale
        MenuChoice = self.Main_menu(GAME_TITLE)

        # choix de la carte
        selected_map = self.choose_map()
        self.read_map_from_csv(selected_map)

        if selected_map is None:
           return self.lunch_game()
        
        # choix des personnages
        if MenuChoice == "PvE":
            self.Characters_choice("player 1", CHARACTER_PER_TEAM)
            self.Characters_choice("enemy", CHARACTER_PER_TEAM)
        elif MenuChoice == "PvP":
            self.Characters_choice("player 1", CHARACTER_PER_TEAM)
            self.Characters_choice("player 2", CHARACTER_PER_TEAM)
        
        # lancer la musique
        self.play_game_music()

        # Lancer la game
        if MenuChoice == "PvE":
            while True:
                self.handle_player_turn("player 1")
                self.enemy_AI_turn()
                # self.handle_enemy_turn()
        elif MenuChoice == "PvP":
            while True:
                self.handle_player_turn("player 1")
                self.handle_player_turn("player 2")
                    
        


# main function
def main():

    

    # Instanciation du jeu
    game = Game(screen)

    # Lancer le jeu
    game.lunch_game()




if __name__ == "__main__":
    main()
