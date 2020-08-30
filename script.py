import os
from PIL import Image
import shutil

"""It is important that the functions are run in the order they are written, some rely on previously created files"""

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


def create_a_mod_file(mod_name, mod_tags: list, game_version, mod_version, path_to_documents):
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
    mod_file_template = r"data/template.mod"
    mod_file_new = f"user_data/template.mod"
    shutil.copyfile(mod_file_template, mod_file_new)
    mod_file = open(f"user_data/template.mod")
    mod_file.write(descriptor_template + f'\npath = "{path_to_documents}/Paradox Interactive/Hearts of Iron IV/mod/test"')
    os.makedirs(f"user_data/{mod_name}/common/countries")
    os.mkdir(f"user_data/{mod_name}/common/country_tags")
    descriptor_file = open(f"user_data/{mod_name}/descriptor.mod", "w+")  # create the descriptor file
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
    if not os.path.exists(f"user_data/{mod_name}/history/countries"):
        os.makedirs(f"user_data/{mod_name}/history/countries")
    if not os.path.exists(f"user_data/{mod_name}/history/states"):
        os.mkdir(f"user_data/{mod_name}/history/states")
    history_file = open(f"user_data/{mod_name}/history/countries/{template}.txt", "w+")
    history_file.close()


def set_nation_capital(mod_name, country_tag, country_name, country_capital):
    template = f"capital = {country_capital}"
    country_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    country_file_content = country_file.read()
    country_file.close()
    ever_line_in_file = country_file_content.split("\n")
    ever_line_in_file.insert(0, template)
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    new_country_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "w+")
    ever_line_in_file.append("\n")
    for i in range(len(ever_line_in_file)):
        new_country_file.write(ever_line_in_file[i])


def assign_nation_states(mod_name, country_tag, desired_territory: list, core: bool, controls: bool):
    list_of_state_files = os.listdir("data/history/states")
    list_of_state_tags = []
    owner_template = f"\t\towner = {country_tag}"
    core_template = f"\t\tadd_core_of = {country_tag}"
    for v in range(len(desired_territory)):
        for i in range(len(list_of_state_files)):
            list_of_state_tags.append(list_of_state_files[i].split("-")[0])
        state_file_index = list_of_state_tags.index(desired_territory[v])
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
        if os.path.isfile(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}"):
            os.remove(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}")
        state_file = open(f"user_data/{mod_name}/history/states/{list_of_state_files[state_file_index]}", "w+")
        for x in range(len(every_line_in_template)):
            state_file.write(every_line_in_template[x] + "\n")
        state_file.close()


