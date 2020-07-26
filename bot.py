import sys
import asyncio
import datetime
import discord

from discord.ext import commands

# -------------------
# |Utility Functions|
# -------------------

# File IO

def read_file(path):
    f = open(path, "r")
    data = f.read().split('\n')
    f.close()
    return data
    
def write_file(path, data):
    f = open(path, "a")
    f.write(data)

def create_file(path):
    f = open(path, "w+")
    f.close


# Lightly formatted logging macro

# Creates a log with a timestamp
current_time = datetime.datetime.now()
LOG_PATH = "./logs/" + str(current_time.day) + "-" + str(current_time.month) + "-" + str(current_time.year) + " " + str(current_time.hour) + "-" + str(current_time.minute) + "-" + str(current_time.second) + ".log"

def init_log():
    create_file(LOG_PATH)

def log(prefix, str, is_error, log_path):
    if(is_error):
        error(prefix + ": " + str)
        write_file(LOG_PATH, prefix + ": " + str + "\n")
        return
    print(prefix + ": " + str)
    write_file(LOG_PATH, prefix + ": " + str + "\n")
        
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
LANGUAGE = PROJECTDATA[3]
BOTDATA = PROJECTDATA[4]

# Reads private bot data - file excluded from git

BOTDATA = read_file(BOTDATA)
TOKEN = BOTDATA[0]
PREFIX = BOTDATA[1]

# Loads language specified by command line args, otherwise loads language specified in project data

LANGUAGE_FILE_EXTENSION = ".lang"
LANGUAGE = read_file(LANGUAGE + LANGUAGE_FILE_EXTENSION)
info("Using language " + LANGUAGE[0] + " from project data. Change language by editing " + PROJECTDATA_PATH)

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
        write_file("time_recorder", message.content + '\n')
        if(message.author.bot): 
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
    await ctx.send(LANGUAGE[4])

bot.run(TOKEN)