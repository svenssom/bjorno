import pygame
import datetime

from triatlon import COLUMN_WIDTH

from triatlon import minutes_and_sec_as_str_to_sec
from triatlon import sec_as_str_to_minutes_and_sec

from Participant import time_to_file_format

class Participant_Button:

    """Create a button, then blit the surface in the while loop"""
    def __init__(self, participant, pos=(0,0)):
        self.x, self.y = pos
        self.participant = participant
        self.rect = pygame.Rect(self.x, self.y, 20, 20) #ny
        self.hoverd = False #ny
        self.font = pygame.font.SysFont("Courier New", 15, bold=True)
        self.change_text(self.participant.display_name + " | inte startat", "beige")
        if self.participant.started & self.participant.still_active:
            if self.participant.start_time == datetime.datetime.fromtimestamp(0.000001):
                self.participant.force_start()
            self.x = self.x
            self.change_text(self.participant.display_name + " | start: " + self.participant.start_time_str, bg="skyblue")

        elif self.participant.started and not self.participant.still_active:
            if self.participant.end_time <= datetime.datetime.fromtimestamp(0.000001):
                self.participant.force_fin()
            self.x = self.x
            self.change_text(self.participant.display_name + " | mål: " + time_to_file_format(self.participant.difference), bg="darkolivegreen3")

    def draw(self, WIN): #ny
        if self.hoverd:
            now = datetime.datetime.now()
            diff = now - self.participant.start_time
            text = self.participant.name[0:6] + " G: " + time_to_file_format(self.participant.guessed_time) + " Start: " + self.participant.start_time_str
            text = self.font.render(text, 1, pygame.Color("white"))
            size = self.size
            surface = pygame.Surface(size)
            surface.blit(text, (5, 2))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            WIN.blit(surface, (self.x, self.y))

    def change_text(self, text, bg="white"):
        #Change the text when you click
        self.text = self.font.render(text, 1, pygame.Color("black"))
        self.size = [COLUMN_WIDTH-20, self.text.get_size()[1]+4]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (5, 2))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


    def show(self, WIN):
        if self.participant.started & self.participant.still_active:
            now = datetime.datetime.now()
            diff = now-self.participant.start_time
            self.change_text(self.participant.display_name + " | tid: "+str(diff)[0:9], bg="skyblue")
        WIN.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                if event.button == 1:
                    #left_button
                    self.left_press()
                #elif event.button == 2:
                    #print("middle mouse button")
                elif event.button == 3:
                    self.right_press()
                    #print("right mouse button")
                #elif event.button == 4:
                    #print("mouse wheel up")
                #elif event.button == 5:
                    #print("mouse wheel down")


    def left_press(self):
        if not self.participant.started:
            self.x = self.x
            self.participant.start()
            self.change_text(self.participant.display_name+ " | start: " + self.participant.start_time_str,
                             bg="skyblue")
            self.participant.started = True
            self.participant.still_active = True
        elif self.participant.still_active:
            self.x = self.x
            self.participant.fin()
            self.change_text(self.participant.display_name + " | mål: " + time_to_file_format(self.participant.difference),
                             bg="darkolivegreen3")
            self.participant.still_active = False
        else:
            self.participant.still_active = True
            self.x = self.x
            self.change_text(self.participant.display_name + " | start: " + self.participant.start_time_str,
                             bg="skyblue")

    
    def start(self):
        if not self.participant.started and not self.participant.still_active: 
            self.participant.start()
            self.x = self.x
            self.change_text(self.participant.display_name + " | start: " + self.participant.start_time_str, bg="skyblue")
    
    def fin(self):
        if self.participant.started and self.participant.still_active: 
            self.participant.fin()
            self.x = self.x
            self.change_text(self.participant.display_name + " | mål: " + time_to_file_format(self.participant.difference), bg="darkolivegreen3")

    def right_press(self):
        print("hej")
        FPS = 30
        player_window = pygame.display.set_mode((600, 600))
        player_font = pygame.font.SysFont("Helvetica", 20)
        pygame.display.set_caption(self.participant.name)
        player_window.fill((1, 1, 1))
        txt_surface = player_font.render("test", True, pygame.Color('lightskyblue3'))


        tmp_input_box = pygame.Rect(40, 0, 140, 40)
        tmp_input_box.w = 600

        player_window.blit(txt_surface, (tmp_input_box.x + 5, tmp_input_box.y + 5))

        pygame.draw.rect(player_window, pygame.Color('lightskyblue3'), tmp_input_box, 2, border_radius=5)
        pygame.display.flip()

        clock = pygame.time.Clock()
        run = True
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        active = False
        text = ''
        comando = ""

        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if tmp_input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = color_active if active else color_inactive
                        #print("left mouse button")
                    #elif event.button == 2:
                        #print("middle mouse button")
                    #elif event.button == 3:
                        #print("right mouse button")
                    #elif event.button == 4:
                        #print("mouse wheel up")
                    #elif event.button == 5:
                        #print("mouse wheel down")

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(text)
                            comando = text
                            text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # end for event in pygame

            if comando != "":
                if comando == "restart":
                    self.participant.started = False
                    self.participant.start_time = datetime.datetime.fromtimestamp(0.000001)
                    self.participant.start_time_str = self.participant.start_time.strftime("%H:%M:%S")
                else:
                    try:
                        self.participant.guessed_time = int(minutes_and_sec_as_str_to_sec(comando))
                    except:
                        print("gick inte att konvetnera på rätt sätt!")
                comando = ""

            player_window.fill("seashell")
            txt_surface = player_font.render(text, True, "blue")

            width = max(200, txt_surface.get_width() + 10)
            tmp_input_box.w = width

            player_window.blit(txt_surface, (tmp_input_box.x + 5, tmp_input_box.y + 5))
            pygame.draw.rect(player_window, "red", tmp_input_box, 2, border_radius=5)
            pygame.display.flip()