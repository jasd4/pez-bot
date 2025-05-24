import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from spotify_client import sp
import requests

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def songinfo(ctx, *, query: str):
    results = sp.search(q=query, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        name = track["name"]
        artist = track["artists"][0]["name"]
        album = track["album"]["name"]
        url = track["external_urls"]["spotify"]

        response = f"🎵 **{name}**\n👤 Artist: {artist}\n💿 Album: {album}\n🔗 {url}"
    else:
        response = "No track found for your search."

    await ctx.send(response)



@bot.command()
async def lyrics(ctx, *, query: str):
    results = sp.search(q=query, type="track", limit=1)
    if not results["tracks"]["items"]:
        await ctx.send("No track found.")
        return

    track = results["tracks"]["items"][0]
    title = track["name"]
    artist = track["artists"][0]["name"]


    api_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        lyrics_text = data.get("lyrics", "Lyrics not found.")
        
        # If too long, trim
        if len(lyrics_text) > 1900:
            lyrics_text = lyrics_text[:1900] + "\n...(truncated)"

        await ctx.send(f"**Lyrics for {title} by {artist}:**\n```{lyrics_text}```")
    else:
        await ctx.send(f"Sorry, no lyrics found for {title} by {artist}.")
    
    

   
   


bot.run(TOKEN)
