from tkinter import *
import threading
import random
import winsound
from queue import *
iap = True
busy = False
def ps():
    while(True):
        winsound.PlaySound("tolby.wav",winsound.SND_FILENAME)

t = threading.Thread(None,ps,None)
t.start()
bit = []
IAF = True
IAW = False

class betterQueue(object):
    """une queue pour les méthodes """
    def __init__(self):
        self.Queue= Queue()
        self.args = []
    def add (self, function, args = "void"):
        self.Queue.put(function)
        self.args.append(args)
    def consume(self):
        if(self.Queue.empty()):
            return "nothing in the queue"
        else:
            self.arg = self.args.pop(0)
            if(self.arg!="void"):
                return self.Queue.get()(*self.arg)
            else:
                return self.Queue.get()()
    def empty(self):
        return self.Queue.empty()
            
def changeIAP():
    global iap
    iap = not iap

           
q = betterQueue()
def actual():
    global q,fenetre
    if not q.empty():
        q.consume()
    fenetre.after(16,actual)



def initialisation():
    global grille,tp1,hasLastPlayerWon,tabRond,barre,fenetre,can,cercle,width,height,IAF
    fenetre = Tk()
    can = Canvas(fenetre, width = 500, height = 500)
    can.pack(fill=BOTH,expand=1)
    rect = can.create_rectangle(1,1,width,height)
    can.itemconfig(rect, fill="blue")
    barre = Menu(fenetre)
    barre.add_command(label = "RESET",command = reset)
    barre.add_command(label = "change IA turn",command = iaChange)
    barre.add_command(label = "contre IA",command = changeIAP)
    fenetre.config(menu = barre)
    for i in range(7):
        lignes.append(can.create_line(i*width/7-1,0,i*width/7-1,height))
    for j in range(7):
        colonnes.append(can.create_line(1,j*height/6-1,width-1,j*height/6-1))
    cercle = can.create_oval(50,50,100,100)
    grille = []
    for i in range(52):
        grille.append(0)
    tp1 = True
    hasLastPlayerWon = False
    for k in range(6):
        for i in range(7):
            j = 6 - k-1
            tabRond.append(can.create_oval(i*width/7+5,j*height/6+10,(i+1)*width/7-10,(j+1)*height/6-10))
        tabRond.append("")
        tabRond.append("")
    reset()
    def configure(event):
        global width, height
        width = event.width
        height = event.height
        can.coords(rect,1,1,width,height)
        for i in range(len(lignes)):
            l=lignes[i]
            can.coords(l,i*width/7-1,0,i*width/7-1,height)
        for j in range(len(colonnes)):
            c = colonnes[j]
            can.coords(c,1,j*event.height/6-1,width-1,j*event.height/6-1)
        for k in range(6):
            for i in range(7):
                j = 6 - k - 1
                r = tabRond[i+9*k]
                can.coords(r,i*width/7+5,j*height/6+10,(i+1)*width/7-10,(j+1)*height/6-10)
    can.bind("<Configure>", configure)
    
    affiche2(grille)



def iaChange():
    global IAF
    IAF = not IAF
    reset()
        




def dans_grille(k):
    return not (k < 0 or k > 52 or k % 9 >= 7)        

def affiche2 (grille):
    global tabRond,can
    for i in range(len(grille)):
        if(dans_grille(i)):
            if(grille[i]==1):
                can.itemconfigure(tabRond[i],fill="yellow")
            if(grille[i] == 2):
                can.itemconfigure(tabRond[i],fill="red")
            if(grille[i] == 0):
                can.itemconfigure(tabRond[i],fill="gray")
def affiche3 ():
    global tabRond,can,grille
    for i in range(len(grille)):
        if(dans_grille(i)):
            if(grille[i]==1):
                can.itemconfigure(tabRond[i],fill="yellow")
            if(grille[i] == 2):
                can.itemconfigure(tabRond[i],fill="red")
            if(grille[i] == 0):
                can.itemconfigure(tabRond[i],fill="gray")
    

def reset():
    global grille,tp1,hasLastPlayerWon,IAF,busy
    busy = False
    tp1 = not IAF
    hasLastPlayerWon = False
    for i in range(len(grille)):
        grille[i]=0
    if IAF:
        grille[3]=1
    affiche2(grille)
    

def calculate():
    global ev
    event = ev
    
