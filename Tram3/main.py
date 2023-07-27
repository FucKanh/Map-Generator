# Cách sử dụng: bấm chạy và dùng 2 nút A D hoặc Left arrow Right arrow
# Code này dùng cho game của Second Meeting 2023 LHPSC
# Bật chế độ output ra màn hình bằng nút V (verbose)


import os
import numpy as np, pygame as pg, time

pg.init()

# PYGAME SETTINGS
w, h = 700, 700
screen = pg.display.set_mode([w, h])
trash = pg.image.load("bag.png").convert_alpha()
iceberg = pg.image.load("water-canon.jpg").convert_alpha()
wall =  pg.image.load("rock.png").convert_alpha()
whirlpool =  pg.image.load("whirlpool.jpg").convert_alpha()
boat =  pg.image.load("boat.png").convert_alpha()
flag =  pg.image.load("flag.png").convert_alpha()


# CREATE MAP
def createMap(times, size, generate_ratio: list):
    gameMapGen = []
    for t in range(times):
        numpyMap = np.random.multinomial(1, generate_ratio, [size, size]).argmax(axis=2)
        with open(f"generated/data/{t + 1}.txt", "w"):
            np.savetxt(f"generated/data/{t + 1}.txt", numpyMap, fmt="%d")
        gameMap = []
        for row in numpyMap:
            gameMap.append([])
            for col in row:
                if col == 0:
                    obj = "T"
                elif col == 1:
                    obj = "B"
                elif col == 2:
                    obj = " "
                else:
                    obj = "W"
                gameMap[-1].append(obj) #<-- For what ? Why not gameMap.append(obj)
                # print(obj + " ", end = "")
            # print("")
        # print("----------------")
        gameMapGen.append(gameMap)

    return gameMapGen


# RESCALE IMAGE
def Rescale(img, imgSize, w, h, size, gridThickness):
    imgW, imgH = imgSize
    if imgW < imgH:
        img = pg.transform.scale(
            img, (imgW / imgH * (w / size - gridThickness), h / size - gridThickness)
        )
    else:
        img = pg.transform.scale(
            img, (w / size - gridThickness, imgH / imgW * (h / size - gridThickness))
        )
    return img


# DRAW UI
def UI(drawMap, w, h, size, gridThickness, trash, iceberg):
    # GRID LINES
    for i in range(size + 1):
        x = 0 + w / size * i
        y = 0 + h / size * i
        pg.draw.line(screen, (0, 0, 0), (x, 0), (x, h), gridThickness)
        pg.draw.line(screen, (0, 0, 0), (0, y), (w, y), gridThickness)

    # DRAW OBSTACLES
    for row in range(size):
        for col in range(size):
            x = w / size * col
            y = h / size * row
            # TRASH
            if drawMap[row][col] == "1":
                screen.blit(
                    trash,
                    (
                        x + round((w / size - trash.get_size()[0]) / 2),
                        y + round((h / size - trash.get_size()[1]) / 2),
                    ),
                )
                # print(w/size, h/size, trash.get_size(), round((h/size-trash.get_size()[1]))/2, round((h/size-trash.get_size()[1]))/3)
                # pg.draw.circle(screen, (250, 250, 0), (w/size*(col+1/2), h/size*(row+1/2)), w/(size*2)-2)

            # BLOCK
            elif drawMap[row][col] == "2":
                screen.blit(
                    whirlpool,
                    (
                        x + round((w / size - whirlpool.get_size()[0]) / 2),
                        y + round((h / size - whirlpool.get_size()[1]) / 2),
                    ),
                )
                # pg.draw.circle(screen, (200, 0, 0), (w/size*(col+1/2), h/size*(row+1/2)), w/(size*2)-2)

            # AIR
            elif drawMap[row][col] == "0":
                continue

            # WALL
            elif drawMap[row][col] == "5":
                screen.blit(
                    boat,
                    (
                        x + round((w / size - boat.get_size()[0]) / 2),
                        y + round((h / size - boat.get_size()[1]) / 2),
                    ),
                )
            # IN GATE
            elif drawMap[row][col] == "6":
                screen.blit(
                    flag,
                    (
                        x + round((w / size - flag.get_size()[0]) / 2),
                        y + round((h / size - flag.get_size()[1]) / 2),
                    ),
                )
            else:
                # print(w/8*(col-1), h/8*(row-1), w/8, h/8)
                screen.blit(
                    wall,
                    (
                        x + round((w / size - wall.get_size()[0]) / 2),
                        y + round((h / size - wall.get_size()[1]) / 2),
                    ),
                )


def main():
    global trash, iceberg, w, h,wall,whirlpool,boat,flag

    # PROBABILITIES
    TRASH_RATIO = 0.02
    BLOCK_RATIO = 0.02
    WALL_RATIO = 0.1
    AIR_RATIO = 1 - TRASH_RATIO - BLOCK_RATIO - WALL_RATIO

    # PARAMETERS
    mapIndex = 0  # Pointer to the current map displayed
    quantity = 4  # How many maps to generate
    size = 15  # Dimension of map
    gridThickness = 1  # Width of grid in pixels (must be divisible by size to not get overlapping due to float calculations)
    run = True
    verbose = False  # Prints out unicode map to output terminal

    # RESCALE IMAGE
    trash = Rescale(trash, trash.get_size(), w, h, size, gridThickness)
    iceberg = Rescale(iceberg, iceberg.get_size(), w, h, size, gridThickness)
    wall = Rescale(wall, wall.get_size(), w, h, size, gridThickness)
    whirlpool = Rescale(whirlpool, whirlpool.get_size(), w, h, size, gridThickness)
    boat = Rescale(boat, boat.get_size(), w, h, size, gridThickness)
    flag = Rescale(flag, flag.get_size(), w, h, size, gridThickness)
    # GENERATE
    
    id = 1
    while run:
        screen.fill((255,255,255))

        MapCreate = [[0 for x in range(size)] for y in range(size)] 
        
        f = open(f"generated/data/{id}.txt", "r")
        col = 0
        row = 0
        for x in f:
            for num in x.split():
                MapCreate[row][col] = num
                col += 1
                if (col == size):
                    row+=1
                    col = 0
        f.close()

        # print(MapCreate)
    
        UI(MapCreate, w, h, size, gridThickness, trash, iceberg)
        # LOAD IMAGES TO FOLDER
        if id <= quantity:
            pg.image.save(screen, f"generated/image/{id}.png")
            mapIndex = (mapIndex + 1) % quantity
            id += 1
        # EVENT
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if (id > quantity):
             run = False

    pg.quit()


if __name__ == "__main__":
    main()
