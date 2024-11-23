import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
client = discord.Client(intents=discord.Intents.all())

# サーバー情報の入力
# 「"」や「'」で囲わず、IDのみ入力　例： GUILD_ID = 0000000000000000000

GUILD_ID = 
WEL_ID   = 
DC_ID    = 
VC_ID    = 



# 起動時の処理

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Game(name="サーバー監視中☆"))

# コンソール出力用
    print("Botは正常に起動しました")
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('---------------------------')



#サーバーへの参加

@client.event
async def on_member_join(member):
    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(WEL_ID)
    now = datetime.utcnow() + timedelta(hours=9)

    embed = discord.Embed(
                          title="サーバーへようこそ☆",
                          color=0xfff2ff,
                          url="https://example.com"
                          )
 
    embed.set_thumbnail(url=f"{member.display_avatar.url}")
    embed.add_field(name="参加したユーザー",value=f"{member.name}")
    embed.add_field(name="参加日時",value=now.strftime('%Y /%m / %d　%H : %M'), inline=True)

    await channel.send(embed=embed)



#サーバーからの脱退

@client.event
async def on_member_remove(member):
    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(DC_ID)

    now = datetime.utcnow() + timedelta(hours=9)

    embed = discord.Embed(
                          title="サーバーからユーザーが脱退しました",
                          color=0xf5051d,
                          url="https://example.com"
                          )
 
    embed.set_thumbnail(url=f"{member.display_avatar.url}")
    embed.add_field(name="脱退したユーザー",value=f"{member.name}")
    embed.add_field(name="脱退日時",value=now.strftime('%Y /%m / %d　%H : %M'), inline=True)

    await channel.send(embed=embed) 



#VC入室＆退室

@client.event
async def on_voice_state_update(member, before, after): 
    if member.guild.id == GUILD_ID and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = client.get_channel(VC_ID)

        # 入室処理

        if before.channel is None: 

            embed = discord.Embed(
                title="VC入室通知",
                color=0xb5f1ff,
                url="https://example.com"
                                        )

            embed.set_thumbnail(url=f"{member.display_avatar.url}")
            embed.add_field(name="チャンネル",value=f"{after.channel.name}")
            embed.add_field(name="ユーザー",value=f"{member.name}")
            embed.add_field(name="入室時刻",value=now.strftime('%Y /%m / %d　%H : %M'), inline=True)         
            
            await alert_channel.send(embed=embed)

        # 退室処理

        elif after.channel is None: 

            embed = discord.Embed(
                title="VC退室通知",
                color=0xd8b5ff,
                url="https://example.com"
                                        )
            
            embed.set_thumbnail(url=f"{member.display_avatar.url}")
            embed.add_field(name="チャンネル",value=f"{before.channel.name}")
            embed.add_field(name="ユーザー",value=f"{member.name}")
            embed.add_field(name="退室時刻",value=now.strftime('%Y /%m / %d　%H : %M'), inline=True)
            
            await alert_channel.send(embed=embed)



client.run(os.environ["TOKEN"])