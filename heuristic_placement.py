from PIL import Image, ImageDraw
import random
import sys


def average(x, y, z):
    avg = (abs(x - y) + abs(y - z) + abs(z - x))/3
    return avg


class HeuristicPlace:

    def __init__(self):
        # single buffer
        self.length_2 = 0
        # single buffer
        self.length_3 = 0
        # single buffer
        self.length_5 = 0

        self.grid = [['0' for i in range(50)] for j in range(13)]

    def ini_place(self, module_area, module_id):
        if module_area == 2:
            self.place([0, 1], module_id, 2)
        elif module_area == 3:
            if self.length_2 < self.length_3:
                self.place([1, 0], module_id, 2)
            else:
                self.place([0, 1], module_id, 3)
        elif module_area == 4:
            if self.length_3 <= self.length_2:
                self.place([1, 0], module_id, 3)
            else:
                self.place([0, 2], module_id, 2)
        else:
            self.heavy_opt_place(module_area, module_id)
        self.create_image()

    def opt_place(self, module_area, module_id):

        # best way to place in 5-section
        best_5 = [-1, -1]
        # # Case1: In 7's
        # need_7 = module_area / 7
        # rem_7 = module_area % 7
        # pos_7 = (rem_7 == 0)
        # best_5 = [need_7, 7] if pos_7 else best_5

        # Case2: In 6's
        need_6 = int(module_area / 6)
        rem_6 = module_area % 6
        pos_6 = (rem_6 == 0)
        best_5 = [need_6, 0] if pos_6 else best_5

        # Case3 : In 5's
        need_5 = int(module_area / 5)
        rem_5 = module_area % 5
        pos_5 = (rem_5 <= need_5)
        best_5 = [rem_5, need_5 - rem_5] if pos_5 and best_5[0] == -1 else best_5

        # best way to place in 3-section
        best_3 = [-1, -1]
        # Case1: In 4's
        need_4 = int(module_area / 4)
        rem_4 = module_area % 4
        pos_4 = (rem_4 == 0)
        best_3 = [need_4, 0] if pos_4 else best_3

        # Case2: In 3's
        need_3 = int(module_area / 3)
        rem_3 = module_area % 3
        pos_3 = (rem_3 <= need_3)
        best_3 = [rem_3, need_3 - rem_3] if pos_3 and best_3[0] == -1 else best_3

        # best way to place in 2-section
        best_2 = [-1, -1]
        # Case1: In 3's
        need_3 = int(module_area / 3)
        rem_3 = module_area % 3
        pos_3 = (rem_3 == 0)
        best_2 = [need_3, 0] if pos_3 else best_2

        # Case2: In 2's
        need_2 = int(module_area / 2)
        rem_2 = module_area % 2
        pos_2 = (rem_2 <= need_2)
        best_2 = [rem_2, need_2 - rem_2] if pos_2 and best_2[0] == -1 else best_2

        # Finding out best placement using average
        avg1 = average(self.length_5 + best_5[0] + best_5[1], self.length_3, self.length_2)
        avg2 = average(self.length_5, self.length_3 + best_3[0] + best_3[1], self.length_2)
        avg3 = average(self.length_5, self.length_3, self.length_2 + best_2[0] + best_2[1])
        min_avg = min(avg1, avg2, avg3)

        if min_avg == avg1:
            self.place(best_5, module_id, 5)
        elif min_avg == avg2:
            self.place(best_3, module_id, 3)
        else:
            self.place(best_2, module_id, 2)

    def place(self, weight, module_id, mode):

        if mode == 2:
            self.fill_main(module_id, self.length_2, 1, int(weight[0] + weight[1]), mode)
            self.fill_buffer(module_id, self.length_2, 0, int(weight[0]))
            self.length_2 += int(weight[0] + weight[1])

        elif mode == 3:
            self.fill_main(module_id, self.length_3, 4, int(weight[0] + weight[1]), mode)
            self.fill_buffer(module_id, self.length_3, 3, int(weight[0]))
            self.length_3 += int(weight[0] + weight[1])

        elif mode == 5:
            self.fill_main(module_id, self.length_5, 8, int(weight[0] + weight[1]), mode)
            self.fill_buffer(module_id, self.length_5, 7, int(weight[0]))
            self.length_5 += int(weight[0] + weight[1])

        else:
            print("Invalid mode:" + str(mode))

    def fill_main(self, module_id, start_x, start_y, length, width):
        # print(start_x)
        # print(length)
        # print(start_y)
        # print(width)
        # print(module_id)
        for j in range(start_x, start_x + length):
            for i in range(start_y, start_y + width):
                self.grid[i][j] = module_id
        # print(self.grid)

    def fill_buffer(self, module_id, start_x, start_y, length):
        for j in range(start_x, start_x + length):
            self.grid[start_y][j] = module_id

    def heavy_opt_place(self, module_area, module_id):
        # Case1: For 2's
        # find optimal x and y for 3x + 2y = module_area
        opt_2 = [-1, -1]
        for x in range(module_area, -1, -1):
            if module_area > 3*x and (module_area - 3 * x) % 2 == 0:
                y = int((module_area - 3 * x) / 2)
                opt_2 = [x, y]
                break

        # Case2: For 3's
        # find optimal x and y for 4x + 3y = module_area
        opt_3 = [-1, -1]
        for x in range(module_area, -1, -1):
            if module_area > 4*x and (module_area - 4 * x) % 3 == 0:
                y = int((module_area - 4 * x) / 3)
                opt_3 = [x, y]
                break

        # Case3: For 5's
        # find optimal x and y for 6x + 5y = module_area
        opt_5 = [-1, -1]
        for x in range(module_area, -1, -1):
            if module_area > 6*x and (module_area - 6 * x) % 5 == 0:
                y = int((module_area - 6 * x) / 5)
                opt_5 = [x, y]
                break

        # Finding out best placement using average
        avg1 = average(self.length_5 + opt_5[0] + opt_5[1], self.length_3, self.length_2) if opt_5[0]!=-1 else 1e9 + 1
        avg2 = average(self.length_5, self.length_3 + opt_3[0] + opt_3[1], self.length_2) if opt_3[0]!=-1 else 1e9 + 1
        avg3 = average(self.length_5, self.length_3, self.length_2 + opt_2[0] + opt_2[1]) if opt_2[0]!=-1 else 1e9 + 1
        min_avg = min(avg1, avg2, avg3)

        if min_avg == avg1:
            print("opt_5 :" + str(opt_5) + str(module_id))
            self.place(opt_5, module_id, 5)
        elif min_avg == avg2:
            print("opt_3 :" + str(opt_3) + str(module_id))
            self.place(opt_3, module_id, 3)
        else:
            print("opt_2 :" + str(opt_2) + str(module_id))
            self.place(opt_2, module_id, 2)

    def create_image(self):
        # Define the size of each square in pixels
        square_size = 50

        # Calculate the size of the image based on the input self.grid
        width = len(self.grid[0]) * square_size
        height = len(self.grid) * square_size

        # Create a new image with a white background
        image = Image.new("RGB", (width, height), "white")

        # Create a draw object for the image
        draw = ImageDraw.Draw(image)

        # Define a color map for the symbols in the input self.grid
        colors = []
        color_map = {}
        for symbol in set([item for sublist in self.grid for item in sublist]):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            while color in colors:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colors.append(color)
            color_map[str(symbol)] = color

        # Draw a square for each symbol in the input self.grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                symbol = str(self.grid[i][j])
                color = color_map[symbol]
                draw.rectangle((j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size),
                               fill=color)

                # Add the symbol to the center of the square
                draw.text((j * square_size + square_size / 2, i * square_size + square_size / 2), symbol,
                          fill=(255, 255, 255), anchor="mm")

        image.save("output.jpg", "JPEG")

# future
# 1.splitting. E.g. module size 6 can be kept as in 3, buffer of 3, 2
# 3. Where to place module size 1

