from abc import ABC
from typing import Final


class Settings(ABC):
    MAIN_COLOR: Final[str] = "#1aadf1"
    SUB_COLOR: Final[str] = "53c2f5"
    SECONDARY_COLOR: Final[str] = "#0dd39e"
    ACCENT_COLOR: Final[str] = "#f4f9fb"

    DATA_AREA_HEIGHT: Final[int] = 625
    EDIT_AREA_HEIGHT: Final[int] = 600
    CONTAINER_WIDTH: Final[int] = 380
