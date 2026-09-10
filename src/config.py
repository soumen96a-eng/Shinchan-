import os


# ============================================================
# DISCORD
# ============================================================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL", "")

# Railway uses postgresql://
# This Tortoise version expects postgres://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgres://",
        1
    )

TORTOISE = {
    "connections": {
        "default": DATABASE_URL
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


# ============================================================
# EXTENSIONS
# ============================================================

EXTENSIONS = [
    "cogs.esports",
    "cogs.events",
    "cogs.mod",
    "cogs.premium",
    "cogs.quomisc",
    "cogs.reminder",
    "cogs.utility",
]


# ============================================================
# BOT SETTINGS
# ============================================================

COLOR = 0x00FFB3
FOOTER = "Shinchan Never Die!"
PREFIX = "q"
PRIME_EMOJI = "⚡"


# ============================================================
# OWNER / DEVELOPERS
# ============================================================

OWNER_ID = 0
DEVS = []


# ============================================================
# SERVER SETTINGS
# ============================================================

SERVER_LINK = ""
SERVER_ID = 0
TOURNEY_CSV_CHANNEL = 0

EMOJIS_SERVER = []


# ============================================================
# BOT INVITE
# ============================================================

BOT_INVITE = ""


# ============================================================
# ACTIVITIES
# ============================================================

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


# ============================================================
# LOGS
# ============================================================

SHARD_LOG = ""
ERROR_LOG = ""
PUBLIC_LOG = ""


# ============================================================
# FASTAPI
# ============================================================

FASTAPI_URL = "https://ocr.gfxvisual.xyz"
FASTAPI_KEY = ""


# ============================================================
# OTHER SETTINGS
# ============================================================

VOTER_ROLE = 0

PREMIUM_ROLE = 0
PREMIUM_AVATAR = ""
PRO_LINK = ""

SERVER_PORT = 8888


# ============================================================
# PAYU
# ============================================================

PAYU_KEY = ""
PAYU_SALT = ""
PAYU_PAYMENT_LINK = ""

SUCCESS_URL = ""
FAILED_URL = ""


# ============================================================
# SOCKET / GUILD LOGS
# ============================================================

GUILD_LOGS = ""

SOCKET_URL = ""
SOCKET_AUTH = ""


# ============================================================
# RILP
# ============================================================

RILP_PREMIUM = ""
RILP_HEADERS = {}
