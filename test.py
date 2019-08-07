from gorgame import game
from gorgame import basics
import random

#CONSTANTS
x = 28
y = 18
tile_size = 5
space_size = 500
size = (700,500)
space_per_pixel = (max(x, y) * tile_size) / space_size

game = game.Game(size)

game.add_map([x,y], "manor map")
game.maps["manor map"].fill_random_tiles("red", 0, 1)
game.maps["manor map"].fill_random_tiles("green", 0, 1)
game.maps["manor map"].fill_random_tiles("blue", 0, 1)

game.add_space([x*5, y*5], "manor space")
game.spaces["manor space"].add_agent([22.5, 22.5], 2.5, "red", faction = "goblin", vision_radius = 60)
#game.spaces["manor space"].add_agent([65.5, -25.5], 2.5, "red", faction = "goblin", vision_radius = 60)
game.spaces["manor space"].add_agent([-52.5, -52.5], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_agent([-52.5, 12.5], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_agent([27.5, 42.5], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_wall([-60, 30], [60, -30], 3, "brown")
game.spaces["manor space"].add_wall([-60, -10], [40, -40], 3, "brown")

game.screen.window.add_component([0, 0], [space_size, space_size], 5, "display", background = "green", window = True)

game.screen.window.get("display").add_component([0, 0], [space_size, space_size], 5, "space", spaceview = True, faction = "party")
game.screen.window.get("display").get("space").add_space(game.spaces["manor space"], space_per_pixel)

game.screen.window.get("display").add_component([0, 0], [space_size, space_size], 4, "map", background = "brown", gridview = True)
game.screen.window.get("display").get("map").add_grid(game.maps["manor map"].tiles)

game.screen.window.add_component([500, 0], [200, 500], 10, "data", background = "teal", window = True)

game.screen.window.get("data").add_component([0, 0], [200, 30], 1, "x_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 30], [200, 30], 1, "y_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 60], [200, 30], 1, "current_entity", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 90], [200, 30], 1, "current_window", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 120], [200, 30], 1, "move_random", background = "blue", button = True)
game.screen.window.get("data").get("move_random").change_attributes(text = "Move", colour = "green")

def my_loop():
    if game.output:
        unit, x, y = None, None, None
        for key, value in game.output.items():
            if key == "unit id":
                unit = value
            if key == "move x":
                x = value
            if key == "move y":
                y = value
        if unit and x and y:
            move(int(game.output["unit id"]), int(game.output["move x"]), int(game.output["move y"]))
        remove_move_inputs()
    if game.screen.window.get("data").get("move_random").pressed:
        make_move_inputs()

def make_move_inputs():
    game.screen.window.get("data").add_component([0, 120], [int(200/3), 30], 1, "unit id", background = "white", input = True)
    game.screen.window.get("data").add_component([0 + int(200/3), 120], [int(200/3), 30], 1, "move x", background = "white", input = True)
    game.screen.window.get("data").add_component([0 + int(2*200/3), 120], [int(200/3), 30], 1, "move y", background = "white", input = True)
    game.screen.window.get("data").get("unit id").change_colours(active = "light grey")
    game.screen.window.get("data").get("move x").change_colours(active = "light grey")
    game.screen.window.get("data").get("move y").change_colours(active = "light grey")
    game.screen.window.get("data").get("unit id").change_default_text("Unit")
    game.screen.window.get("data").get("move x").change_default_text("x")
    game.screen.window.get("data").get("move y").change_default_text("y")

def remove_move_inputs():
    game.screen.window.get("data").remove("unit id")
    game.screen.window.get("data").remove("move x")
    game.screen.window.get("data").remove("move y")

def move_random():
    target = random.randint(0, len(game.spaces["manor space"].agents) - 1)
    x_dir = random.random() * tile_size * 2 - tile_size
    y_dir = random.random() * tile_size * 2 - tile_size
    move(target, x_dir, y_dir)

def move(unit, x, y):
    game.spaces["manor space"].agents[unit].loc.add(basics.Coords([x, y]))
    game.screen.window.get("display").get("space").space.agents[unit].loc.add(basics.Coords([x, y]))
    game.screen.window.get("display").get("space").update_locs()

while True:
    game.screen.window.get("data").get("x_coord_box").change_attributes(text = "x: " + str(game.screen.mouse_pos.x), colour = "red")
    game.screen.window.get("data").get("y_coord_box").change_attributes(text = "y: " + str(game.screen.mouse_pos.y), colour = "red")
    game.screen.window.get("data").get("current_entity").change_attributes(text = str(game.screen.current_entity), colour = "red")
    game.screen.window.get("data").get("current_window").change_attributes(text = str(game.screen.current_window), colour = "red")
    game.loop()
    my_loop()
