import copy

import pytest

from models.enums import OutputBinStatus
from models.item import Item
from models.output_bin import OutputBin


def assert_output_bin_state(
    output_bin: OutputBin,
    expected_load: int,
    expected_status: OutputBinStatus,
    expected_full: bool,
) -> None:
    assert output_bin.current_load == expected_load
    assert output_bin.status == expected_status
    assert output_bin.is_full is expected_full


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
    bin_id: int,
    capacity: int,
) -> None:
    with pytest.raises(ValueError):
        OutputBin(
            bin_id=bin_id,
            capacity=capacity,
        )


def test_output_bin_state_management(
    item: Item,
) -> None:
    # Create an empty OutputBin
    # Создаем пустой OutputBin
    output_bin = OutputBin(
        bin_id=1,
        capacity=2,
    )

    assert_output_bin_state(
        output_bin,
        0,
        OutputBinStatus.EMPTY,
        False,
    )

    # Add the first Item
    # Добавляем первый Item
    output_bin.add_item(item)

    assert_output_bin_state(
        output_bin,
        1,
        OutputBinStatus.OCCUPIED,
        False,
    )

    # Add the second Item
    # Добавляем второй Item
    second_item = copy.deepcopy(item)
    output_bin.add_item(second_item)

    assert_output_bin_state(
        output_bin,
        2,
        OutputBinStatus.FULL,
        True,
    )

    # Clear the OutputBin
    # Очищаем OutputBin
    output_bin.remove_all_items()

    assert_output_bin_state(
        output_bin,
        0,
        OutputBinStatus.EMPTY,
        False,
    )
