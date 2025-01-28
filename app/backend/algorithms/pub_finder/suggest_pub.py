# Chosen to make this modular. Means testing will be easier to carry out. Ensure this module does not depend on anything Flask related. This will make it easier to test in a standalone way.
# Take all inputs as arguments

# Currently takes a list of all users and all pubs as input. Down the line, this can be changed to take a group_id and query pubs from the database based upon say lat and lng, which will make the function ultimately more modular and easier to test, and also more efficient.

# Dictionary to hold available algorithms
ALGORITHMS = {}


def register_algorithm(name):
    def decorator(func):
        ALGORITHMS[name] = func
        return func

    return decorator


@register_algorithm("geo-centre")
def geographical_centre(users, pubs):
    print(users)
    print(pubs)


@register_algorithm("simulated_annealing")
def simulated_annealing(users, pubs):
    # Your simulated annealing algorithm implementation here
    pass


# TODO(@TS): Decide upon where I should put the default algorithm value. Maybe just at os.getenv() level.
def suggest_pub(users, pubs, algorithm="geo-centre"):
    """
    Function to find optimal pub based on user locations using the specified algorithm.
    Returns: Pub object
    """
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Algorithm {algorithm} is not registered.")

    return ALGORITHMS[algorithm](users, pubs)
