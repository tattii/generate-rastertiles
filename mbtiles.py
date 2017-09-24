import sqlite3

class Mbtiles:

    def __init__(self, mbtiles):
        self.conn = sqlite3.connect(mbtiles)

    def images(self):
        c = self.conn.cursor()
        sql = 'SELECT count(*) FROM images'
        c.execute(sql)
        row = c.fetchone()
        return row[0]
        
    def tiles(self):
        c = self.conn.cursor()
        sql = 'SELECT count(*) FROM tiles'
        c.execute(sql)
        row = c.fetchone()
        return row[0]

    def getimages(self):
        c = self.conn.cursor()
        sql = 'SELECT * FROM images'

        i = 0
        for row in c.execute(sql):
            #if i == 100: return
            rows = self.fetchtiles(row[1])
            if len(rows) > 1:
                print len(rows)
                print rows[:5]
            i += 1
    
    def getimagesiter(self):
        c = self.conn.cursor()
        sql = 'SELECT tile_id FROM images'
        return c.execute(sql)

    def fetchtiles(self, tile_id):
        c = self.conn.cursor()
        sql = 'SELECT zoom_level AS z, tile_column AS x, tile_row AS y FROM map WHERE tile_id=?'
        c.execute(sql, (tile_id,))
        return c.fetchall()

if __name__ == '__main__':
    import sys
    mbtiles = Mbtiles(sys.argv[1])
    print mbtiles.images()
    print mbtiles.tiles()
    #mbtiles.getimages()

