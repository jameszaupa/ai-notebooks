# Paper link: https://wwwf.imperial.ac.uk/~dturaev/neller-lanctot.pdf
import numpy as np

ROCK, PAPER, SCISSOR, ACTION_SPACE = 0, 1, 2, 3
ACTION = {
    0: "ROCK",
    1: "PAPER",
    2: "SCISSOR",
}

opponent_distribution = [0.7, 0.2, 0.1]

regret_prob = [0, 0, 0]
regret_sum = 0


def get_action(prob):
    r = np.random.uniform(high=1.0)
    t = 0

    for i, p in enumerate(prob):
        t += p
        if r <= t:
            return i


def get_winnner(action_p_1, action_p_2):
    # Returns 1 for p1 win else -1 (0 for draw)
    if action_p_1 == 0 and action_p_2 == 2:
        return 1
    if action_p_1 == 1 and action_p_2 == 0:
        return 1
    if action_p_1 == 2 and action_p_2 == 1:
        return 1
    if action_p_1 == action_p_2:
        return 0
    return -1


def update_regret_vector(r_v, action, end_state):
    # Draw
    if end_state == 0:
        if action == 0:
            # Rock -> Paper+1
            r_v[PAPER] += 1
        if action == 1:
            # Paper -> Scissor+1
            r_v[SCISSOR] += 1
        if action == 2:
            # Scissor -> Rock+1
            r_v[ROCK] += 1

    # Loss
    elif end_state == -1:
        if action == 0:
            # Regret not winning
            r_v[SCISSOR] += 2
            # Regret not drawing
            r_v[PAPER] += 1
        if action == 1:
            r_v[ROCK] += 2
            r_v[SCISSOR] += 1
        if action == 2:
            r_v[PAPER] += 2
            r_v[ROCK] += 1


def normalize_regret_vector(r_v, r_sum):
    return [r/r_sum for r in r_v]


regret_vector = [0]*ACTION_SPACE
regret_vector_norm = [0.33]*ACTION_SPACE
regret_sum = 0
p1_score = 0
p2_score = 0
episodes_n = 100000

for i in range(episodes_n):
    # P1 is the agent
    action_p_1 = get_action(regret_vector_norm)
    # P2 is the opponent
    action_p_2 = get_action(opponent_distribution)

    assert action_p_1 in (0, 1, 2)
    assert action_p_2 in (0, 1, 2)

    end_state = get_winnner(action_p_1, action_p_2)

    if end_state == 1:
        p1_score += 1
    elif end_state == -1:
        p2_score += 1

    # Update, normalize and sum the regret
    if end_state != 1:
        update_regret_vector(regret_vector, action_p_1, end_state)
        regret_sum = sum(regret_vector)
        regret_vector_norm = normalize_regret_vector(regret_vector, regret_sum)
    # print(ACTION[action_p_1], ACTION[action_p_2], end_state)

print(f'Final distribution: {regret_vector_norm}')
print(
    f'P1 score: {p1_score/episodes_n*100}%, P2 score {p2_score/episodes_n*100}%, Draw {(episodes_n-p1_score-p2_score)/episodes_n*100}%')
