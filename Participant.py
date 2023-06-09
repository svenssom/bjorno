import numpy as np
from random import randint
import datetime


def time_to_file_format(guessed_time):
    tot_sec = guessed_time
    min = tot_sec // 60
    sec = tot_sec % 60
    min_and_sec = str(min) + ":" + str(sec)
    return min_and_sec

class Participant:
    def __init__(self, name="unnamed", guessed_time=0, bike=False, run=False, swim=False, start_group="0",
                 start_time=datetime.datetime.fromtimestamp(0.000001),
                 end_time=datetime.datetime.fromtimestamp(0.000001), difference_as_percentage=-1, still_active=False,
                 started=False):
        if name == "unnamed":
            self.name = "unnamed" + str(randint(0, 10000))
        else:
            self.name = name

        self.guessed_time = guessed_time
        self.bike = bike
        self.run = run
        self.swim = swim
        self.start_time = start_time
        self.start_time_str = self.start_time.strftime("%H:%M:%S")
        self.end_time = end_time
        self.end_time_str = self.end_time.strftime("%H:%M:%S")
        self.difference = 0
        self.difference_as_percentage = difference_as_percentage
        self.still_active = still_active

        if bike & run & swim:
            self.do_all_three = True
        else:
            self.do_all_three = False
        self.start_group = start_group
        self.started = started
        self.name_and_group = str(self.start_group) + " " + self.name

    def start(self):
        # så man inte startar någon som redan har startat
        if not self.started:
            now = datetime.datetime.now()
            self.start_time = now
            self.start_time_str = now.strftime("%H:%M:%S")
        self.started = True
        self.still_active = True

    def force_start(self):
        now = datetime.datetime.now()
        self.start_time = now
        self.start_time_str = now.strftime("%H:%M:%S")
        self.started = True
        self.still_active = True

    def fin(self):
        now = datetime.datetime.now()
        self.end_time = now
        self.end_time_str = now.strftime("%H:%M:%S")
        self.still_active = False
        self.calculate_result()
        self.back_up_fin()

    def back_up_fin(self):
        file_name = self.name + "." + datetime.datetime.now().strftime("%H_%M_%S") + ".txt"
        f = open(r'out/' + file_name, "w")
        f.write(self.to_file())
        f.close()
        return

    def force_fin(self):
        now = datetime.datetime.now()
        self.end_time = now
        self.end_time_str = now.strftime("%H:%M:%S")
        self.still_active = False
        self.calculate_result()
        self.back_up_fin()

    def fuck_it_change_stuff(self):
        print("vad vill du ändra? (gissadTid, name,)")
        x = input()
        # dubbelkolla så att input inte ger någon typ \n eller skit på slutet
        if x == "gissadTid":
            print("vilken ny gissad tid vill du gissa på?")
            y = int(input())
            self.guessed_time = y
        elif x == "name":
            print("vilket name?")
            self.name = input()
        else:
            print("okänd input")

    def to_file(self):
        return str(self.name) + " " + str(self.guessed_time) + " " + str(self.bike) + " " + str(self.run) + " " + str(
            self.swim) + " " + str(self.start_time) + " " + str(self.end_time) + " " + str(
            self.difference_as_percentage) + " " + str(self.still_active) + " " + str(self.start_group) + " " + str(
            self.started) + "\n"

    def to_file_simpel_quickest(self):
        return str(self.name) + " " + str(self.difference) + " " + "\n"

    def to_file_simple_presentega(self):
        return str(self.name) + " procentfel: " + str(self.difference_as_percentage) + " gissad tid: " + str(
            self.guessed_time) + " faktiskt tid: " + str(self.difference) + " \n"

    def to_file_simple(self):
        return str(self.name) + " " + str(self.guessed_time) + " " + str(self.difference) + " " + str(
            self.difference_as_percentage) + " " + str(self.still_active) + "\n"

    def to_file_form(self):
        return str("date time\t" + self.name + "\t" + ("Simma," if self.swim else "") +
                   ("Springa/Gå," if self.run else "") + ("Cykla" if self.bike else "") + "\t" +
                   time_to_file_format(self.guessed_time) + "\t" + ("Ja" if self.start_group == 1 else "Nej") + "\t" +
                   str(self.start_group) + "\t" + self.start_time_str + "\t" + self.end_time_str) + "\n"


    def __repr__(self):
        return "\n" + str(self.name) + "\n   gissad tid: " + str(self.guessed_time) + "\n   cyklar? " + str(
            self.bike) + "\n   springer? " + str(self.run) + "\n   simmar? " + str(self.swim) + "\n   starttid: " + str(
            self.start_time) + "\n   sluttid: " + str(self.start_time_str) + "\n   grupp: " + str(self.start_group)

    def calculate_result(self):
        self.difference_as_percentage = np.abs(
            np.abs(self.start_time.timestamp() - self.end_time.timestamp()) - self.guessed_time) / self.guessed_time
        self.difference = self.end_time.timestamp() - self.start_time.timestamp()
        print(self.difference)

# end class deltagare
