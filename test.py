from gorgame import game
from gorgame import basics
import random

#CONSTANTS
x = 28
y = 18
tile_size = 5
space_size = 400
size = (700,500)
space_per_pixel = (max(x, y) * tile_size) / space_size

game = game.Game(size)

game.add_map([x,y], "manor map")
game.fill_map("random tiles", colour = "red", span = [0, 1])
game.fill_map("random tiles", colour = "green", span = [0, 1])
game.fill_map("random tiles", colour = "blue", span = [0, 1])

game.add_space([x*5, y*5], "manor space", default_agent_radius = 1.0, default_faction = "villager", default_wall_thickness = 5.0, default_speed = 25)
game.spaces["manor space"].add_faction_stats("goblin", agent_radius = 3.0, colour = "red", vision_radius = 60)
game.spaces["manor space"].add_faction_stats("party", agent_radius = 2.5, colour = "green", vision_radius = 30)
game.add_agent([22.5, 22.5], faction = "goblin", speed = 50)
game.add_agent([-47.5, 7.5], faction = "goblin")
game.add_agent([67.5, -27.5], faction = "goblin")
game.add_agent([-52.5, -52.5], faction = "party")
game.add_agent([-52.5, 12.5], faction = "party", speed = 10)
game.add_agent([27.5, 42.5], faction = "party")
game.add_agent([-47.5, -47.5])
game.add_wall([-60, 30], [60, -30])
game.add_wall([-60, -10], [40, -40])

game.screen.window.add_component([0, 0], [500, 500], "display", background = "green", window = True)

game.screen.window.get("display").add_component([50, 50], [space_size, space_size], "space", height = 2, spaceview = True, faction = "party")
game.screen.window.get("display").get("space").add_space(game.spaces["manor space"], space_per_pixel)

game.screen.window.get("display").add_component([50, 50], [space_size, space_size], "map", background = "brown", gridview = True)
game.screen.window.get("display").get("map").add_grid(game.maps["manor map"].tiles)

game.screen.window.add_component([500, 0], [200, 500], "data", background = "teal", window = True)

game.screen.window.get("data").add_component([0, 0], [200, 30], "x_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 30], [200, 30], "y_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 60], [200, 30], "current_entity", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 90], [200, 30], "current_window", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 120], [200, 30], "move_random", background = "blue", button = True, text = "Move", text_colour = "green")
game.screen.window.get("data").add_component([0, 150], [200, 30], "view_choice", background = "purple", toggleview = True, buttons = ["party_button", "goblin_button"], texts = ["Party", "Goblins"], formation = [2, 1], default = "party_button")

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
    check_vision_toggle()

def check_vision_toggle():
    if game.screen.window.get("data").get("view_choice").get("party_button").active:
        game.screen.window.get("display").get("space").change_faction("party")
    if game.screen.window.get("data").get("view_choice").get("goblin_button").active:
        game.screen.window.get("display").get("space").change_faction("goblin")

def make_move_inputs():
    game.screen.window.get("data").add_component([0, 120], [int(200/3), 30], "unit id", background = "white", input = True, text = "Unit")
    game.screen.window.get("data").add_component([0 + int(200/3), 120], [int(200/3), 30], "move x", background = "white", input = True, text = "x")
    game.screen.window.get("data").add_component([0 + int(2*200/3), 120], [int(200/3), 30], "move y", background = "white", input = True, text = "y")

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
