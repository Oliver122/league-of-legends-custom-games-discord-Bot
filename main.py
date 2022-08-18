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


# Current custom

class MyClient(discord.Client):
    client = discord.Client()

    @client.event
    async def on_ready(self):
        print("Login Version 0.1")

    @client.event
    async def on_message(self, message):

        async def get_user_data(data_str):
            names = []
            points = [][5]
            for data in data_str:
                data = data.split(":")
                names.append(data[0])
                points.append(int(data[1]))
            return names, points

        async def balance_teams(participants):
            data = await read_file()
            balanced_teams = []
            user_points = []

            data = await get_user_data(data)
            names = data[0]
            points = data[1]

            # -> username.contains = true >> add associated user/points to user_points
            # so data is (participants)[user0, user1] & (user_points)[num0,num1]
            # if username.contains = false associate participant (p) with 0
            # >> (participants)[unknownUser0, unknownUser1] & (user_points)[0, 0]

            for p in participants:
                if names.__contains__(p):
                    print(p)
                    for j in range(len(names)):
                        if p == names[j]:
                            user_points.append(points[j])
                else:
                    user_points.append(0)
            print("Unprocessed:")
            print(participants)
            print(user_points)
            print("---------:")

            balanced_array = await balance_arrays(20, user_points)

            print(balanced_array[1])

            for balanced_user_points in balanced_array[1]:
                for k in range(len(user_points)):
                    if balanced_user_points == user_points[k]:
                        balanced_teams.append(participants[k])
                        del user_points[k]
                        del participants[k]
                        break
            print(balanced_teams)
            print("balanced Teams")

            return balanced_teams

        async def balance_arrays(rounds, points):
            global old_div
            print("rounds left : " + str(rounds))
            rounds -= 1
            if rounds != 0:
                team_one = []
                team_two = []
                old_team_one = []
                old_team_two = []
                old_points = points.copy()

                random.shuffle(points)

                for i in range(len(points)):

                    if i % 2 == 0:
                        team_two.append(points[i])
                        old_team_two.append(old_points[i])
                    else:
                        team_one.append(points[i])
                        old_team_one.append(old_points[i])

                if sum(team_one) - sum(team_two) == 0:
                    for p in team_two:
                        team_one.append(p)
                    return 0, team_one

                if sum(team_one) - sum(team_two) < 0:
                    div = (sum(team_one) - sum(team_two)) * (-1)
                else:
                    div = sum(team_one) - sum(team_two)

                if sum(old_team_one) - sum(old_team_two) < 0:
                    old_div = (sum(old_team_one) - sum(old_team_two)) * (-1)

                print(str(old_div) + " DIV")

                if div < old_div:
                    return await balance_arrays(rounds, points)
                else:
                    return await balance_arrays(rounds, old_points)
            else:
                return 0, points

        async def read_file():
            # important !!
            # player_data.txt needs a line space below one entry!
            # line 1  >user:0
            # line 2  >
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
            data = await read_file()
            data = await get_user_data(data)
            names = data[0]
            points = data[1]

            for u_name in usernames:
                if names.__contains__(str(u_name)):
                    for i in range(len(names)):
                        if str(names[i]) == str(u_name):
                            points[i] = points[i] + 1
                else:
                    # print(user + " been appended")
                    names.append(u_name)
                    points.append(0)

            # https://pynative.com/python-write-list-to-file/
            with open('player_data.txt', 'w') as fp:
                for i in range(len(names)):
                    item = str(names[i]) + ":" + str(points[i])
                    fp.write("%s\n" % item)
            print('Done')

        async def minus_point(usernames):
            data = await read_file()
            data = await get_user_data(data)
            names = data[0]
            points = data[1]

            for u_name in usernames:
                if names.__contains__(str(u_name)):
                    for i in range(len(names)):
                        if str(names[i]) == str(u_name):
                            points[i] = points[i] - 1
                else:
                    names.append(u_name)
                    points.append(0)

            # https://pynative.com/python-write-list-to-file/
            with open('player_data.txt', 'w') as fp:
                for i in range(len(names)):
                    item = str(names[i]) + ":" + str(points[i])
                    fp.write("%s\n" % item)

        global game_started
        if (message.author == client.user):
            return

        elif message.content.startswith("!help"):
            await message.channel.send("How the LCMB bot works: \n" +
                "First 10 peapole need to join the game by typing !join into a chat with the Bot (gaming chat). \n" +
                "After the game has to be either started with #random for random teams or #balance for balanced ,that balances teams with before collected data.\n" +
                "when balanced the game can be started with #start. #start does also work with the same teams as before or the order the participants joined. \n"+
                "Games can be ended with #winner [team] to save the data or #cancel to just stop a running one. \n" +
                "Participants can leave the lobby with !leave or the admin can clear the lobby with #clear \n"+
                "important: # commands are admin commands \n" +
                "to get admin privileges type !enable [password] \n"
            )

        elif message.content.startswith("!join"):
            if (len(participants_list) >= 10):
                await message.channel.send("already 10 players! \n list of players with !pList")
                return
            # check if already joined
            if participants_list.__contains__(message.author):
                await message.channel.send("you have already joined!")
            else:
                participants_list.append(str(message.author))
                await message.channel.send(
                    f'''you are in! \n {len(participants_list)} Player in for the custom game!''')
                participants_list.append("1")
                participants_list.append("2")
                participants_list.append("3")
                participants_list.append("4")
                participants_list.append("5")
                participants_list.append("6")
                participants_list.append("7")
                participants_list.append("8")
                participants_list.append("9")

        elif message.content.startswith("!list"):
            if len(participants_list) == 0:
                await message.channel.send("no one joined yet")
            for i in participants_list:
                await message.channel.send(i)

        elif message.content.startswith("!points"):
            data = await get_user_data(await read_file())
            if not data[0].__contains__(str(message.author)):
                await message.channel.send("no points yet!")
            else:
                def position_names(num, to_add_string):
                    return str(num) + to_add_string

                for i in range(len(data[0])):
                    if str(message.author) == data[0][i]:
                        author_points = data[1][i]
                        sorted_points = data[1]
                        sorted_points.sort(reverse=True)
                        position = sorted_points.index(author_points) + 1
                        if position == 1:
                            position = position_names(1, "st")
                        elif position == 2:
                            position = position_names(2, "nd")
                        elif position == 3:
                            position = position_names(3, "rd")
                        else:
                            position = position_names(position, "th")

                        await message.channel.send(f'{message.author} you got {author_points} points! \n your place is {position}.')
        elif message.content.startswith("!leaderboard"):
            async def list_to_paragraph(list):
                string = list[0]
                del list[0]
                for r in list:
                    string += "\n" + str(r)
                return string

            data = await get_user_data(await read_file())
            sorted_points = data[1].copy()
            top_ten = []
            sorted_points.sort(reverse=True)
            print(sorted_points)

            for score_i in range(len(sorted_points[:10])):
                index = -1
                for i in range(len(data[1])):
                    if data[1][i] == sorted_points[score_i]:
                        index = i
                top_ten.append(f'{score_i + 1}. : {data[0][index]} with {data[1][index]} points!')
                del data[1][index]
                del data[0][index]

            await message.channel.send(await list_to_paragraph(top_ten))


        elif message.content.startswith("!leave"):
            if participants_list.__contains__(message.author):
                participants_list.remove(message.author)
                await message.channel.send(
                    f''' {message.author} left the custom \n {len(participants_list)} players are still in the custom !''')

        elif message.content.startswith("!enable"):
            # should also delete message before testing
            content = str(message.content)
            to_check_pwd = content.split()[1]
            if str(hashlib.sha3_256(to_check_pwd.encode('utf-8')).hexdigest()) == adminPassword:
                # print("correct")
                await message.channel.send(">")
                globals()['admin_usr'] = message.author
            print(str(hashlib.sha3_256(to_check_pwd.encode('utf-8')).hexdigest()))

        elif message.content.startswith("#"):  # Stops all users that are not admin_usr
            if message.author != admin_usr:
                return

            elif message.content.startswith("#clear"):
                participants_list.clear()
                await message.channel.send("Lobby cleared")

            elif message.content.startswith("#pw"):
                content = str(message.content)
                to_set_pwd = content.split()[1]
                globals()['adminPassword'] = str(hashlib.sha3_256(to_set_pwd.encode('utf-8')).hexdigest())
                await message.channel.send("password changed")

            elif message.content.startswith("#start"):
                if game_started:
                    await message.channel.send("a game is still running")
                if len(participants_list) != 10:
                    if len(participants_list) == 1:
                        await message.channel.send(
                            f'''not enough players!  \n {len(participants_list)} player is in the custom!''')
                        return
                    await message.channel.send(
                        f'''not enough players!  \n {len(participants_list)} Players are in the custom!''')
                    return
                else:
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
            elif message.content.startswith("#cancel"):
                globals().game_started = False

            elif message.content.startswith("#random"):
                if game_started:
                    await message.channel.send("a game is still running")
                if len(participants_list) != 10:
                    if len(participants_list) == 1:
                        await message.channel.send(
                            f'''not enough players!  \n {len(participants_list)} player is in the custom!''')
                        return
                    await message.channel.send(
                        f'''not enough players!  \n {len(participants_list)} Players are in the custom!''')
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
            elif message.content.startswith("#winner"):
                if not game_started:
                    await message.channel.send("No game started")
                    return
                else:
                    winner_msg = str(message.content)
                    winner = winner_msg.split(" ")
                    if int(winner[1]) == 1:
                        await message.channel.send("Winning Team 1!")
                        # Team1 gets +1 point
                        winner_list = [participants_list[0], participants_list[1], participants_list[2],
                                       participants_list[3], participants_list[4]]
                        await plus_point(winner_list)
                        looser_list = [participants_list[5], participants_list[6], participants_list[7],
                                       participants_list[8], participants_list[9]]
                        await minus_point(looser_list)
                    elif int(winner[1]) == 2:
                        await message.channel.send("Winning Team 2!")
                        looser_list = [participants_list[0], participants_list[1], participants_list[2],
                                       participants_list[3], participants_list[4]]
                        await minus_point(looser_list)
                        winner_list = [participants_list[5], participants_list[6], participants_list[7],
                                       participants_list[8], participants_list[9]]
                        await plus_point(winner_list)
                    else:
                        await message.channel.send('Syntax incorrect :(#winner [team[1/2]]) ')
                        return
                    game_started = False
            elif message.content.startswith("#balance"):
                usernames = await balance_teams(participants_list)
                participants_list.clear()
                for user in usernames:
                    participants_list.append(user)
                    print("added " + str(user))


client = MyClient()
client.run('OTk0MzgxMTY0NjYxOTg1Mzgw.Glx42q.nw_8nb-sr1NLNxjRmeIH03plm_POVIctsCXlh4')
