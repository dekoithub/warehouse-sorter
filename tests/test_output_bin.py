import pytest

from models.output_bin import OutputBin


@pytest.mark.parametrize(
    ("bin_id", "capacity"),
    [
        (0, 1),
        (-1, 1),
        (1, 0),
        (1, -1),
    ],
)
def test_output_bin_rejects_invalid_data(
    bin_id,
    capacity,
):
    with pytest.raises(ValueError):
        OutputBin(
            bin_id=bin_id,
            capacity=capacity,
        )