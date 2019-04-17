from tkinter import *
from reseaudeneurones import *
from random import *
from threading import Thread
from random import *
from math import *
from time import *
from reseaudeneurones import *

VALEUR_RANDOM  = 50
NOMBRE_ELEM = 200
TAUXMUT = 80
NOMBREADV = 200
started = False
sle = False

def genElem():
    return (2*random() - 1) ;

class Element(object):
    def __init__(this, tableau = [],tableauBias = []):
        if(len(tableau) == 0):
            tableau = [genElem() for i in range(1712)];
            tableauBias = [genElem() for i in range(39)];
        this.tableau = tableau;
        this.tableauBias = tableauBias;
        this.value = ReseauNeuronePuissance4(tableau, tableauBias);
    def setEntree(this, tab):
        this.value.setEntree(tab)
    def calculer(this):
        this.value.calculer()
    
    def eval(this, autres):
        global dataGrid,sle
        this.score = 0;
        for i in range(NOMBREADV):
            if (sle):
                sleep(0.08)
            adversaire =  autres[i];
            ret = False
            k = 0;
            while(not ret):
                k+= 1;
                normalizedDataGrid = [lo for lo in dataGrid]
                this.value.setEntree(normalizedDataGrid);
                this.value.calculer();
                sortie = this.value.decisions;
                for i in sortie:
                    val = onClickReact2(i)
                    
                    if (val != -1):
                        break;
                if(abs(val) == 5):
                    ret = True
                    this.score += 42 - k;
                    adversaire.score -= 10 * (42 - k)
                if (val == -2):
                    ret = True;
                if (sle):
                    sleep(0.08)
                if(not ret):
                    k += 1
                    normalizedDataGrid = [[2 - k + 1 if k > 0 else 0 for k in lo] for lo in dataGrid]
                    adversaire.setEntree(normalizedDataGrid);
                    adversaire.calculer();
                    sortie = adversaire.value.decisions;
                    for i in sortie:
                        val = onClickReact2(i)
                        if (val != -1):
                            break;
                    if(abs(val) == 5):
                        ret = True;
                        adversaire.score += 42 - k
                    if (val == -2):
                        ret = True;
    def coups(this, dataGrid):
        reseau.setEntree(dataGrid);
        reseau.calculer();
        sortie = reseau.decisions;
        return sortie
    def muter(this):
        for i in range(randint(5, 20)):
            this.tableau[randint(0,1712 - 1)] = genElem();
            this.tableauBias[randint(0,39 - 1)] = genElem();
            this.value = ReseauNeuronePuissance4(this.tableau, this.tableauBias);
    def copy(this):
        return Element(this.tableau, this.tableauBias);

class algo_genetique(object):
    def __init__(this):
        this.tab = []
        for i in range(NOMBRE_ELEM):
            this.tab.append(Element())
    def progress(this):
        for t in this.tab:
            t.score = 0
        for t in this.tab:
            t.eval(this.tab);
        this.tab.sort(key = lambda x : x.score);
        this.tab.reverse();
        print(this.tab[0].score);
        for i in range(len(this.tab)):
            
            kill = exp(- 1 * float(i) / 200.0) < random()
            if(kill):
                kill = randint(0,100) > TAUXMUT;
                if(kill):
                    this.tab[i] = Element();
                else:
                    j = 0
                    while (exp(- 10 * float(j) / 200.0) > random()):
                        j += 1
                    this.tab[i] = this.tab[randint(0,10)].copy();
                    this.tab[i].muter();
        return this.tab[0]

fenetre = Tk();
COULEURS = ["grey","yellow", "red"];
canvas = Canvas(master = fenetre, width = 700, height = 600);
canvas.pack();
canvas.create_rectangle(0,0,699,599,fill= "#00F");
grid = [];
dataGrid = [];
joueur = 0;

#neurones
AG = algo_genetique();

def start():
    global hauteurs,joueurActuel
    joueurActuel = 2;
    hauteurs = [0] * 7
    for i in range(7):
        grid.append([]);
        dataGrid.append([]);
        for j in range(6):
            dataGrid[i].append(0);
            grid[i].append(canvas.create_oval(4 + 100 * i ,4 + 100 * j,96 + 100 * i ,96 + 100 * j, fill="grey"));
        grid[i].reverse();
  
def restart():
    global hauteurs,joueurActuel
    joueurActuel = 2;

    hauteurs = [0] * 7
    for i in range(7):
        for j in range(6):
            dataGrid[i][j] = 0;

def testerLigneHorizontale(x,y):
    joueur = (dataGrid[x])[y]
    compte = 1;
    for i in range(3):
        if((x + i + 1 >= 7) or (dataGrid[x + i + 1][y] != joueur)):
                break;
        compte += 1;
    for i in range(3):
        if((x - i - 1 < 0) or (dataGrid[x - i - 1][y] != joueur)):
                break;
        compte += 1
    return (compte >= 4)

