class Palya:
    txt_fajl: str
    palya_vege: str
    kezdo_pont: str

    def palya_beolvasasa(self, palya):
        vissza: str = ''
        for kar in palya:
            if kar != '\n':
                vissza += kar
        return vissza

    def __init__(self, fajl):
        t = fajl[0:1413]
        pv = fajl[1414:1419]
        kp = fajl[1420:1425]
        self.txt_fajl = self.palya_beolvasasa(t)
        self.palya_vege = pv
        self.kezdo_pont = kp