def onClick (event):
    global x,y,grille,tp1,hasLastPlayerWon,iap,busy,ev,q
    if(not busy):
        busy = True
        can.move(cercle, event.x - x, event.y - y)
        x = event.x
        y = event.y
        
        a = findColonne(x)
        if not hasLastPlayerWon:
            i = 5
            if not (dans_grille(a + 5 * 9) and grille[a + 5 * 9] == 0):
                print("veuillez réessayer vous ne pouvez pas jouer la")
                busy = False
                return "noplay"
            else:
                while(dans_grille(a + i * 9) and grille[a + i * 9] == 0):
                    print(i)
                    i -= 1
                i += 1
                print(a + i * 9)
                if(tp1):
                    grille[a + i * 9] = 1
                else:
                    grille[a + i * 9] = 2
            affiche(grille)
            affiche(grille)
            if(test_grille(grille) >= 4):
                hasLastPlayerWon = True
                IAW = False
                if(tp1):
                    print("le joueur 1 a gagné")
                else:
                    print("le joueur 2 a gagné")
                return ""
            countLeft = 0
            for i in range(52):
                if(grille[i] == 0):
                    countLeft += 1
            if(countLeft == 10):
                print("ceci est un macth nul")
                return -1
            if(not iap):
                tp1 = not tp1
                busy = False
            else:
                affiche2(grille)
                def iaplays():
                    global busy,hasLastPlayerWon
                    jIA = 1
                    if(tp1):
                        jIA = 2
                    a = IA()
                    b = a.play(jIA,Grille(grille),4)
                    print(b)
                    i = 5
                    while(dans_grille(b + i * 9) and grille[b + i * 9] == 0):
                        i -= 1
                    i += 1
                    grille[b + i * 9] = jIA
                    affiche2(grille)
                    
                    print("ia just played")
                    if(test_grille(grille) >= 4):
                        hasLastPlayerWon = True
                        print("ia won this time")
                        IAW = True
                    busy = False
                    q.add(affiche2,(grille,))
                th = threading.Thread(None,iaplays,None)
                th.start()
        

