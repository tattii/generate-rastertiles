import sys
from mbtiles import Mbtiles

def main():
    mbtiles = Mbtiles(sys.argv[1])
    print mbtiles.images()

    i = 0
    for row in mbtiles.getimagesiter():
        tile_id = row[0]
        print tile_id

        tiles = mbtiles.fetchtiles(tile_id)
        if len(tiles) < 1000:
            print tiles
            for tile in tiles:
                print tilecoord(tile) 

        i += 1
        if i == 100: break

def tilecoord(row):
    z, x, y = row

    # Flip Y coordinate because MBTiles files are TMS.
    y = (1 << z) - 1 - y

    return x, y, z


if __name__ == '__main__':
    main()


