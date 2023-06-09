from copy import deepcopy
from datetime import time
from os.path import exists

from ParticipantButton import *
from Participant import *
from GroupButton import *

pygame.init()
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
        tmp.append(read_participant_line(x))
    print("just nu är ser deltagarlistan ut som följer:", tmp)
    return tmp


def read_participant_line(line):
    fields = line.split("\t")
    name = fields[1]
    swimming = "Simma" in fields[2]
    running = "Springa" in fields[2]
    biking = "Cykla" in fields[2]
    guessed_time = minutes_and_sec_as_str_to_sec(fields[3])
    group = 1 if "Ja" in fields[4] else 2
    return Participant(name, guessed_time, biking, running, swimming, group)


# skapa knappar för alla deltagare i deltagare_lista
def set_up_buttons():
    buttons = []
    i = 0
    j = 90
    current_group = 1
    for participant in participants:
        if j > HEIGHT - 100 or participant.start_group > current_group:
            i += 500
            j = 90
        current_group = participant.start_group
        buttons.append(Participant_Button(participant, (i, j)))
        j += 30

    return buttons


def make_group_button(group_number):
    i = 500*(group_number-1) + 20
    j = 40
    tmp_buttons = []
    for button in participant_buttons:
        if button.participant.start_group == group_number:
            tmp_buttons.append(button)
    return Group_Button(group_number, tmp_buttons, (i,j))


def make_group_buttons():
    tmp_buttons = []
    for x in [1,2,3,4]:
        tmp_buttons.append(make_group_button(x))
    return tmp_buttons

# skapa korrekt formaterad backup fil
def back_up(lista):
    tid = datetime.datetime.now().strftime("%H_%M_%S") + ".txt"
    print(tid)

    f = open(r'out/' + tid, "w")
    for participant in lista:
        f.write(participant.to_file_form())
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
    for participant in participants:
        participant.calculate_result()

    quickest = deepcopy(participants)
    best = deepcopy(participants)

    for i in range(len(participants) - 1):
        for j in range(len(participants) - 1):
            if best[j].difference_as_percentage > best[j + 1].difference_as_percentage:
                best[j], best[j + 1] = best[j + 1], best[j]

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

# end sort

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
    participants = set_up(r'in/participants.tsv')
    sort_by_name()  # soterar listan i bokstavsordning
    global participant_buttons
    participant_buttons = set_up_buttons()
    global group_buttons
    group_buttons = make_group_buttons()
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
            for button in group_buttons:
                button.click(event)
            # button1.click(event)

        # end for event in pygame

        if comando == "result":
            sort()
            comando = ""
        elif comando == "add competitor":
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
        for button in group_buttons:
            button.show(WIN)

        WIN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(WIN, color, input_box, 2, border_radius = 5)
        pygame.display.flip()

        # draw_window()
    # end while run
    pygame.quit()


# end main()


if __name__ == "__main__":
    main()
    sort()