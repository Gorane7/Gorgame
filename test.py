from gorgame import game

#CONSTANTS
size = (700,500)

game = game.Game(size)

game.add_map([50,50], "test")
game.maps["test"].fill_random("red", 0, 1)
game.maps["test"].fill_random("green", 0, 1)
game.maps["test"].fill_random("blue", 0, 1)

game.screen.window.add_component([0, 0], [500, 500], "white", 5, "display", window = True)
game.screen.window.get("display").add_component([0, 0], [500, 500], "brown", 5, "map", gridview = True)
game.screen.window.get("display").get("map").add_grid(game.maps["test"].data)

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
