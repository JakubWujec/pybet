import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests


@dataclass(frozen=True)
class MatchResultDTO:
    home_team_short_name: str
    away_team_short_name: str
    home_team_score: int
    away_team_score: int
    finished: bool


class ScoreProvider(abc.ABC):
    def get_match_results(self, gamestage_id: int) -> List[MatchResultDTO]:
        raise NotImplementedError


class FPLScoreProvider(ScoreProvider):
    BASE_URL = "https://fantasy.premierleague.com/api/fixtures/?event={FPL_EVENT}"
    FPL_ID_TO_NAME_MAPPING = {
        1: "ARS",
        2: "AVL",
        3: "BOU",
        4: "BRE",
        5: "BHA",
        6: "CHE",
        7: "CRY",
        8: "EVE",
        9: "FUL",
        10: "IPS",
        11: "LEI",
        12: "LIV",
        13: "MCI",
        14: "MUN",
        15: "NEW",
        16: "NFO",
        17: "SOU",
        18: "TOT",
        19: "WHU",
        20: "WOL",
    }

    def get_match_results(self, gamestage_id: int) -> List[MatchResultDTO]:
        r = requests.get(url=self.BASE_URL.format(FPL_EVENT=gamestage_id))
        data = r.json()
        result = [
            MatchResultDTO(
                home_team_short_name=self.FPL_ID_TO_NAME_MAPPING[fixture["team_h"]],
                away_team_short_name=self.FPL_ID_TO_NAME_MAPPING[fixture["team_a"]],
                home_team_score=fixture["team_h_score"],
                away_team_score=fixture["team_a_score"],
                finished=fixture["finished"],
            )
            for fixture in data
        ]

        return result
