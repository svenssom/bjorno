import pygame
import datetime

import triatlon
class Group_Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, group_number, participants = [], pos=(0, 0)):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Courier New", 18, bold=True)
        self.number = group_number
        self.change_text(" | inte startat", "beige")
        self.started = False
        self.still_active = True
        self.participant_buttons = participants


    def change_text(self, text, bg="seashell"):
        # Change the text when you click
        if self.number == 2:
            self.text = self.font.render("Barn-Grupp " + text, 1, pygame.Color("black"))
        elif self.number == 1:
            self.text = self.font.render("Snabb-grupp " + text, 1, pygame.Color("black"))
        else:
            self.text = self.font.render("Grupp " + str(self.number) + text, 1, pygame.Color("black"))
        #self.text = self.font.render("Grupp " + str(self.number) + text, 1, pygame.Color("black"))
        self.size = [triatlon.COLUMN_WIDTH - 20, self.text.get_size()[1] + 10]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (10, 5))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, WIN):
        if self.started & self.still_active:
            self.change_text(" | Startad", bg="skyblue")
        WIN.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.left_press()

    def left_press(self):
        if not self.started:
            self.change_text(" | Startad ", bg="skyblue")
            self.started = True
            self.still_active = True
            for participant in self.participant_buttons:
                participant.start()
        elif self.still_active:
            self.change_text(" | Avslutad", bg="darkolivegreen3")
            self.still_active = False
            for participant in self.participant_buttons:
                participant.fin()
        else:
            self.change_text(" | Startad ", bg="skyblue")
            self.started = True
            self.still_active = True
            for participant in self.participant_buttons:
                participant.left_press()


