"""Creates the chart for pj02. 

I hypothesize that if I run a simulation with a bounds width of 600, a speed of 5.0,
300 total cells, 10 initially infected, and 2 initially immune,then the chart will 
display 1/2 or about 150 cells as the maximum number of infected cells during any one time,
given that the cells recover relatively quickly after approximately 3 seconds. 
I also think that there will be a steady upward trendline showing the immune cells, 
since all infected cells will be immunized, capping out at around 225 or 3/4 of all 300 cells. 
To my surprise, about 270 cells out of the 300 became infected at the peak of the pandemic, 
showing that nearly all of the 300 cells became infected at the same point in time.
It is a little mind boggling that even with increased bounds, 300 cells, and only 10 infected
from the start was enough to infect almost every cell before each cell's inevitable recovery. 
I was correct in that there was a steady upward trend of immune cells during the simmulation,
but I did not think that the line would reach the ceiling of 300, and it did.
"""


from typing import List
import argparse
from projects.pj02.model import Model
from projects.pj02 import constants


def main() -> None:
    parser = argparse.ArgumentParser(description='Determine number and types of initial cells')
    parser.add_argument("cells", type=int, help="Total number of cells present.")
    parser.add_argument("infected", type=int, help="Initial number of infected cells present.")
    parser.add_argument("immune", type=int, help="Initial number of immune cells present.")
    args = parser.parse_args()
    print(f"{args.cells} cells total, {args.infected} infected initially, {args.immune} immune initially")
    model = Model(args.cells, constants.CELL_SPEED, args.infected, args.immune)
    tick_list: List[int] = []
    num_infected: List[int] = []
    num_immune: List[int] = []
    while model.is_complete() != True:
        model.tick()
        tick_list.append(model.time)
        infected_counter: int = 0
        immune_counter: int = 0
        for cell in model.population:
            if cell.is_infected():
                infected_counter += 1
            if cell.is_immune():
                immune_counter += 1  
        num_infected.append(infected_counter)
        num_immune.append(immune_counter)
    if model.is_complete:
        chart_data(num_infected, num_immune, tick_list)
        print("done")
  

def chart_data(infected_cells: List[int], immune_cells: List[int], time: List[int]) -> None:
    """Charts data over a period of one month."""
    import matplotlib.pyplot as plt
    plt.plot(time, infected_cells, label = "infected cells")
    plt.plot(time, immune_cells, label = "immune cells")
    plt.xlabel("Time Ticks in the Simulation")
    plt.ylabel("Number of Cells")
    plt.title(f"Infected and Immune Cells Over Time")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()