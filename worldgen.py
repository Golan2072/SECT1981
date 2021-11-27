# worldgenlib.py
# Library file for the 3-Book Classic Traveller Subsector Generator by Omer Golan-Joel.
# This is open source code, feel free to use it for any purpose.
# For any questions, contact me at golan2072@gmail.com.

# Import modules
import agama
import os


# Functions

def atmo_gen(size):
    if size == 0:
        atmosphere = 0
    else:
        atmosphere = agama.dice(2, 6) - 7 + size
    if atmosphere > 12:
        atmosphere = 12
    if atmosphere < 0:
        atmosphere = 0
    return atmosphere


def hydro_gen(size, atmosphere):
    hydrographics = agama.dice(2, 6) - 7 + size
    if size <= 1:
        hydrographics = 0
    elif atmosphere in [0, 1, 10, 11, 12]:
        hydrographics -= 4
    elif atmosphere == 14:
        hydrographics -= 2
    if hydrographics < 0:
        hydrographics = 0
    if hydrographics > 10:
        hydrographics = 10
    return hydrographics


def gov_gen(population):
    government = agama.dice(2, 6) - 7 + population
    if population == 0:
        government = 0
    if government < 0:
        government = 0
    if government > 15:
        government = 15
    return government


def law_gen(government):
    law = agama.dice(2, 6) - 7 + government
    if government == 0:
        law = 0
    if law < 0:
        law = 0
    if law > 10:
        law = 10
    return law


def starport_gen(population):
    starport_roll = agama.dice(2, 6) - 7 + population
    starport = "X"
    if starport_roll <= 4:
        starport = "A"
    elif starport_roll in [5, 6]:
        starport = "B"
    elif starport_roll in [7, 8]:
        starport = "C"
    elif starport_roll == 9:
        starport = "D"
    elif starport_roll in [10, 11]:
        starport = "E"
    elif starport_roll >= 11:
        starport = "X"
    if population == 0:
        starport = "X"
    return starport


def tech_gen(uwp_dict):
    tech = agama.dice(1, 6)
    if uwp_dict["starport"] == "A":
        tech += 6
    elif uwp_dict["starport"] == "B":
        tech += 4
    elif uwp_dict["starport"] == "C":
        tech += 2
    elif uwp_dict["starport"] == "X":
        tech -= 4
    if uwp_dict["size"] in [0, 1]:
        tech += 2
    elif uwp_dict["size"] in [2, 3, 4]:
        tech += 1
    if uwp_dict["atmosphere"] <= 3:
        tech += 1
    elif uwp_dict["atmosphere"] >= 10:
        tech += 1
    elif uwp_dict["hydrographics"] in [9, 10]:
        tech += 1
    if uwp_dict["population"] in range(0, 6):
        tech += 1
    elif uwp_dict["population"] == 9:
        tech += 2
    elif uwp_dict["population"] == 10:
        tech += 4
    if uwp_dict["government"] in [1, 5]:
        tech += 1
    elif uwp_dict["government"] == 13:
        tech -= 2
    elif uwp_dict["population"] == 0:
        tech = 0
    return tech


def base_gen(starport):
    naval = False
    scout = False
    base = " "
    if starport in ["A", "B"] and agama.dice(2, 6) >= 8:
        naval = True
    if starport in ["A", "B", "C", "D"]:
        scout_presence = agama.dice(2, 6)
        if starport == "C":
            scout_presence -= 1
        elif starport == "B":
            scout_presence -= 2
        elif starport == "A":
            scout_presence -= 3
        if scout_presence >= 7:
            scout = True
    if naval and not scout:
        base = "N"
    elif scout and not naval:
        base = "S"
    elif scout and naval:
        base = "A"
    return base


def trade_gen(uwp_dict):
    trade_list = []
    if uwp_dict["atmosphere"] in range(4, 10) and uwp_dict["hydrographics"] in range(4, 9) and uwp_dict[
        "population"] in range(5, 8):
        trade_list.append("Ag")
    if uwp_dict["size"] == 0:
        trade_list.append("As")
    if uwp_dict["atmosphere"] >= 2 and uwp_dict["hydrographics"] == 0:
        trade_list.append("De")
    if uwp_dict["atmosphere"] <= 1 and uwp_dict["hydrographics"] >= 1:
        trade_list.append("Ic")
    if uwp_dict["atmosphere"] in [0, 1, 2, 4, 7, 9] and uwp_dict["population"] >= 9:
        trade_list.append("In")
    if uwp_dict["atmosphere"] <= 3 and uwp_dict["hydrographics"] <= 3 and uwp_dict["population"] >= 6:
        trade_list.append("Na")
    if uwp_dict["population"] in range(4, 7):
        trade_list.append("Ni")
    if uwp_dict["atmosphere"] in range(2, 6) and uwp_dict["hydrographics"] <= 3:
        trade_list.append("Po")
    if uwp_dict["atmosphere"] in [6, 8] and uwp_dict["population"] in range(6, 9):
        trade_list.append("Ri")
    if uwp_dict["hydrographics"] >= 10:
        trade_list.append("Wa")
    if uwp_dict["atmosphere"] <= 0:
        trade_list.append("Va")
    return trade_list


