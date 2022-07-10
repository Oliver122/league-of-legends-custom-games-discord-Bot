import hashlib
import os
import random
import discord
import json

adminPassword = "1d6442ddcfd9db1ff81df77cbefcd5afcc8c7ca952ab3101ede17a84b866d3f3"
admin_usr = "no one yet"

# Admin Shell

participants_list = []
game_started = False


# Current Coustom

class MyClient(discord.Client):
    client = discord.Client()

    @client.event
    async def on_ready(self):
        print("Login Version 0.1")



    @client.event
    async def on_message(self, message):

        async def read_file():
            # https://pynative.com/python-write-list-to-file/
            data = []
            with open(r'player_data.txt', 'r') as fp:
                for line in fp:
                    x = line[:-1]
                    data.append(x)
            return data

        # def plus_point / def minus_point
        # plus_point and minus_point are both equal functions just the operator changes from + to -
        # the data is read out from the file then split up into the username and points after that
        # its checked if participants are in the list of the users in the File. If so
        # it iterates over all of the winning/losing participants to find their index when found it
        # increases / decreases their value by 1.
        # Lastly it writes to data file in the same format

        async def plus_point(usernames):
            data_list = await read_file()
            names = []
            points = []
            for l in data_list:
                data = l.split(":")
                names.append(data[0])
                points.append(int(data[1]))

            for user in usernames:
                if names.__contains__(str(user)):
                    for i in range(len(names)):
                        if str(names[i]) == str(user):
                            points[i] = points[i] + 1
                else:
                    #print(user + " been appended")
                    names.append(user)
                    points.append(0)

            # https://pynative.com/python-write-list-to-file/
            with open('player_data.txt', 'w') as fp:
                for i in range(len(names)):
                    item = str(names[i]) + ":" + str(points[i])
                    fp.write("%s\n" % item)
            print('Done')

        async def minus_point(usernames):
            data_list = await read_file()
            names = []
            points = []
            for l in data_list:
                data = l.split(":")
                names.append(data[0])
                points.append(int(data[1]))

            for user in usernames:
                if names.__contains__(str(user)):
                    for i in range(len(names)):
                        if str(names[i]) == str(user):
                            points[i] = points[i] - 1
                else:
                    #print(user + " been appended")
                    names.append(user)
                    points.append(0)

            # https://pynative.com/python-write-list-to-file/
            with open('player_data.txt', 'w') as fp:
                for i in range(len(names)):
                    item = str(names[i]) + ":" + str(points[i])
                    fp.write("%s\n" % item)
            #print('Done')

            # display list

        global game_started
        if (message.author == client.user):
            return

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
            if game_started:
                await message.channel.send("a game is still running")
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
                    await message.channel.send("Winning Team 1!")
                    #Team1 gets +1 point
                    winner_list = [participants_list[0], participants_list[1], participants_list[2], participants_list[3], participants_list[4]]
                    await plus_point(winner_list)
                    looser_list = [participants_list[5], participants_list[6], participants_list[7], participants_list[8], participants_list[9]]
                    await minus_point(looser_list)
                elif int(winner[1]) == 2:
                    await message.channel.send("Winning Team 2!")
                    looser_list = [participants_list[0], participants_list[1], participants_list[2], participants_list[3], participants_list[4]]
                    await minus_point(looser_list)
                    winner_list = [participants_list[5], participants_list[6], participants_list[7], participants_list[8], participants_list[9]]
                    await plus_point(winner_list)
                else:
                    await message.channel.send("Please Say what team won the Game!")
                    return
                game_started = False
        elif message.content.startswith("!enable"):
            # should also delete message before testing

            content = str(message.content)
            to_check_pwd = content.split()[1]
            if str(hashlib.sha3_256(to_check_pwd.encode('utf-8')).hexdigest()) == adminPassword:
                #print("correct")
                await message.channel.send(">")
                globals()['admin_usr'] = message.author
            print(str(hashlib.sha3_256(to_check_pwd.encode('utf-8')).hexdigest()))

        elif message.content.startswith("#"):  # Stops all users that are not admin_usr
            if message.author != admin_usr:
                #print(admin_usr)
                return

            elif message.content.startswith("#pw"):
                content = str(message.content)
                to_set_pwd = content.split()[1]
                globals()['adminPassword'] = str(hashlib.sha3_256(to_set_pwd.encode('utf-8')).hexdigest())
                await message.channel.send("password changed")



client = MyClient()
client.run('OTk0MzgxMTY0NjYxOTg1Mzgw.GijgxW.6MXX7nOGK5js6mWIVjivTY3FC3WxMXlcxqzlIc')
