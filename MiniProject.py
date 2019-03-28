from flask import Flask, render_template, request, jsonify
from cassandra.cluster import Cluster
import json
import requests
import requests_cache
import sqlite3
requests_cache.install_cache('fut_api_cache', backend='sqlite', expire_after=36000)
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)
session.execute("DROP KEYSPACE IF EXISTS futplayers")
session.execute("""CREATE KEYSPACE futplayers WITH REPLICATION =
                {'class' : 'SimpleStrategy', 'replication_factor' : 1}""")
#database creation sqlite3.connect("playerdata.db")

#db.execute("PRAGMA foreign_keys_ = ON")
sql = """CREATE TABLE IF NOT EXISTS futplayers.players
         (id INT,
         firstName TEXT,
         lastName TEXT,
         commonName TEXT,
         pace INT,
         shooting INT,
         passing INT,
         dribbling INT,
         defence INT,
         physical INT,
         rarity INT,
         PRIMARY KEY(id));"""
session.execute(sql)

#page = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page=' + page
#rarityid = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?rarityid=' + rarityid
#player = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?name=' + name
#https://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22ovr%22:%2290:99%22,%22pageSize%22:40,%22position%22:%22LW%22%7D

page_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page={page}'
player_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?name={name}'
rarity_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?rarity={rarityID}'
rarename_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?name={name}&rarity={rarityID}'

#example: Hirving Lozano, various versions with rarities such as 3, 1, 0
#rarities: 0 = common, 1 = rare, 3 = special
#0 returns all rarities


@app.route('/',  methods=['GET', 'POST'])
def home():
    return "Home"
#returns the best version of a player by name
@app.route('/name/<playerName>',  methods=['GET', 'POST'])
def playerLookUp(playerName):
    player_url = player_url_template.format(name = playerName)
    resp = requests.get(player_url)
    if resp.ok:
        pageOfPlayers = resp.json()
    else:
        print(resp.reason)

    varPlayers = pageOfPlayers['items'][0]
    varPlayersAtt = pageOfPlayers['items'][0]['attributes']
    id = int(varPlayers['id'])
    firstName = varPlayers['firstName']
    lastName = varPlayers['lastName']
    commonName = varPlayers['commonName']
    pace = str(varPlayersAtt[0]['value'])
    shooting = str(varPlayersAtt[1]['value'])
    passing = str(varPlayersAtt[3]['value'])
    dribbling = str(varPlayersAtt[2]['value'])
    defence = str(varPlayersAtt[4]['value'])
    physical = str(varPlayersAtt[5]['value'])
    rarity = str(varPlayers['rarityId'])
    #print(pageOfPlayers)
    #returns the first player from the api
    #return str(pageOfPlayers['items'][0]['commonName'])
    data = """<table style="width:100%">
                <tr>
                    <th>First name</th>
                    <th>Last name</th>
                    <th>Common name</th>
                    <th>Pace</th>
                    <th>Shooting</th>
                    <th>Passing</th>
                    <th>Dribbling</th>
                    <th>Defence</th>
                    <th>Physical</th>
                    <th>Rarity</th>
                </tr>
                """

    data += "<tr>\n"
    data += "<td>" + firstName + "</td>\n"
    data += "<td>" + lastName + "</td>\n"
    data += "<td>" + commonName + "</td>\n"
    data += "<td>" + str(pace) + "</td>\n"
    data += "<td>" + str(shooting) + "</td>\n"
    data += "<td>" + str(passing) + "</td>\n"
    data += "<td>" + str(dribbling) + "</td>\n"
    data += "<td>" + str(defence) + "</td>\n"
    data += "<td>" + str(physical) + "</td>\n"
    data += "<td>" + str(rarity) + "</td>\n"
    data += "</tr>\n"
    data += "</table>"
    #with Cluster(['cassandra']).connect() as db:
    #db.execute("PRAGMA foreign_keys_ = ON")
    sql = "INSERT INTO futplayers.players(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});"
    sql = sql.format(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity)
    session.execute(sql)
    return data

#returns a specific page of players
@app.route('/page/<pageNumber>',  methods=['GET', 'POST'])
def pageLookUp(pageNumber):
    page_url = page_url_template.format(page = pageNumber)
    resp = requests.get(page_url)
    if resp.ok:
        pageOfPlayers = resp.json()
    else:
        print(resp.reason)

    data = """<table style="width:100%">
            <tr>
                <th>First name</th>
                <th>Last name</th>
                <th>Common name</th>
                <th>Pace</th>
                <th>Shooting</th>
                <th>Passing</th>
                <th>Dribbling</th>
                <th>Defence</th>
                <th>Physical</th>
                <th>Rarity</th>
            </tr>
            """
    for i in range(0,len(pageOfPlayers['items'])):

        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        id = int(varPlayers['id'])
        firstName = varPlayers['firstName']
        lastName = varPlayers['lastName']
        commonName = varPlayers['commonName']
        pace = str(varPlayersAtt[0]['value'])
        shooting = str(varPlayersAtt[1]['value'])
        passing = str(varPlayersAtt[3]['value'])
        dribbling = str(varPlayersAtt[2]['value'])
        defence = str(varPlayersAtt[4]['value'])
        physical = str(varPlayersAtt[5]['value'])
        rarity = str(varPlayers['rarityId'])
        #print(pageOfPlayers)
        #returns the first player from the api
        #return str(pageOfPlayers['items'][0]['commonName'])

        data += "<tr>\n"
        data += "<td>" + firstName + "</td>\n"
        data += "<td>" + lastName + "</td>\n"
        data += "<td>" + commonName + "</td>\n"
        data += "<td>" + str(pace) + "</td>\n"
        data += "<td>" + str(shooting) + "</td>\n"
        data += "<td>" + str(passing) + "</td>\n"
        data += "<td>" + str(dribbling) + "</td>\n"
        data += "<td>" + str(defence) + "</td>\n"
        data += "<td>" + str(physical) + "</td>\n"
        data += "<td>" + str(rarity) + "</td>\n"
        data += "</tr>\n"
        #with Cluster(['cassandra']).connect() as db:
        #db.execute("PRAGMA foreign_keys_ = ON")
        sql = "INSERT INTO futplayers.players(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});"
        sql = sql.format(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity)
        session.execute(sql)

    data += "</table>"
    return data

