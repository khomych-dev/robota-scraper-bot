# Robota.ua Scraper Bot

A Telegram bot designed to automatically scrape the [robota.ua](https://robota.ua/) job portal, specifically searching for Python vacancies suitable for beginners (Juniors, Trainees, Interns, or those without experience). The bot periodically checks for fresh vacancies and alerts you directly in Telegram.

## Features
- **Automated Scraping:** Uses the robota.ua GraphQL API to fetch the latest Python vacancies.
- **Smart Filtering:** Filters listings to find those ideal for beginners (keywords: junior, trainee, intern, no experience, etc.).
- **Deduplication:** Keeps track of previously seen vacancies in a local SQLite database (`vacancies.db`) so you're only notified of *new* opportunities.
- **Scheduled Checks:** Employs `apscheduler` to routinely perform background checks and dispatch alerts.
- **Modern Tech Stack:** Built with Python 3.12+, `aiogram` 3.x, and `uv` for dependency management.

## Prerequisites
- Python 3.12+
- `uv` (Fast Python package and project manager)

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/khomych-dev/robota-scraper-bot.git
   cd robota-scraper-bot
   ```

2. **Set up the environment variables:**
   Create a `.env` file in the root directory and configure it with your Telegram bot token and admin ID:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ADMIN_ID=your_telegram_user_id_here
   ```

3. **Install dependencies using `uv`:**
   ```bash
   uv sync
   ```

## Running the Bot

To start the bot and the scheduler, run:
```bash
uv run python main.py
```

## Running Tests and Linting

The project is configured with `ruff` (linter/formatter), `mypy` (type checking), and `pytest` (testing). You can run them as follows:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest
```

## How It Works
- Sending the `/start` command will greet you.
- Sending the `/search` command will trigger an immediate manual search for new Python job postings and notify you.
- Background jobs will automatically scrape the platform on an interval, storing seen jobs in `vacancies.db`.
