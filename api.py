from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import dbman
import hmac
import hashlib

# An api wrapper to add U-Boat games to the db to be accesed from the bot and wesbsite.
# Will be fexible for columns. first column is the id of the game, 2nd will be the amount of axis players, 3rd will be the amount of allies players, 4th will be uboats, 5th will be ships, 6th will be a list of steamid's, 6th will be axis score, 7th will be allies score. the rest will be added later.

workspace = dbman.Workspace("games")
passwords = dbman.Workspace("passwords")
app = Flask(__name__)
app.secret_key = "rahh"


def generate_user_token(username, password):
    # Create a secret key (store this securely in your application)

    # Combine username and password with a delimiter
    message = f"{username}:{password}".encode("utf-8")

    # Create HMAC using SHA-256
    token = hmac.new(
        app.secret_key.encode(), msg=message, digestmod=hashlib.sha256
    ).hexdigest()

    return token


@app.route("/api/v1/add_game", methods=["GET"])
def add_game():
    game_id = request.args.get("game_id")
    axis = request.args.get("axis")
    allies = request.args.get("allies")
    uboats = request.args.get("uboats")
    ships = request.args.get("ships")
    steamids = request.args.get("steamids")
    axis_score = request.args.get("axis_score")
    allies_score = request.args.get("allies_score")

    if not game_id or not axis or not allies or not uboats or not ships or not steamids:
        return "Missing parameters", 400

    workspace.set(
        game_id, [axis, allies, uboats, ships, steamids, axis_score, allies_score]
    )
    return "Game added", 200


@app.route("/api/v1/update_scores", methods=["GET"])
def update_scores():
    game_id = request.args.get("game_id")
    axis = request.args.get("axisScore")
    allies = request.args.get("alliesScore")

    if not game_id or not axis or not allies:
        return "Missing parameters", 400

    game = workspace.get(game_id)
    if not game:
        return "Game not found", 404

    game[5] = axis
    game[6] = allies
    workspace.set(game_id, game)
    return "Scores updated", 200


# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # use new passwords workspace
        if passwords.get(username) == None:
            return "Invalid username or password", 401
        if passwords.get(username) != password:
            return "Invalid username or password", 401
        session["logged_in"] = True
        session["username"] = username
        session["token"] = generate_user_token(username, password)
        return redirect(url_for("index"))
    # if the user is already logged in, redirect to index

    return render_template("login.html")


# logout page
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


# change password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        print(request.form)
        old_password = request.form["currentPassword"]
        new_password = request.form["newPassword"]
        new_password_repeat = request.form["confirmPassword"]
        if passwords.get(session["username"]) != old_password:
            return "Invalid password", 401
        if new_password != new_password_repeat:
            return "Passwords do not match", 401
        # update password in the passwords workspace
        return redirect(url_for("index"))
    return render_template("change_password.html")


@app.route("/")
def index():
    # redirect to login if not logged in
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
