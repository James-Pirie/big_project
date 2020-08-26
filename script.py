import os
list_of_cultures = ["middle_eastern_", "eastern_european_", "southamerican_", "commonwealth_",  "western_european_"
                    "african_", "asian_"]

list_of_tags = ["AFG", "ALB", "ARG", "AST", "AUS", "BEL", "BHU", "BOL", "BRA", "MAL", "RAJ", "BUL", "CHL", "CHI", "COL",
                "PRC", "COS", "CUB", "CZE", "DEN", "DOM", "CAN", "INS", "ECU", "ELS", "EST", "ETH", "FIN", "FRA", "GER",
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
    """This function creates a mod file for the game to recognize the data. This function must always be run first"""
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

    os.makedirs(f"user_data/{mod_name}/common/countries")
    os.mkdir(f"user_data/{mod_name}/common/country_tags")
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


def assign_nation_tag(mod_name, tag, country_name):
    template = f'{tag} = "countries/{country_name}.txt"'
    if os.path.isfile(f"user_data/{mod_name}/common/country_tags/00_countries.txt"):
        countries_file = open(f"user_data/{mod_name}/common/country_tags/00_countries.txt", "r")
        replacement_countries_file = open(f"user_data/{mod_name}/common/country_tags/00_countries2.txt", "w+")
        original_countries_file_contents = countries_file.read()
        every_line_in_countries_file = original_countries_file_contents.split("\n")
        list_of_tags_in_file = []
        for i in range(len(every_line_in_countries_file)):
            current_line = every_line_in_countries_file[i]
            list_of_tags_in_file.append(current_line.split(" =")[0])
        if tag in list_of_tags_in_file:
            for i in range(len(every_line_in_countries_file)):
                every_word_on_current_line = every_line_in_countries_file[i].split()
                if tag in every_word_on_current_line:
                    del every_line_in_countries_file[i]
                    print(every_line_in_countries_file)
                    break
        every_line_in_countries_file.append(template)
        for z in range(len(every_line_in_countries_file)):
            if every_line_in_countries_file[z] != "":
                replacement_countries_file.write(every_line_in_countries_file[z] + "\n")
        os.remove(f"user_data/{mod_name}/common/country_tags/00_countries.txt")
        os.rename(f"user_data/{mod_name}/common/country_tags/00_countries2.txt",
                  f"user_data/{mod_name}/common/country_tags/00_countries.txt")

    else:
        original_countries_file_data = open("data/country_tags/00_countries.txt", "r")
        new_countries_file_template = original_countries_file_data.read()
        country_tag_file = open(f"user_data/{mod_name}/common/country_tags/00_countries.txt", "w+")
        country_tag_file.write(template + "\n")
        country_tag_file.write(new_countries_file_template)


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
        new_colors_file = open(f"user_data/{mod_name}/common/country_tags/colors2.txt", "w+")
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
                    del every_line_in_colors[i - 1]

                    break
                previous_line = every_line_in_colors[i]

        for i in range(len(new_tag_insert)):
            new_colors_file.write(new_tag_insert[i] + "\n")
        for i in range(len(every_line_in_colors)):
            new_colors_file.write(every_line_in_colors[i] + "\n")
        os.remove(f"user_data/{mod_name}/common/colors.txt")
        os.rename(f"user_data/{mod_name}/common/colors2.txt", f"user_data/{mod_name}/common/colors.txt")

    else:
        colour_file_template = open(f"data/colors.txt").read()
        new_colors_file = open(f"user_data/{mod_name}/common/country_tags/colors.txt", "w+")
        for i in range(len(new_tag_insert)):
            new_colors_file.write(new_tag_insert[i] + "\n")
        new_colors_file.write(colour_file_template)
    new_colors_file.close()


def create_history_file(mod_name, tag, country_name):
    template = f"{tag} - {country_name}"
    os.makedirs(f"user_data/{mod_name}/history/countries")
    os.mkdir(f"user_data/{mod_name}/history/states")
    history_file = open(f"user_data/{mod_name}/history/countries/{template}.txt", "w+")
    history_file.close()


def assign_nation_states(mod_name, country_tag, desired_territory, core, controls):
    list_of_state_files = os.listdir("data/history/states")
    list_of_state_tags = []
    owner_template = f"\t\towner = {country_tag}"
    core_template = f"\t\tadd_core_of = {country_tag}"
    for v in range(len(desired_territory)):
        for i in range(len(list_of_state_files)):
            list_of_state_tags.append(list_of_state_files[i].split("-")[0])
        state_file_index = list_of_state_tags.index(desired_territory[v])
        print(list_of_state_files[state_file_index])
        template_file = open(f"data/history/states/{list_of_state_files[state_file_index]}", "r")
        template = template_file.read()
        every_line_in_template = template.split("\n")
        core_counter = 0
        for i in range(len(every_line_in_template)):
            if "owner" in every_line_in_template[i].split() and controls:
                every_line_in_template[i] = owner_template
            elif core and "add_core_of" in every_line_in_template[i].split() and core_counter == 0:
                every_line_in_template.insert(i, core_template)
                core_counter += 1
        if os.path.isfile(f"user_data/{mod_name}/history/states"):
            print("Here")
            if os.path.isfile(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}"):
                os.remove(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}")
        state_file = open(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}", "w+")
        for x in range(len(every_line_in_template)):
            state_file.write(every_line_in_template[x] + "\n")
        state_file.close()


nation_name = "Bikini Bottom"
nation_tag = "BKB"
rgb_value = "{ 192 168 123 }"
culture = list_of_cultures[2]
states = ["23", "1", "199", "300"]
assign_nation_states("Test2", "ELS", states, True, True)
# create_history_file("Test2", nation_tag, nation_name)
