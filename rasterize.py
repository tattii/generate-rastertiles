import sys
import threading
from queue import Queue
import requests

from mbtiles import Mbtiles
    
queue = Queue()

def main():
    mbtiles = Mbtiles(sys.argv[1])
    print mbtiles.images()

    i = 0
    for row in mbtiles.getimagesiter():
        tile_id = row[0]

        tiles = mbtiles.fetchtiles(tile_id)
        if len(tiles) < 1000:
            for tile in tiles:
                queue.put(tilecoord(tile))

        i += 1
        if i == 100: break

    print queue.qsize()

    download_all()


def tilecoord(row):
    z, x, y = row
    # Flip Y coordinate because MBTiles files are TMS.
    y = (1 << z) - 1 - y
    return x, y, z


def download_tile(url, filename):
    res = requests.get(url)
    with open(filename, "wb") as f:
        f.write(res.content)


def worker(num):
    print "Worker", num
    while not queue.empty():
        tile = queue.get()

        print tile

        queue.task_done()

def download_all():
    num_worker = 4
    threads = []

    for i in range(num_worker):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    queue.join()

if __name__ == '__main__':
    main()


