import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()

if DISCORD_TOKEN.startswith("Bot "):
    DISCORD_TOKEN = DISCORD_TOKEN[4:].strip()


TORTOISE = {
    "connections": {
        "default": "postgres://username:password@host/db_name",
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


EXTENSIONS = [
    "cogs.esports",
    "cogs.events",
    "cogs.mod",
    "cogs.premium",
    "cogs.quomisc",
    "cogs.reminder",
    "cogs.utility",
]


COLOR = 0x00FFB3
FOOTER = "Shinchan Never Die!"
PREFIX = "q"
PRIME_EMOJI = "⚡"

OWNER_ID = 0
DEVS = []

SERVER_LINK = ""
SERVER_ID = 0
TOURNEY_CSV_CHANNEL = 0
EMOJIS_SERVER = []

BOT_INVITE = ""


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


SHARD_LOG = ""
ERROR_LOG = ""
PUBLIC_LOG = ""


FASTAPI_URL = "https://ocr.gfxvisual.xyz"
FASTAPI_KEY = ""


VOTER_ROLE = 0

PREMIUM_ROLE = 0
PREMIUM_AVATAR = ""
PRO_LINK = ""

SERVER_PORT = 8888

PAYU_KEY = ""
PAYU_SALT = ""
PAYU_PAYMENT_LINK = ""

SUCCESS_URL = ""
FAILED_URL = ""

GUILD_LOGS = ""

SOCKET_URL = ""
SOCKET_AUTH = ""

RILP_PREMIUM = ""
RILP_HEADERS = {}
