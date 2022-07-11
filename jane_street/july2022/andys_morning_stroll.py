# Ryan Grayson
# Jane Street Puzzle July 2022
# Andy's Morning Stroll

from fractions import Fraction

'''
Expected number of steps to return home on soccer ball:

(where Ex is the expected number of steps when andy is x steps away from home hexagon)

E = 1 + E1
E1 = 1 + (2/3)*E2
E2 = 1 + (1/3)*E1 + (1/3)*E2 + (1/3)*E3
E3 = 1 + (1/3)*E2 + (1/3)*E3 + (1/3)*E4
E4 = 1 + (2/3)*E3 + (1/3)*E5
E5 = 1 + E4

Solving, we get E = 20

Thus, for the floor, we need to find the probability that andy does NOT 
make it back to the home hexagon in 20 or less steps.

To do this, we will find the probability that andy makes it back to the home hexagon
on the floor in 20 or less steps, and 1 - this result will be our answer.
'''

freq = [1] + [ i * 3 for i in range(1, 12) ]

def get_neighbors(steps_away):
    if steps_away == 0:
        return [ [(1, 0), (1, 1), (1, 2)] ]

    if steps_away == 1:
        return [
            [ (0, 0), (2, 5), (2, 0) ], 
            [ (0, 0), (2, 1), (2, 2) ],
            [ (0, 0), (2, 3), (2, 4) ],
        ]

    neighbors = []
    odd = steps_away % 2
    increments = [steps_away // 2 + 1, steps_away // 2 ]
    if not odd:
        increments[1] -= 1
    upper_offset, lower_offset = 0, -1
    cur_inc, next_section = 1, 0

    if not odd:
        start, end = 0, freq[steps_away]
    else:
        start, end = (steps_away + 1) // 2, freq[steps_away] + (steps_away + 1) // 2
        lower_offset += 1
        
    for position in range(start, end):
        if (position - start) == next_section:
            cur_inc = (cur_inc + 1) % 2
            next_section += increments[cur_inc]

            if cur_inc == 1:
                upper_offset += 1
                if odd and position >= freq[steps_away]:
                    upper_offset %= 3

        if (position - start) % steps_away == 0:
            lower_offset += 1
            if odd and position >= freq[steps_away]:
                    lower_offset %= 3

        if steps_away == 2:
            upper_offset = lower_offset
        elif odd and position >= freq[steps_away]:
            lower_offset %= 3
            upper_offset %= 3
            position %= freq[steps_away]

        if odd and position == 0:
            neis_here = [
                (steps_away - 1, 0 ),
                (steps_away + 1, freq[steps_away + 1] - 1 ),
                (steps_away + 1, 0 ),
            ]
        elif cur_inc == 0 or steps_away == 2:
            neis_here = [
                (steps_away - 1, (position - lower_offset) % freq[steps_away - 1] ),
                (steps_away + 1, (position + upper_offset) ),
                (steps_away + 1, (position + upper_offset + 1)),
            ]
        else:
            neis_here = [
                (steps_away - 1, (position - lower_offset - 1) ),
                (steps_away - 1, (position - lower_offset) % freq[steps_away - 1] ),
                (steps_away + 1, (position + upper_offset ) ),
            ]

        neighbors.append(neis_here)

    if odd:
        neighbors = neighbors[-start:] + neighbors[:-start]
    return neighbors


mem = [ [ [-1] * freq[steps_away] for steps_away in range(12) ] for steps_taken in range(21) ]
for steps_taken in range(21):
    for steps_away in range(12):
        for position in range(freq[steps_away]):
            if steps_away == 11 or steps_taken + steps_away > 20:
                mem[steps_taken][steps_away][position] = 0
            elif steps_away == 0:
                mem[steps_taken][steps_away][position] = 1


def prob_back_in_20(steps_taken, steps_away, position):
    if steps_away == 0:
        if position == 0:
            return 1
        # otherwise, we are at the home hexagon
        position = 0
    elif mem[steps_taken][steps_away][position] != -1:
        return mem[steps_taken][steps_away][position]

    prob = 0
    for neighbor in adj_map[steps_away][position]:
        nei_sa, nei_pos = neighbor
        prob += (1/3) * prob_back_in_20(steps_taken + 1, nei_sa, nei_pos)

    mem[steps_taken][steps_away][position] = prob
    return prob


adj_map = []
for steps_away in range(11):
    adj_map.append( get_neighbors(steps_away) )

for steps, row in enumerate(adj_map):
    for position, neighbors in enumerate(row):
        print('steps_away: ', steps, 'position: ', position)
        print('neighbors: ', neighbors)
        print()
    print()


print('probability of making back to home hexagon in <= 20 steps on the floor: ')
# using -1 for first position to indicate the start of the walk
prob_20 = prob_back_in_20(0, 0, -1)
print(prob_20)
print()
ans = 1 - prob_20
print('ANSWER: ')
print(ans)
# print()