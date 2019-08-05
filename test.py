from gorgame import game

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

game.screen.window.add_component([500, 0], [200, 500], 10, "data", background = "blue", window = True)

game.screen.window.get("data").add_component([0, 0], [200, 30], 1, "x_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 30], [200, 30], 1, "y_coord_box", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 60], [200, 30], 1, "current_entity", background = "black", textbox = True)
game.screen.window.get("data").add_component([0, 90], [200, 30], 1, "current_window", background = "black", textbox = True)

while True:
    game.screen.window.get("data").get("x_coord_box").add_text("x: " + str(game.screen.mouse_pos.x), "red")
    game.screen.window.get("data").get("y_coord_box").add_text("y: " + str(game.screen.mouse_pos.y), "red")
    game.screen.window.get("data").get("current_entity").add_text(str(game.screen.current_entity), "red")
    game.screen.window.get("data").get("current_window").add_text(str(game.screen.current_window), "red")
    game.loop()
