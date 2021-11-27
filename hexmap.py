# Cepheus Light Retro Hexagon Map Generator.

import agama
import worldgen


def hex_number(column, row, world_type):
    if column % 2 == 0:
        if (row == 1) or (row == 0):
            return "____"
        elif world_type == " ":
            return "____"
        elif row == 11:
            return f"0{column}10"
        else:
            return f"0{column}0{row - 1}"
    else:
        if world_type == " ":
            return "____"
        elif row == 10:
            return f"0{column}10"
        else:
            return f"0{column}0{row}"


def base_row(base_row_string):
    row_string = ""
    for i in range(0, 4):
        row_string += base_row_string
    return row_string


def empty_world(column, row):
    empty_world = worldgen.World(column, row)
    empty_world.uwp_dict['starport'] = " "
    empty_world.gas_giant_display = " "
    empty_world.scout = "_"
    empty_world.naval = " "
    empty_world.world_type = " "
    empty_world.name_display = "       "
    return empty_world

def blank_starmap():
    starmap = {}
    for column in range (0, 9):
        starmap[column] = {}
        for row in range (0, 11):
            starmap[column][row] = empty_world(column, row)
    return starmap


def generate_starmap(stars):
    starmap = blank_starmap()
    for column in range(0, 9):
        for row in range(0, 11):
            if column in stars:
                if row in stars[column]:
                    starmap[column][row] = stars[column][row]
                else:
                    pass
            else:
                pass
    return starmap


def starmap_string(starmap):
    global row
    star_string = f" UNIVERSAL OS v.21.1\n\n S U B S E C T O R  M A P\n\n {base_row('  _____       ')}\n"
    for row in range(1, 11):
        star_string += f"  /  {starmap[1][row].uwp_dict['starport']} {starmap[1][row].gas_giant_display}\{starmap[2][row - 1].name_display}/  {starmap[3][row].uwp_dict['starport']} {starmap[3][row].gas_giant_display}\{starmap[4][row - 1].name_display}/  {starmap[5][row].uwp_dict['starport']} {starmap[5][row].gas_giant_display}\{starmap[6][row - 1].name_display}/  {starmap[7][row].uwp_dict['starport']} {starmap[7][row].gas_giant_display}\{starmap[8][row - 1].name_display}/ \n"
        star_string += f" /{starmap[1][row].naval}  {starmap[1][row].world_type}   \{starmap[2][row - 1].scout}{hex_number(2, row, starmap[2][row - 1].world_type)}/{starmap[3][row].naval}  {starmap[3][row].world_type}   \{starmap[4][row - 1].scout}{hex_number(4, row, starmap[4][row - 1].world_type)}/{starmap[5][row].naval}  {starmap[5][row].world_type}   \{starmap[6][row - 1].scout}{hex_number(6, row, starmap[6][row - 1].world_type)}/{starmap[7][row].naval}  {starmap[7][row].world_type}   \{starmap[8][row - 1].scout}{hex_number(8, row, starmap[8][row - 1].world_type)}/ \n"
        star_string += f" \{starmap[1][row].name_display}/  {starmap[2][row].uwp_dict['starport']} {starmap[2][row].gas_giant_display}\{starmap[3][row].name_display}/  {starmap[4][row].uwp_dict['starport']} {starmap[4][row].gas_giant_display}\{starmap[5][row].name_display}/  {starmap[6][row].uwp_dict['starport']} {starmap[6][row].gas_giant_display}\{starmap[7][row].name_display}/  {starmap[8][row].uwp_dict['starport']} {starmap[8][row].gas_giant_display}\ \n"
        star_string += f"  \{starmap[1][row].scout}{hex_number(1, row, starmap[1][row].world_type)}/{starmap[2][row].naval}  {starmap[2][row].world_type}   \{starmap[3][row].scout}{hex_number(3, row, starmap[3][row].world_type)}/{starmap[4][row].naval}  {starmap[4][row].world_type}   \{starmap[5][row].scout}{hex_number(5, row, starmap[5][row].world_type)}/{starmap[6][row].naval}  {starmap[6][row].world_type}   \{starmap[7][row].scout}{hex_number(7, row, starmap[7][row].world_type)}/{starmap[8][row].naval}  {starmap[8][row].world_type}   \ \n"
    star_string += f"        \{starmap[2][10].name_display}/     \{starmap[4][10].name_display}/     \{starmap[6][10].name_display}/     \{starmap[8][10].name_display}/\n"
    star_string += f"         \{starmap[2][10].scout}{hex_number(2, 11, starmap[2][row].world_type)}/       \{starmap[4][10].scout}{hex_number(4, 11, starmap[4][10].world_type)}/       \{starmap[6][10].scout}{hex_number(6, 11, starmap[6][10].world_type)}/       \{starmap[8][10].scout}{hex_number(8, 11, starmap[8][10].world_type)}/\n\n"
    return star_string


# Test area

