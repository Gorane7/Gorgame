from gorgame import game

#CONSTANTS
x = 28
y=40
map_size = 500
size = (700,500)
map_tile_size = map_size / max(x, y)

game = game.Game(size)

game.add_map([x,y], "manor map")
game.maps["manor map"].fill_random_tiles("red", 0, 1)
game.maps["manor map"].fill_random_tiles("green", 0, 1)
game.maps["manor map"].fill_random_tiles("blue", 0, 1)

game.add_space([x*5, y*5], "manor space")

game.screen.window.add_component([0, 0], [map_size, map_size], "green", 5, "display", window = True)
game.screen.window.get("display").add_component([(map_size - map_tile_size * x) / 2, (map_size - map_tile_size * y) / 2], [map_tile_size * x, map_tile_size * y], "brown", 5, "map", gridview = True)
game.screen.window.get("display").get("map").add_grid(game.maps["manor map"].tiles)

game.screen.window.add_component([500, 0], [200, 500], "grey", 10, "data", window = True)

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
