from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
requests_cache.install_cache('fut_api_cache', backend='sqlite', expire_after=36000)



app = Flask(__name__)

#page = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page=' + page
#rarityid = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?rarityid=' + rarityid
#player = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?name=' + name
#https://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22ovr%22:%2290:99%22,%22pageSize%22:40,%22position%22:%22LW%22%7D

page_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page={page}'
player_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?name={name}'
rarity_url_template = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?rarity={rarityID}'

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
#    pace shot pass dri def phy
    data = "<br />First name: " + pageOfPlayers['items'][0]['firstName']
    data += "<br />Last name: " + pageOfPlayers['items'][0]['lastName']
    data += "<br />Common name: " + pageOfPlayers['items'][0]['commonName']
    data += "<br />"
    data += "<br />Core Player Stats:"
    data += "<br />Pace: " + str(pageOfPlayers['items'][0]['attributes'][0]['value'])
    data += "<br /> Shooting: " + str(pageOfPlayers['items'][0]['attributes'][1]['value'])
    data += "<br />Passing: " + str(pageOfPlayers['items'][0]['attributes'][2]['value'])
    data += "<br />Dribbling: " + str(pageOfPlayers['items'][0]['attributes'][3]['value'])
    data += "<br />Defence: " + str(pageOfPlayers['items'][0]['attributes'][4]['value'])
    data += "<br />Physical: " + str(pageOfPlayers['items'][0]['attributes'][5]['value'])
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
            data += "<br />First name: " + pageOfPlayers['items'][i]['firstName']
            data += "<br />Last name: " + pageOfPlayers['items'][i]['lastName']
            data += "<br />Common name: " + pageOfPlayers['items'][i]['commonName']
            data += "<br />"
            data += "<br />Core Player Stats:"
            data += "<br />Pace: " + str(pageOfPlayers['items'][i]['attributes'][0]['value'])
            data += "<br /> Shooting: " + str(pageOfPlayers['items'][i]['attributes'][1]['value'])
            data += "<br />Passing: " + str(pageOfPlayers['items'][i]['attributes'][2]['value'])
            data += "<br />Dribbling: " + str(pageOfPlayers['items'][i]['attributes'][3]['value'])
            data += "<br />Defence: " + str(pageOfPlayers['items'][i]['attributes'][4]['value'])
            data += "<br />Physical: " + str(pageOfPlayers['items'][i]['attributes'][5]['value'])
            data += "<br />"
            data += "<br />"

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
        data += "<br />"
        data += "<br />"
    #print(pageOfPlayers)
    #returns the first player from the api
    return data

if __name__=="__main__":
    app.run(port=8080, debug=True)
