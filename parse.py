# -*- coding: utf8 -*-
def parse_choix(data, col, param):
    Liste = []
    tmp = []
    variable = data[0][0][col]
    for ligne in data[0] :
        if ligne[col] == variable:
            tmp.append(ligne[param])
        else :
            variable = ligne[col]
            print len(tmp)
            Liste.append(tmp)
            tmp = []
            tmp.append(ligne[param])
    Liste.append(tmp)
    print Liste
    return Liste
