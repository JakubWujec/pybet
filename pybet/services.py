from config import Config


def calculate_points(
    bet_home_score: int,
    bet_away_score: int,
    match_home_score: int,
    match_away_score: int,
):
    match_score_diff = match_home_score - match_away_score
    bet_score_diff = bet_home_score - bet_away_score

    if bet_home_score == match_home_score and match_away_score == bet_away_score:
        return Config.POINTS_FOR_EXACT_SCORE
    elif bet_score_diff == 0 and match_score_diff == 0:
        return Config.POINTS_FOR_DRAW
    elif match_score_diff * bet_score_diff > 0:
        return Config.POINTS_FOR_WINNER

    return Config.POINTS_FOR_MISS


def calculate_points_for_score(
    bet_home_score: int,
    bet_away_score: int,
    match_home_score: int,
    match_away_score: int,
) -> int:
    if bet_home_score == match_home_score and match_away_score == bet_away_score:
        return Config.POINTS_FOR_EXACT_SCORE
    return 0


def calculate_points_for_result(
    bet_home_score: int,
    bet_away_score: int,
    match_home_score: int,
    match_away_score: int,
) -> int:
    if match_home_score == match_away_score and bet_home_score == bet_away_score:
        return Config.POINTS_FOR_DRAW
    match_score_diff = match_home_score - match_away_score
    bet_score_diff = bet_home_score - bet_away_score
    if match_score_diff * bet_score_diff > 0:
        return Config.POINTS_FOR_WINNER
    return Config.POINTS_FOR_MISS