def testerLigneVerticale(x,y):
    joueur = (dataGrid[x])[y]
    compte = 1;
    for i in range(3):
        if((y + i + 1 >= 6) or (dataGrid[x][y + i + 1] != joueur)):
                break;
        compte += 1;
    for i in range(3):
        if((y - i - 1 < 0) or (dataGrid[x][y - i - 1] != joueur)):
                break;
        compte += 1
    return (compte >= 4)

def testerDiagonale1(x,y):
    joueur = (dataGrid[x])[y]
    compte = 1;
    for i in range(3):
        if((y + i + 1 >= 6) or (x + i + 1 >= 7) or
           (dataGrid[x + i + 1][y + i + 1] != joueur)):
                break;
        compte += 1;
    for i in range(3):
        if ((y - i - 1 < 0) or (x - i - 1 < 0) or
           (dataGrid[x - i - 1][y - i - 1] != joueur)):
                break;
        compte += 1
    return (compte >= 4)

def testerDiagonale2(x,y):
    joueur = (dataGrid[x])[y]
    compte = 1;
    for i in range(3):
        if((y + i + 1 >= 6) or (x - i - 1 < 0) or
           (dataGrid[x - i - 1][y + i + 1] != joueur)):
                break;
        compte += 1;
    for i in range(3):
        if ((y - i - 1 < 0) or (x + i + 1 >= 7) or
           (dataGrid[x + i + 1][y - i - 1] != joueur)):
                break;
        compte += 1
    return (compte >= 4)

def testerVictoire(x,y):
    victoire  = testerLigneHorizontale(x,y);
    victoire = victoire or testerLigneVerticale(x,y);
    victoire = victoire or testerDiagonale1(x,y);
    victoire = victoire or testerDiagonale2(x,y);
    if(victoire):
        restart();
        return 5;
#jouer contre l'ia

rel = True
def onClick(click):
    global bestNeurone
    indiceItem = int(click.x / 100);
    onClickReact(indiceItem);
    bestNeurone.setEntree(dataGrid);
    bestNeurone.calculer();
    sortie = bestNeurone.decisions;
    for i in sortie:
        if (onClickReact(i) != -1):
            break;

def reload():
    global rel
    for x in range(7):
        for y in range(6):
            canvas.itemconfig(grid[x][y], fill = COULEURS[dataGrid[x][y]]);
    if rel:
        fenetre.after(30,reload);
    else:
        canvas.bind("<Button-1>",onClick);

def progresser():
    global started,bestNeurone,rel
    gen = 0
    while(started):
        print(gen)
        bestNeurone = AG.tab[0]
        bestNeurone = AG.progress()
        tab = bestNeurone.tableau;
        tab += bestNeurone.tableauBias;
        bestNeurone = bestNeurone.value;
        file = open("best"+ str(gen) + ".csv","w")
        file.write(";".join([str(i) for i in tab]))
        gen += 1
        file.close()
    rel = False;
loop = 0

def onClick2(click):
    global loop,started
    if(not started):
        started = True;
        print("start");
        reload();
        loop = Thread(target = progresser)
        loop.start();
    else:
        started = False;

def onClickReact(indiceItem):
    global joueurActuel,grid,dataGrid
    if (hauteurs[indiceItem] >= 6):
        return -1;
    
    if (joueurActuel == 2):
        joueurActuel = 0;
    joueurActuel += 1
    canvas.itemconfig(grid[indiceItem][hauteurs[indiceItem]], fill = COULEURS[joueurActuel]);
    dataGrid[indiceItem][hauteurs[indiceItem]] = joueurActuel;
    hauteurs[indiceItem] += 1;
    i = testerVictoire(indiceItem, hauteurs[indiceItem] - 1);
    if( i == 5):
        return (5*(2*joueur - 1))
    if(sum(hauteurs) == 42):
        restart()
        return -2;
    return 0;

def onClickReact2(indiceItem):
    global joueurActuel,grid,dataGrid
    if (hauteurs[indiceItem] >= 6):
        return -1;
    if (joueurActuel == 2):
        joueurActuel = 0;
    joueurActuel += 1
    dataGrid[indiceItem][hauteurs[indiceItem]] = joueurActuel;
    hauteurs[indiceItem] += 1;
    i = testerVictoire(indiceItem, hauteurs[indiceItem] - 1);
    if( i == 5):
        return (5*(2*joueur - 1))
    if(sum(hauteurs) == 42):
        restart()
        return -2;
    return 0;
start();

canvas.bind("<Button-1>",onClick2);
fenetre.loop = Thread(target = fenetre.mainloop)
fenetre.loop.__init__(target = fenetre.mainloop)
fenetre.loop.start();



