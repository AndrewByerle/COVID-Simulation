"""This specially named module makes the package runnable."""

from projects.pj02 import constants
from projects.pj02.model import Model
from projects.pj02.ViewController import ViewController


def main() -> None:
    """Entrypoint of simulation."""
    model = Model(constants.CELL_COUNT, constants.CELL_SPEED, constants.FIRST_INFECTED, constants.FIRST_IMMUNE)
    vc = ViewController(model)
    vc.start_simulation()


if __name__ == "__main__":
    main()