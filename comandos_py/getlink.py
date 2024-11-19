import discord
from discord import app_commands
from discord.ext import commands
from utils.firestore_initiator import db  # Asegúrate de que Firestore esté configurado correctamente

class GetLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función de autocompletado para "dia"
    async def autocompletar_dias(self, interaction: discord.Interaction, current: str):
        opciones_dias = [
            "Lunes/Monday", "Martes/Tuesday", "Miércoles/Wednesday", 
            "Jueves/Thursday", "Viernes/Friday", "Sábado/Saturday", "Domingo/Sunday"
        ]
        # Filtrar las opciones según lo que escribe el usuario
        return [
            app_commands.Choice(name=dia, value=dia)
            for dia in opciones_dias if current.lower() in dia.lower()
        ]

    @app_commands.command(name="getlink", description="Obtiene los links de raws de un día específico")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1308266941135327253, 841509684174520340, 818273252531109919)
    async def getlink(self, interaction: discord.Interaction, dia: str):
        try:
            # Consultar Firestore
            query = db.collection('nuevasseries').where('dia', '==', dia).stream()
            series = [doc.to_dict() for doc in query]

            if not series:
                await interaction.response.send_message(f"No se encontraron raws para el día {dia}")
                return

            # Crear embed con los resultados
            embed = discord.Embed(title=f"Raws de {dia}", description="Estas son las raws del día:", color=0x00FF00)
            for idx, serie in enumerate(series, start=1):
                embed.add_field(
                    name=f"{idx}. {serie.get('nombre', 'Nombre no definido')}",
                    value=(
                        f"**Serie:** <#{serie['id_canal']}>\n"
                        f"**Link:** [Click here]({serie['link']})"
                    ),
                    inline=False
                )

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"Error al obtener raws: {e}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed)

    # Enlace del autocompletado para "dia"
    @getlink.autocomplete('dia')
    async def autocompletar_dia(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_dias(interaction, current)

async def setup(bot):
    await bot.add_cog(GetLink(bot))
