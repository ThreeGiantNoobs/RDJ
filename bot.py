import os
import json

import interactions
from interactions import Client, listen, slash_command
from dotenv import load_dotenv

from utils import get_song


load_dotenv()

with open('config.json') as config_file:
    config = json.load(config_file)

GUILDS = config['SERVERS']
PREFIX = config['PREFIX']

bot = Client(
    token=os.getenv('DISCORD_TOKEN'),
    default_scope=GUILDS
)


@listen()
async def on_startup():
    print('Bot is online')
    await bot.get_channel(channel_id=837582224361652237).send(f'<@{bot.user.id}> has connected to Discord!')


@slash_command(name='join', description="Join the voice channel you are in")
async def join_voice_channel(ctx):
    await ctx.defer()
    voice_client = ctx.author.voice
    if voice_client:
        await voice_client.channel.connect()
        await ctx.send(f'Joined <#{voice_client.channel.id}>')
    else:
        await ctx.send('You are not in a voice channel')


@slash_command(name='play', description="Play a song")
@interactions.slash_option(name="song", description="Song Name or Link", required=True, opt_type=3)
async def play_song(ctx: interactions.SlashContext, song: str = None):
    await ctx.defer()
    if not ctx.voice_state:
        await ctx.author.voice.channel.connect()
    if not song:
        await ctx.send('No song specified')
        return
    audio, url = get_song(song)
    await ctx.send(f'Playing {url}')
    await ctx.voice_state.play(audio)


@slash_command(name='pause', description="Pause the current song")
async def pause_song(ctx: interactions.SlashContext):
    await ctx.defer()
    if ctx.voice_state.playing:
        print("Pausing the song")
        ctx.voice_state.pause()
        await ctx.send('Paused the song')


@slash_command(name='resume', description="Resume the current song")
async def resume_song(ctx: interactions.SlashContext):
    await ctx.defer()
    if ctx.voice_state.paused:
        print("Resuming the song")
        ctx.voice_state.resume()
        await ctx.send('Resumed the song')


@slash_command(name='stop', description="Stop the current song")
async def stop_song(ctx: interactions.SlashContext):
    await ctx.defer()
    if ctx.voice_state.playing or ctx.voice_state.paused:
        print("Stopping the song")
        await ctx.voice_state.stop()
        await ctx.send('Stopped the song')


@slash_command(name='leave', description="Leave the voice channel")
async def leave_voice_channel(ctx: interactions.SlashContext):
    await ctx.defer()
    if ctx.voice_state:
        await ctx.voice_state.disconnect()
        await ctx.send('Left voice channel')
    else:
        await ctx.send('I am not in a voice channel')

bot.start()
