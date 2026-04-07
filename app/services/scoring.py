from app.models.models import PlayerScore, Player, SCORING_RULES


def calculate_points(score: PlayerScore, position) -> float:
    pts = 0.0
    if score.minutes_played > 0:
        pts += SCORING_RULES["played"]
    pts += score.goals * SCORING_RULES["goal"].get(position, 3)
    pts += score.assists * SCORING_RULES["assist"]
    if score.clean_sheet:
        pts += SCORING_RULES["clean_sheet"].get(position, 0)
    pts += score.yellow_cards * SCORING_RULES["yellow_card"]
    pts += score.red_cards * SCORING_RULES["red_card"]
    pts += score.own_goals * SCORING_RULES["own_goal"]
    return pts
