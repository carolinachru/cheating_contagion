# PART III. Simulating alternative universe


## Base functions
# III.A Player-to-player randomization

import random

def random_player_assignation(kills_ls, cheaters_ls):
    ''' Assumes that kills_ls data is organized by match, i.e. observations from the same match are adjacent.
    Kills_ls is a list of the killings record and cheaters_ls a dictionary with cheater's
    information regarding estimated cheating date.

    Returns a dictionary with a within-match randomization of non-cheater players (at the match date).
    Each key is a match and the value is another dictionary with the equivalence/permutation of randomized
    players (which are not cheaters at the day the match started).
    Example: {'match3x' : {player1 : player6, player4 : player10, ...}, ...}
    '''
    # Part A
    # Creates a dictionary were keys are the match_id, and the values are dictionaries were the
    #   keys are (non-cheater) players about to be randomized
    # Registers all players by each match which aren't cheaters at the day of the match

    permut_ran = {}

    for i in range(len(kills_ls)):

        match_id = kills_ls[i][0]

        if match_id != kills_ls[i-1][0]: # Recognizes new match by the ID
            permut_ran[match_id] = {}
            match_date = kills_ls[i][3]

        acc_kill = kills_ls[i][1]
        acc_vic = kills_ls[i][2]

        # Add non-cheater (at day of the match) killer to dictionary for the respective match
        if acc_kill not in permut_ran and \
        ((acc_kill not in cheaters_ls) or ((acc_kill in cheaters_ls) and (match_date < cheaters_ls[acc_kill][0]))):
            permut_ran[match_id][acc_kill] = 0

        # Add non-cheater (at day of the match) victim to dictionary for the respective match
        if acc_vic not in permut_ran and \
        ((acc_vic not in cheaters_ls) or ((acc_vic in cheaters_ls) and (match_date < cheaters_ls[acc_vic][0]))):
            permut_ran[match_id][acc_vic] = 0

    # Part B
    # Uses permut_ran from Part A to assign the randomized player equivalent
    # to each of the non-cheater players within match

    all_matches = list(permut_ran.keys())

    for m in all_matches:

        # All players except active cheaters
        all_players = list(permut_ran[m].keys())

        all_players_ran = random.sample(all_players, len(all_players))

        for i in range(len(all_players)):
            permut_ran[m][all_players[i]] = all_players_ran[i] # Insert the equivalent player

    return permut_ran


# III.B Creating alternative universe

def new_random_data(kills_ls, permut_ran_dict):
    '''Assumes that kills_ls data is a list with the match record of killings, and permut_ran_dict, a
    dictionary that captures a within-match permutation of non-cheating players (at the time) denoting
    randomization.

    Returns a new list with the same structure as kills_ls but with randomized non-cheating players.
    '''
    kills_new_ls = [x[:] for x in kills_ls]

    for i in range(len(kills_new_ls)):
        match_id = kills_new_ls[i][0]
        acc_kill = kills_new_ls[i][1]
        acc_vic = kills_new_ls[i][2]

        # Conditional to avoid testing cheaters
        if acc_kill in permut_ran_dict[match_id]:
            kills_new_ls[i][1] = permut_ran_dict[match_id][acc_kill]

        if acc_vic in permut_ran_dict[match_id]:
            kills_new_ls[i][2] = permut_ran_dict[match_id][acc_vic]

    return(kills_new_ls)

# List was not being copied fully so used solution from:
# https://stackoverflow.com/questions/8913026/list-copy-not-working


## Implementation functions
# III.C Randomize and save each file

import pickle

def randomize_save(file_name, kills_ls, cheaters_ls, n_randomiz):
    '''Assumes file_name, a string denoting the root name for which the files will be saved;
    kills_ls the data of killings; cheaters_ls the data of cheaters; and, n_randomiz, the
    number of randomizations to be carried out.

    Returns n_randomiz randomizations of kills_ls saved in the current working directory.
    For example, if the user specifies file_name = 'Random' and n_randomiz = 2,
    it will save two files: Random0 and Random1.
    '''

    # Run randomization
    permutations = [random_player_assignation(kills_ls, cheaters_ls) for n in range(n_randomiz)]
    new_data_ls = [new_random_data(kills_ls, permutations[n]) for n in range(n_randomiz)]

    # Save file
    file_list = [file_name + str(num) for num in range(n_randomiz)]

    for f in range(n_randomiz):
        with open (file_list[f], 'wb') as fw:
            pickle.dump(new_data_ls[f], fw)

    print(n_randomiz, 'file(s) saved!')

# III.D Load all files to a single list

def load_data_onelist(file_name, num_files):
    '''Assumes that file_name is a string to locate the data to be loaded, num_files determine
    the number of files to be loaded. This is, assumes there are specific number of files (num_files) with the
    same root name (file_name).

    Returns a single list that contains all the randomizations of the killings data.
    '''

    file_list = [file_name + str(num) for num in range(num_files)]
    obj_retrieved_open = []

    for i in range(num_files):
        with open (file_list[i], 'rb') as fr:
            obj_retrieved_open.append(pickle.load(fr))

    return obj_retrieved_open
