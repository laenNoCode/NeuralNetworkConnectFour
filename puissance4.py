from tkinter import *

fenetre = Tk();
COULEURS = ["yellow", "red","grey"];
canvas = Canvas(master = fenetre, width = 700, height = 600);
canvas.pack();
canvas.create_rectangle(0,0,699,599,fill= "#00F");
grid = [];
dataGrid = [];

def start():
    global hauteurs,joueurActuel
    joueurActuel = 0;
    hauteurs = [0] * 7
    for i in range(7):
        grid.append([]);
        dataGrid.append([]);
        for j in range(6):
            dataGrid[i].append(2);
            grid[i].append(canvas.create_oval(4 + 100 * i ,4 + 100 * j,96 + 100 * i ,96 + 100 * j, fill="grey"));
        grid[i].reverse();
  
def restart():
    global hauteurs,joueurActuel
    joueurActuel = 0;
    hauteurs = [0] * 7
    for i in range(7):
        for j in range(6):
            dataGrid[i][j] = 2;
            canvas.itemconfig(grid[i][j],fill="grey");
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
    print(victoire)
    if(victoire):
        restart();

def onClick(click):
    global joueurActuel,grid,dataGrid
    indiceItem = int(click.x / 100);
    if (hauteurs[indiceItem] >= 6):
        return;

    joueurActuel =  1 - joueurActuel;
    canvas.itemconfig(grid[indiceItem][hauteurs[indiceItem]], fill = COULEURS[joueurActuel]);
    print(dataGrid);
    dataGrid[indiceItem][hauteurs[indiceItem]] = joueurActuel;
    hauteurs[indiceItem] += 1;
    testerVictoire(indiceItem, hauteurs[indiceItem] - 1);
start();
canvas.bind("<Button-1>",onClick);
fenetre.mainloop();

