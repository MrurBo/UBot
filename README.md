# UBoat Bot

UBoat Bot is a Discord bot designed to manage game statistics, teams, and player data for a game portal. It provides features such as user authentication, game performance tracking, and administrative commands for managing teams and stats.

## Features

- **Discord Integration**: Commands for managing teams, stats, and more.
- **Game Statistics Dashboard**: A web interface to view game performance and player stats.
- **Admin Tools**: Commands for adding/removing admins and modifying player stats.
- **User Authentication**: Login and registration system for accessing the dashboard.
- **Database Management**: Persistent storage for player data, game stats, and admin credentials.

## Project Structure

```
UBoat Bot/
├── dbman/                 # Database management module
│   └── __init__.py        # Workspace class for database operations
├── templates/             # HTML templates for the web interface
│   ├── login.html         # Login page
│   └── index.html         # Dashboard page
├── .gitignore             # Git ignore file
├── db.json                # JSON file for storing database data
├── main.py                # Main bot script
└── README.md              # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Discord bot token
- Flask (for web interface)
- Chart.js (for rendering charts in the dashboard)
- Bootstrap 5 (for styling)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/UBoat-Bot.git
   cd UBoat-Bot
   ```

2. **Install Docker (skip this step if already installed)**:
   Install Docker on your system via:
   ```bash
   winget install --id Docker.DockerDesktop
   ```
   or on Linux (Debain);
   ```bash
   sudo apt install docker
   ```

3. **Build the Docker Image**:
   Build the Docker Image via
   ```bash
   docker build
   ```

4. **Run the Bot**:
   Start the bot using the following command:
   ```bash
   docker run -p 5000:5000 -p 8080:8080 (the file name generated)
   ```

5. **Access the Web Interface**:
   Open your browser and navigate to the appropriate URL (e.g., `http://localhost:5000`) to access the dashboard.

## Usage

### Discord Commands

- `/hi`: Say hi to the bot.
- `/join`: Join a team (Axis or Allies).
- `/add_admin`: Add a new admin (admin-only).
- `/remove_admin`: Remove an admin (admin-only).
- `/setstat`: Modify a player's stats (admin-only).
- `/stats`: View a player's stats.
- `/board`: Display the current game board (admin-only).
- `/ping`: Check the bot's latency.

### Web Interface

- **Login Page**: Authenticate using your username and password.
- **Dashboard**: View game performance, recent activity, and achievements.

## Database

The bot uses a JSON file (`db.json`) to store data such as:
- Admin credentials
- Player statistics
- Current game data

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please contact the project maintainer at `your-email@example.com`.