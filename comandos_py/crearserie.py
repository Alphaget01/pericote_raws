import discord
from discord import app_commands
from discord.ext import commands
from utils.firestore_initiator import db  # Asegúrate de que Firestore esté configurado correctamente

class CrearSerie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función de autocompletado para "serie" (canales)
    async def autocompletar_canales(self, interaction: discord.Interaction, current: str):
        canales = [channel for channel in interaction.guild.channels if isinstance(channel, discord.TextChannel)]
        # Filtrar canales por el texto introducido
        return [
            app_commands.Choice(name=channel.name, value=str(channel.id))
            for channel in canales if current.lower() in channel.name.lower()
        ][:25]  # Limitar a 25 opciones

    # Función de autocompletado para "dia"
    async def autocompletar_dias(self, interaction: discord.Interaction, current: str):
        opciones_dias = [
            "Lunes/Monday", "Martes/Tuesday", "Miércoles/Wednesday", 
            "Jueves/Thursday", "Viernes/Friday", "Sábado/Saturday", "Domingo/Sunday"
        ]
        return [
            app_commands.Choice(name=dia, value=dia)
            for dia in opciones_dias if current.lower() in dia.lower()
        ]

    # Función de autocompletado para "precio"
    async def autocompletar_precios(self, interaction: discord.Interaction, current: str):
        opciones_precios = ["1.5 usd", "0 usd"]
        return [
            app_commands.Choice(name=precio, value=precio)
            for precio in opciones_precios if current.lower() in precio.lower()
        ]

    @app_commands.command(name="crearserie", description="Registra una nueva serie en la base de datos")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1308266941135327253, 841509684174520340, 818273252531109919)
    async def crearserie(
        self,
        interaction: discord.Interaction,
        serie: str,  # ID del canal seleccionado
        nombre: str,
        link: str,
        dia: str,
        precio: str
    ):
        try:
            # Obtener el canal real a partir del ID
            canal = interaction.guild.get_channel(int(serie))
            if not canal:
                await interaction.response.send_message("El canal seleccionado no es válido.", ephemeral=True)
                return

            canal_nombre = canal.name  # Nombre del canal seleccionado

            # Guardar en Firestore
            db.collection('nuevasseries').add({
                'id_canal': serie,  # ID del canal
                'serie': f"#{canal_nombre}",  # Guardar con formato de canal
                'nombre': nombre,  # Nombre proporcionado por el usuario
                'link': link,
                'dia': dia,
                'precio': precio
            })
            embed = discord.Embed(
                title="Serie registrada",
                description="Serie registrada para las raws correctamente",
                color=0xFFD700  # Color dorado
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"No se pudo registrar la serie: {e}",
                color=0xFF0000  # Color rojo para errores
            )
            await interaction.response.send_message(embed=embed)

    # Enlace del autocompletado para "serie"
    @crearserie.autocomplete('serie')
    async def autocompletar_serie(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_canales(interaction, current)

    # Enlace del autocompletado para "dia"
    @crearserie.autocomplete('dia')
    async def autocompletar_dia(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_dias(interaction, current)

    # Enlace del autocompletado para "precio"
    @crearserie.autocomplete('precio')
    async def autocompletar_precio(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_precios(interaction, current)

async def setup(bot):
    await bot.add_cog(CrearSerie(bot))
