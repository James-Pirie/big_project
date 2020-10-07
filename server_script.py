from flask import Flask, render_template, url_for, redirect
import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "78cbbe98d4ba83b97ee3e569c46e81da915da48434257baebdd47980e0be2d30a5532211fe16ce146ed8a110d" \
                           "b5588e1deeb022677bc60b38aeb895795b05159698fff89646b1eebccb4eb97ccfaf7174f1e2857c19f02440a" \
                           "07c9af3f04834ddb5bb7fb6561f753d416d0f09023e28cda13621ae8bacb6df85e9dff6a6270df"

ALLOWED_EXTS = {"jpg", "jpeg", "png"}


mod = [{
    "Author": "Corey Schafer",
    "Mod_Name": "Kaiserreich",
    "Tags": ["Events", "Alternate History"],
    "Upload_Date": 'Jan 1, 1936'

},
{
    "Author": "James Pirie",
    "Mod_Name": "Old World Blues",
    "Tags": ["Events", "Alternate History"],
    "Upload_Date": 'Oct 21, 1949'

}
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('main.html', title="home", mods=mod)


@app.route("/about")
def about():
    return "about"


@app.route("/new-mod", methods=["GET", "POST"])
def new_mod():
    form = forms.Create_new_mod_form()
    if form.validate_on_submit():
        return redirect(url_for('new_country'))
    return render_template("new_mod.html", title="New Mod", form=form)


@app.route("/new-country", methods=["GET", "POST"])
def new_country():
    form = forms.Create_New_Country()
    if form.validate_on_submit():
        return redirect(url_for("set_territory"))
    return render_template("create_new_nation.html", title="New Country", form=form)


@app.route("/set-territroy", methods=["GET", "POST"])
def set_territory():
    form = forms.Set_Territory()
    return render_template("territory.html", title="Set Territory", form=form)


@app.route("/new-leader", methods=["GET", "POST"])
def new_leader():
    form = forms.Create_Leader()
    ideology = "Fascist"


    return render_template("new_leader.html", title="New Leader", form=form, ideology=ideology)


if __name__ == '__main__':
    app.run(debug=True)