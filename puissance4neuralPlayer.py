from tkinter import *
from reseaudeneurones import *
from random import *
from threading import Thread
from random import *
from math import *
from time import *
from reseaudeneurones2 import *
VALEUR_RANDOM  = 50
NOMBRE_ELEM = 200
TAUXMUT = 80
NOMBREADV = 200
VALEURSNEURONES = 3936;
VALEURSBIAS = 71;
file = "best55.csv";
started = False
sle = False

def loadFromFile(file):
    file = open(file, "r");
    a = ""
    for i in file:
        a += i
    a = a.split(";");
    a = [float(t) for t in a]
    return ReseauNeuronePuissance4(a[:VALEURSNEURONES],a[VALEURSNEURONES:VALEURSNEURONES + VALEURSBIAS]);



fenetre = Tk();
COULEURS = ["grey","yellow", "red"];
canvas = Canvas(master = fenetre, width = 700, height = 600);
canvas.pack();
canvas.create_rectangle(0,0,699,599,fill= "#00F");
grid = [];
dataGrid = [];
joueur = 0;

#neurones

neurone = loadFromFile(file);
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
    sleep(2);
    hauteurs = [0] * 7
    for i in range(7):
        for j in range(6):
            dataGrid[i][j] = 0;
            canvas.itemconfig(grid[i][j], fill = "grey")
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
    indiceItem = int(click.x / 100);
    onClickReact(indiceItem);
    neurone.setEntree(dataGrid);
    for i in neurone.entree.neurones:
        i.valeur = [0.0,1.0,0.5][int(i.valeur)];
    neurone.calculer();
    sortie = neurone.decisions;
    for i in sortie:
        if (onClickReact(i) != -1):
            break;


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

canvas.bind("<Button-1>",onClick);
loop = Thread(target = fenetre.mainloop)
loop.start();



