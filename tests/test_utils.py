from app.utils import transform_input

def test_transform_input():
    """Unit test for input transformation."""
    assert transform_input(5) == 5
    assert transform_input(-3) == 0  # Ensuring negative values are set to 0
    assert transform_input(0) == 0
