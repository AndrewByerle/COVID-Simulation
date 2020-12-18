"""Constants used through the simulation."""

BOUNDS_WIDTH: int = 600
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 600
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20

CELL_RADIUS: int = 10
CELL_COUNT: int = 150
CELL_SPEED: float = 3.0

BOUNCE_CUSHION: float = CELL_RADIUS * 0.01

VULNERABLE: int = 0
INFECTED: int = 1
IMMUNE: int = -1
RECOVERY_PERIOD: int = 90

FIRST_INFECTED: int = 1
FIRST_IMMUNE: int = 0

