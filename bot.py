import sys
import os
import asyncio
import datetime
import subprocess
import discord

from discord.ext import commands

# -------------------
# |Utility Functions|
# -------------------

# File IO

def read_file(path):
    f = open(path, 'r')
    data = f.read().split('\n')
    f.close()
    return data
    
def write_append_file(path, data):
    f = open(path, 'a')
    f.write(data)

def write_file(path, data):
    f = open(path, 'w')
    f.write(data)

def create_file(path):
    f = open(path, 'w+')
    f.close


# Lightly formatted logging macro

# Creates a log with a timestamp
today = datetime.datetime.now()
LOG_PATH = "./logs/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + " " + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second) + ".log"

def init_log():
    create_file(LOG_PATH)

def log(prefix, str, is_error, log_path):
    if(is_error):
        error(prefix + ": " + str)
        write_append_file(LOG_PATH, prefix + ": " + str + "\n")
        return
    print(prefix + ": " + str)
    write_append_file(LOG_PATH, prefix + ": " + str + "\n")
        
def performance(str):
    log("PERF", str, False, LOG_PATH)
    
def debug(str):
    log("DEBG", str, False, LOG_PATH)
    
def info(str):
    log("INFO", str, False, LOG_PATH)
    
def warning(str):
    log("WARN", str, True, LOG_PATH)
    
def error(str):
    log("EROR", str, True, LOG_PATH)
    
def fatal(str):
    log("FATL", str, True, LOG_PATH)
    exit(-1)

init_log()

# Reads and catagorizes generic project data

PROJECTDATA_PATH = "./projectdata"
PROJECTDATA = read_file(PROJECTDATA_PATH)
NAME = PROJECTDATA[0]
AUTHOR = PROJECTDATA[1]
VERSION = PROJECTDATA[2]
LANGUAGE_PATH = PROJECTDATA[3]
BOTDATA = PROJECTDATA[4]
IMAGE_DATA = PROJECTDATA[5]

# Reads private bot data - file excluded from git

BOTDATA = read_file(BOTDATA)
TOKEN = BOTDATA[0]
PREFIX = BOTDATA[1]

# Loads language specified by command line args, otherwise loads language specified in project data

LANGUAGE_FILE_EXTENSION = ".lang"
LANGUAGE = read_file(read_file(LANGUAGE_PATH)[0] + LANGUAGE_FILE_EXTENSION)
info("Using language " + LANGUAGE[0] + " from project data. Change language by editing " + LANGUAGE_PATH)

def set_language(path):
    global LANGUAGE
    LANGUAGE = read_file(path)
    write_file(LANGUAGE_PATH, '.' + path.split('.')[1])

info(NAME + " version " + VERSION + " initialized")

# -----------------------
# |Discord Functionality|
# -----------------------

# Magic bot stuff the Library author told me to do
class SoulBot(commands.Bot):
    async def on_ready(self):
        info("Soul Bot has connected to Discord successfully!")
        info("Command prefix is set to " + PREFIX)
        
    async def on_message(self, message):
        write_append_file("time_recorder", message.content + '\n')
        if(message.author.bot): 
            return
        
        if '++' in message.content:
            if "Emily" in message.author.name:
                return await bot.process_commands(message)
            else:
                return
        return await bot.process_commands(message)

bot = SoulBot(command_prefix=PREFIX)
# I agree with Ash
bot.remove_command("help")

# Ping command
@bot.command(name = LANGUAGE[1])
async def ping(ctx):
    debug("Pinged by " + ctx.author.name)
    await ctx.send(LANGUAGE[2])

# Help command
@bot.command(name = LANGUAGE[3])
async def help(ctx):
    await ctx.send('>>> ```' + NAME + LANGUAGE[13] + VERSION + '\n\n' + LANGUAGE[14] + '\n\n' + LANGUAGE[15] + PREFIX + '\n' + LANGUAGE[16] + '\n\n' + LANGUAGE[17] + '\n\n' + LANGUAGE[18] + '\n\n' + LANGUAGE[19] + '\n\n' + LANGUAGE[20] + "```")

# Displays the last day of images
@bot.command(name = LANGUAGE[5])
async def display(ctx):
    should_return = False

    m = today.month
    while(m > 0):

        d = today.day
        while(d > 0):

            for f in os.listdir(IMAGE_DATA):
                if(f.endswith(".jpg")):

                    image_date = f.split('-')
                    if(m == int(image_date[1]) and d == int(image_date[2].split('_')[0])):
                        should_return = True
                        await ctx.send(file = discord.File(IMAGE_DATA + "/" + f))

            if(should_return):
                return
            d -= 1

        m -= 1

# Fetches images from Instagram
@bot.command(name = LANGUAGE[7])
async def fetch(ctx):
    await ctx.send(LANGUAGE[8])
    subprocess.Popen("instaloader --fast-update sole_nyu".split(), stdout=subprocess.PIPE)
    await ctx.send(LANGUAGE[9])

# Change the language
@bot.command(name = LANGUAGE[10])
async def language(ctx, arg0):
    global bot
    if(arg0 + LANGUAGE_FILE_EXTENSION in os.listdir("./res/lang/")):
        set_language("./res/lang/" + arg0 + LANGUAGE_FILE_EXTENSION)
        await ctx.send(LANGUAGE[11] + LANGUAGE[0])
        return
    await ctx.send(LANGUAGE[12] + arg0)

# Test all functions
@bot.command(name = "+DEBUG_TESTALL")
async def test_all(ctx):
    await ping(ctx)

    for f in os.listdir("./res/lang/"):
        await language(ctx, f.split('.')[0])
    
    set_language("./res/lang/en-gb.lang")

    await fetch(ctx)

    await display(ctx)

bot.run(TOKEN)