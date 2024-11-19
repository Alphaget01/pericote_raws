import discord
from discord.ext import commands
from discord import app_commands
import logging
import os
from dotenv import load_dotenv
from utils.firestore_initiator import db  # Asegúrate de que 'db' esté importado correctamente.

# Cargar variables de entorno
load_dotenv()

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurar permisos del bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="$pericote ", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"{bot.user.name} ha iniciado sesión en Discord")

    # Cargar extensiones (comandos)
    extensiones = [
        "comandos_py.crearserie",
        "comandos_py.getlink",
        "comandos_py.addregister",
        "comandos_py.verregistro",
        "comandos_py.pagoraws",
        "comandos_prefijos.prefijos"
    ]

    for extension in extensiones:
        try:
            await bot.load_extension(extension)
            logging.info(f"Extensión '{extension}' cargada correctamente.")
        except commands.ExtensionAlreadyLoaded:
            logging.warning(f"La extensión '{extension}' ya estaba cargada.")
        except commands.ExtensionError as e:
            logging.error(f"Error al cargar la extensión '{extension}': {e}")
        except Exception as e:
            logging.error(f"Error inesperado al cargar '{extension}': {e}")

    # Sincronización de comandos slash global
    try:
        synced = await bot.tree.sync()
        logging.info(f"Comandos slash globales sincronizados correctamente: {len(synced)} comandos.")
        for command in synced:
            logging.info(f"Comando sincronizado: {command.name}")
    except discord.errors.HTTPException as e:
        logging.error(f"Error HTTP al sincronizar comandos slash: {e.status} - {e.text}")
    except Exception as e:
        logging.error(f"Error al sincronizar comandos slash: {e}")

# Ejecutar el bot con el token de Discord desde el archivo .env
bot.run(os.getenv("DISCORD_TOKEN"))
