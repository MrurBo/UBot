import os
import secrets
from flask import Flask, redirect, url_for, session, request, render_template
from flask_discord import DiscordOAuth2Session
from dotenv import load_dotenv
import dbman

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

playerData = dbman.Workspace("playerData")

# Development settings (remove in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Discord OAuth config
app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = os.environ["DISCORD_REDIRECT_URI"]

# Initialize Flask-Discord with proper state handling
discord = DiscordOAuth2Session(app)


@app.route("/login")
def login():
    """Start OAuth flow with automatic state management"""
    session.clear()
    return discord.create_session(scope=["identify"])


@app.route("/callback")
def callback():
    """Handle OAuth callback with library-managed state verification"""
    try:
        discord.callback()  # Let the library handle state verification
        user = discord.fetch_user()

        session.update(
            {
                "logged_in": True,
                "user_id": user.id,
                "username": user.name,
                "avatar_url": user.avatar_url or "",
            }
        )

        return redirect(url_for("index"))

    except Exception as e:
        return f"Authentication failed: {str(e)}", 400


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template(
        "index.html",
        username=session["username"],
        avatar_url=session["avatar_url"],
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# api


@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "user_id is required"}, 400
    data = playerData.get(str(user_id))
    if data is None:
        return {"error": "User not found"}, 404
    return data, 200


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True, port=8080)
