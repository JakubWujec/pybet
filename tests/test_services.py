import pytest
from pybet.services import calculate_points
from config import Config

# Mock configuration for testing
class MockConfig:
    POINTS_FOR_EXACT_SCORE = 5
    POINTS_FOR_DRAW = 3
    POINTS_FOR_WINNER = 2
    POINTS_FOR_MISS = 0

# Replace the actual Config with MockConfig in your test environment
Config.POINTS_FOR_EXACT_SCORE = MockConfig.POINTS_FOR_EXACT_SCORE
Config.POINTS_FOR_DRAW = MockConfig.POINTS_FOR_DRAW
Config.POINTS_FOR_WINNER = MockConfig.POINTS_FOR_WINNER
Config.POINTS_FOR_MISS = MockConfig.POINTS_FOR_MISS

@pytest.mark.parametrize(
    "bet_home_score, bet_away_score, match_home_score, match_away_score, expected_points",
    [
        # Exact score match
        (2, 1, 2, 1, MockConfig.POINTS_FOR_EXACT_SCORE),
        # Exact score for a draw
        (0, 0, 0, 0, MockConfig.POINTS_FOR_EXACT_SCORE),
         # Correct winner prediction
        (3, 1, 2, 0, MockConfig.POINTS_FOR_WINNER),
        # Correct winner prediction (negative score difference)
        (0, 2, 1, 3, MockConfig.POINTS_FOR_WINNER),
        # Correct draw prediction
        (1, 1, 2, 2, MockConfig.POINTS_FOR_DRAW),
        # Incorrect prediction
        (1, 2, 3, 0, MockConfig.POINTS_FOR_MISS),
        # Match draw, incorrect prediction
        (2, 3, 1, 1, MockConfig.POINTS_FOR_MISS),
    ],
)
def test_calculate_points(bet_home_score, bet_away_score, match_home_score, match_away_score, expected_points):
    points = calculate_points(bet_home_score, bet_away_score, match_home_score, match_away_score)
    assert points == expected_points