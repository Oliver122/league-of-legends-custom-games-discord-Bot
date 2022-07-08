import os
import random
import discord
import json

adminPassword = "pwd"
adminUsr = ""

# Admin Shell

participants_list = []
game_started = False

# Current Coustom
def init():
    print("yeen")


class MyClient(discord.Client):


    client = discord.Client()

    async def get_data(self, username):
        player = '{"username, points"}'

        f = open('data.json', )
        data = json.loads(f)

        for i in data:
            if data['name'] == username:
                return data['points']

    async def set_data(self, username, points):

        print("setData")

    @client.event
    async def on_ready(self):
        print("Login Version 0.1")

    @client.event
    async def on_message(self, message):
        global game_started
        if (message.author == client.user):
            return

        elif message.content.startswith("!enable"):
            checkpwd = message.content
            message.author.delete

        elif message.content.startswith("!join"):
            if (len(participants_list) >= 10):
                await message.channel.send("already 10 players! \n list of players with !pList")
                return
            # check if already joined
            if participants_list.__contains__(message.author):
                await message.channel.send("you have already joined!")
            else:
                participants_list.append(message.author)
                await message.channel.send(
                    f'''you are in! \n {len(participants_list)} Player in for the coustom game!''')

            print(participants_list)
        elif message.content.startswith("!list"):
            if len(participants_list) == 0:
                await message.channel.send("no one joined yet")
            for i in participants_list:
                await message.channel.send(i)

        elif message.content.startswith("!leave"):
            if participants_list.__contains__(message.author):
                participants_list.remove(message.author)
                await message.channel.send(
                    f''' {message.author} left the coustom \n {len(participants_list)} players are still in the coustom !''')

        elif message.content.startswith("!start"):
            if len(participants_list) != 10:
                if len(participants_list) == 1:
                    await message.channel.send(
                        f'''not enough players!  \n {len(participants_list)} player is in the coustom!''')
                    return
                await message.channel.send(
                    f'''not enough players!  \n {len(participants_list)} Players are in the coustom!''')
                return
            else:
                random.shuffle(participants_list)
                await message.channel.send(f''' Team 1 
                Top     {participants_list[0]}  
                Mid     {participants_list[1]}  
                Jgl     {participants_list[2]}
                ADC     {participants_list[3]}
                SUP     {participants_list[4]}  \n''')
                await message.channel.send(f''' Team 2
                Top     {participants_list[5]}  
                Mid     {participants_list[6]} 
                Jgl     {participants_list[7]}
                ADC     {participants_list[8]}  
                SUP     {participants_list[9]}  ''')

                game_started = True
        elif message.content.startswith("!winner"):
            if not game_started:
                await message.channel.send("No game started")
                return
            else:
                winner_msg = str(message.content)
                winner = winner_msg.split(" ")
                if int(winner[1]) == 1:
                    await message.channel.send("Winning Team 1 registered")

                elif int(winner[1]) == 2:
                    await message.channel.send("Winning Team 2 registered")

                else:
                    await message.channel.send("Please Say what Team won!")
                    print(winner)
                    return
                print(winner)
                game_started = False
client = MyClient()
client.run(os.getenv('TOKEN'))
