from gorgame import screen

#CONSTANTS
size = (700,500)

game = screen.Screen(size)

game.window.add_window([0, 0], [500, 500], "white", 5, "display")
game.window.get("display").add_window([20, 20], [100, 200], "green", 1, "gwin")
game.window.get("display").add_window([50, 50], [300, 30], "blue", 2, "bwin")
game.window.get("display").get("gwin").add_window([10, 10], [5, 5], "red", 2, "rdot")
game.window.get("display").get("gwin").add_window([-5, 12], [100, 2], "yellow", 1, "yline")
game.window.add_window([500, 0], [200, 500], "grey", 10, "data")

while True:
    game.loop()
