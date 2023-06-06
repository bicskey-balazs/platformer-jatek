class Palya:
    txt_fajl: str
    kezdo_pont_x: str
    kezdo_pont_y: str

    def palya_beolvasasa(self, palya: list):
        vissza: str = ''
        for e in palya:
            vissza += str(e).strip('\n')
        return vissza

    def __init__(self, fajl):
        self.txt_fajl = self.palya_beolvasasa(fajl[0:14])
        self.kezdo_pont_x = int(str(fajl[15]).strip('\n'))
        self.kezdo_pont_y = int(str(fajl[16]).strip('\n'))

#pv = fajl[1414:1419]
#kp = fajl[1420:1425]
