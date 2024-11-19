import discord
from discord import app_commands
from discord.ext import commands
from utils.firestore_initiator import db  # Asegúrate de que Firestore esté configurado correctamente

class AddRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función de autocompletado para "nombre"
    async def autocompletar_nombres(self, interaction: discord.Interaction, current: str):
        # Consultar Firestore para obtener los nombres registrados en "nuevasseries"
        query = db.collection('nuevasseries').stream()
        nombres = [
            doc.to_dict().get('nombre', '').strip()
            for doc in query
            if doc.to_dict().get('nombre', '').strip() and len(doc.to_dict().get('nombre', '').strip()) <= 100
        ]  # Filtrar nombres válidos
        nombres_filtrados = nombres if not current else [nombre for nombre in nombres if current.lower() in nombre.lower()]
        return [
            app_commands.Choice(name=nombre, value=nombre) for nombre in nombres_filtrados[:25]
        ]

    # Función de autocompletado para "mes"
    async def autocompletar_meses(self, interaction: discord.Interaction, current: str):
        opciones_meses = [
            "octubre2024", "noviembre2024", "diciembre2024", "enero2025"
        ]
        meses_filtrados = opciones_meses if not current else [mes for mes in opciones_meses if current.lower() in mes.lower()]
        return [
            app_commands.Choice(name=mes, value=mes) for mes in meses_filtrados
        ]

    @app_commands.command(name="addregister", description="Agrega un registro a la base de datos")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(1308266941135327253, 841509684174520340, 818273252531109919)
    async def addregister(
        self,
        interaction: discord.Interaction,
        nombre: str,
        chapter: int,
        mes: str
    ):
        try:
            # Guardar en Firestore
            db.collection('registroderaws').add({
                'nombre': nombre,
                'chapter': chapter,
                'mes': mes
            })
            embed = discord.Embed(
                title="Registro agregado",
                description=f"Registro agregado correctamente:\n\n**Nombre:** {nombre}\n**Chapter:** {chapter}\n**Mes:** {mes}",
                color=0x00FF00
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"No se pudo agregar el registro: {e}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed)

    # Enlace del autocompletado para "nombre"
    @addregister.autocomplete('nombre')
    async def autocompletar_nombre(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_nombres(interaction, current)

    # Enlace del autocompletado para "mes"
    @addregister.autocomplete('mes')
    async def autocompletar_mes(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_meses(interaction, current)

async def setup(bot):
    await bot.add_cog(AddRegister(bot))
