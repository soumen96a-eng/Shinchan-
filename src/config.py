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

DISCORD_TOKEN = "..."

COLOR = 0x00FFB3
FOOTER = "Shinchan Never Die!"
PREFIX = "q"
PRIME_EMOJI = "⚡"
OWNER_ID = "..."
DEVS = []

SERVER_LINK = "https://discord.gg/vcVVr7GdU"
SERVER_ID = 0
TOURNEY_CSV_CHANNEL = 0
EMOJIS_SERVER = []

BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=1547597946286243921"

ACTIVITIES = [
    {"type": "playing", "name": "scrims across {servers} servers"},
    {"type": "listening", "name": "strategic calls from {members} players"},
    {"type": "watching", "name": "tournament brackets update in real time"},
    {"type": "competing", "name": "to lead the eSports automation arena"},
    {"type": "streaming", "name": "live event analytics", "url": "https://twitch.tv/Shinchan"},
]

SHARD_LOG = "..."
ERROR_LOG = "..."
PUBLIC_LOG = "..."

WEBSITE = "https://github.com/CycloneAddons/Shinchan-Legacy"
REPOSITORY = "https://github.com/CycloneAddons/Shinchan-Legacy"
FASTAPI_URL = "https://ocr.gfxvisual.xyz"
FASTAPI_KEY = "cyclonestrongsecret"
