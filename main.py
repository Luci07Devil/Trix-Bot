import discord
import os 
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["brokenhearted", "downhearted", "gloomy", "glum", "heartbroken", "heartsick", "heartsore", "heavyhearted", "joyless", "low", "depressed", "miserable", "mournful", "sad", "sorrowful", "sorry", "unhappy"]

happy_words = ["beaming", "cheerful", "gay", "gladsome", "sunny", "upbeat","gleeful", "jolly", "jovial", "laughing", "merry", "smiling", "happy","jubilant", "excited", "thrilled",
"hopeful", "optimistic", "sanguine"]

starter = ["Hang in there !!", "Cheer-up !!", "You are a great personbot !!"]

if "responding" in db.keys():
  db["responding"] = True
else:
  db["responding"] = True

def update_quote(quote):
  if "quotes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote]
  

def delete_quote(index):
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
    db["quotes"] = quotes

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

@client.event
#works when the bot is ready to use
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  options = []
  options = starter
  msg = message.content
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello {0}'.format(message.author))

  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    #if "quotes" in db.keys():
    #  options = options + db["quotes"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    quote = msg.split("$new ",1)[1]
    update_quote(quote)
    await message.channel.send("New quote added.")
  
  if msg.startswith("$del"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_quote(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)

  if msg.startswith("$list"):
    quotes = []
    if "quotes" in db.keys():
      quotes = db["quotes"]
    await message.channel.send(quotes)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")

    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))