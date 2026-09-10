import os


# =========================
# DATABASE
# =========================

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

# Railway gives postgresql://
# Old Tortoise version requires postgres://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgres://", 1)

TORTOISE = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "models.misc",
                "models",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}


# =========================
# EXTENSIONS
# =========================

EXTENSIONS = [
    "cogs.esports",
    "cogs.events",
    "cogs.mod",
    "cogs.premium",
    "cogs.quomisc",
    "cogs.reminder",
    "cogs.utility",
]


# =========================
# DISCORD
# =========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()

if DISCORD_TOKEN.startswith("Bot "):
    DISCORD_TOKEN = DISCORD_TOKEN[4:].strip()


# =========================
# BASIC CONFIG
# =========================

COLOR = 0x00FFB3
FOOTER = "Shinchan Never Die!"
PREFIX = "q"
PRIME_EMOJI = "⚡"

OWNER_ID = "..."
DEVS = []


# =========================
# SERVER
# =========================

SERVER_LINK = "https://discord.gg/vcVVr7GdU"

SERVER_ID = 0

TOURNEY_CSV_CHANNEL = 0

EMOJIS_SERVER = []


# =========================
# BOT INVITE
# =========================

BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=1547597946286243921"


# =========================
# ACTIVITIES
# =========================

ACTIVITIES = [
    {
        "type": "playing",
        "name": "scrims across {servers} servers"
    },
    {
        "type": "listening",
        "name": "strategic calls from {members} players"
    },
    {
        "type": "watching",
        "name": "tournament brackets update in real time"
    },
    {
        "type": "competing",
        "name": "to lead the eSports automation arena"
    },
    {
        "type": "streaming",
        "name": "live event analytics",
        "url": "https://twitch.tv/Shinchan"
    },
]


# =========================
# LOGS
# =========================

SHARD_LOG = "..."

ERROR_LOG = "..."

PUBLIC_LOG = "https://discord.com/api/webhooks/1547625152957911091/tL92DiZ_aDViSopupDdDgLhH3tzID8BJ1F7bGYjuuQpfzqo5bThWfMZSFrkT3mIxSNV1"


# =========================
# OTHER
# =========================

WEBSITE = "https://github.com/CycloneAddons/Shinchan-Legacy"

REPOSITORY = "https://github.com/CycloneAddons/Shinchan-Legacy"

FASTAPI_URL = "https://ocr.gfxvisual.xyz"

FASTAPI_KEY = "cyclonestrongsecret"
