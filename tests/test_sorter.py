import pytest

from models.sorter import Sorter


@pytest.mark.parametrize(
    ("sorter_id", "supported_directions"),
    [
        (0, [1, 2, 3]),
        (-1, [1, 2, 3]),
        (1, []),
        (1, [0, 1, 2]),
        (1, [-1, 1, 2]),
        (1, [1, 2, 2]),
    ],
)
def test_sorter_rejects_invalid_data(
    sorter_id,
    supported_directions,
):
    with pytest.raises(ValueError):
        Sorter(
            sorter_id=sorter_id,
            supported_directions=supported_directions,
            is_available=True,
        )