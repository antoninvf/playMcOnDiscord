import asyncio
import os

import logging
import nextcord
import gradio_client
from dotenv import load_dotenv
from pynput.keyboard import Key, Controller
from pyautogui import *

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = nextcord.Client(intents=nextcord.Intents.all())

#gradioclient = gradio_client.Client("http://127.0.0.1:7860/")

bot_ownerid = 222002051960406026

serverId = 735991813168562238
channelId = 994708652747403344

online_message = "Are you ready for Smelvin?"

# a map of key names with boolean values for toggling features on and off
config = {
    "minecraft": False,
    "rvc": False,
}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.get_guild(serverId).get_channel(channelId).send("Are you ready for Smelvin?")

    # check if channel is a voice channel
    if client.get_guild(serverId).get_channel(channelId).type == nextcord.ChannelType.voice:
        await client.get_guild(serverId).get_channel(channelId).connect()


async def msg(string):
    await client.get_guild(serverId).get_channel(channelId).send(string)


async def write(string):
    keyboard = Controller()
    for char in string:
        keyboard.press(char)
        await asyncio.sleep(0.1)
        keyboard.release(char)


async def speak(string):
    voice = "markiplier"
    speed = 0
    edge_voice = "en-US-EricNeural-Male"
    transpose = -5
    pitch_method = "rmvpe"
    index_rate = 0.5
    protect = 0.33
    fn_index = 0

    #job = gradioclient.submit(voice, speed, string, edge_voice, transpose, pitch_method, index_rate, protect, fn_index=fn_index)

    # TODO: MAKE IT WORK

    #if client.voice_clients:
    #    vc = client.voice_clients[0]
    #    vc.play(nextcord.FFmpegPCMAudio(job.result()[2]))


async def hold(key, howlong):
    keyDown(key)
    await asyncio.sleep(howlong)
    keyUp(key)


async def holdMouse(howlong):
    mouseDown()
    await asyncio.sleep(howlong)
    mouseUp()


@client.event
async def on_message(m):
    if m.channel.id != channelId:
        return

    print(f'[{m.author}]: {m.content}')

    ##
    # Config checks
    ##
    if config["minecraft"]:
        await minecraft(m)

    if config["rvc"]:
        if m.author.id != client.user.id:
            if m.content.startswith("say"):
                await speak(m.content[4:])

    # Config toggle cmd
    if m.content.startswith("toggle") and m.author.id == bot_ownerid:
        config[m.content.split(" ")[1]] = not config[m.content.split(" ")[1]]
        await client.get_guild(serverId).get_channel(channelId).send(f"{m.content.split(' ')[1]} is now {config[m.content.split(' ')[1]]}")

    # Join VC cmd
    if m.content == "joinvc" and m.author.id == bot_ownerid:
        if client.get_guild(serverId).get_channel(channelId).type == nextcord.ChannelType.voice:
            await client.get_guild(serverId).get_channel(channelId).connect()

    # Leave VC cmd
    if m.content == "leavevc" and m.author.id == bot_ownerid:
        # check if bot is in a voice channel
        if client.voice_clients:
            await client.voice_clients[0].disconnect(force=True)

    # Bot shutdown cmd
    if m.content in ["shutdown", "stop"] and m.author.id == bot_ownerid:
        await client.get_guild(serverId).get_channel(channelId).send("Shutting down...")
        await client.close()
        exit()


##
# Minecraft
##
async def minecraft(m):
    if m.content in ["forwards", "forward", "walk"]:
        await hold("w", 5)

    if m.content in ["jump forwards", "jump forward", "jump walk"]:
        keyDown("space")
        keyDown("w")
        await asyncio.sleep(5)
        keyUp("space")
        keyUp("w")

    if m.content in ["little forwards", "little forward"]:
        await hold("w", 1)

    if m.content in ["little jump forwards", "little jump forward"]:
        keyDown("space")
        keyDown("w")
        await asyncio.sleep(1)
        keyUp("space")
        keyUp("w")

    if m.content in ["backwards", "backward"]:
        await hold("s", 5)

    if m.content in ["little backwards", "little backward"]:
        await hold("s", 1)

    if m.content in ["turn left", "left"]:
        await hold("num4", 0.8)

    if m.content in ["turn right", "right"]:
        await hold("num6", 0.8)

    if m.content in ["look up", "up"]:
        await hold("num8", 0.8)

    if m.content in ["look down", "down"]:
        await hold("num2", 0.8)

    if m.content in ["little turn left", "little left"]:
        await hold("num4", 0.1)

    if m.content in ["little turn right", "little right"]:
        await hold("num6", 0.1)

    if m.content in ["little look up", "little up"]:
        await hold("num8", 0.1)

    if m.content in ["little look down", "little down"]:
        await hold("num2", 0.1)

    if m.content in ["strafe left"]:
        await hold("a", 1)

    if m.content in ["strafe right"]:
        await hold("d", 1)

    if m.content in ["little strafe left"]:
        await hold("a", 0.1)

    if m.content in ["little strafe right"]:
        await hold("d", 0.1)

    if m.content in ["jump", "hop"]:
        await hold("space", 1)

    if m.content in ["jump right click"]:
        keyDown("space")
        mouseDown(button="right")
        await asyncio.sleep(1)
        keyUp("space")
        mouseUp(button="right")

    if m.content in ["crouch", "sneak"]:
        press("shift")

    if m.content in ["left click", "punch", "attack", "click"]:
        click()

    if m.content in ["sprint"]:
        press("ctrl")

    if m.content in ["right click", "place", "use"]:
        click(button="right")

    if m.content in ["hold right click", "eat"]:
        await hold("right", 3)

    if m.content in ["mine"]:
        await holdMouse(5)

    # control inventory
    if m.content in ["inventory"]:
        press("e")

    if m.content in ["drop"]:
        press("q")

    if m.content in ["drop all"]:
        hotkey("ctrl", "q")

    if m.content in ["little mouse up"]:
        moveRel(0, -10, 1)

    if m.content in ["little mouse down"]:
        moveRel(0, 10, 1)

    if m.content in ["little mouse left"]:
        moveRel(-10, 0, 1)

    if m.content in ["little mouse right"]:
        moveRel(10, 0, 1)

    if m.content in ["mouse up"]:
        moveRel(0, -100, 1)

    if m.content in ["mouse down"]:
        moveRel(0, 100, 1)

    if m.content in ["mouse left"]:
        moveRel(-100, 0, 1)

    if m.content in ["mouse right"]:
        moveRel(100, 0, 1)

    # control hotbar
    if m.content in ["hotbar 1", "slot 1"]:
        press("1")

    if m.content in ["hotbar 2", "slot 2"]:
        press("2")

    if m.content in ["hotbar 3", "slot 3"]:
        press("3")

    if m.content in ["hotbar 4", "slot 4"]:
        press("4")

    if m.content in ["hotbar 5", "slot 5"]:
        press("5")

    if m.content in ["hotbar 6", "slot 6"]:
        press("6")

    if m.content in ["hotbar 7", "slot 7"]:
        press("7")

    if m.content in ["hotbar 8", "slot 8"]:
        press("8")

    if m.content in ["hotbar 9", "slot 9"]:
        press("9")


client.run(TOKEN)