def findColonne(x):
    global width
    return int(x//(width/7))





def affiche(grille):
    print(" 1 2 3 4 5 6 7")
    ligneBase = "---------------"
    print(ligneBase)
    for i in range(6):
        toDisp = "|"
        for j in range(7):
            k = grille[(6 - i - 1) * 9 + j]
            if (k == 1):
                toDisp += "O"
            else:
                if(k == 2):
                    toDisp += "X"
                else :
                    toDisp += " "
            toDisp += "|"
        print(toDisp)
    print(ligneBase)
    affiche2(grille)

def nombreElements(pos):
    global grille
    maxi = 0
    element = grille[pos]
    if(dans_grille(pos) and not element == 0):
        # on commence par la ligne

        count = 0
        i = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 1
            count +=1
        i = 1
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 1
            count +=1
        maxi = count
        # on soccupe d'une diagonale

        i = 0
        count = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 8
            count +=1
        i = 8
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 8
            count +=1
        maxi = max(count, maxi)
        # on s'occupe de l'autre diagonale
        
        i = 0
        count = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 10
            count +=1
        i = 10
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 10
            count +=1
        maxi = max(maxi, count)
        # on soccupe de la collone

        count = 0
        i = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 9
            count +=1
        i = 9
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 9
            count +=1
        maxi = max(maxi, count)

        return maxi
    else :
        return -1


def nombreElements2(pos,grille):
    maxi = 0
    element = grille[pos]
    if(dans_grille(pos) and not element == 0):
        # on commence par la ligne

        count = 0
        i = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 1
            count +=1
        i = 1
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 1
            count +=1
        maxi = count
        # on soccupe d'une diagonale

        i = 0
        count = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 8
            count +=1
        i = 8
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 8
            count +=1
        maxi = max(count, maxi)
        # on s'occupe de l'autre diagonale
        
        i = 0
        count = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 10
            count +=1
        i = 10
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 10
            count +=1
        maxi = max(maxi, count)
        # on soccupe de la collone

        count = 0
        i = 0
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i -= 9
            count +=1
        i = 9
        while(dans_grille(i + pos) and grille[i + pos] == element):
            i += 9
            count +=1
        maxi = max(maxi, count)

        return maxi
    else :
        return -1

def test_grille(grille):
    cmax = 0
    for i in range(len(grille)):
        cmax = max(cmax,nombreElements2(i,grille))
    return cmax

def play():
    global grille
    a = IA()
    grille = []
    for i in range(52):
        grille.append(0)
    tp1 = True
    hasLastPlayerWon = False
    while not hasLastPlayerWon:
        hp = False
        while not hp:
            if(tp1):
               a = waitForPlayer("c'est au tour du joueur 1. qu'il entre le numéro d'une collone : ")
            else :
                a = waitForPlayer("c'est au tour du joueur 2. qu'il entre le numéro d'une collone : ")
            i = 5
            if not (dans_grille(a + 5 * 9) and grille[a + 5 * 9] == 0):
                print("veuillez réessayer vous ne pouvez pas jouer la")
            else:
                hp = True
                while(dans_grille(a + i * 9) and grille[a + i * 9] == 0):
                    i -= 1
                i += 1
                print(a + i * 9)
                if(tp1):
                    grille[a + i * 9] = 1
                else:
                    grille[a + i * 9] = 2
        affiche(grille)                
        if(test_grille(grille) >= 4):
            hasLastPlayerWon = True
            if(tp1):
                print("le joueur 1 a gagné")
            else:
                print("le joueur 2 a gagné")
            return ""
        countLeft = 0
        for i in range(52):
            if(grille[i] == 0):
                countLeft += 1
        if(countLeft == 10):
            print("ceci est un macth nul")
            return -1
        if(not iap):
            tp1 = not tp1
        else:
            "o"
            

width = 500
height = 500
lignes = []
colonnes = []
tabRond = []
initialisation()
can.bind("<Button-1>",onClick)


x=75
y=75
joue = 0


class IA(object):
    def play(self, joueur, grille, profondeur):
        maxi = -1000-5
        k = 0
        for j in range(7):
            if not (dans_grille(j + 5 * 9) and grille.grid[j + 5 * 9] == 0):
                if (j != k):
                    a = "passe"
                else:
                    k+= 1
            else:
                grille.play(j, joueur)
                if(test_grille(grille.grid) >= 4):
                    grille.unplay(j)
                    return j
                i = self.mini(grille, joueur, profondeur, maxi)
                print(j,i)
                if(i > maxi):
                    maxi = i
                    k = j
                grille.unplay(j)
        return k
    
    def mini(self, grille, joueur, profondeur, maxi):
        mini = 1000
        if(profondeur == 0):
            return grille.evaluation(joueur)
        for j in range(7):
            if not (dans_grille(j + 5 * 9) and grille.grid[j + 5 * 9] == 0):
                a = "passe"
            else:
                grille.play(j,abs(joueur - 2) + 1)
                if(test_grille(grille.grid) >= 4):
                    grille.unplay(j)
                    return -1000-profondeur
                i = self.maxi(grille, joueur, profondeur - 1, mini)
                if(i < mini):
                    mini = i
                grille.unplay(j)
                if(mini < maxi):
                    return mini
        return mini
    
    def maxi(self, grille, joueur, profondeur, mini):
        maxi = -1000-5
        if(profondeur == 0):
            return grille.evaluation(joueur)
        for j in range(7):
            if not (dans_grille(j + 5 * 9) and grille.grid[j + 5 * 9] == 0):
                a = "passe"
            else:
                grille.play(j,joueur)
                if(test_grille(grille.grid) >= 4):
                    grille.unplay(j)
                    return 1000
                i = self.mini(grille, joueur, profondeur - 1, maxi)
                if(i > maxi):
                    maxi = i
                grille.unplay(j)
                if(maxi > mini):
                    return maxi
        return maxi

class Grille(object):
    def __init__(self, grid):
        self.grid = grid[:]
        self.tableau = [3,4,5,7,5,4,3,0,0,4,6,8,10,8,6,4,0,0,5,8,11,13,11,8,5,0,0,5,8,11,13,11,8,5,0,0,4,6,8,10,8,6,4,0,0,3,4,5,7,5,4,3]
    def dans_grille(self,k):
        return not (k < 0 or k > 52 or k % 9 >= 7) 
    def play(self,pos, joueur):
        i = 5
        while(self.dans_grille(pos + i * 9) and self.grid[pos + i * 9] == 0):
            i -= 1
        i += 1
        self.grid[pos + i * 9] = joueur
    def unplay(self, pos):
        i = 5
        while(self.dans_grille(pos + i * 9) and self.grid[pos + i * 9] == 0):
            i -= 1
        self.grid[pos + i * 9] = 0
    def evaluation(self, joueur):
        somme = 0
        for i in range(len(self.grid)):
            j = self.grid[i]
            if (j != 0):
                if(j==joueur):
                    somme += self.tableau[i]
                else:
                    somme -= self.tableau[i]
        return somme





        

fenetre.after(500,actual)
fenetre.mainloop()
        

