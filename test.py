from gorgame import screen

#CONSTANTS
size = (700,500)

game = screen.Screen(size)

game.window.add_component([0, 0], [500, 500], "white", 5, "display", window = True)
game.window.get("display").add_component([20, 20], [100, 200], "green", 2, "gwin", window = True)
game.window.get("display").add_component([50, 50], [300, 30], "blue", 1, "bwin")
game.window.get("display").get("gwin").add_component([10, 10], [5, 5], "red", 2, "rdot")
game.window.get("display").get("gwin").add_component([-5, 12], [100, 2], "yellow", 1, "yline")

game.window.add_component([500, 0], [200, 500], "grey", 10, "data", window = True)

game.window.get("data").add_component([0, 0], [200, 30], "black", 1, "x_coord_box", textbox = True)
game.window.get("data").add_component([0, 30], [200, 30], "black", 1, "y_coord_box", textbox = True)
game.window.get("data").add_component([0, 60], [200, 30], "black", 1, "current_entity", textbox = True)
game.window.get("data").add_component([0, 90], [200, 30], "black", 1, "current_window", textbox = True)

while True:
    game.window.get("data").get("x_coord_box").add_text("x: " + str(game.mouse_pos.x), "red")
    game.window.get("data").get("y_coord_box").add_text("y: " + str(game.mouse_pos.y), "red")
    game.window.get("data").get("current_entity").add_text(str(game.current_entity), "red")
    game.window.get("data").get("current_window").add_text(str(game.current_window), "red")
    game.loop()
