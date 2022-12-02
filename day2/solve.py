with open('input.txt') as fh:
    plays = [line.strip().split() for line in fh.readlines()]

victories = {'R':'S','S':'P','P':'R'}
loses = {v:k for k,v in victories.items()}
play_points = {'R':1,'P':2,'S':3}

# Part 1
conversions = {'A':'R','B':'P','C':'S',
               'X':'R','Y':'P','Z':'S'}

score = 0
for play in plays:
    other_elf, me = [conversions[part] for part in play]
    round_score = play_points[me]
    if other_elf == me: # draw
        round_score += 3
    elif other_elf == victories[me]: # i win
        round_score += 6
    score += round_score

print(score)

# Part 2
conversions = {'A':'R','B':'P','C':'S',
               'X':'L','Y':'D','Z':'W'}
win_lose_scores = {'W':6,'D':3,'L':0}

score = 0
for play in plays:
    other_elf, end_state = [conversions[part] for part in play]
    round_score = win_lose_scores[end_state]
    if end_state == 'W':
        round_score += play_points[loses[other_elf]] # other elf needs to lose
    elif end_state == 'L':
        round_score += play_points[victories[other_elf]] # other elf needs to win
    elif end_state == 'D':
        round_score += play_points[other_elf] # play is same points as elf
    score += round_score

print(score)
