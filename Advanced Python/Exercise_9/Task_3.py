import matplotlib.pyplot as plt
import matplotlib.animation as animation

grid_height, grid_width = 10, 20
grid = [[1 for _ in range(grid_height)] for _ in range(grid_width)]
cell_colors = {0: 'black', 1: 'white'}

move_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
current_direction = 0
ant_position_x, ant_position_y = grid_width // 2, grid_height // 2
steps_to_precompute = 1000

fig, axis = plt.subplots()
axis.set_xlim(0, grid_width)
axis.set_ylim(0, grid_height)
axis.set_aspect('equal', adjustable='box')


def color_cell(x, y, color):
    axis.add_patch(plt.Rectangle((x, y), 1, 1, fc=color))


def animate_frame(frame_number):
    global ant_position_x, ant_position_y, grid_width, grid_height, grid, current_direction, move_directions

    if grid[ant_position_x][ant_position_y] == 1:
        current_direction = (current_direction + 1) % 4
        grid[ant_position_x][ant_position_y] = 0
    else:
        current_direction = (current_direction - 1) % 4
        grid[ant_position_x][ant_position_y] = 1
    color_cell(ant_position_x, ant_position_y, cell_colors[grid[ant_position_x][ant_position_y]])

    ant_position_x += move_directions[current_direction][0]
    ant_position_y += move_directions[current_direction][1]
    ant_position_x %= grid_width
    ant_position_y %= grid_height
    color_cell(ant_position_x, ant_position_y, 'green')


for step in range(steps_to_precompute):
    if grid[ant_position_x][ant_position_y] == 1:
        current_direction = (current_direction + 1) % 4
        grid[ant_position_x][ant_position_y] = 0
    else:
        current_direction = (current_direction - 1) % 4
        grid[ant_position_x][ant_position_y] = 1 

    ant_position_x += move_directions[current_direction][0]
    ant_position_y += move_directions[current_direction][1]
    ant_position_x %= grid_width
    ant_position_y %= grid_height

for x in range(grid_width):
    for y in range(grid_height):
        color_cell(x, y, cell_colors[grid[x][y]])

color_cell(ant_position_x, ant_position_y, 'green')

animation_instance = animation.FuncAnimation(fig, animate_frame, frames=60, interval=1000, repeat=True)
plt.show()
