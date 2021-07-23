import requests
from requests.api import head





url = "https://discord.com/api/webhooks/864566703995879435/-hjC2pdhfHz7pgPhLeMWZi4JzmK-zNlCkGwpURrPHQDOTpT70S86Py6GXbOuQste8ZF9"

data = {


    "embeds": [



        {
        "title": "Command used!",
        "description": "Server sent a command",
        "color": 2614846,
        "fields": [

        {
            "name": "Command used",
            "value": "?ping"
        },
        {
            "name": "User",
            "value": "Markiemm#0001",
            "inline": "true"
        },
        {
            "name": "User ID:",
            "value": "274087234328498",
            "inline": "true"
        },
        {
            "name": "User input",
            "value": "?ping 4.5.5.5",
            "inline": "true"
        },
        {
            "name": "Server name",
            "value": "lolserver",
            "inline": "true"
        },
        {
            "name": "Server ID",
            "value": "4329492369476923467923"
        }
    ],
    "author": {
        "name": "Markiemm#0001",
        "icon_url": "https://media.discordapp.net/attachments/866002022464487444/866003896429314048/DB-Icons-Pen-Testing.png"
    },
    "footer": {
        "text": "Output"
    }
    }
]
}

result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))