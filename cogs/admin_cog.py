import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from core import db, rate_limit, audit

OWNER_ID = os.getenv("OWNER_ID")  # あなたのユーザーID

class AdminOwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(interaction):
        return str(interaction.user.id) == OWNER_ID


    # ===========================================================
    # ① データ編集系
    # ===========================================================

    @app_commands.command(name="admin_set_stat", description="(OWNER) 任意ユーザーのステータスを変更")
    async def admin_set_stat(self, interaction: discord.Interaction, user: str, key: str, value: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用です", ephemeral=True)

        path = f"users/{user}"
        data = db.get(path) or {}

        # 数値変換
        try:
            if value.isdigit():
                value = int(value)
        except:
            pass

        data[key] = value
        db.put(path, data)

        await interaction.response.send_message(f"🔧 `{user}` の `{key}` を `{value}` に更新しました")


    @app_commands.command(name="admin_get_data", description="(OWNER) ユーザーデータ参照")
    async def admin_get_data(self, interaction: discord.Interaction, user: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        data = db.get(f"users/{user}")
        if data is None:
            return await interaction.response.send_message("データなし")

        await interaction.response.send_message(f"```\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```")


    @app_commands.command(name="admin_delete_user", description="(OWNER) ユーザーデータ完全削除")
    async def admin_delete_user(self, interaction: discord.Interaction, user: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        db.delete(f"users/{user}")
        await interaction.response.send_message(f"🗑 `{user}` をデータベースから削除しました")


    # ===========================================================
    # ② 国操作
    # ===========================================================

    @app_commands.command(name="admin_set_country_stat", description="(OWNER) 国データ編集")
    async def admin_set_country_stat(self, interaction: discord.Interaction, country_id: str, key: str, value: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        path = f"countries/{country_id}"
        data = db.get(path) or {}

        if value.isdigit():
            value = int(value)

        data[key] = value
        db.put(path, data)

        await interaction.response.send_message(f"🏰 国 `{country_id}` の `{key}` を `{value}` に変更しました")


    # ===========================================================
    # ③ ゲームチート系
    # ===========================================================

    @app_commands.command(name="admin_give_item", description="(OWNER) 任意ユーザーにアイテム付与")
    async def admin_give_item(self, interaction: discord.Interaction, user: str, item: str, amount: int = 1):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        path = f"users/{user}/inventory"
        inv = db.get(path) or {}

        inv[item] = inv.get(item, 0) + amount
        db.put(path, inv)

        await interaction.response.send_message(f"`{user}` に `{item} x{amount}` を付与しました")


    @app_commands.command(name="admin_add_money", description="(OWNER) お金増減")
    async def admin_add_money(self, interaction: discord.Interaction, user: str, amount: int):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        path = f"users/{user}"
        data = db.get(path) or {}

        data["money"] = data.get("money", 0) + amount
        db.put(path, data)

        await interaction.response.send_message(f"`{user}` の所持金を `{amount:+}` 変更しました")


    @app_commands.command(name="admin_heal", description="(OWNER) HP 全回復")
    async def admin_heal(self, interaction: discord.Interaction, user: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        path = f"users/{user}"
        data = db.get(path) or {}

        data["hp"] = data.get("max_hp", 100)
        db.put(path, data)

        await interaction.response.send_message(f"`{user}` の HP を全回復しました")


    @app_commands.command(name="admin_revive", description="(OWNER) 死亡状態から復活させる")
    async def admin_revive(self, interaction: discord.Interaction, user: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        path = f"users/{user}"
        data = db.get(path) or {}

        data["dead"] = False
        db.put(path, data)

        await interaction.response.send_message(f"`{user}` を復活させました")


    @app_commands.command(name="admin_reset_cooldown", description="(OWNER) 行動クールダウンをリセット")
    async def admin_reset_cooldown(self, interaction: discord.Interaction, user: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        db.delete(f"rate_limits/users/{user}")
        await interaction.response.send_message(f"⏱ `{user}` のクールダウンをリセットしました")


    # ===========================================================
    # ④ 破壊系
    # ===========================================================

    @app_commands.command(name="admin_wipe_all_data", description="(OWNER) 全データ削除（危険）")
    async def admin_wipe_all(self, interaction: discord.Interaction):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        db.delete("")  # ルートで全部消す
        await interaction.response.send_message("**全データを完全削除しました**（復元不可）")


    @app_commands.command(name="admin_shutdown_bot", description="(OWNER) Bot を停止")
    async def admin_shutdown_bot(self, interaction: discord.Interaction):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        await interaction.response.send_message("Bot を停止します…")
        await self.bot.close()


    # ===========================================================
    # ⑤ Python コード実行
    # ===========================================================

    @app_commands.command(name="admin_exec", description="(OWNER) Python コード実行（危険）")
    async def admin_exec(self, interaction: discord.Interaction, code: str):
        if not AdminOwnerCog.is_owner(interaction):
            return await interaction.response.send_message("OWNER専用", ephemeral=True)

        try:
            result = eval(code)
            await interaction.response.send_message(f"結果:\n```\n{result}\n```")
        except Exception as e:
            await interaction.response.send_message(f"エラー:\n```\n{e}\n```")


async def setup(bot):
    await bot.add_cog(AdminOwnerCog(bot))