# fix the error where this duplicates if run more than once and every function below
def set_tech_and_convoys(mod_name, country_tag, country_name, starting_tech: list, convoys):
    user_data_template = ["# Starting tech", "set_technology = {", "}", "", f"set_convoys = {convoys}"]
    for i in range(len(starting_tech)):
        user_data_template.insert(2, "\t" + starting_tech[i])
    history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    history_file_content = history_file.read()
    every_line_in_history = history_file_content.split("\n")

    for i in range(len(user_data_template)):
        every_line_in_history.append(user_data_template[i])

    new_history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt", "w+")
    for i in range(len(every_line_in_history)):
        new_history_file.write(every_line_in_history[i] + "\n")
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    os.rename(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt",
              f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")


def set_1939_start(mod_name, country_tag, country_name):
    start_1939_file = open("data/history/countries/1939_template.txt", "r")
    start_1939_content = start_1939_file.read()
    every_line_in_1939_start = start_1939_content.split("\n")
    country_history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    country_history_content = country_history_file.read()
    every_line_in_history = country_history_content.split("\n")
    for i in range(len(every_line_in_1939_start)):
        every_line_in_history.append(every_line_in_1939_start[i])
    new_history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt", "w+")
    for i in range(len(every_line_in_history)):
        new_history_file.write(every_line_in_history[i] + "\n")
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    os.rename(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt",
              f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")


def set_political_popularity(mod_name, country_name, country_tag, ideology_popularity: dict, start_game):
    ideologies = ["democratic", "fascism", "communism", "neutrality"]
    lookers = {"1939": "\tset_popularities = {", "1936": "set_popularities = {"}
    file_location = "data/history/countries/politics.txt"
    time_period = "1936"
    indentation = "\t"
    if not start_game:
        file_location = "data/history/countries/1939_politics.txt"
        time_period = "1939"
        indentation = "\t\t"

    political_popularity_template = open(file_location)
    political_popularity_content = political_popularity_template.read()
    every_line_in_file = political_popularity_content.split("\n")
    for i in range(len(every_line_in_file)):
        if every_line_in_file[i] == lookers[time_period]:
            for c in range(len(ideologies)):
                every_line_in_file.insert(i + 1, f"{indentation}{ideologies[c]} = {ideology_popularity[ideologies[c]]}")
    history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    history_content = history_file.read()
    every_line_in_history = history_content.split("\n")
    new_history_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt", "w+")
    for i in range(len(every_line_in_file)):
        every_line_in_history.append(every_line_in_file[i])
    for i in range(len(every_line_in_history)):
        new_history_file.write(every_line_in_history[i] + "\n")
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    os.rename(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt",
              f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")


def set_politics(mod_name, country_name, country_tag, ruling_ideology, game_start):
    elections_allowed = "no"
    indentation = "\t\t"
    template_file = open("data/history/countries/1939_policies.txt")
    if game_start:
        template_file = open("data/history/countries/policies.txt")
        indentation = "\t"
    if ruling_ideology == "democratic":
        elections_allowed = "yes"
    government = [f"ruling_party = {ruling_ideology}", 'last_election = "1936.1.1"', "election_frequency = 48",
                  f"elections_allowed = {elections_allowed}"]
    template_content = template_file.read()
    every_line_in_template = template_content.split("\n")
    looker = "set_politics"
    for i in range(len(every_line_in_template)):
        if looker in every_line_in_template[i].split():
            for c in range(len(government)):
                every_line_in_template.insert(i + 1, f"{indentation}{government[c]}")
    for i in range(len(every_line_in_template)):
        print(every_line_in_template[i])
    original_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    original_content = original_file.read()
    every_line_in_original = original_content.split("\n")
    for i in range(len(every_line_in_template)):
        every_line_in_original.append(every_line_in_template[i])
    new_history = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt", "w+")
    for i in range(len(every_line_in_original)):
        new_history.write(every_line_in_original[i] + "\n")
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    os.rename(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt",
              f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")


def create_new_leader(mod_name, country_tag, country_name, leader_name, ideology):
    template = ["create_country_leader = {", f'\tname = "{leader_name}"', '\tdesc = ""',
                f'\tpicture = "{leader_name}.dds"', f"\tideology = {ideology}",
                "\ttraits = {", "\t\t#",
                "\t}", "}", " "]
    original_file = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt", "r")
    original_content = original_file.read()
    every_line_in_original = original_content.split("\n")
    template.reverse()
    for i in range(len(every_line_in_original)):
        if "1939.1.1" in every_line_in_original[i].split():
            for x in range(len(template)):
                every_line_in_original.insert(i, template[x])
            break
    os.remove(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")
    new_history = open(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt", "w+")
    for i in range(len(every_line_in_original)):
        new_history.write(every_line_in_original[i] + "\n")
    new_history.close()
    os.rename(f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}2.txt",
              f"user_data/{mod_name}/history/countries/{country_tag} - {country_name}.txt")


def assign_leader_portrait(mod_name, country_tag, leader_name):
    os.makedirs(f"user_data/{mod_name}/gfx/leaders/{country_tag}")
    leader_portrait = Image.open(f"user_portraits/{leader_name}.png")
    new_height = 210
    new_width = 156
    new_size = leader_portrait.resize((new_width, new_height))
    new_size.save(f"user_portraits/{leader_name}.png")
    os.rename(f"user_portraits/{leader_name}.png", f"user_data/{mod_name}/gfx/leaders/{country_tag}/{leader_name}.dds")


def set_country_flag(mod_name, country_tag, ideology):
    if not os.path.isfile(f"user_data/{mod_name}/gfx/flags"):
        os.makedirs(f"user_data/{mod_name}/gfx/flags/medium")
        os.mkdir(f"user_data/{mod_name}/gfx/flags/small")
    leader_portrait = Image.open(f"user_flags/{country_tag}_{ideology}.png")
    standard_dimensions = {"height": 52, "width": 82}
    medium_dimensions = {"height": 26, "width": 41}
    small_dimensions = {"height": 7, "width": 10}
    standard = leader_portrait.resize((standard_dimensions["width"], standard_dimensions["height"]))
    medium = leader_portrait.resize((medium_dimensions["width"], medium_dimensions["height"]))
    small = leader_portrait.resize((small_dimensions["width"], small_dimensions["height"]))
    standard_32 = standard.convert("RGBA")
    medium_32 = medium.convert("RGBA")
    small_32 = small.convert("RGBA")
    standard_32.save(f"user_data/{mod_name}/gfx/flags/{country_tag}_{ideology}.tga")
    medium_32.save(f"user_data/{mod_name}/gfx/flags/medium/{country_tag}_{ideology}.tga")
    small_32.save(f"user_data/{mod_name}/gfx/flags/small/{country_tag}_{ideology}.tga")


def localisation(mod_name, country_tag, country_name, country_name_f, country_name_c, country_name_d, country_name_n):
    country_name_adjective = f"{country_name}n"
    template = [
        f' {country_tag}_fascism:0 "{country_name_f}"',
        f' {country_tag}_fascism_DEF:0 "{country_name_f}"',
        f' {country_tag}_democratic:0 "{country_name_d}"',
        f' {country_tag}_democratic_DEF:0 "{country_name_d}"',
        f' {country_tag}_neutrality:1 "{country_name_n}"',
        f' {country_tag}_neutrality_DEF:1 "{country_name_f}"',
        f' {country_tag}_communism:0 "{country_name_c}"',
        f' {country_tag}_communism_DEF:0 "{country_name_c}"',
        f' {country_tag}_fascism_ADJ:0 "{country_name_adjective}"',
        f' {country_tag}_democratic_ADJ:0 "{country_name_adjective}"',
        f' {country_tag}_neutrality_ADJ:0 "{country_name_adjective}"',
        f' {country_tag}_communism_ADJ:0 "{country_name_adjective}"',
        f' {country_tag}:0 "{country_name}"',
        f' {country_tag}_DEF:0 "{country_name}"',
        f' {country_tag}_ADJ:0 "{country_name}"']
    if os.path.isfile(f"user_data/{mod_name}/localisation/countries_l_english.yml"):
        localisation_file_template = open(f"user_data/{mod_name}/localisation/countries_l_english.yml")
        localisation_file_content = localisation_file_template.read()
        every_line_in_localisation = localisation_file_content.split("\n")
        for i in range(len(every_line_in_localisation)):
            if every_line_in_localisation[i].strip() == f'{country_tag}_fascism:0 "{country_name_f}"':
                for c in range(len(template)):
                    del every_line_in_localisation[i]
                break
        for i in range(len(template)):
            every_line_in_localisation.append(template[i])
    else:
        os.mkdir(f"user_data/{mod_name}/localisation")
        localisation_file_template = open(f"data/localisation/countries_l_english.yml", "r")
        localisation_file_content = localisation_file_template.read()
        every_line_in_localisation = localisation_file_content.split("\n")
        for i in range(len(template)):
            every_line_in_localisation.append(template[i])
    for i in range(len(every_line_in_localisation)):
        if every_line_in_localisation[i].strip() == "":
            del every_line_in_localisation[i]
            break
    new_localisation_file = open(f"user_data/{mod_name}/localisation/countries_l_english.yml", "w+")
    for i in range(len(every_line_in_localisation)):
        new_localisation_file.write(every_line_in_localisation[i] + "\n")

