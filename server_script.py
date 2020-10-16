from flask import Flask, render_template, url_for, redirect, request, flash, send_file
import forms
import os
import shutil
import admin
import webbrowser
from script import *

# all variables that the survey will process
list_of_tags = ["AFG", "ALB", "ARG", "AST", "AUS", "BEL", "BHU", "BOL", "BRA", "MAL", "RAJ", "BUL", "CHL", "CHI", "COL",
                "PRC", "COS", "CUB", "CZE", "DEN", "DOM", "CAN", "INS", "ECU", "ELS", "EST", "ETH", "FIN", "FRA", "GER",
                "GRE", "GXC", "GUA", "HAI", "HON", "PER", "IRQ", "IRE", "ITA", "JAP", "HUN", "ROM", "LAT", "LIB", "LIT",
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

mod_name = ""
path = ""
pie = {}
list_of_countries = []
country_tags = {}
country_names_f = {}
country_names_d = {}
country_names_c = {}
country_names_n = {}
ruling_ideologies = {}
country_color = {}
cultures = {}
cored_owned_territory = {}
cored_not_owned_territory = {}
occupied_owned_territory = {}
leader_name_d = {}
leader_name_f = {}
leader_name_c = {}
leader_name_n = {}
current_country = ""
capital = {}
message = []
ALLOWED_EXTS = ["jpg", "jpeg", "png"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "78cbbe98d4ba83b97ee3e569c46e81da915da48434257baebdd47980e0be2d30a5532211fe16ce146ed8a110d" \
                           "b5588e1deeb022677bc60b38aeb895795b05159698fff89646b1eebccb4eb97ccfaf7174f1e2857c19f02440a" \
                           "07c9af3f04834ddb5bb7fb6561f753d416d0f09023e28cda13621ae8bacb6df85e9dff6a6270df"


@app.route("/", methods=["GET", "POST"])
@app.route("/new-mod", methods=["GET", "POST"])
def new_mod():
    global mod_name, path
    form = forms.Create_new_mod_form()
    if form.validate_on_submit():
        path_split = form.path.data.split("/")
        if path_split[0] != "C:" or path_split[len(path_split)-1] != "Documents":
            message.append(flash("Make sure your path is the same format is the example"))
            return render_template("new_mod.html", title="New Mod", form=form, message=message)
        else:
            mod_name = form.mod_name.data
            path = form.path.data
            return redirect(url_for('new_country'))
    return render_template("new_mod.html", title="New Mod", form=form)


@app.route("/new-country", methods=["GET", "POST"])
def new_country():
    global list_of_countries, country_tags, cultures, ruling_ideologies, current_country,\
        country_names_c, country_names_d, country_names_f, country_names_n, country_color, pie
    form = forms.Create_New_Country()

    if form.validate_on_submit():
        rgb = form.RGB_color.data
        rgb_list = rgb.split()
        not_number = False
        out_of_bounds = False
        errors = False
        for i in range(len(rgb_list)):
            if not rgb_list[i].isnumeric():
                not_number = True
            else:
                if int(rgb_list[i]) < 0 or int(rgb_list[i]) > 255:
                    out_of_bounds = True
        if form.country_tag.data in list_of_tags:
            message.append(flash("This tag already exists, please choose a unique one"))
            errors = True
        if not_number:
            message.append(flash("Please ensure you have three RGB numerical values"))
            errors = True
        if out_of_bounds:
            message.append(flash("Please ensure all RGB values are equal to or between 1 and 255"))
            errors = True
        if len(rgb.split()) > 3:
            message.append(flash("Please ensure your RGB values are in the same format as the example"))
            errors = True
        if len(form.country_tag.data) != 3:
            message.append(flash("Please ensure your country tag is only three letters long"))
            errors = True
        if not form.country_tag.data.isalpha():  # doesn't work
            message.append(flash("Please ensure your country tag is only letters"))
            errors = True
        if not errors:
            list_of_countries.append(form.country_name.data)  # add to nation to the list
            country_tags[form.country_name.data] = form.country_tag.data
            current_country = form.country_name.data
            cultures[form.country_name.data] = form.culture.data
            ruling_ideologies[form.country_name.data] = form.ruling_ideology.data

            ideologies = ["democratic", "fascism", "communism", "neutrality"]
            print(ruling_ideologies[form.country_name.data])
            for i in range(len(ideologies)):
                if ideologies[i] == ruling_ideologies[form.country_name.data].lower():
                    pie[ideologies[i]] = 70
                else:
                    pie[ideologies[i]] = 10
            print(pie)
            country_names_n[form.country_name.data] = form.country_name_neutral.data  # non-aligned nation name
            country_names_f[form.country_name.data] = form.country_name_fascist.data  # fascist nation name
            country_names_c[form.country_name.data] = form.country_name_communist.data  # communist nation name
            country_names_d[form.country_name.data] = form.country_name_democratic.data  # democratic nation name
            rgb_data = form.RGB_color.data.split()  # country color
            rgb_data_formatted = {"{" + f" {rgb_data[0]}", f" {rgb_data[1]}", f" {rgb_data[2]}" + " }"}
            country_color[form.country_name.data] = rgb_data_formatted
            return redirect(url_for("set_territory"))
        return render_template("create_new_nation.html", title="New Country", form=form, messages=message)
    return render_template("create_new_nation.html", title="New Country", form=form)


@app.route("/set_territory", methods=["GET", "POST"])
def set_territory():
    global cored_not_owned_territory, cored_owned_territory, occupied_owned_territory, capital
    form = forms.Set_Territory()
    if form.validate_on_submit():
        capital[current_country] = form.nations_capital.data.strip()
        cored_owned_territory[current_country] = form.cored_owned.data.split()
        occupied_owned_territory[current_country] = form.cored_not_owned.data.split()
        cored_not_owned_territory[current_country] = form.occupied_not_owned.data.split()

        return redirect(url_for("create_leaders"))
    return render_template("territory.html", title="Set Territory", form=form)


@app.route("/create-leaders", methods=["GET", "POST"])
def create_leaders():
    global leader_name_c, leader_name_d, leader_name_f, leader_name_n
    existing_leaders = []
    for i in range(len(list_of_countries)-1):
        existing_leaders.append(leader_name_f[list_of_countries[i]])
        existing_leaders.append(leader_name_c[list_of_countries[i]])
        existing_leaders.append(leader_name_d[list_of_countries[i]])
        existing_leaders.append(leader_name_n[list_of_countries[i]])
    form = forms.Create_Leader()
    if form.validate_on_submit():
        leader_name_n[current_country] = form.Leader_Name_n.data
        leader_name_f[current_country] = form.Leader_Name_f.data
        leader_name_c[current_country] = form.Leader_Name_c.data
        leader_name_d[current_country] = form.Leader_Name_d.data
        if leader_name_n in existing_leaders or leader_name_d in existing_leaders or leader_name_c in existing_leaders \
                or leader_name_f in existing_leaders:
            note = flash("Please ensure you have not used this name in another country")
            return render_template("leader_names.html", message=note)

        return redirect(url_for("new_leader_portrait_d"))

    return render_template("leader_names.html", title="New Leaders", form=form)


@app.route("/new-leader-portraits-d", methods=["GET", "POST"])
def new_leader_portrait_d():
    ideology_letter = "d"
    leader_name_insert = leader_name_d[current_country]
    if request.method == "POST":
        democratic_portrait = request.files["file_d"]
        democratic_portrait.save(os.path.join("user_portraits", democratic_portrait.filename))
        os.rename(f"user_portraits/{democratic_portrait.filename}", f"user_portraits/{leader_name_insert}.png")
        return redirect(url_for("new_leader_portrait_f"))
    return render_template("new_leader_portrait.html",ideology_letter=ideology_letter, leader=leader_name_insert)


@app.route("/new-leader-portraits-f", methods=["GET", "POST"])
def new_leader_portrait_f():
    ideology_letter = "f"
    leader_name_insert = leader_name_f[current_country]
    if request.method == "POST":
        fascist_portrait = request.files["file_d"]
        fascist_portrait.save(os.path.join("user_portraits", fascist_portrait.filename))
        os.rename(f"user_portraits/{fascist_portrait.filename}", f"user_portraits/{leader_name_insert}.png")
        return redirect(url_for("new_leader_portrait_c"))
    return render_template("new_leader_portrait.html", ideology_letter=ideology_letter, leader=leader_name_insert)


@app.route("/new-leader-portraits-c", methods=["GET", "POST"])
def new_leader_portrait_c():
    ideology_letter = "c"
    leader_name_insert = leader_name_c[current_country]
    if request.method == "POST":
        communist_portrait = request.files["file_d"]
        communist_portrait.save(os.path.join("user_portraits", communist_portrait.filename))
        os.rename(f"user_portraits/{communist_portrait.filename}", f"user_portraits/{leader_name_insert}.png")
        return redirect(url_for("new_leader_portrait_n"))
    return render_template("new_leader_portrait.html", ideology_letter=ideology_letter, leader=leader_name_insert)


@app.route("/new-leader-portraits-n", methods=["GET", "POST"])
def new_leader_portrait_n():
    ideology_letter = "n"
    leader_name_insert = leader_name_n[current_country]
    if request.method == "POST":
        non_aligned_portrait = request.files["file_d"]
        non_aligned_portrait.save(os.path.join("user_portraits", non_aligned_portrait.filename))
        os.rename(f"user_portraits/{non_aligned_portrait.filename}", f"user_portraits/{leader_name_insert}.png")
        return redirect(url_for("choose_flag_d"))
    return render_template("new_leader_portrait.html", ideology_letter=ideology_letter, leader=leader_name_insert)


@app.route("/choose-flag-d", methods=["GET", "POST"])
def choose_flag_d():
    ideology_letter = "d"
    messages = f"{current_country}'s Democratic Flag"
    if request.method == "POST":
        democratic_flag = request.files["file_flag"]
        democratic_flag.save(os.path.join("user_flags", democratic_flag.filename))
        os.rename(f"user_flags/{democratic_flag.filename}",
                  f"user_flags/{country_tags[current_country]}_democratic.png")
        return redirect(url_for("choose_flag_f"))
    return render_template("new_flag.html", ideology_letter=ideology_letter, message=messages)


@app.route("/choose-flag-f", methods=["GET", "POST"])
def choose_flag_f():
    ideology_letter = "f"
    messages = f"{current_country}'s Fascist Flag"
    if request.method == "POST":
        fascist_flag = request.files["file_flag"]
        fascist_flag.save(os.path.join("user_flags", fascist_flag.filename))
        os.rename(f"user_flags/{fascist_flag.filename}",
                  f"user_flags/{country_tags[current_country]}_fascism.png")
        return redirect(url_for("choose_flag_c"))
    return render_template("new_flag.html", ideology_letter=ideology_letter, message=messages)


@app.route("/choose-flag-c", methods=["GET", "POST"])
def choose_flag_c():
    ideology_letter = "c"
    messages = f"{current_country}'s Communist Flag"
    if request.method == "POST":
        communist_flag = request.files["file_flag"]
        communist_flag.save(os.path.join("user_flags", communist_flag.filename))
        os.rename(f"user_flags/{communist_flag.filename}",
                  f"user_flags/{country_tags[current_country]}_communism.png")
        return redirect(url_for("choose_flag_n"))
    return render_template("new_flag.html", ideology_letter=ideology_letter, message=messages)


@app.route("/choose-flag-n", methods=["GET", "POST"])
def choose_flag_n():
    ideology_letter = "n"
    note = f"{current_country}'s Non-Aligned Flag"
    if request.method == "POST":
        neutral_flag = request.files["file_flag"]
        neutral_flag.save(os.path.join("user_flags", neutral_flag.filename))
        os.rename(f"user_flags/{neutral_flag.filename}",
                  f"user_flags/{country_tags[current_country]}_neutrality.png")
        return redirect(url_for("save_or_repeat"))
    return render_template("new_flag.html", ideology_letter=ideology_letter, message=note)


@app.route("/save",  methods=["GET", "POST"])
def save_or_repeat():
    nations = []
    for i in range(len(list_of_countries)):
        nations.append({"nation_name": list_of_countries[i]})
    if "open" in request.form:
        print("Here")
        return redirect(url_for("new_country"))
    elif "close" in request.form:
        print("Here")
        return redirect(url_for("finish"))
    print(nations)
    return render_template("save.html", nations=nations)


@app.route("/finish")
def finish():
    create_a_mod_file(mod_name, ["Events"], "1.9.3", "1", path)
    for i in range(len(list_of_countries)):
        country_selected = list_of_countries[i]

        create_new_nation(mod_name, country_selected, cultures[country_selected], country_color[country_selected])
        assign_nation_tag(mod_name, country_tags[country_selected], country_selected)
        assign_nation_color(mod_name, country_tags[country_selected], country_color[country_selected])
        create_history_file(mod_name, country_tags[country_selected], country_selected)
        set_nation_capital(mod_name, country_tags[country_selected], country_selected, capital[country_selected])
        assign_nation_states(mod_name, country_tags[country_selected], cored_owned_territory[country_selected],
                             True, True)
        if country_selected in cored_not_owned_territory.keys():
            assign_nation_states(mod_name, country_tags[country_selected], cored_not_owned_territory[country_selected],
                                 True, False)
        if country_selected in occupied_owned_territory:
            assign_nation_states(mod_name, country_tags[country_selected], occupied_owned_territory[country_selected],
                                 False, True)
        set_tech_and_convoys(mod_name, country_tags[country_selected], country_selected, [], "60")
        set_1939_start(mod_name, country_tags[country_selected], country_selected)
        set_politics(mod_name, country_selected, country_tags[country_selected], ruling_ideologies[country_selected], True)
        set_political_popularity(mod_name, country_selected, country_tags[country_selected], pie, True)
        set_politics(mod_name, country_selected, country_tags[country_selected], ruling_ideologies[country_selected], False)
        set_political_popularity(mod_name, country_selected, country_tags[country_selected], pie, False)
        create_new_leader(mod_name, country_tags[country_selected], country_selected, leader_name_d[country_selected], "liberalism")  # democratic leader
        assign_leader_portrait(mod_name, country_tags[country_selected], leader_name_d[country_selected])
        create_new_leader(mod_name, country_tags[country_selected], country_selected, leader_name_n[country_selected], "despotism")  # neutral leader
        assign_leader_portrait(mod_name, country_tags[country_selected], leader_name_n[country_selected])
        create_new_leader(mod_name, country_tags[country_selected], country_selected, leader_name_c[country_selected], "stalinism")  # communist leader
        assign_leader_portrait(mod_name, country_tags[country_selected], leader_name_c[country_selected])
        create_new_leader(mod_name, country_tags[country_selected], country_selected, leader_name_f[country_selected], "nazism")  # fascist leader
        assign_leader_portrait(mod_name, country_tags[country_selected], leader_name_f[country_selected])
        set_country_flag(mod_name, country_tags[country_selected], "democratic")
        set_country_flag(mod_name, country_tags[country_selected], "fascism")
        set_country_flag(mod_name, country_tags[country_selected], "communism")
        set_country_flag(mod_name, country_tags[country_selected], "neutrality")
        localisation(mod_name, country_tags[country_selected], country_selected, country_names_f[country_selected], country_names_c[country_selected],
                     country_names_d[country_selected],
                     country_names_n[country_selected])

        flags = os.listdir("user_flags")
        for c in range(len(flags)):
            if flags[c] == "git_holder.txt":
                pass
            else:
                os.remove(f"user_flags/{flags[c]}")
        shutil.make_archive(f"{mod_name}", 'zip', "user_data")
        download_file = f"{mod_name}.zip"
        os.remove(f"{mod_name}.zip")
        return send_file(download_file, as_attachment=True)
    return render_template("finish.html")


if __name__ == '__main__':
    mod = os.listdir("user_data")

    webbrowser.open("http://127.0.0.1:5000/new-mod")
    app.run(debug=True)
