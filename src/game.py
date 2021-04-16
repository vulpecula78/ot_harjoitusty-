'''Game loop for Another Pong Clone Again'''
import pygame
from computer_ai import ComputerAi
from wait import Wait

class Game():
    def __init__(self, score, ball, bat1, bat2, clock, scr_width, scr_height):
        self.bat1 = bat1
        self.bat2 = bat2
        self.ball = ball
        self.score = score
        self.clock = clock
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.wait = Wait(scr_width, scr_height)

    def main(self, fps, game_type, all_sprites, background, screen):
        '''Game main loop'''
        running = True
        pvp = True
        player2 = 2
        p1_score = 0
        p2_score = 0
        self.wait.launch(0, self.ball)
        if game_type == "computer":
            computer = ComputerAi(self.ball, self.bat2, self.scr_width)
            player2 = 3
            pvp = False

        while running:
            self.clock.tick(fps)
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:            # pylint: disable=no-member
                    self.bat1.move_up()
                if keys[pygame.K_z]:            # pylint: disable=no-member
                    self.bat1.move_down()
                if pvp:
                    if keys[pygame.K_UP]:           # pylint: disable=no-member
                        self.bat2.move_up()
                    if keys[pygame.K_DOWN]:         # pylint: disable=no-member
                        self.bat2.move_down()
                if event.type == pygame.QUIT:   # pylint: disable=no-member
                    running = False

            if not pvp:
                computer.ai_player_move()

            self.wait.collision(self.bat1, self.bat2, self.ball)

            if self.ball.rect.x < -40:
                p2_score += 1
                #Player 2 wins if 11 pts
                if p2_score == 3:
                    self.score.victory(player2)
                    self.wait.wait(player2)
                    running = False
                    continue
                self.score.player_scores(2)
                pygame.display.update()
                running = self.wait.launch(1, self.ball)

            if self.ball.rect.x > self.scr_width:
                p1_score += 1
                #Player 1 wins if 11 pts
                if p1_score == 3:
                    self.score.victory(1)
                    self.wait.wait(1)
                    running = False
                    continue
                self.score.player_scores(1)
                pygame.display.update()
                if pvp:
                    running = self.wait.launch(2, self.ball)
                else:
                    running = self.wait.launch(3, self.ball)

            self.ball.update()
            screen.blit(background, (0,0))
            self.score.scores(p1_score, p2_score)
            all_sprites.draw(screen)
            pygame.display.update()
