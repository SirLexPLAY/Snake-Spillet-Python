class Tools:
    @staticmethod
    def get_pos(cords, BOX_SPACING, BOX_SIZE):
        """
        Returns position to the box in px.
        """
        x_pos, y_pos = BOX_SPACING, BOX_SPACING

        x_pos += (BOX_SIZE[0] + BOX_SPACING) * (cords[0] - 1)
        y_pos += (BOX_SIZE[1] + BOX_SPACING) * (cords[1] - 1)

        return (x_pos, y_pos)

    @staticmethod
    def get_box_pos(x, y, BOX_SPACING, BOX_SIZE):
        """
        Returns position to the box in boxes.
        """
        x_pos = (x-BOX_SPACING)//(BOX_SIZE[0]+BOX_SPACING)
        y_pos = (y-BOX_SPACING)//(BOX_SIZE[1]+BOX_SPACING)
        
        return (x_pos, y_pos)

    @staticmethod
    def check_outside(last_box, AMOUNT_BOXES):
        return last_box[0] <= 0 or last_box[1] <= 0 or last_box[0] > AMOUNT_BOXES[0] or last_box[1] > AMOUNT_BOXES[1]

    @staticmethod
    def load_map(wall_boxes, map):
        boxes = []
        map_size_x = 0
        map_size_y = 0
        start_pos = []

        file = None

        try:
            file = open(map)
        except:
            print("Something went wrong loading map!")

        y = 1
        for line in file:
            x = 1
            for sign in line:
                if sign == "#":
                    boxes.append([x,y])
                if sign.lower() == "s":
                    start_pos = [x, y]

                x += 1
            y += 1
        
        map_size_x = x-1
        map_size_y = y-1

        file.close()
        
        return boxes, [map_size_x, map_size_y], start_pos