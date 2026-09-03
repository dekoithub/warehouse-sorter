import pytest
import copy

from models.enums import OutputBinStatus
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

def test_output_bin_state_management(item):
    # Create an empty OutputBin
    # Создаем пустой OutputBin
    output_bin = OutputBin(
        bin_id=1,
        capacity=2,
    )

    assert output_bin.current_load == 0
    assert output_bin.status == OutputBinStatus.EMPTY
    assert output_bin.is_full is False

    # Add the first Item
    # Добавляем первый Item
    output_bin.add_item(item)

    assert output_bin.current_load == 1
    assert output_bin.status == OutputBinStatus.OCCUPIED
    assert output_bin.is_full is False

    # Add the second Item
    # Добавляем второй Item
    second_item = copy.deepcopy(item)
    output_bin.add_item(second_item)

    assert output_bin.current_load == 2
    assert output_bin.status == OutputBinStatus.FULL
    assert output_bin.is_full is True

    # Clear the OutputBin
    # Очищаем OutputBin
    output_bin.remove_all_items()

    assert output_bin.current_load == 0
    assert output_bin.status == OutputBinStatus.EMPTY
    assert output_bin.is_full is False