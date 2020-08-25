import os
list_of_cultures = ["middle_eastern_", "eastern_european_", "southamerican_", "commonwealth_",  "western_european_"
                    "african_", "asian_"]

list_of_tags = ["AFG", "ALB", "ARG", "AST", "AUS", "BEL", "BHU", "BOL", "BRA", "MAL", "RAJ", "BUL", "CHL", "CHI", "COL",
                "PRC", "COS", "CUB", "CZE", "DEN","DOM", "CAN", "INS", "ECU", "ELS", "EST", "ETH", "FIN", "FRA", "GER",
                "GRE", "GXC", "GUA", "HAI", "HON", "PER", "IRQ", "IRE", "ITA", "JAP", "HUN" ,"ROM", "LAT", "LIB", "LIT",
                "LUX", "MAN", "MEN", "MEX", "MON", "NEP", "HOL", "NZL", "NIC", "NOR", "OMA", "PAN", "PAR", "PRU", "PHI",
                "POL", "POR", "SAU", "SHX", "SIA", "SIK", "SAF", "SOV", "SPR", "D01", "SWE", "SWI", "TAN", "TIB", "TUR",
                "ENG", "USA", "URG", "VEN", "XSM", "YEM", "YUG", "YUN", "ALG", "ANG", "AZR", "BAH", "BAN", "BLZ", "BOS",
                "BOT", "BRM", "BRD", "CMR", "CAR", "CHA", "CSA", "RCG", "IVO", "CRO", "DAH", "DJI", "DDR", "EQG", "ERI",
                "GAB", "GAM", "GHA", "GNA", "GNB", "GYA", "ISR", "JAM", "KAZ", "KEN", "EGY", "JOR", "LBA", "MOR", "KOR",
                "KUW", "KYR", "LEB", "MLW", "MLD", "MLI", "MLT", "MRT", "FIJ", "MOL", "MZB", "NMB", "CRC", "NGR", "NGA",
                "NIR", "PAK", "PAL", "PNG", "PUE", "ARM", "BLR", "CAM", "CAY", "CYP", "GEO", "GDL", "LAO", "MAC", "MAD",
                "MNT", "QAT", "SLV", "SUR", "TAJ", "BAS", "TRI", "TMS", "UKR", "UZB", "VIN", "RWA", "WES", "SCO", "SEN",
                "SER", "SIE", "SLO", "SOM", "SUD", "SRL", "SYR", "TZN", "TOG", "TUN", "UGA", "USB", "UAE", "VOL", "WLS",
                "WGR", "COG", "ZAM", "ZIM"]


def create_a_mod_file(mod_name, mod_tags, game_version, mod_version):
    """This function creates a mod file for the game to recognize the data."""
    # I apologize in advance for the terrible indentation of the docstring
    # The indentation is adapted to meet the hoi4 file format
    tags_formatted = """{"""
    for i in range(len(mod_tags)):
        tags_formatted += "\n" + "    " + '"' + mod_tags[i] + '"'
    tags_formatted += "\n}"
    # this docstring inserts user values into a template to create a functional descriptor file
    descriptor_template = f"""version="{mod_version}"
tags={tags_formatted}
name="{mod_name}"
supported_version="{game_version}" """

    os.mkdir(f"user_data/{mod_name}")  # create the mod file
    os.makedirs(f"user_data/{mod_name}/common/countries")
    descriptor_file = open(f"user_data/{mod_name}/descriptop.mod", "w+")  # create the descriptor file
    descriptor_file.write(descriptor_template)  # write the content to the file
    descriptor_file.close()


def create_new_nation(mod_name, country_name, gfx, rgb_value):
    country_file = open(f"user_data/{mod_name}/common/countries/{country_name}.txt", "w+")
    gfx_2d = gfx + "2d"
    gfx_3d = gfx + "gfx"
    country_file_template = f"""\n
graphical_culture = {gfx_3d}
graphical_culture_2d = {gfx_2d}
color = { rgb_value } #"""
    country_file.write(country_file_template)
    country_file.close()


def assign_nation_color(mod_name, tag, rgb):
    """Create the colours document, and assign the colour of our nation to the nation's tag"""
    new_tag_insert = [f"{tag} = " + "{", f"\tcolor = rgb {rgb}", f"\tcolor_ui = rgb {rgb}", "}"]

    if os.path.isfile(f"user_data/{mod_name}/common/colors.txt"):
        original_colour_file = open(f"user_data/{mod_name}/common/colors.txt", "r")
        colors_content = original_colour_file.read()
        original_colour_file.close()
        list_of_existing_tags = colors_content.split()
        list_of_existing_tags_formatted = []
        previous_line = None
        every_line_in_colors = colors_content.split("\n")
        new_colors_file = open(f"user_data/{mod_name}/common/colors2.txt", "w+")
        f = 0

        while f < len(list_of_existing_tags):
            list_of_existing_tags_formatted.append(list_of_existing_tags[f])
            f += 20
        if tag in list_of_existing_tags_formatted:
            for i in range(len(every_line_in_colors)):
                if tag in every_line_in_colors[i].split():
                    for x in range(3):
                        every_line_in_colors.remove(every_line_in_colors[i])
                    break
            for i in range(len(every_line_in_colors)):
                if i >= 1 and previous_line.strip() == every_line_in_colors[i].strip():
                    print(previous_line + " v " + every_line_in_colors[i - 1])
                    del every_line_in_colors[i - 1]

                    break
                previous_line = every_line_in_colors[i]

        for i in range(len(new_tag_insert)):
            new_colors_file.write(new_tag_insert[i] + "\n")
        for i in range(len(every_line_in_colors)):
            new_colors_file.write(every_line_in_colors[i] + "\n")
        new_colors_file.close()
        os.remove(f"user_data/{mod_name}/common/colors.txt")
        os.rename(f"user_data/{mod_name}/common/colors2.txt", f"user_data/{mod_name}/common/colors.txt")
        print(every_line_in_colors)

    else:
        colour_file_template = open(f"data/colors.txt").read()
        new_colors_file = open(f"user_data/{mod_name}/common/colors.txt", "w+")
        for i in range(len(new_tag_insert)):
            new_colors_file.write(new_tag_insert[i] + "\n")
        new_colors_file.write(colour_file_template)



