import discord
from discord import app_commands
from discord.ext import commands
from utils.firestore_initiator import db  # Asegúrate de que Firestore esté configurado correctamente

class VerRegistro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función de autocompletado para "mes"
    async def autocompletar_meses(self, interaction: discord.Interaction, current: str):
        # Opciones de meses predefinidos
        opciones_meses = [
            "octubre2024", "noviembre2024", "diciembre2024", "enero2025"
        ]
        # Si no hay texto en el campo, devuelve todas las opciones
        meses_filtrados = opciones_meses if not current else [mes for mes in opciones_meses if current.lower() in mes.lower()]
        return [
            app_commands.Choice(name=mes, value=mes) for mes in meses_filtrados
        ]

    @app_commands.command(name="verregistro", description="Ver registros de raws por mes")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(841509684174520340, 818273252531109919)
    async def verregistro(self, interaction: discord.Interaction, mes: str):
        try:
            # Consultar Firestore para obtener registros del mes seleccionado
            query = db.collection('registroderaws').where('mes', '==', mes).stream()
            registros = [doc.to_dict() for doc in query]

            if not registros:
                await interaction.response.send_message(f"No se encontraron registros para el mes: {mes}")
                return

            # Crear embed con los registros encontrados
            embed = discord.Embed(
                title=f"Registro de las raws del {mes}",
                description=f"Hay un total de raws registradas en {mes}: {len(registros)}",
                color=0x00FF00
            )

            for idx, registro in enumerate(registros, start=1):
                # Buscar el precio correspondiente desde "nuevasseries"
                nombre = registro.get('nombre', 'Nombre no definido')
                consulta_precio = db.collection('nuevasseries').where('nombre', '==', nombre).stream()
                precio = "No definido"

                for serie_doc in consulta_precio:
                    precio = serie_doc.to_dict().get('precio', 'No definido')
                    break  # Solo necesitamos el primer resultado

                # Añadir los datos al embed
                embed.add_field(
                    name=f"{idx}. {nombre}",
                    value=(
                        f"**Chapter:** {registro.get('chapter', 'No definido')}\n"
                        f"**Precio:** {precio}"
                    ),
                    inline=False
                )

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"No se pudo obtener el registro: {e}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed)

    # Enlace del autocompletado para "mes"
    @verregistro.autocomplete('mes')
    async def autocompletar_mes(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_meses(interaction, current)

async def setup(bot):
    await bot.add_cog(VerRegistro(bot))
