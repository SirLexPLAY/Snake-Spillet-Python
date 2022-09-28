class User:
    @staticmethod
    def get_settings():
        print("=== Welcome to my Snake game! ===")
        print("How big level do you want to play?")
        print("1. Small (20x20 tiles)")
        print("2. Medium (40x40 tiles)")
        print("3. Big (60x60 tiles)")
        
        choice = int(input("> "))
        maps = {
            1 : (20, 20),
            2 : (40, 40),
            3 : (60, 60)
        }

        return maps[choice]
    