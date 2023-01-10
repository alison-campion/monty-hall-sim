import random
import numpy as np
import pandas as pd

# functions used in the simulation

def fill_doors(n=3):
    """
    fills the doors with prizes: 1 with a car, the remaining with goats
    """
    # create an empty list of doors
    doorlist = list(np.arange(1, n+1))
    doors = pd.DataFrame(columns=doorlist)
    
    # pick one door at random to put the car behind
    car = random.choice(doorlist)
    doors.loc[0, car] = "c"

    # drop the car door from the list
    goatlist = doorlist.copy()
    goatlist.remove(car)

    # put goats behind the other two doors
    doors.loc[0, goatlist] = "g"

    # return this set of n doors
    return doors

def door_reveal(row, doorlist):
    """
    function to determine which door should be revealed.
    the door revealed MUST have a goat and MUST NOT be the door you picked
    """
    # first drop the column that reports what is behind the chosen door
    temp = row.drop("first_choice")

    # next select the doors that have goats behind them
    temp = temp[(temp=="g")]

    # drop the door you picked
    temp = temp[temp.index!=row["first_door"]]

    # pick randomly from the remaining doors to select the door to be revealed
    door_reveal = random.choice(list(temp.index))

    return door_reveal


def identify_result(row, n=3):

    # if you stayed, the prize is whatever is behind the first choice door
    if row["decision"] == "stay":
        prize = row.loc["first_choice"]

    # if you switch, the prize is whatever is behind the remaining door (not first choice, not revealed)
    elif row["decision"] == "switch":
        
        # create the doorlist
        doorlist = list(np.arange(1, n+1))

        # find the door you switch to (not the first choice nor the revealed door)
        door = [x for x in doorlist if x not in list(row[["first_door", "door_revealed"]])][0]

        # find the prize behind the door
        prize = row[door]

    # if the prize is goat, it's a lose
    if prize == "g":
        result = "lose"

    # if the prize is a car, it's a win
    elif prize == "c":
        result = "win"
        
    return result

def random_choice(x, doorlist):
    """
    Instead of stay or switch, doors are randomized and you pick one.
    In this scenario, you have no information about the two doors left
    after the reveal of one goat door.
    """
    temp = doorlist.copy()
    temp.remove(x)
    rc = random.choice(temp)
    return rc
