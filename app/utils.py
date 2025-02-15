def transform_input(years_of_experience: int) -> int:
    """Ensures that experience is non-negative."""
    return max(0, years_of_experience)
