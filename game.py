import pygame
import random
import copy

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

        self.player_units = []
        self.player2_units = []
        self.enemy_units = [Unit(6, 6, 8, 1, 2, 'enemy', None, 5, 5),
                            Unit(7, 6, 8, 1, 2, 'enemy', None, 7, 5)]
    
    def Characters_choice(self, player, NumberOfCharacters):
        """
        input :
            - player : string : "player 1" or "player 2" or "computer"
        output : 
            append chosen list 
        """

        selected_units = []
        while len(selected_units) < NumberOfCharacters:
            self.screen.fill(BLACK)

            # Afficher l'instruction de choix :
            font = pygame.font.Font(None, 36)
            text = font.render(f"{player}: Choose your characters ({len(selected_units) + 1}/{NumberOfCharacters})", True, WHITE)
            self.screen.blit(text, (int(WIDTH/5), 50))

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
                self.player_units[i].x = 0
                self.player_units[i].y = 2 + i

        elif player == "player 2":
            self.player2_units = selected_units
            # position initiale des personnages :
            for i in range(len(self.player2_units)):
                self.player2_units[i].x = GRID_SIZE_WIDTH - 1
                self.player2_units[i].y = GRID_SIZE_HEIGHT - 3 - i
        else :
            self.enemy_units = selected_units
            # position initiale des personnages :
            for i in range(len(self.enemy_units)):
                self.enemy_units[i].x = GRID_SIZE_WIDTH - 1
                self.enemy_units[i].y = GRID_SIZE_HEIGHT - 3 - i
        
        return selected_units


    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            endurence = selected_unit.endurence_max
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
                            if endurence > 0:
                                dx = -1
                                endurence = endurence - 1
                        elif event.key == pygame.K_RIGHT:
                            if endurence > 0:
                                dx = 1
                                endurence = endurence - 1
                        elif event.key == pygame.K_UP:
                            if endurence > 0:
                                dy = -1
                                endurence = endurence - 1
                        elif event.key == pygame.K_DOWN:
                            if endurence > 0:
                                dy = 1
                                endurence = endurence - 1

                        selected_unit.move(dx, dy)
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

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()


    def Main_menu(self, GameName):
        """
        Affiche le menu principale
        Output : 
            - str : "1vC" pour jouer contre l'ordinateur, "1v1" pour jouer contre un autre utilisateur
        """

        # Charger l'image de fond
        splash_menu_image = pygame.image.load("data\Screen_MainMenu.png")
        splash_menu_image = pygame.transform.scale(splash_menu_image, (WIDTH,HEIGHT))

        # Charger la musique de fond
        pygame.mixer.music.load("data\Ost_MainMenu.mp3")
        pygame.mixer.music.play(-1) # joue en boucle

        # Texte du titre
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render(GameName, True, WHITE)

        # Buttons 
        button_font = pygame.font.Font(None, 36)
        buttons = {
            "Solo Deathmatch" : {"rect" : pygame.Rect(WIDTH//3, HEIGHT//2, WIDTH//3, 50), "mode": "1vC"},
            "Multiplayer Deathmatch" : {"rect" : pygame.Rect(WIDTH//3, HEIGHT//2+70, WIDTH//3, 50), "mode" : "1v1"}
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
                            pygame.mixer.music.stop() # Arréte la musique de fond
                            return info["mode"]
                    


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    # Instanciation du jeu
    game = Game(screen)

    # Menu principale
    MenuChoice = game.Main_menu(GAME_TITLE)

    # Choix des caractères
    if MenuChoice == "1vC" :
        game.Characters_choice("player 1", CHARACTER_PER_TEAM)
        game.Characters_choice("computer", CHARACTER_PER_TEAM)
    elif MenuChoice == "1v1" :
        game.Characters_choice("player 1", CHARACTER_PER_TEAM)
        game.Characters_choice("player 2", CHARACTER_PER_TEAM)

    # Boucle principale du jeu
    if MenuChoice == "1vC" :
        while True:
            game.handle_player_turn()
            game.handle_enemy_turn()
    elif MenuChoice == "1v1" :
        while True:
            game.handle_player_turn()


if __name__ == "__main__":
    main()
