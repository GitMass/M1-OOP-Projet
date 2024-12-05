import pygame
import random
import copy

from unit import *
 
class Gamestate:
    CHARACTER_SELECTION = "character_selection"
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    GAME_OVER = "game_over"
    


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
        self.enemy_units =[]
        self.state=Gamestate.CHARACTER_SELECTION
        self.winner=None

        
    
    def Characters_choice(self,player):

        selected_units = self.player_units
        while len(selected_units) < CHARACTER_PER_TEAM:
            self.screen.fill(BLACK)

            # Afficher l'instruction de choix :
            font = pygame.font.Font(None, 36)
            text = font.render(f"{player}: Choose your characters ({len(selected_units) + 1}/{CHARACTER_PER_TEAM})", True, WHITE)
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
                            selected_units[-1].x = len(selected_units)-1
                            selected_units[-1].y = 0
        return selected_units
    
    def Characters_choice_enemy(self,enemy):
        selected_units=self.enemy_units


        while len(selected_units) < CHARACTER_PER_TEAM:
            self.screen.fill(BLACK)

            # Afficher l'instruction de choix :
            font = pygame.font.Font(None, 36)
            text = font.render(f"{enemy}: Choose your characters ({len(selected_units) + 1}/{CHARACTER_PER_TEAM})", True, WHITE)
            self.screen.blit(text, (int(WIDTH/5), 50))

            # Affiche les personnages disponibles :
            for key in Enemy:
                Enemy[key].choiceButton_draw(self.screen)
            
            # update screen :
            pygame.display.flip()

            # Gestion des evennements :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for key in Enemy:
                        if Enemy [key].button.collidepoint(mouse_pos):
                            selected_units.append(copy.copy(Enemy[key]))
                            selected_units[-1].x = len(selected_units)-1
                            selected_units[-1].y = 6
        return selected_units
 
    """def Characters_choice_enemy(self):
        for i in range(CHARACTER_PER_TEAM):
           enemy_type=random.choice(list(Enemy.values())) 
           self.enemy_units.append(enemy_type)"""

 
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
        #for enemy_unit in self.enemy_units:
          # enemy_unit.is_selected = True
          # self.flip_display()

        if not self.player_units:
            self.state = Gamestate.GAME_OVER
            self.winner = "Enemy"
            return  # Arrête le tour si aucun joueur rest 
    
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
         

        # Fin du tour de l'unité ennemie
           # enemy_unit.is_selected = False
        self.flip_display()

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



    #Gestion de fin de jeu
    def game_over(self):
        
        surface=pygame.Surface((300, 200))
        surface.fill(WHITE )
        font=pygame.font.Font(None, 60)
        message=f"{self.winner} Wins!"
        text=font.render(message, True, (WHITE))
         


        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(text, text_rect)
       
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                exit()
             #elif event.type == pygame.KEYDOWN:
             #   if event.key == pygame.K_q:
              #     pygame.quit()
               #    exit()
               # elif event.key == pygame.K_r:
               #     return "restart"  # Renvoie "restart" pour relancer le jeu""""""""
    
    
    def restart_game(self):
        
        self.state = Gamestate.CHARACTER_SELECTION
        self.player_units = []
        self.enemy_units = []
        self.winner = None


    def handle_gamestate(self):
        if self.state == Gamestate.CHARACTER_SELECTION:
            # Gérer la sélection des personnages
            self.player_units = self.Characters_choice("Player")
            self.enemy_units = self.Characters_choice_enemy("Enemy")
            self.state = Gamestate.PLAYER_TURN

        elif self.state == Gamestate.PLAYER_TURN:
           self.handle_player_turn()
           if len(self.enemy_units)==0:
            self.winner="Player"
            self.state=Gamestate.GAME_OVER
           else:
            self.state = Gamestate.ENEMY_TURN

        elif self.state == Gamestate.ENEMY_TURN:
            self.handle_enemy_turn()
            if len( self.player_units)==0:
                self.winner = "Enemy"
                self.state = Gamestate.GAME_OVER
            else:
                self.state = Gamestate.PLAYER_TURN
               

       
        elif self.state == Gamestate.GAME_OVER:
           if self.game_over() == "restart":
              self.restart_game()
 

def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)
    game.player_units = game.Characters_choice("player")
    game.enemy_units=game.Characters_choice_enemy("enemy")
   


    



    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        game.handle_gamestate()


if __name__ == "__main__":
    main()
