import random
import simpy

main_list = []


def clear_main_list():
    # Clear the list before running it again
    main_list.clear()


def filter_main_list(main_list):
    filtered_data_out = list(filter(lambda x: "Out" in x.get("Status"), main_list))
    count_out_status = len(filtered_data_out)
    return count_out_status


class Loadingtruck(object):
    """A lading has a limited number of loading stations (``NUM_LOADING``) to
    fill truck in parallel.

    Trucks have to request one of the loading stations. When they got one, they
    can start the loading processes and wait for it to finish (which
    takes ``loading time`` minutes).
    """

    def __init__(self, env, num_loading_station, loadingtime):
        self.env = env
        self.loadingstation = simpy.Resource(env, num_loading_station)
        self.loadingtime = loadingtime

    # def filltruck(self, truck):
    def filltruck(self, truck, loadingtime):
        """The loading processes. It takes a ``Truck`` processes and starts
        to fill it oil."""
        yield self.env.timeout(random.randint(loadingtime - 10, loadingtime + 10))

    def drivetrucktostation(self, truck):
        """The moving process to enter the truck to loading processes. It takes a ``truck`` processes and tries."""
        yield self.env.timeout(random.randint(5, 15))


def truck(env, name, cw, loadingtime):
    """The truck process (each truck has a ``name``) arrives at the loading stations
    (``cw``) and requests a cleaning loading station.

    It then starts the loading process, waits for it to finish and
    leaves to never come back ...
    """
    with cw.loadingstation.request() as request:
        yield request

        data = {
            "Event": f"{name} drives to loading station 🚛",
            "Time": round(env.now / 60, 2),
            "Status": "In",
        }
        main_list.append(data)

        yield env.process(cw.drivetrucktostation(name))
        data = {
            "Event": f"{name} Start loading process ⛽️",
            "Time": round(env.now / 60, 2),
            "Status": "Fill",
        }
        main_list.append(data)

        yield env.process(cw.filltruck(name, loadingtime))
        yield env.process(cw.drivetrucktostation(name))
        data = {
            "Event": f"{name} left the loading station 🏁",
            "Time": round(env.now / 60, 2),
            "Status": "Out",
        }
        main_list.append(data)


def setup(env, num_loading_station, loadingtime, t_inter, no_trucks):
    """Create a loading truck, a number of initial trucks and keep creating trucks
    approx. Every ``t_inter`` minutes."""
    # Create the loading truck
    loadingtruck = Loadingtruck(env, num_loading_station, loadingtime)

    # Create x initial trucks
    for i in range(no_trucks):
        env.process(truck(env, f"Truck {i}", loadingtruck, loadingtime))

    # Create more trucks while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 5, t_inter + 5))
        i += 1
        env.process(truck(env, f"Truck {i}", loadingtruck, loadingtime))
