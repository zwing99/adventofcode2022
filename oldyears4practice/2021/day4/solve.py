import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

numbers_called = lines.pop(0).split(',')
#print(numbers_called)

def read_cards_markers():
    cards = []
    markers = []

    for i in range(int(len(lines)/6)):
        card_lines = lines[6*i+1:6*i+6]
        card = []
        marker = []
        m = [False for i in range(5)]
        for line in card_lines:
            line_parts = line.split()
            card.append(line_parts)
            m = [False for i in range(5)]
            marker.append(m)
        cards.append(card)
        markers.append(marker)
    return cards, markers

def call_number(number):
    for c, card in enumerate(cards):
        for i in range(5):
            for j in range(5):
                if card[i][j] == number:
                    markers[c][i][j] = True


def look_for_winners():
    for m, marker in enumerate(markers):
        for i in range(5):
            row_wins = True
            for j in range(5):
                row_wins &= marker[i][j]
            if row_wins:
                return m
        for i in range(5):
            row_wins = True
            for j in range(5):
                row_wins &= marker[j][i]
            if row_wins:
                return m
    return -1


def score_card(number, m):
    marker = markers[m]
    card = cards[m]
    sum = 0
    for i in range(5):
        for j in range(5):
            if marker[i][j] == False:
                sum += int(card[i][j])
    return sum * int(number)


# part 1
cards, markers = read_cards_markers()
for number in numbers_called:
    #print(number)
    call_number(number)
    c = look_for_winners()
    if c != -1:
        print(f"winner: {c}")
        score = score_card(number, c)
        print(score)
        break

# part 2
cards, markers = read_cards_markers()
last_winner = -1
for number in numbers_called:
    #print(number)
    call_number(number)
    c = look_for_winners()
    while c != -1:
        score = score_card(number, c)
        last_winner = score
        markers.pop(c)
        cards.pop(c)
        c = look_for_winners()

print(last_winner)

