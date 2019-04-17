from random import *
from math import *
from reseaudeneurones import *
VALEUR_RANDOM  = 5000
NOMBRE_ELEM = 200
TAUXMUT = 80
NOMBREADV = 20
class Element(object):
    def __init__(this, tableau = []):
        if(len(tableau) == 0):
            tableau = [float(randint(-VALEUR_RANDOM,VALEUR_RANDOM)) /
                       float(VALEUR_RANDOM) for i in range(1040)];
        this.tableau = tableau;
        this.value = ReseauNeuronePuissance4(tableau);
    def eval(this, autres):
        global dataGrid
        this.score = 0;
        for i in range(NOMBREADV):
            adversaire =  autres[randint(0,NOMBRE_ELEM - 1)];
            ret = False
            while(not ret):
                this.value.setEntree(dataGrid);
                this.value.calculer();
                sortie = this.value.decisions;
                for i in sortie:
                    val = onClickReact(i)
                    if (val != -1):
                        break;
                    if(abs(val) == 5):
                        ret = True
                        this.score += 1;
                    if (val == -2):
                        ret = True;
                if(not ret):
                    adversaire.setEntree(dataGrid);
                    adversaire.calculer();
                    sortie = adversaire.decisions;
                    for i in sortie:
                        val = onClickReact(i)
                        if (val != -1):
                            break;
                        if(abs(val) == 5):
                            ret = True
                            this.score -= 1;
                        if (val == -2):
                            ret = True;
    def coups(this, dataGrid):
        reseau.setEntree(dataGrid);
        reseau.calculer();
        sortie = reseau.decisions;
        return sortie
    def muter(this):
        for i in range(randint(5, 20)):
            this.tableau[randint(0,1039)] =float(
                randint(-VALEUR_RANDOM,VALEUR_RANDOM)) / float(VALEUR_RANDOM)
            this.value = ReseauNeuronePuissance4(tableau);
    def copy(this):
        return Element(tableau);
class algo_genetique(object):
    def __init__(this):
        this.tab = []
        for i in range(NOMBRE_ELEM):
            this.tab.append(Element())
    def progress(this):
        for t in this.tab:
            t.eval(this.tab);
        this.tab.sort(key = lambda x : x.score);
        this.tab.reverse();
        for i in range(len(this.tab)):
            kill = exp(- float(i) / 340.0) < random()
            if(kill):
                kill = randint(0,100) > TAUXMUT;
                if(kill):
                    tab[i] = Element();
                else:
                    tab[i] = tab[randint(0,10)].copy();
                    tab[i].muter();
