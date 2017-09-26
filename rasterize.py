import os, sys
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
                if tile[0] <= 10: # zoom
                    queue.put(tilecoord(tile))

        #i += 1
        #if i == 100: break

    print queue.qsize()

    download_all()


def mainz():
    mbtiles = Mbtiles(sys.argv[1])
    print mbtiles.images()

    for zoom in range(10, 11):
        for row in mbtiles.gettilesiter(zoom):
            queue.put(tilecoord(row))

    print queue.qsize()

    download_all()


def tilecoord(row):
    z, x, y = row
    # Flip Y coordinate because MBTiles files are TMS.
    y = (1 << z) - 1 - y
    return x, y, z


def download_tile(url, filename):
    if os.path.exists(filename): return
    
    res = requests.get(url)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, "wb") as f:
        f.write(res.content)


def worker(num):
    print "Worker", num
    while not queue.empty():
        tile = queue.get()

        print tile
        url = 'http://localhost:8081/styles/terrain/%d/%d/%d.png' % (tile[2], tile[0], tile[1])
        filename = 'tiles/%d/%d/%d.png' % (tile[2], tile[0], tile[1])

        #download_tile(url, filename)
        
        url2 = 'http://localhost:8081/styles/terrain/%d/%d/%d@2x.png' % (tile[2], tile[0], tile[1])
        filename2 = 'tiles@2x/%d/%d/%d.png' % (tile[2], tile[0], tile[1])

        download_tile(url2, filename2)

        queue.task_done()


def download_all():
    num_worker = 1
    threads = []

    for i in range(num_worker):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)

    queue.join()

if __name__ == '__main__':
    mainz()


