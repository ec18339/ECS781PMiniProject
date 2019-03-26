from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
import sqlite3
requests_cache.install_cache('fut_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__)

#database creation
with sqlite3.connect("playerdata.db") as db:
    cursor = db.cursor()

    cursor.execute("PRAGMA foreign_keys_ = ON")
    sql = """CREATE TABLE IF NOT EXISTS players
             (playerID INTEGER PRIMARY KEY,
             firstName TEXT,
             lastName TEXT,
             commonName TEXT,
             pace INTEGER,
             shooting INTEGER,
             passing INTEGER,
             dribbling INTEGER,
             defence INTEGER,
             physical INTEGER,
             rarity INTEGER)"""
    cursor.execute(sql)
    db.commit()

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

#returns the best version of a player by name
@app.route('/name/<playerName>',  methods=['GET', 'POST'])
def playerLookUp(playerName):
    player_url = player_url_template.format(name = playerName)
    resp = requests.get(player_url)
    if resp.ok:
        pageOfPlayers = resp.json()
    else:
        print(resp.reason)
    #print(pageOfPlayers)
    #returns the first player from the api
    #return str(pageOfPlayers['items'][0]['commonName'])
    varPlayers = pageOfPlayers['items'][0]
    varPlayersAtt = pageOfPlayers['items'][0]['attributes']
    data = "<br />First name: " + varPlayers['firstName']
    data += "<br />Last name: " + varPlayers['lastName']
    data += "<br />Common name: " + varPlayers['commonName']
    data += "<br />"
    data += "<br />Core Player Stats:"
    data += "<br />Pace: " + str(varPlayersAtt[0]['value'])
    data += "<br />Shooting: " + str(varPlayersAtt[1]['value'])
    data += "<br />Passing: " + str(varPlayersAtt[2]['value'])
    data += "<br />Dribbling: " + str(varPlayersAtt[3]['value'])
    data += "<br />Defence: " + str(varPlayersAtt[4]['value'])
    data += "<br />Physical: " + str(varPlayersAtt[5]['value'])
    data += "<br />Rarity: " + str(varPlayers['rarityId'])
    with sqlite3.connect("playerdata.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys_ = ON")
        sql = "INSERT INTO players(firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        sql = sql.format(varPlayers['firstName'], varPlayers['lastName'], varPlayers['commonName'], varPlayersAtt[0]['value'], varPlayersAtt[1]['value'], varPlayersAtt[2]['value'], varPlayersAtt[3]['value'], varPlayersAtt[4]['value'], varPlayersAtt[5]['value'], varPlayers['rarityId'])
        cursor.execute(sql, entryData)
        db.commit()
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
    data = ""
    for i in range(0,len(pageOfPlayers['items'])):
        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        data += "<br />First name: " + pageOfPlayers['items'][i]['firstName']
        data += "<br />Last name: " + pageOfPlayers['items'][i]['lastName']
        data += "<br />Common name: " + pageOfPlayers['items'][i]['commonName']
        data += "<br />"
        data += "<br />Core Player Stats:"
        data += "<br />Pace: " + str(pageOfPlayers['items'][i]['attributes'][0]['value'])
        data += "<br />Shooting: " + str(pageOfPlayers['items'][i]['attributes'][1]['value'])
        data += "<br />Passing: " + str(pageOfPlayers['items'][i]['attributes'][2]['value'])
        data += "<br />Dribbling: " + str(pageOfPlayers['items'][i]['attributes'][3]['value'])
        data += "<br />Defence: " + str(pageOfPlayers['items'][i]['attributes'][4]['value'])
        data += "<br />Physical: " + str(pageOfPlayers['items'][i]['attributes'][5]['value'])
        data += "<br />Rarity: " + str(pageOfPlayers['items'][i]['rarityId'])
        data += "<br />"
        data += "<br />"
        with sqlite3.connect("playerdata.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "INSERT INTO players(firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
            sql = sql.format(varPlayers['firstName'], varPlayers['lastName'], varPlayers['commonName'], varPlayersAtt[0]['value'], varPlayersAtt[1]['value'], varPlayersAtt[2]['value'], varPlayersAtt[3]['value'], varPlayersAtt[4]['value'], varPlayersAtt[5]['value'], varPlayers['rarityId'])
            cursor.execute(sql, entryData)
    #print(pageOfPlayers)
    #returns the first player from the api
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
    data = ""
    for i in range(0,len(pageOfPlayers['items'])):
        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        data += "<br />First name: " + pageOfPlayers['items'][i]['firstName']
        data += "<br />Last name: " + pageOfPlayers['items'][i]['lastName']
        data += "<br />Common name: " + pageOfPlayers['items'][i]['commonName']
        data += "<br />"
        data += "<br />Core Player Stats:"
        data += "<br />Pace: " + str(pageOfPlayers['items'][i]['attributes'][0]['value'])
        data += "<br />Shooting: " + str(pageOfPlayers['items'][i]['attributes'][1]['value'])
        data += "<br />Passing: " + str(pageOfPlayers['items'][i]['attributes'][2]['value'])
        data += "<br />Dribbling: " + str(pageOfPlayers['items'][i]['attributes'][3]['value'])
        data += "<br />Defence: " + str(pageOfPlayers['items'][i]['attributes'][4]['value'])
        data += "<br />Physical: " + str(pageOfPlayers['items'][i]['attributes'][5]['value'])
        data += "<br />Rarity: " + str(pageOfPlayers['items'][i]['rarityId'])
        data += "<br />"
        data += "<br />"

        with sqlite3.connect("playerdata.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "INSERT INTO players(firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
            sql = sql.format(varPlayers['firstName'], varPlayers['lastName'], varPlayers['commonName'], varPlayersAtt[0]['value'], varPlayersAtt[1]['value'], varPlayersAtt[2]['value'], varPlayersAtt[3]['value'], varPlayersAtt[4]['value'], varPlayersAtt[5]['value'], varPlayers['rarityId'])
            cursor.execute(sql, entryData)

    #print(pageOfPlayers)
    #returns the first player from the api
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
    data = ""
    for i in range(0,len(pageOfPlayers['items'])):
        varPlayers = pageOfPlayers['items'][i]
        varPlayersAtt = pageOfPlayers['items'][i]['attributes']
        data += "<br />First name: " + pageOfPlayers['items'][i]['firstName']
        data += "<br />Last name: " + pageOfPlayers['items'][i]['lastName']
        data += "<br />Common name: " + pageOfPlayers['items'][i]['commonName']
        data += "<br />"
        data += "<br />Core Player Stats:"
        data += "<br />Pace: " + str(pageOfPlayers['items'][i]['attributes'][0]['value'])
        data += "<br />Shooting: " + str(pageOfPlayers['items'][i]['attributes'][1]['value'])
        data += "<br />Passing: " + str(pageOfPlayers['items'][i]['attributes'][2]['value'])
        data += "<br />Dribbling: " + str(pageOfPlayers['items'][i]['attributes'][3]['value'])
        data += "<br />Defence: " + str(pageOfPlayers['items'][i]['attributes'][4]['value'])
        data += "<br />Physical: " + str(pageOfPlayers['items'][i]['attributes'][5]['value'])
        data += "<br />Rarity: " + str(pageOfPlayers['items'][i]['rarityId'])
        data += "<br />"
        data += "<br />"

        with sqlite3.connect("playerdata.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "INSERT INTO players(firstName, lastName, commonName, pace, shooting, passing, dribbling, defence, physical, rarity) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
            sql = sql.format(varPlayers['firstName'], varPlayers['lastName'], varPlayers['commonName'], varPlayersAtt[0]['value'], varPlayersAtt[1]['value'], varPlayersAtt[2]['value'], varPlayersAtt[3]['value'], varPlayersAtt[4]['value'], varPlayersAtt[5]['value'], varPlayers['rarityId'])
            cursor.execute(sql, entryData)
    #print(pageOfPlayers)
    #returns the first player from the api
    return data

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)
