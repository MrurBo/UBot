from flask import Flask, request, jsonify
import dbman
import math
import main


app = Flask(__name__)

currentGame = dbman.Workspace("currentGame")
teams = dbman.Workspace("teams")
currentGame.set("players", {})
teams.set("team1", {})
teams.set("team2", {})
teams.set("team3", {})
teams.set("team4", {})
teams.set("team5", {})
teams.set("team6", {})


@app.route("/api/v1/join_game", methods=["GET"])
def join():
    if currentGame.get("players") == None:
        currentGame.set("players", {})
    old = currentGame.get("players")
    old[str(request.args.get("steamID"))] = {
        "name": request.args.get("name"),
        "team": None,
        "crewID": None,
        "torpedo_hits": 0,
        "ships_disabled": 0,
        "ships_sunk": 0,
        "score": 0,
    }
    currentGame.set("players", old)
    return "", 200


@app.route("/api/v1/update", methods=["GET"])
def update():
    old = currentGame.get("players")
    data = request.args
    old2 = old[str(request.args.get("steamID"))]
    if old2 == None:
        return "", 400
    old2["torpedo_hits"] = int(data.get("torpedo_hits"))
    old2["ships_disabled"] = int(data.get("ships_disabled"))
    old2["ships_sunk"] = int(data.get("ships_sunk"))
    old2["score"] = math.floor(
        old2["torpedo_hits"] * 5 + old2["ships_disabled"] * 20 + old2["ships_sunk"] * 50
    )
    currentGame.set("players", old)
    return "", 200


@app.route("/api/v1/leave_game", methods=["GET"])
def leave():
    old = currentGame.get("players")
    del old[str(request.args.get("steamID"))]
    currentGame.set("players", old)
    return "", 200


@app.route("/api/v1/change_teams", methods=["GET"])
def change_teams():
    old = currentGame.get("players")
    print(request.args)
    old[str(request.args.get("steamID"))]["team"] = request.args.get("team")
    print(old)
    currentGame.set("players", old)
    return "", 200


@app.route("/api/v1/crew_join", methods=["GET"])
def crew_join():
    old2 = currentGame.get("players")
    crews = currentGame.get("crews")
    if old2 == None:
        old2 = {}
    old = old2[str(request.args.get("steamID"))]
    if old == None:
        old = {}
    old["crewID"] = request.args.get("crewID")
    if crews == None:
        crews = {}
    if crews.get(request.args.get("crewID")) == None:
        crews[request.args.get("crewID")] = "Unnamed Crew"
    currentGame.set("players", old2)
    return "", 200


@app.route("/api/v1/crew_rename", methods=["GET"])
def crew_rename():
    crews = currentGame.get("crews")
    if crews == None:
        crews = {}
    crews[request.args.get("crewID")] = request.args.get("name")
    currentGame.set("crews", crews)
    return "", 200


@app.route("/api/v1/stop", methods=["GET"])
def stop():
    old1 = currentGame.get("players")
    old1 = {}
    old2 = currentGame.get("crews")
    old2 = {}
    currentGame.set("players", old1)
    currentGame.set("crews", old2)
    return "", 200


if __name__ == "__main__":
    app.run(port=5000)
