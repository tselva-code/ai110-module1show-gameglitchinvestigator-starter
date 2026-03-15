def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # Defect 4 Fix (range): Original code returned 1–20 for Easy and 1–50 for
    # Hard, creating a mismatch — the UI showed 1–100 but the secret was drawn
    # from a narrower range and Defect 7's validation also blocked guesses above
    # that narrower bound. We spotted this by switching to Easy, guessing 50,
    # and receiving a range error even though the UI said 1–100 was valid.
    # Discussed with AI, which confirmed difficulty should be expressed through
    # attempt count alone. All tiers now return the same 1–100 range.
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Defect 1 - Issue 1 Fix Start: The original AI-generated code had the hint
    # messages swapped — "Go HIGHER!" was shown when the guess was too high, and
    # "Go LOWER!" when too low. We caught this by playing the game and noticing
    # the hints led players in the wrong direction. Collaborated with AI to
    # confirm the logic inversion, then swapped the two return strings to match
    # the conditions.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"
    # Defect 1 - Issue 1 Fix End


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # Defect 5 Fix Start: scoring formula used (attempt_number + 1) instead of
    # (attempt_number - 1), so a perfect first guess scored 80 instead of 100.
    # Wrong-guess penalties also had no floor, letting the score go negative.
    # We verified the off-by-one by tracing the formula with attempt_number=1
    # on paper; AI confirmed the correct expression and suggested max(0, ...)
    # as the standard pattern for flooring a running total at zero.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return max(0, current_score + 5)
        return max(0, current_score - 5)

    if outcome == "Too Low":
        return max(0, current_score - 5)
    # Defect 5 Fix End

    return current_score
