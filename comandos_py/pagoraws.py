import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from utils.firestore_initiator import db  # Asegúrate de que Firestore esté configurado correctamente

class PagoRaws(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función de autocompletado para "mes"
    async def autocompletar_meses(self, interaction: discord.Interaction, current: str):
        opciones_meses = [
            "octubre2024", "noviembre2024", "diciembre2024", "enero2025"
        ]
        meses_filtrados = opciones_meses if not current else [mes for mes in opciones_meses if current.lower() in mes.lower()]
        return [
            app_commands.Choice(name=mes, value=mes) for mes in meses_filtrados
        ]

    @app_commands.command(name="pagoraws", description="Calcula el total de pagos de raws por mes")
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(841509684174520340, 818273252531109919)
    async def pagoraws(self, interaction: discord.Interaction, mes: str):
        try:
            # Consultar Firestore para obtener los registros del mes seleccionado (limitado a 20)
            query = db.collection('registroderaws').where('mes', '==', mes).limit(20).stream()
            registros = [doc.to_dict() for doc in query]

            # Consultar todos los registros para el cálculo total
            query_total = db.collection('registroderaws').where('mes', '==', mes).stream()
            registros_totales = [doc.to_dict() for doc in query_total]

            # Calcular el total de pagos
            total_pago = 0
            for registro in registros_totales:
                nombre = registro.get('nombre', 'Nombre no definido')
                consulta_precio = db.collection('nuevasseries').where('nombre', '==', nombre).stream()
                precio = "No definido"

                for serie_doc in consulta_precio:
                    precio = serie_doc.to_dict().get('precio', 'No definido')
                    if precio != "No definido" and precio != "0 usd":
                        total_pago += 1.5
                    break

            # Crear el embed con los registros de la primera página
            def crear_embed(pagina_actual):
                embed = discord.Embed(
                    title=f"Registro del precio de las raws del {mes}",
                    description=f"Hay un total de {len(registros_totales)} registros.",
                    color=0x00FF00
                )

                # Determinar el rango de registros para la página actual
                inicio = (pagina_actual - 1) * 20
                fin = min(inicio + 20, len(registros_totales))

                # Añadir los registros de la página al embed
                for idx, registro in enumerate(registros_totales[inicio:fin], start=inicio + 1):
                    nombre = registro.get('nombre', 'Nombre no definido')
                    consulta_precio = db.collection('nuevasseries').where('nombre', '==', nombre).stream()
                    precio = "No definido"

                    for serie_doc in consulta_precio:
                        precio = serie_doc.to_dict().get('precio', 'No definido')
                        if precio != "No definido" and precio != "0 usd":
                            break

                    embed.add_field(
                        name=f"{idx}. {nombre}",
                        value=(f"**Chapter:** {registro.get('chapter', 'No definido')}\n"
                               f"**Precio:** {precio}"),
                        inline=False
                    )

                # Añadir el total por todas las raws al final
                embed.add_field(
                    name="Total",
                    value=f"El total por raws en {mes} es: {total_pago:.2f} usd",
                    inline=False
                )

                return embed

            # Calcular el total de páginas
            total_paginas = (len(registros_totales) // 20) + (1 if len(registros_totales) % 20 else 0)

            # Clase para los botones de paginación
            class PaginacionView(View):
                def __init__(self, pagina_actual):
                    super().__init__(timeout=60)
                    self.pagina_actual = pagina_actual
                    self.total_paginas = total_paginas

                @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
                async def pagina_anterior(self, button: Button, interaction: discord.Interaction):
                    if self.pagina_actual > 1:
                        self.pagina_actual -= 1
                        await interaction.response.edit_message(embed=crear_embed(self.pagina_actual), view=self)

                @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
                async def pagina_siguiente(self, button: Button, interaction: discord.Interaction):
                    if self.pagina_actual < self.total_paginas:
                        self.pagina_actual += 1
                        await interaction.response.edit_message(embed=crear_embed(self.pagina_actual), view=self)

            # Crear vista de los botones y el embed para la primera página
            view = PaginacionView(pagina_actual=1)
            await interaction.response.send_message(embed=crear_embed(1), view=view)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"No se pudo calcular el pago: {e}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed)

    # Enlace del autocompletado para "mes"
    @pagoraws.autocomplete('mes')
    async def autocompletar_mes(self, interaction: discord.Interaction, current: str):
        return await self.autocompletar_meses(interaction, current)

async def setup(bot):
    await bot.add_cog(PagoRaws(bot))
