import pygame
import datetime

class Participant_Button:

    """Create a button, then blit the surface in the while loop"""
    def __init__(self, participant, pos=(0,0)):
        self.x, self.y = pos
        self.participant = participant
        self.font = pygame.font.SysFont("Arial", 20)
        self.change_text(self.participant.name_and_group +" - inte startat", "red")
        if self.participant.started & self.participant.still_active:
            if self.participant.start_time == datetime.datetime.fromtimestamp(0.000001):
                self.participant.force_start()
            self.x = self.x + 20
            self.change_text(self.participant.name_and_group + " - starttid: "+self.participant.start_time_str, bg="white")

        elif self.participant.started and not self.participant.still_active:
            if self.participant.end_time <= datetime.datetime.fromtimestamp(0.000001):
                self.participant.force_fin()
            self.x = self.x + 40
            self.change_text(self.participant.name_and_group + " - måltid: " +self.participant.start_time_str, bg="green")



    def change_text(self, text, bg="black"):
        #Change the text when you click
        self.text = self.font.render(text, 1, pygame.Color("blue"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


    def show(self, WIN):
        if self.participant.started & self.participant.still_active:
            now = datetime.datetime.now()
            diff = now-self.participant.start_time
            self.change_text(self.participant.name + " tid: "+str(diff)[0:9], bg="white")
        WIN.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.press()


    def press(self):
        if not self.participant.started:
            self.x = self.x + 20
            self.participant.start()
            self.change_text(self.participant.name_and_group + " - starttid: " + self.participant.start_time_str,
                             bg="white")
            self.participant.started = True
            self.participant.still_active = True
        elif self.participant.still_active:
            self.x = self.x + 20
            self.participant.fin()
            self.change_text(self.participant.name_and_group + " - måltid: " + self.participant.slut_tid_str,
                             bg="green")
            self.participant.still_active = False
        else:
            self.participant.still_active = True
            self.x = self.x - 20
            self.change_text(self.participant.name_and_group + " - starttid: " + self.participant.start_time_str,
                             bg="white")
    
    def start(self):
        if not self.participant.started and not self.participant.still_active: 
            self.participant.start()
            self.x = self.x + 20
            self.change_text(self.participant.name_and_group +" - starttid: "+self.participant.start_time_str, bg="white")
    
    def fin(self):
        if self.participant.started and self.participant.still_active: 
            self.participant.fin()
            self.x = self.x + 20
            self.change_text(self.participant.name_and_group +" - måltid: "+self.participant.slut_tid_str, bg="green")
