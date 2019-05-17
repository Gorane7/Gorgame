from gorgame import screen

#CONSTANTS
size = (700,500)

game = screen.Screen(size)

game.window.add_window([0, 0], [500, 500], "white", 5, "display", scrollable = True)
game.window.get("display").add_window([20, 20], [100, 200], "green", 2, "gwin")
game.window.get("display").add_window([50, 50], [300, 30], "blue", 1, "bwin")
game.window.get("display").get("gwin").add_window([10, 10], [5, 5], "red", 2, "rdot")
game.window.get("display").get("gwin").add_window([-5, 12], [100, 2], "yellow", 1, "yline")

game.window.add_window([500, 0], [200, 500], "grey", 10, "data")

game.window.get("data").add_window([0, 0], [200, 30], "black", 1, "x_coord_box")
game.window.get("data").add_window([0, 30], [200, 30], "black", 1, "y_coord_box")
game.window.get("data").add_window([0, 60], [200, 30], "black", 1, "current_box")

while True:
    game.window.get("data").get("x_coord_box").add_text("x: " + str(game.mouse_pos.x), "red")
    game.window.get("data").get("y_coord_box").add_text("y: " + str(game.mouse_pos.y), "red")
    game.window.get("data").get("current_box").add_text(str(game.current_window), "red")
    game.loop()
