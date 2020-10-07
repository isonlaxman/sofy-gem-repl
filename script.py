import numpy as np
import pprint

initialState = [
    {
        "name": 'connections',
        "weight": 0.7,
        "paths": [
            {
                "name": 'relationships',
                "weight": 0.5,
                "gemGroups": [
                    {
                        "type": "seen",
                        "weight": .1,
                        "gems": [
                            {
                                "name": "g1"
                            }
                        ],
                    },
                    {
                        "type": "hearted",
                        "weight": .2,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            },
                            {
                                "name": "g3"
                            }
                        ],
                    },
                    {
                        "type": "new",
                        "weight": .7,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            }
                        ],
                    }
                ]
            }
        ]
    },
    {
        "name": 'nonConnections',
        "weight": 0.3,
        "paths": [
            {
                "name": 'happiness',
                "weight": 1/3,
                "gemGroups": [
                    {
                        "type": "seen",
                        "weight": .1,
                        "gems": [
                            {
                                "name": "g1"
                            }
                        ],
                    },
                    {
                        "type": "hearted",
                        "weight": .2,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            },
                            {
                                "name": "g3"
                            }
                        ],
                    },
                    {
                        "type": "new",
                        "weight": .7,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            }
                        ],
                    }
                ]
            },
            {
                "name": 'love',
                "weight": 1/3,
                "gemGroups": [
                    {
                        "type": "seen",
                        "weight": .1,
                        "gems": [
                            {
                                "name": "g1"
                            }
                        ],
                    },
                    {
                        "type": "hearted",
                        "weight": .2,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            },
                            {
                                "name": "g3"
                            }
                        ],
                    },
                    {
                        "type": "new",
                        "weight": .7,
                        "gems": [
                            {
                                "name": "g1"
                            },
                            {
                                "name": "g2"
                            }
                        ],
                    }
                ]
            }
        ]
    }
]

state = initialState

def heart(groupIndex, pathIndex, gemIndex, gemGroupIndex):
    # layer 1
    layer_1_change = 1/state[groupIndex]["weight"] / 100
    gWeight = state[groupIndex]["weight"]
    neg_gWeight = state[1 - groupIndex]["weight"]

    if gWeight + layer_1_change > 0.92:
        layer_1_change = 0.92 - gWeight
    elif neg_gWeight - layer_1_change < 0.08:
        layer_1_change = neg_gWeight - 0.08

    state[groupIndex]["weight"] += layer_1_change
    state[1-groupIndex]["weight"] -= layer_1_change

    # layer 2
    path = state[groupIndex]["paths"][pathIndex]
    layer_2_change = 1/path["weight"] / 100

    if path["weight"] + layer_2_change > 0.8:
        layer_2_change = 0.8 - path["weight"]

    min_path_weight = 1
    for p in state[groupIndex]["paths"]:
        if p["weight"] < min_path_weight:
            min_path_weight = p["weight"]
    
    if min_path_weight - layer_2_change < 0.2:
        layer_2_change = 0.2 - min_path_weight

    for p in range(len(state[groupIndex]["paths"])):
        if p == pathIndex:
            state[groupIndex]["paths"][p]["weight"] += layer_2_change
        else:
            state[groupIndex]["paths"][p]["weight"] -= layer_2_change / len(state[groupIndex]["paths"])

    # layer 3
    gem = state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"][gemIndex]
    del state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"][gemIndex]

    state[groupIndex]["paths"][pathIndex]["gemGroups"][1]["gems"].append(gem)


def skip(groupIndex, pathIndex, gemIndex, gemGroupIndex):
    if gemGroupIndex == 2:
        gem = state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"][gemIndex]
        del state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"][gemIndex]

        state[groupIndex]["paths"][pathIndex]["gemGroups"][0]["gems"].append(gem)

def chooseGem():
    group_p = np.array([state[0]["weight"], state[1]["weight"]])
    group_p /= group_p.sum()

    groupIndex = np.random.choice(list(range(len(state))), p=group_p)

    path_p = np.array(list(map(lambda x: x["weight"], state[groupIndex]["paths"])))
    path_p /= path_p.sum()

    pathIndex = np.random.choice(list(range(len(state[groupIndex]["paths"]))), p=path_p)

    gem_p = np.array(list(map(lambda x: x["weight"], state[groupIndex]["paths"][pathIndex]["gemGroups"])))
    gem_p /= gem_p.sum()

    while True:
        gemGroupIndex = np.random.choice(list(range(len(state[groupIndex]["paths"][pathIndex]["gemGroups"]))), p=gem_p)
        if state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"]:
            gemIndex = np.random.choice(list(range(len(state[groupIndex]["paths"][pathIndex]["gemGroups"][gemGroupIndex]["gems"]))))

    print(groupIndex, pathIndex, gemIndex, gemGroupIndex)
    return groupIndex, pathIndex, gemIndex, gemGroupIndex

pp = pprint.PrettyPrinter()
print("Welcome to Sofy's gem weight testing system. At each step, you'll be provided with a gem and will be give the choice to heart [h] or skip [s]. After every action, you'll be show the latest weights")
while True:
    pp.pprint(state)

    groupIndex, pathIndex, gemIndex, gemGroupIndex = chooseGem()
    print("Your gem for the day is: " + str(gemIndex) + " in path " + str(state[groupIndex]["paths"][pathIndex]["name"]) + " in group " + str("non connections" if groupIndex else "connections"))
    print("Enter h or s")

    command = input()

    if (command == "h"):
        heart(groupIndex, pathIndex, gemIndex, gemGroupIndex)
    elif (command == "s"):
        skip(groupIndex, pathIndex, gemIndex, gemGroupIndex)
    else:
        continue

