import copy

import pytest

from models.buffer import Buffer
from models.controller import Controller
from models.conveyor import Conveyor
from models.enums import ItemStatus
from models.scanner import Scanner
from models.sorter import Sorter
from models.wms import WMS


def create_controller(
    routes: dict[str, int],
    wms_available: bool = True,
) -> Controller:
    # Create a standard Scanner for Controller integration tests
    # Создаем стандартный Scanner для интеграционных тестов Controller
    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    # Create WMS with configurable routes and availability
    # Создаем WMS с настраиваемыми маршрутами и доступностью
    wms = WMS(
        routes=routes,
        available_destinations=[1, 2, 3, 4, 5],
        is_available=wms_available,
    )

    # Return a ready-to-use Controller
    # Возвращаем готовый к использованию Controller
    return Controller(
        scanner=scanner,
        wms=wms,
    )


@pytest.mark.parametrize(
    ("routes", "wms_available"),
    [
        ({}, True),
        ({"4601234567890": 5}, False),
    ],
)
def test_controller_sends_item_to_manual_processing_on_wms_error(
    item,
    routes,
    wms_available,
):
    # Create Controller with either a missing route or unavailable WMS
    # Создаем Controller либо без маршрута, либо с недоступной WMS
    controller = create_controller(
        routes=routes,
        wms_available=wms_available,
    )

    # Try to route the Item through WMS
    # Пытаемся получить маршрут для Item через WMS
    result = controller.route_item(item)

    # Controller must handle the exception instead of crashing
    # Controller должен обработать исключение, а не завершить программу
    assert result is None

    # Item must be redirected to manual processing
    # Item должен быть перенаправлен на ручную обработку
    assert item.status == ItemStatus.MANUAL_PROCESSING
    assert item.location == "Manual Processing"


def test_controller_uses_next_conveyor_when_first_is_unavailable(item):
    # Create Controller with a valid route
    # Создаем Controller с корректным маршрутом
    controller = create_controller(
        routes={item.barcode: 5},
    )

    # First Conveyor is unavailable and must raise an equipment error
    # Первый Conveyor недоступен и должен вызвать ошибку оборудования
    unavailable_conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=False,
    )

    # Second Conveyor is available and should accept the Item
    # Второй Conveyor доступен и должен принять Item
    available_conveyor = Conveyor(
        conveyor_id=2,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    # Register both conveyors in processing order
    # Добавляем оба конвейера в порядке обработки
    controller.conveyors.extend(
        [
            unavailable_conveyor,
            available_conveyor,
        ]
    )

    # Route the Item through Controller
    # Маршрутизируем Item через Controller
    destination = controller.route_item(item)

    # Controller must skip the unavailable Conveyor
    # Controller должен пропустить недоступный Conveyor
    assert destination == 5
    assert item not in unavailable_conveyor.items

    # Item must be accepted by the second Conveyor
    # Item должен быть принят вторым Conveyor
    assert item in available_conveyor.items
    assert item.status == ItemStatus.MOVING
    assert item.location == "Conveyor 2"


def test_controller_uses_next_buffer_when_first_is_full(item):
    # WMS is irrelevant for this test because we test send_to_buffer directly
    # WMS здесь не важна, потому что тестируем send_to_buffer напрямую
    controller = create_controller(routes={})

    # First Buffer can store only one Item
    # Первый Buffer может хранить только один Item
    first_buffer = Buffer(
        buffer_id=1,
        capacity=1,
    )

    # Second Buffer will remain available
    # Второй Buffer останется свободным
    second_buffer = Buffer(
        buffer_id=2,
        capacity=1,
    )

    # Create a separate Item so the first Buffer becomes full
    # Создаем отдельный Item, чтобы полностью заполнить первый Buffer
    blocking_item = copy.deepcopy(item)
    first_buffer.add_item(blocking_item)

    # Register buffers in processing order
    # Добавляем буферы в порядке обработки
    controller.buffers.extend(
        [
            first_buffer,
            second_buffer,
        ]
    )

    # Controller must try to buffer the original Item
    # Controller должен попытаться отправить исходный Item в буфер
    result = controller.send_to_buffer(item)

    # First Buffer raises BufferFullError,
    # so Controller must continue to the second Buffer
    # Первый Buffer вызывает BufferFullError,
    # поэтому Controller должен перейти ко второму Buffer
    assert result is True
    assert item in second_buffer.items
    assert item.status == ItemStatus.BUFFERED
    assert item.location == "Buffer 2"


def test_controller_sends_item_to_buffer_when_sorter_is_unavailable(item):
    # Create Controller with a valid route
    # Создаем Controller с корректным маршрутом
    controller = create_controller(
        routes={item.barcode: 5},
    )

    # Add a Buffer for fallback processing
    # Добавляем Buffer для резервной обработки
    buffer = Buffer(
        buffer_id=1,
        capacity=2,
    )
    controller.buffers.append(buffer)

    # Create an unavailable Sorter
    # Создаем недоступный Sorter
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=False,
    )

    # Item already has a destination before reaching the Sorter
    # Перед попаданием в Sorter у Item уже должно быть назначение
    item.set_destination(5)

    # Simulate a valid sensor event near the Sorter
    # Имитируем корректное событие сенсора возле Sorter
    result = controller.process_sorter_event(
        {"item_id": item.id},
        item,
        sorter,
    )

    # Controller must catch EquipmentUnavailableError
    # and redirect the Item to Buffer
    # Controller должен поймать EquipmentUnavailableError
    # и перенаправить Item в Buffer
    assert result is None
    assert item in buffer.items
    assert item.status == ItemStatus.BUFFERED
    assert item.location == "Buffer 1"


def test_controller_handles_unsupported_sorter_direction(item):
    # Create Controller for a normal warehouse route
    # Создаем Controller для обычного маршрута склада
    controller = create_controller(
        routes={item.barcode: 5},
    )

    # Sorter supports only directions from 1 to 5
    # Sorter поддерживает только направления от 1 до 5
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    # Assign an unsupported destination to trigger the exception
    # Устанавливаем неподдерживаемое направление для вызова исключения
    item.set_destination(99)

    # Process the Item at the Sorter
    # Обрабатываем Item на Sorter
    result = controller.process_sorter_event(
        {"item_id": item.id},
        item,
        sorter,
    )

    # Controller must catch UnsupportedDirectionError
    # instead of allowing the whole system to crash
    # Controller должен поймать UnsupportedDirectionError,
    # а не позволить всей системе завершиться с ошибкой
    assert result is None

    # Item must be redirected to manual processing
    # Item должен быть перенаправлен на ручную обработку
    assert item.status == ItemStatus.MANUAL_PROCESSING
    assert item.location == "Manual Processing"