def name_converter(name):
    new_name = f"{name: <{7}}".upper()
    new_name = (new_name[:7]) if len(new_name) > 7 else new_name
    return new_name


def generate_subsector():
    stars = {}
    for column in range (1, 9):
        stars[column] = {}
        for row in range (1, 11):
            if agama.dice(1, 6) >= 4:
                stars[column][row] = World(column, row)
        else:
            pass
    return stars

def string_subsector(stars):
    subsector_string = ""
    for column in range (0, 9):
        for row in range (0,11):
            if column in stars:
                if row in stars[column]:
                    subsector_string += stars[column][row].get_world_row() + "\n"
                else:
                    pass
            else:
                pass
    return subsector_string


# Classes

class World:

    def __init__(self, column, row):
        self.name = agama.random_line(os.path.join('data', 'worlds.txt'))
        self.column = column
        self.row = row
        self.uwp_dict = {"starport": "X", "size": agama.dice(2, 6) - 2, "atmosphere": 0, "hydrographics": 0,
                         "population": agama.dice(2, 6) - 2, "government": 0, "law": 0, "tl": 0}
        self.uwp_dict["atmosphere"] = atmo_gen(self.uwp_dict["size"])
        self.uwp_dict["hydrographics"] = hydro_gen(self.uwp_dict["size"], self.uwp_dict["atmosphere"])
        self.uwp_dict["government"] = gov_gen(self.uwp_dict["population"])
        self.uwp_dict["law"] = law_gen(self.uwp_dict["government"])
        self.uwp_dict["starport"] = starport_gen(self.uwp_dict["population"])
        self.uwp_dict["tl"] = tech_gen(self.uwp_dict)
        self.hex_uwp = {"starport": self.uwp_dict["starport"], "size": agama.pseudo_hex(self.uwp_dict["size"]),
                        "atmosphere": agama.pseudo_hex(self.uwp_dict["atmosphere"]),
                        "hydrographics": agama.pseudo_hex(self.uwp_dict["hydrographics"]),
                        "population": agama.pseudo_hex(self.uwp_dict["population"]),
                        "government": agama.pseudo_hex(self.uwp_dict["government"]),
                        "law": agama.pseudo_hex(self.uwp_dict["law"]),
                        "tl": agama.pseudo_hex(self.uwp_dict["tl"])}

        if agama.dice(2, 6) < 10:
            self.gas_giant = "G"
        else:
            self.gas_giant = " "
        self.base = base_gen(self.uwp_dict["starport"])
        self.trade_list = trade_gen(self.uwp_dict)
        self.trade_string = " ".join(self.trade_list)
        self.allegiance = "Na"
        if self.column == 10 and self.row != 10:
            self.hex = f"100{self.row}"
        elif self.column != 10 and self.row == 10:
            self.hex = f"0{self.column}10"
        elif self.column == 10 and self.row == 10:
            self.hex = "1010"
        else:
            self.hex = f"0{self.column}0{self.row}"
        self.world_type = " "
        if self.uwp_dict["hydrographics"] == "A":
            self.uwp_dict["hydrographics"] = 10
        if int(self.uwp_dict["hydrographics"]) > 0:
            self.world_type = "@"
        elif int(self.uwp_dict["size"]) == 0:
            self.world_type = "#"
        else:
            self.world_type = "O"
        self.scout = " "
        self.naval = " "
        if self.base == "A":
            self.scout = "^"
            self.naval = "*"
        elif self.base == "N":
            self.naval = "*"
        elif self.base == "S":
            self.scout = "^"
        else:
            self.scout = "_"
            self.naval = " "
        if self.gas_giant == "G":
            self.gas_giant_display = "*"
        else:
            self.gas_giant_display = " "
        self.name_display = name_converter(self.name)

    def print_raw_uwp(self):
        print(self.uwp_dict["starport"], self.uwp_dict["size"], self.uwp_dict["atmosphere"],
              self.uwp_dict["hydrographics"], self.uwp_dict["population"], self.uwp_dict["government"],
              self.uwp_dict["law"], "-", self.uwp_dict["tl"])

    def print_uwp(self):
        print(
            f"{self.hex_uwp['starport']}{self.hex_uwp['size']}{self.hex_uwp['atmosphere']}{self.hex_uwp['hydrographics']}{self.hex_uwp['population']}{self.hex_uwp['government']}{self.hex_uwp['law']}-{self.hex_uwp['tl']} {self.base}   {self.zone}   {self.gas_giants}   {self.trade_string}  ")

    def get_uwp_string(self):
        return (
            f"{self.hex_uwp['starport']}{self.hex_uwp['size']}{self.hex_uwp['atmosphere']}{self.hex_uwp['hydrographics']}{self.hex_uwp['population']}{self.hex_uwp['government']}{self.hex_uwp['law']}-{self.hex_uwp['tl']}")

    def get_world_row(self):
        uwp_string = self.get_uwp_string()
        return f"{self.hex: <{5}}{self.name: <{13}}{uwp_string: <{10}}{self.gas_giant: <{3}}{self.trade_string: <{10}}{self.base: <{3}}"


# Test area
