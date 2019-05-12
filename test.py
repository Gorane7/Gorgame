from gorgame import screen

#CONSTANTS
size = (700,500)

game = screen.Screen(size)

game.window.add_window([20, 20], [100, 200], "green", 1, "gwin")
game.window.add_window([50, 50], [300, 30], "blue", 0, "bwin")
game.window.get("gwin").add_window([10, 10], [5, 5], "red", 1, "rdot")

while True:
    game.loop()
