from gorgame import game

#CONSTANTS
x = 28
y = 18
tile_size = 5
space_size = 500
size = (700,500)
space_per_pixel = (max(x, y) * tile_size) / space_size

game = game.Game(size)

#game.add_map([x,y], "manor map")
#game.maps["manor map"].fill_random_tiles("red", 0, 1)
#game.maps["manor map"].fill_random_tiles("green", 0, 1)
#game.maps["manor map"].fill_random_tiles("blue", 0, 1)

game.add_space([x*5, y*5], "manor space")
game.spaces["manor space"].add_agent([22.5, 22.5], 2.5, "red", faction = "goblin", vision_radius = 60)
#game.spaces["manor space"].add_agent([65.5, -25.5], 2.5, "red", faction = "goblin", vision_radius = 60)
game.spaces["manor space"].add_agent([-50, -50], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_agent([-50, 10], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_agent([25, 40], 2.5, "green", faction = "party", vision_radius = 30)
game.spaces["manor space"].add_wall([-60, 30], [60, -30], 3, "brown")
game.spaces["manor space"].add_wall([-60, -10], [40, -40], 3, "brown")

game.screen.window.add_component([0, 0], [space_size, space_size], "green", 5, "display", window = True)
game.screen.window.get("display").add_component([0, 0], [space_size, space_size], "grey", 5, "space", spaceview = True, faction = None)
game.screen.window.get("display").get("space").add_space(game.spaces["manor space"], space_per_pixel)

#game.screen.window.add_component([0, 0], [space_size, space_size], "green", 5, "display", window = True)
#game.screen.window.get("display").add_component([0, 0], [space_size, space_size], "brown", 5, "map", gridview = True)
#game.screen.window.get("display").get("map").add_grid(game.maps["manor map"].tiles)

game.screen.window.add_component([500, 0], [200, 500], "blue", 10, "data", window = True)

game.screen.window.get("data").add_component([0, 0], [200, 30], "black", 1, "x_coord_box", textbox = True)
game.screen.window.get("data").add_component([0, 30], [200, 30], "black", 1, "y_coord_box", textbox = True)
game.screen.window.get("data").add_component([0, 60], [200, 30], "black", 1, "current_entity", textbox = True)
game.screen.window.get("data").add_component([0, 90], [200, 30], "black", 1, "current_window", textbox = True)

while True:
    game.screen.window.get("data").get("x_coord_box").add_text("x: " + str(game.screen.mouse_pos.x), "red")
    game.screen.window.get("data").get("y_coord_box").add_text("y: " + str(game.screen.mouse_pos.y), "red")
    game.screen.window.get("data").get("current_entity").add_text(str(game.screen.current_entity), "red")
    game.screen.window.get("data").get("current_window").add_text(str(game.screen.current_window), "red")
    game.loop()
