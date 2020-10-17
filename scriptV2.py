import requests
import json

CONFIG = {}

with open('./config.json') as f:
    CONFIG = json.load(f)

global_headers = {
    'admin': CONFIG["admin"],
}


def init_database():
    url = "http://localhost:5001/sofy-firebase-backend/us-central1/api/sigma/initDatabase"

    payload = {}

    response = requests.request(
        "POST", url, headers=global_headers, data=payload)
    return json.loads(response.text)["data"]["userId"]


def get_weights(userId):
    url = "http://localhost:5001/sofy-firebase-backend/us-central1/api/sigma/user/getWeights?userId=" + userId

    payload = {}

    response = requests.request(
        "GET", url, headers=global_headers, data=payload)
    return json.loads(response.text)["data"]["weights"]


def get_gem(userId):
    url = "http://localhost:5001/sofy-firebase-backend/us-central1/api/sigma/user/getGem"

    payload = {"userId": userId, "lastGemTime": None}

    response = requests.request("POST", url, headers=global_headers, json=payload)
    return json.loads(response.text)["data"]["gem"]


def heart(userId, gemId):
    url = "http://localhost:5001/sofy-firebase-backend/us-central1/api/sigma/userGem/heart"

    payload = {
        "userId": userId,
        "gemId": gemId
    }

    response = requests.request(
        "POST", url, headers=global_headers, json=payload)

    return json.loads(response.text)

def read(userId, gemId):
    url = "http://localhost:5001/sofy-firebase-backend/us-central1/api/sigma/userGem/read"

    payload = {
        "userId": userId,
        "gemId": gemId
    }

    response = requests.request(
        "POST", url, headers=global_headers, json=payload)

    return json.loads(response.text)


gemGroupMap = {
    0: "seen",
    1: "heart",
    2: "new"
}


def get_relevant_info(chosenGem, weights):
    retVal = {}

    for gi, g in enumerate(weights):
        for _, p in enumerate(g["items"]):
            if p["id"] == chosenGem["pathId"]:
                retVal["group"] = {
                    "weight": g["weight"], "name": "connections" if gi == 0 else "non-connections"}
                retVal["path"] = {"weight": p["weight"], "id": p["id"]}

                for ggi, gg in enumerate(p["gemGroups"]):
                    for _, gem in enumerate(gg["gems"]):
                        if gem["id"] == chosenGem["id"]:
                            retVal["gemGroup"] = {"name": gemGroupMap[ggi]}
                            retVal["gem"] = {
                                "id": chosenGem["id"]
                            }

                break

    return retVal


def pre_loop():
    id = init_database()
    return id


userId = pre_loop()
print(userId)


print("\n\nWelcome to Sofy's weight testing script")

# get gem -> show old weight -> heart/skip -> show new weight
while True:
    gem = get_gem(userId)

    curr_weights = get_weights(userId)
    print("\nWeight", get_relevant_info(gem, curr_weights))

    i = input("Press h to heart and s to skip\n")

    if (i == "h"):
        heart(userId, gem["id"])
    else:
        read(userId, gem["id"])

    curr_weights = get_weights(userId)
    print("\nUpdated weight", get_relevant_info(gem, curr_weights))
