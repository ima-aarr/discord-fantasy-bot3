import discord, json
from discord import app_commands
from discord.ext import commands
from core.auth import is_owner
from core import db
class AdminCog(commands.Cog):
    def __init__(self, bot): self.bot=bot
    async def _owner_check(self, interaction: discord.Interaction):
        if not is_owner(interaction.user.id):
            await interaction.response.send_message('権限がありません（Owner限定）。', ephemeral=True); return False
        return True
    @app_commands.command(name='owner_get', description='Owner: get DB path')
    async def owner_get(self, interaction: discord.Interaction, path: str):
        if not await self._owner_check(interaction): return
        await interaction.response.defer()
        data = db.get(path)
        await interaction.followup.send(f'``\n{json.dumps(data, ensure_ascii=False, indent=2)}\n``')
    @app_commands.command(name='owner_set', description='Owner: set DB path')
    async def owner_set(self, interaction: discord.Interaction, path: str, value: str):
        if not await self._owner_check(interaction): return
        await interaction.response.defer()
        try:
            v = json.loads(value)
        except:
            v = value
        db.put(path, v); await interaction.followup.send('OK')
    @app_commands.command(name='owner_stop', description='Owner: stop bot')
    async def owner_stop(self, interaction: discord.Interaction):
        if not await self._owner_check(interaction): return
        await interaction.response.defer()
        await interaction.followup.send('Stopping...'); await self.bot.close()
async def setup(bot): await bot.add_cog(AdminCog(bot))
