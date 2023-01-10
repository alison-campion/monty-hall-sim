import random
import numpy as np
import pandas as pd
from collections import Counter

# set number of doors and create a list of n doors
n = 3
doorlist = list(np.arange(1, n+1))

# set number of iterations
N = 1000

# ------------------ #
# Initiate all doors #
# ------------------ #

# create a dataframe with 1 set of doors
df = fill_doors(n)

# loop over the sample size and fill a set of doors for each sample
for i in np.arange(0, N):

    # fill the new doors
    doors = fill_doors(n)
    
    # append the set of doors to the dataframe
    df = pd.concat([df, doors]).reset_index(drop=True)

# ------------ #
# First choice #
# ------------ #
# pick your first door randomly
df["first_door"] = df.apply(lambda row: random.choice(list(doorlist)), axis=1)

# determine what prize was behind that first door
df["first_choice"] = df.apply(lambda row: row[row["first_door"]], axis=1)

# ----------- #
# Door reveal #
# ----------- #    
# identify which door will be revealed, based on your first choice
df["door_revealed"] = df.apply(lambda row: door_reveal(row, doorlist), axis=1)

# -------------- #
# Switch or stay #
# -------------- #
# randomly choose switch or stay
df["decision"] = df.apply(lambda row: random.choice(["switch", "stay"]), axis=1)

# ---------------------- #
# Determine the outcomes #
# ---------------------- #

# determine the outcomes
df["outcome"] = df.apply(lambda row: identify_result(row), axis=1)

# probability for switching
switch_outcomes = Counter(df.loc[((df["decision"]=="switch")), "outcome"])
switch_win_p = switch_outcomes["win"] / (switch_outcomes["win"] + switch_outcomes["lose"])
switch_win_p = np.round(switch_win_p * 100, 1)

# probability for staying
stay_outcomes = Counter(df.loc[((df["decision"]=="stay")), "outcome"])
stay_win_p = stay_outcomes["win"] / (stay_outcomes["win"] + stay_outcomes["lose"])
stay_win_p = np.round(stay_win_p * 100, 2)

print(f"{N} iterations: switching won {switch_win_p}%, staying won {stay_win_p}%.")


# ------------------------------------------------------- #
# ALTERNATIVE: randomly select one of the remaining doors #
# ------------------------------------------------------- #

# make the random choice
df["random_choice"] = df["door_revealed"].apply(lambda x: random_choice(x, doorlist))

# determine the winner
df["rc_outcome"] = df.apply(lambda row: row[row["random_choice"]], axis=1)
df["rc_outcome"] = df["rc_outcome"].replace({"g": "lose", "c": "win"})

# probabilities
rc_outcomes = Counter(df["rc_outcome"])
rc_win_p = rc_outcomes["win"] / (rc_outcomes["win"] + rc_outcomes["lose"])
rc_win_p = np.round(rc_win_p * 100, 2)
print(f"{N} iterations: random choice gives you a win {rc_win_p}%.")
