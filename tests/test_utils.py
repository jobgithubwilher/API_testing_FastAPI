import pytest

from app.utils import transform_input


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        (5, 5),  # Normal case
        (-3, 0),  # Negative values should be set to 0
        (0, 0),  # Zero should remain zero
        (100, 100),  # Large positive number
        (-100, 0),  # Large negative number
    ],
)
def test_transform_input(input_value, expected_output):
    """Unit test for input transformation."""
    assert (
        transform_input(input_value) == expected_output
    ), f"Expected {expected_output} but got {transform_input(input_value)}"
