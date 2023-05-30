import pygame
import numpy as np
import time
from random import randint
import datetime
from os.path import exists
from copy import deepcopy
from Participant import Participant
from ParticipantButton import *

pygame.init()
global participants
participants = []
global fuck_it_ofsett_x
global fuck_it_ofsett_y
fuck_it_offset_x = 100
fuck_it_offset_y = 0
WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 15)
pygame.display.set_caption("main window")
WHITE = (255, 255, 255)
FPS = 20


def start_group(group):
    for button in participant_buttons:
        if button.participant.start_group == group:
            button.start()


def minutes_and_sec_as_str_to_sec(str):
    str_parts = str.split(":")
    str_parts[0] = int(str_parts[0])
    str_parts[1] = int(str_parts[1])
    seconds = str_parts[0] * 60 + str_parts[1]
    return seconds


def sec_as_str_to_minutes_and_sec(str):
    tot_sec = int(str)
    min = int(tot_sec // 60)
    sec = tot_sec % 60
    min_and_sec = str(min) + ":" + str(sec)
    return min_and_sec


# ladda in fil och skapa deltagare_lista
def set_up(file_name):
    tmp = []
    f = open(file_name, "r")
    for x in f:
        y = x.split()
        if len(y) < 3:
            continue
        # formatet på datetime lägger till ett mellanslag/elemet. Sätter ihop elementen och tar bort det "onödiga" elementet.
        if len(y) > 11:
            y[5] = y[5] + " " + y[6]
            del y[6]
            y[6] = y[6] + " " + y[7]
            del y[7]
        # gissad_tid formatering
        try:
            y[1] = int(y[1])
        except ValueError:
            # Handle the exception
            if ":" in y[1]:
                y[1] = minutes_and_sec_as_str_to_sec(y[1])
            else:
                y[0] = "*" + y[0]
                y[1] = 100000

        if y[2] == "True":
            y[2] = True
        else:
            y[2] = False
        if y[3] == "True":
            y[3] = True
        else:
            y[3] = False
        if y[4] == "True":
            y[4] = True
        else:
            y[4] = False
        if y[5] == "0" or len(y) == 5 or y[5] == "start_tid":
            tmp.append(Participant(y[0], y[1], y[2], y[3], y[4]))
            continue
        else:
            # 2022-06-20 11:40:15.846478
            y[5] = datetime.datetime.strptime(y[5], "%Y-%m-%d %H:%M:%S.%f")
        if y[6] == "0" or len(y) == 5 or y[6] == "slut_tid":
            y[6] = None
        else:
            y[6] = datetime.datetime.strptime(y[6], "%Y-%m-%d %H:%M:%S.%f")
        if y[7] == "0" or y[7] == "-1" or len(y) == 5 or y[7] == "procentuell_skilnad":
            y[7] = -1
        if y[8] == "True":
            y[8] = True
        else:
            y[8] = False

        if y[10] == "True":
            y[10] = True
        else:
            y[10] = False

        # tmp = name, gissda_tid, cykla, springa, simma, start_tid, slut_tid, procentruell_skilnad, fortfarande_aktiv, start_grupp, startat
        tmp.append(Participant(y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8], y[9], y[10]))
    print("just nu är ser deltagarlistan ut som följer:", tmp)
    return tmp


# skapa knappar för alla deltagare i deltagare_lista
def set_up_buttons():
    buttons = []
    i = 0
    j = 40
    for participant in participants:
        buttons.append(Participant_Button(participant, (i, j)))
        j += 30
        if j > HEIGHT - 100:
            i += 500
            j = 40
    return buttons


# skapa korrekt formaterad backup fil
def back_up(lista):
    tid = datetime.datetime.now().strftime("%H_%M_%S") + ".txt"
    print(tid)

    f = open(r'out/' + tid, "w")
    for participant in lista:
        f.write(participant.to_file())
    f.close()
    return


# skapa en "snyggare" fil
def back_up_simpel(lista, version):
    tid = datetime.datetime.now().strftime("%H_%M_%S") + version + ".txt"
    f = open(r'out/' + tid, "w")
    for participant in lista:
        f.write(participant.to_file_simple())
    f.close()
    return


# end back_up

def back_up_simpel_presentega(lista, version):
    tid = datetime.datetime.now().strftime("%H_%M_%S") + version + ".txt"
    f = open(r'out/' + tid, "w")
    for participant in lista:
        if participant.started and not participant.still_active:
            f.write(participant.to_file_simple_presentega())
    f.close()
    return


def back_up_simpel_quickest(lista, version):
    tid = datetime.datetime.now().strftime("%H_%M_%S") + version + ".txt"
    f = open(r'out/' + tid, "w")
    for participant in lista:
        f.write(participant.to_file_simpel_quickest())
    f.close()
    return


