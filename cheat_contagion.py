# PART II. Identifying cheating contagion

# GENERAL ASSUMPTIONS
# 1.1 - A player observed cheating if its killer was cheating on the day the match started, and
#       either the player was not on the cheating's list or it was but the estimated date for
#       when they started cheating was on the day the match started or after.
# 1.2 - If a cheater player kills 3 players, for the next
# 1.3 - If a match happens across two days, the starting day of the match is used for further
#       calculations.
# 1.4 - The date when the player was banned was not taken into account, as the player should be
#       removed by the game and if was not, there might be an internal administrative process or
#       management of the situation which allowed the ID to be used.


# II.A Observing cheating behavior

def observed_cheating(kills_ls, cheaters_ls):
    ''' Assumes that within matches, kills_ls is sorted by the sequence of killings, i.e. by time, and
    that it is organized by match, i.e. observations from the same match are adjacent. Algorithm works
    row by row, important that data are sorted.
    Kills_ls is a list with the match record of killings and cheaters_ls a dictionary with cheater's
    information regarding estimated cheating date.

        Returns a list of lists, which characterize players which observed cheating under assumption 1.1 and 1.2.
    The scheme of an observation is the following:
    [possible cheater observer ID, date of observation, date cheating started]. The last argument is 0 if the
    player is not on the cheaters list (cheaters_ls).
    '''
    observed_cheat = []
    count_kill = {}

    for i in range(len(kills_ls)):

        # Identify new match and define start date of match
        if kills_ls[i][0] != kills_ls[i-1][0]:
            count_kill = {}
            match_date = kills_ls[i][3]

        killer = kills_ls[i][1]
        victim = kills_ls[i][2]

        kill_count = max(list(count_kill.values()), default = 0)

        # Case 1.
        #  If no cheating player has accumulated 3 or more killings
        if kill_count < 3:

            # If killer is cheater and started/was cheating on the day of the match
            if (killer in cheaters_ls) and (match_date >= cheaters_ls[killer][0]):

                # If victim not an actual cheater before match day
                if (victim not in cheaters_ls) or ((victim in cheaters_ls) and \
                                                    (match_date <= cheaters_ls[victim][0])):

                    # Add victim to motif-probable-cheater list
                    motif_temp = [victim,
                                  match_date,
                                  cheaters_ls[victim][0] if victim in cheaters_ls else 0]

                    observed_cheat.append(motif_temp)


                # Keep count of actual cheaters' number of kills
                if killer not in count_kill:
                    count_kill[killer] = 1
                else:
                    new_val = count_kill[killer] + 1
                    count_kill[killer] = new_val


        # Case 2:
        #  If at least one cheater sums 3 kills,
        #  for the next killings, actual non-cheater victims join motif-probable-cheater list
        else:
            if ((victim not in cheaters_ls) or ((victim in cheaters_ls) and \
                                                (match_date <= cheaters_ls[victim][0]))):

                motif_temp = [victim,
                              match_date,
                              cheaters_ls[victim][0] if victim in cheaters_ls else 0]
                observed_cheat.append(motif_temp)

    return observed_cheat


# II.B Observer-cheater motifs

def obs_cheater_motifs(observed_cheat_ls):
    ''' Assumes that observed_cheat_ls is a list of lists that contains possible observer-cheater motifs.
    The structure of such list should have the general scheme:
    [possible cheater-observer ID, date of observation, date cheating started]

    Returns a list with all observer-cheater motif's player ID.
    '''

    motif_cheater = []

    for i in range(len(observed_cheat_ls)):
        cheat_acc = observed_cheat_ls[i][0]
        match_saw = observed_cheat_ls[i][1]
        start_che = observed_cheat_ls[i][2]

        # Takes into account if player A observes cheating in different periods.
        if start_che != 0 and (cheat_acc not in motif_cheater):
            diff_days = start_che - match_saw

            if diff_days.days < 5:
                motif_cheater.append(cheat_acc)

    return motif_cheater