#returns a page of players of a certain rarity
@app.route('/rarity/<rarityIDNo>',  methods=['GET', 'POST'])
def rarityLookUp(rarityIDNo):
    rarity_url = rarity_url_template.format(rarityID = rarityIDNo)
    resp = requests.get(rarity_url)
    if resp.ok:
        pageOfPlayers = resp.json()
    else:
        print(resp.reason)

    data = """<table style="width:100%">
            <tr>
                <th>First name</th>
                <th>Last name</th>
                <th>Common name</th>
                <th>Pace</th>
                <th>Shooting</th>
                <th>Passing</th>
                <th>Dribbling</th>
                <th>Defence</th>
                <th>Physical</th>
                <th>Rarity</th>
            </tr>
            """
    for i in range(0,len(pageOfPlayers['items'])):

        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        id = int(varPlayers['id'])
        firstName = varPlayers['firstName']
        lastName = varPlayers['lastName']
        commonName = varPlayers['commonName']
        pace = str(varPlayersAtt[0]['value'])
        shooting = str(varPlayersAtt[1]['value'])
        passing = str(varPlayersAtt[3]['value'])
        dribbling = str(varPlayersAtt[2]['value'])
        defence = str(varPlayersAtt[4]['value'])
        physical = str(varPlayersAtt[5]['value'])
        rarity = str(varPlayers['rarityId'])
        #print(pageOfPlayers)
        #returns the first player from the api
        #return str(pageOfPlayers['items'][0]['commonName'])

        data += "<tr>\n"
        data += "<td>" + firstName + "</td>\n"
        data += "<td>" + lastName + "</td>\n"
        data += "<td>" + commonName + "</td>\n"
        data += "<td>" + str(pace) + "</td>\n"
        data += "<td>" + str(shooting) + "</td>\n"
        data += "<td>" + str(passing) + "</td>\n"
        data += "<td>" + str(dribbling) + "</td>\n"
        data += "<td>" + str(defence) + "</td>\n"
        data += "<td>" + str(physical) + "</td>\n"
        data += "<td>" + str(rarity) + "</td>\n"
        data += "</tr>\n"
        #with Cluster(['cassandra']).connect() as db:
        #db.execute("PRAGMA foreign_keys_ = ON")
        sql = "INSERT INTO futplayers.players(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});"
        sql = sql.format(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity)
        session.execute(sql)

    data += "</table>"
    return data

#returns a page of players of a certain rarity
@app.route('/name/<playerName>/rarity/<rarityIDNo>',  methods=['GET', 'POST'])
def rarityAndNameLookUp(playerName, rarityIDNo):
    rarity_name_url = rarename_url_template.format(name = playerName, rarityID = rarityIDNo)
    resp = requests.get(rarity_name_url)
    if resp.ok:
        pageOfPlayers = resp.json()
    else:
        print(resp.reason)

    data = """<table style="width:100%">
            <tr>
                <th>First name</th>
                <th>Last name</th>
                <th>Common name</th>
                <th>Pace</th>
                <th>Shooting</th>
                <th>Passing</th>
                <th>Dribbling</th>
                <th>Defence</th>
                <th>Physical</th>
                <th>Rarity</th>
            </tr>
            """
    for i in range(0,len(pageOfPlayers['items'])):

        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        id = int(varPlayers['id'])
        firstName = varPlayers['firstName']
        lastName = varPlayers['lastName']
        commonName = varPlayers['commonName']
        pace = str(varPlayersAtt[0]['value'])
        shooting = str(varPlayersAtt[1]['value'])
        passing = str(varPlayersAtt[3]['value'])
        dribbling = str(varPlayersAtt[2]['value'])
        defence = str(varPlayersAtt[4]['value'])
        physical = str(varPlayersAtt[5]['value'])
        rarity = str(varPlayers['rarityId'])
        #print(pageOfPlayers)
        #returns the first player from the api
        #return str(pageOfPlayers['items'][0]['commonName'])

        data += "<tr>\n"
        data += "<td>" + firstName + "</td>\n"
        data += "<td>" + lastName + "</td>\n"
        data += "<td>" + commonName + "</td>\n"
        data += "<td>" + str(pace) + "</td>\n"
        data += "<td>" + str(shooting) + "</td>\n"
        data += "<td>" + str(passing) + "</td>\n"
        data += "<td>" + str(dribbling) + "</td>\n"
        data += "<td>" + str(defence) + "</td>\n"
        data += "<td>" + str(physical) + "</td>\n"
        data += "<td>" + str(rarity) + "</td>\n"
        data += "</tr>\n"
        #with Cluster(['cassandra']).connect() as db:
        #db.execute("PRAGMA foreign_keys_ = ON")
        sql = "INSERT INTO futplayers.players(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});"
        sql = sql.format(id, firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity)
        session.execute(sql)

    data += "</table>"
    return data

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)