# bubbelsort, går att optimera lite granna
def sort():
    quickest = []
    best = []

    for participant in participants:
        participant.calculate_result()

    quickest = deepcopy(participants)
    best = deepcopy(participants)

    for i in range(len(participants) - 1):
        for j in range(len(participants) - 1):
            if best[j].difference_as_percentage > best[j + 1].difference_as_percentage:
                best[j], best[j + 1] = best[j + 1], best[j]

    # for i in range(len(quickest)): #i = [1,2,3,4,5,6,7,8,9,10,11,13,14]
    #     if not quickest[i].do_all_three:
    #         del quickest[i]
    #         i=i-1
    i = 0
    while i < len(quickest):
        if not quickest[i].do_all_three:
            del quickest[i]
            i -= 1
        i += 1

    i = 0
    while i < len(quickest):
        if quickest[i].difference <= 0:
            del quickest[i]
            i -= 1
        i += 1

    for i in range(len(quickest) - 1):
        for j in range(len(quickest) - 1):
            if quickest[j].difference > quickest[j + 1].difference:
                quickest[j], quickest[j + 1] = quickest[j + 1], quickest[j]

    print("Snabbast: \n", quickest)  # skriv ut resultatet i terminalen
    print("Bäst gissat: \n", best)
    back_up(quickest)  # skriv in resultatet i en txt-fil
    back_up(best)
    back_up_simpel_quickest(quickest, "snabbast")
    # back_up_simpel(quickest, "snabbast")
    back_up_simpel_presentega(best, "bäst gissat")


# end sortera

def sort_by_name():
    for i in range(len(participants) - 1):
        for j in range(len(participants) - 1):
            current = participants[j]
            next = participants[j + 1]
            if str(current.start_group) + current.name > str(next.start_group) + next.name:
                participants[j], participants[j + 1] = participants[j + 1], participants[j]
    print(participants)  # skriv ut resultatet i terminalen
    back_up(participants)  # skriv in resultatet i en txt-fil


def fuckit():
    print("startgrupp namn gissad_tid alla_grenar(y/n)")
    inputs = ""
    inputs = input()
    inputs = inputs.split()
    if len(inputs) != 4:
        print("malformed input")
        return
    try:
        inputs[2] = int(inputs[2])
    except ValueError:
        # Handle the exception
        if ":" in inputs[2]:
            inputs[2] = minutes_and_sec_as_str_to_sec(inputs[2])
        else:
            print("malformated input")
            return

    if inputs[3] == "n":
        bike = False
    else:
        bike = True

    participants.append(Participant(inputs[1], inputs[2], bike, True, True, datetime.datetime.fromtimestamp(0.000001),
                                    datetime.datetime.fromtimestamp(0.000001), -1, False, inputs[0], False))

    global fuck_it_offset_y
    global fuck_it_offset_x
    participant_buttons.append(
        Participant_Button(participants[-1], (WIDTH - fuck_it_offset_x, HEIGHT - fuck_it_offset_y)))
    fuck_it_offset_y = fuck_it_offset_y + 30
    print("la till en deltagare")


def main():
    global fuck_it_offset_y
    fuck_it_offset_y = 40
    global fuck_it_offset_x
    fuck_it_offset_x = 300
    global participants  # VARFÖR BEHÖVS DENNA?! ÄR JU DEKLARERAD GLOBAL LÄNGD UPP I KODEN?!
    participants = set_up(r'in/bjorno_deltagare.txt')
    sort_by_name()  # soterar listan i bokstavsordning
    global participant_buttons
    participant_buttons = set_up_buttons()
    clock = pygame.time.Clock()
    run = True
    input_box = pygame.Rect(0, 0, 140, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    comando = ""

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                back_up(participants)
                # lägg till så back-up fil skapas
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
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

            for button in participant_buttons:
                button.click(event)
            # button1.click(event)

        # end for event in pygame

        if comando == "resultat":
            sort()
            comando = ""
        elif comando == "add competetor":
            # todo
            x = 6
        elif comando == "redo set-up":
            print("skriv filname i terminalen")
            file_name = input()
            if exists(file_name):
                participants = set_up(r'in/' + file_name)
                set_up_buttons()
            comando = ""
        elif comando == "f":
            fuckit()
            comando = ""
        elif comando[0:5] == "start":
            comando = comando.split()
            print("startade grupp: " + comando[-1])
            start_group(comando[-1])
            comando = ""
        elif comando == "sluta alla":
            for button in participant_buttons:
                button.start()
            print("sover")
            time.sleep(2)
            print("vaknat")
            for button in participant_buttons:
                button.fin()
            comando = ""

        # WIN.fill((WHITE))
        WIN.fill((1, 1, 1))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # button1.show()
        # Blit the text.

        for button in participant_buttons:
            button.show(WIN)

        WIN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(WIN, color, input_box, 2)
        pygame.display.flip()

        # draw_window()
    # end while run
    pygame.quit()


# end main()


if __name__ == "__main__":
    main()
