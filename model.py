"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730310107"  # TODO


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, a_point: Point) -> float:
        """Calculates the distance between two points."""
        return sqrt((a_point.x - self.x)**2 + (a_point.y - self.y)**2)


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        """Responsible for cell movement."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
        if self.sickness > constants.RECOVERY_PERIOD:
            self.immunize()
        
    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable():
            return "gray"
        elif self.is_infected():
            return "red"
        elif self.is_immune():
            return "blue"
        else:
            return "gray"

    def contract_disease(self) -> None:
        """Asigns the INFECTED constant defined above to the sickness attribute."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Checks to see if sickness attribute equals VULNERABLE or not."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Checks to see if the cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, a_cell: Cell) -> None:
        """Transfers infection when two cells collide."""
        if a_cell.is_infected() and self.is_vulnerable():
            self.contract_disease()
        if self.is_infected() and a_cell.is_vulnerable():
            a_cell.contract_disease()

    def bounce(self, distance: float) -> None:
        """Bounces cells that come into contact."""
        if distance > 0 and distance < constants.CELL_RADIUS: 
            displacement: float = constants.CELL_RADIUS - distance 
            dir_x = -1 * self.direction.x
            dir_y = -1 * self.direction.y
            loc_x = self.location.x + (-1 * self.direction.x * displacement + constants.BOUNCE_CUSHION)
            loc_y = self.location.y + (-1 * self.direction.y * displacement + constants.BOUNCE_CUSHION)
            self.location.x = loc_x
            self.location.y = loc_y
            self.direction.x = dir_x
            self.direction.y = dir_y

    def immunize(self) -> None:
        """Recovers infected cell."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Checks if cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False


class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, first_infected: int, first_immune: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if first_infected >= cells:
            raise ValueError(f"Starting infected population must be less than {cells}")
        elif first_immune >= cells:
            raise ValueError(f"Starting immune population must be less than {cells}")
        elif first_infected <= 0:
            raise ValueError("Starting infected population must be greater than 0")
        elif first_immune < 0:
            raise ValueError("Starting immune population must be 0 or higher.")
        elif first_infected + first_immune >= cells:
            raise ValueError(f"Starting infected + immune population must be less than {cells}")
        for _ in range(0, cells - first_infected - first_immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for _ in range(0, first_infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            a_cell = Cell(start_loc, start_dir)
            a_cell.contract_disease()
            self.population.append(a_cell)
        for _ in range(0, first_immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            a_cell = Cell(start_loc, start_dir)
            a_cell.immunize()
            self.population.append(a_cell)

    def check_contacts(self) -> None:
        """Checks when cells collide and transfer the infection."""
        for cell in self.population:
            for cell2 in self.population:
                if cell2.location.distance(cell.location) < constants.CELL_RADIUS:
                    cell2.contact_with(cell)
   
    def bounce(self) -> None:
        """Bounces cells."""
        for cell in self.population:
            for cell2 in self.population:
                if cell2.location.distance(cell.location) < constants.CELL_RADIUS:
                    distance: float = cell2.location.distance(cell.location)
                    cell2.bounce(distance)
                           
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)         
        self.check_contacts()
        self.bounce()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        i: int = 0
        for cell in self.population:
            if cell.is_immune() or cell.is_vulnerable():
                i += 1
        if i == len(self.population):
            return True
        else:
            return False
