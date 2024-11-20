import discord
from discord.ext import commands
import asyncio

class Prefijos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "$pericote"  # Prefijo inicial

    @commands.command()
    async def saluda(self, ctx):
        """Comando para saludar."""
        embed = discord.Embed(
            title="Saludos",
            description="El prefijo de este comando funciona bien",
            color=0x00FF00  # Verde
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def cambiar_prefijo(self, ctx):
        """Comando para cambiar el prefijo."""
        await ctx.send("¿Cuál es el nuevo prefijo? (Usa `$` + alguna palabra, por ejemplo: `$kk`)")

        # Esperar el mensaje del usuario con el nuevo prefijo
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            message = await self.bot.wait_for('message', check=check, timeout=30.0)
            nuevo_prefijo = message.content.strip()

            if not nuevo_prefijo.startswith("$"):
                await ctx.send("El prefijo debe comenzar con `$`. Inténtalo de nuevo.")
                return

            self.prefix = nuevo_prefijo
            embed = discord.Embed(
                title="Prefijo cambiado",
                description=f"El nuevo prefijo es: `{self.prefix}`",
                color=0xFFD700  # Dorado
            )
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send("Se agotó el tiempo para cambiar el prefijo.")

    @commands.command()
    async def rm(self, ctx, tiempo: str):
        """Comando para recordatorios."""
        try:
            # Convertir el tiempo proporcionado a segundos
            unidad = tiempo[-1]
            cantidad = int(tiempo[:-1])
            if unidad == 's':
                delay = cantidad
            elif unidad == 'm':
                delay = cantidad * 60
            elif unidad == 'h':
                delay = cantidad * 3600
            else:
                await ctx.send("Formato de tiempo inválido. Usa 's', 'm' o 'h'.")
                return

            # Confirmación en el canal donde se ejecutó el comando
            confirm_embed = discord.Embed(
                title="Recordatorio Actualizado",
                description="Dentro del tiempo que me has dado Voy a recodarle",
                color=0x00FF00  # Verde
            )
            await ctx.send(embed=confirm_embed)

            # Esperar el tiempo indicado
            await asyncio.sleep(delay)

            # Obtener el canal donde se debe enviar el recordatorio
            target_channel_id = 1308255604778733650  # Canal de destino para el recordatorio
            target_channel = self.bot.get_channel(target_channel_id)

            # Obtener el rol por ID
            role_id = 1308254862584057917  # ID del rol que será mencionado
            role = ctx.guild.get_role(role_id)

            if not target_channel:
                await ctx.send(f"No se encontró el canal con ID {target_channel_id}.")
                return

            if not role:
                await ctx.send(f"No se encontró el rol con ID {role_id}. Asegúrate de que es correcto.")
                return

            # Enviar el mensaje de mención del rol
            await target_channel.send(content=f"{role.mention}")

            # Crear un embed para el recordatorio
            reminder_embed = discord.Embed(
                title="Recordatorio",
                description="# u can get raws today?",
                color=0xFFD700  # Dorado
            )
            await target_channel.send(embed=reminder_embed)

        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"Ha ocurrido un error: {e}",
                color=0xFF0000  # Rojo
            )
            await ctx.send(embed=error_embed)

    @commands.command()
    async def borrar(self, ctx, cantidad: int):
        """Comando para borrar un número específico de mensajes en el canal actual."""
        if cantidad <= 0:
            await ctx.send("Por favor, proporciona un número válido de mensajes para borrar.")
            return

        try:
            await ctx.channel.purge(limit=cantidad)
            embed = discord.Embed(
                title="Borrado Completo",
                description=f"Se han borrado {cantidad} mensajes en este canal.",
                color=0x00FF00  # Verde
            )
            await ctx.send(embed=embed, delete_after=5)  # Borra este mensaje después de 5 segundos
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"No se pudo borrar los mensajes: {e}",
                color=0xFF0000  # Rojo
            )
            await ctx.send(embed=error_embed)

    @commands.command()
    async def borratodo(self, ctx):
        """Comando para borrar todos los mensajes en el canal actual."""
        try:
            await ctx.channel.purge()
            embed = discord.Embed(
                title="Borrado Completo",
                description="Todos los mensajes en este canal han sido borrados.",
                color=0x00FF00  # Verde
            )
            await ctx.send(embed=embed, delete_after=5)  # Borra este mensaje después de 5 segundos
        except Exception as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"No se pudo borrar los mensajes: {e}",
                color=0xFF0000  # Rojo
            )
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Prefijos(bot))
