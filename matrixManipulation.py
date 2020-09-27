import numpy as np


matrix_size = 1024  # defines the size of the matrix
current_generation = np.zeros((matrix_size, matrix_size))  # sets up the matrix (full of zeroes)

# creates an empty matrix that will count the neighbours for each cell
neighbor_count = np.zeros((matrix_size, matrix_size))

to_live = np.empty([1, 1])
to_die = np.empty([1, 1])
to_be_born = np.empty([1, 1])
print(to_die)
gen_saver = []

# current_generation = np.random.randint(low= 0, high= 1, size= (matrix_size, matrix_size))

current_generation[501, 501] = 1
current_generation[501, 502] = 1
current_generation[501, 503] = 1
current_generation[502, 501] = 1
current_generation[503, 502] = 1


def create_neighbour_matrix():
    global neighbor_count
    neighbor_count = np.zeros((matrix_size, matrix_size))
    live_cells = np.where(current_generation == 1)
    # print(live_cells)
    for pos in range(len(live_cells[0])):
        for col in range(-1, 2):  # when added to the x position, will be x-1, x , and x + 1
            for row in range(-1, 2):  # when added to the y position will be y-1, y, and y + 1
                neighbor_count[live_cells[0][pos] + row, live_cells[1][pos] + col] += 1
                # adds one to the current count of neighbours in all
        neighbor_count[live_cells[0][pos], live_cells[1][pos]] -= 1
        # the process of adding neighbors adds 1 the the cell itself. However you cannot be your own neighbour,
        # so the line above hack removes the extra count


create_neighbour_matrix()


# print(neighbor_count)


def remove_outer_cells():   # this function removes the cells on the outside which could move outside the
    # range of the function and cause
    current_generation[matrix_size-5:matrix_size, 0:matrix_size] = 0
    current_generation[0:matrix_size - 5, matrix_size - 5:matrix_size] = 0
    # print(current_generation)


def next_generation():
    remove_outer_cells()
    create_neighbour_matrix()  # calculates the neighbours
    global current_generation
    # to_die = np.where(neighbor_count <= 1 or neighbor_count >=4)
    # commented out because it will die without haaving to check this since it won't live/be born
    to_live = np.where(neighbor_count == 2)
    to_be_born = np.where(neighbor_count == 3)
    if (len(gen_saver) >= 100):  # removes the first (oldest) array in the list
        gen_saver.pop(0)
    gen_saver.append(current_generation)  # caches the old generations
    interim_matrix = np.zeros((matrix_size, matrix_size))  # temporary matrix so we can reference the old matrix
    for cell in range(len(to_live[0])):  # keeps cells alive if they are live previously
        if current_generation[to_live[0][cell], to_live[1][cell]] == 1:
            interim_matrix[to_live[0][cell], to_live[1][cell]] = 1
    for cell in range(len(to_be_born[0])):  # births all new cells + those who are alive with 3 neighbors
        interim_matrix[to_be_born[0][cell], to_be_born[1][cell]] = 1
    current_generation = interim_matrix
    # print(to_live)
    # print(to_be_born)
    # print(current_generation)
    # print(gen_saver)

