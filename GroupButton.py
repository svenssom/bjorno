import pygame
import datetime


class Group_Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, group_number, participants = [], pos=(0, 0)):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", 20)
        self.number = group_number
        self.change_text(str(group_number) + " - inte startat", "red")
        self.started = False
        self.still_active = True
        self.participant_buttons = participants


    def change_text(self, text, bg="black"):
        # Change the text when you click
        self.text = self.font.render(text, 1, pygame.Color("blue"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, WIN):
        if self.started & self.still_active:
            self.change_text(" Startad", bg="white")
        WIN.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.press()

    def press(self):
        if not self.started:
            self.change_text(str(self.number) + " - Startad ", bg="white")
            self.started = True
            self.still_active = True
            for participant in self.participant_buttons:
                participant.start()
        elif self.still_active:
            self.change_text(str(self.number) + " - Avslutad", bg="green")
            self.still_active = False
            for participant in self.participant_buttons:
                participant.fin()
        else:
            self.change_text(str(self.number) + " - Startad ", bg="white")
            self.started = True
            self.still_active = True
            for participant in self.participant_buttons:
                participant.press()


