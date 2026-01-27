from collections import Counter

def rank_combined(chunk_scores: dict[int, float], frequency: Counter, bonus=0.1):
    final_scores = {}

    for idx, sim_score in chunk_scores.items():
        freq_score = frequency.get(idx, 0)
        final_scores[idx] = sim_score + (freq_score * bonus)

    return sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )