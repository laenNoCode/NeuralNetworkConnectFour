from math import tanh
from time import sleep
class Neurone(object):
    def __init__(this,valeur):
        this.valeur = valeur;
        this.liens = []
    def FinaliserNeurone(this):
        this.valeur = tanh(this.valeur);
        
class Lien(object):
    def __init__(this,valeur,neurone):
        this.valeur = valeur;
        this.neurone = neurone;
    def CalculerNeurone(this,valeurNeuroneEntree):
        this.neurone.valeur += this.valeur * valeurNeuroneEntree;

class CoucheNeurone(object):
    def __init__(this, valeurNeurones, valeursLiens = [],valeurBias = [],
                 neuronesCouchePrecedente = [], biasPrecedent = []):
        this.neurones = [];
        this.bias = Neurone(1);
        for valeur in valeurNeurones:
            this.neurones.append(Neurone(valeur))
        for i in range(len(neuronesCouchePrecedente)):
            for j in range(len(valeurNeurones)):
                neuronesCouchePrecedente[i].liens.append(
                    Lien(valeursLiens[i * len(valeurNeurones) + j],                       
                this.neurones[j]));
        for i in range(len(valeurBias)):    
            biasPrecedent.liens.append(Lien(valeurBias[i],this.neurones[i]))
    def calculer(this):
        for neurone in this.neurones:
            neurone.FinaliserNeurone()
            for lien in neurone.liens:
                lien.CalculerNeurone(neurone.valeur);
        for lien in this.bias.liens:
            lien.CalculerNeurone(1);
    def afficher(this):
        for i in range(len(this.neurones)):
            print(i,this.neurones[i].valeur)
        sleep(1);
    def reinitNeurVal(this):
        for n in this.neurones:
            n.valeur = 0.0;
    def getNeuronesVal(this):
        tab = []
        for n in this.neurones:
            tab.append(n.valeur);
        return tab

class ReseauNeuronePuissance4(object):
    def __init__(this, tableau = [0] * 3936, tableauBias = [0] * 71):
        this.slow = False
        this.entree = CoucheNeurone([2] * 84);
        #taille tableau 1056
        #256
        this.c1 = CoucheNeurone([0] * 32, tableau[:2688],tableauBias[:32],
                                             this.entree.neurones,this.entree.bias);
        this.c2 = CoucheNeurone([0] * 32, tableau[2688:2688+1024],tableauBias[32:64],
                                                 this.c1.neurones, this.c1.bias);
        this.sortie = CoucheNeurone([0] * 7, tableau[2688+1024:],tableauBias[64:],
                                             this.c2.neurones, this.c2.bias);


    def calculer(this):
        this.c1.reinitNeurVal();
        this.c2.reinitNeurVal();
        this.sortie.reinitNeurVal();
        this.entree.calculer();
        this.c1.calculer();
        this.c2.calculer();
        #this.c1.afficher();
        if 0:
            for i in range(len(this.sortie.neurones)):
                print(i," ",this.sortie.neurones[i].valeur);
            sleep(1.2);
        #print(this.coucheIntermediaire2.getNeuronesVal())
        this.decisions = sorted(range(len(this.sortie.neurones)),
                                key = lambda x : -this.sortie.neurones[x].valeur)

    def setEntree(this, tableau):
        for i in range(7):
            for j in range(6):
                this.entree.neurones[i * 6 + j].valeur = tableau[i][j];
                this.entree.neurones[i * 6 + j + 42].valeur = tableau[i][j];
                if (this.entree.neurones[i * 6 + j].valeur == 2):
                    this.entree.neurones[i * 6 + j].valeur = 0;
                if (this.entree.neurones[i * 6 + j + 42].valeur == 1):
                    this.entree.neurones[i * 6 + j + 42].valeur = 0;
                this.entree.neurones[i * 6 + j + 42].valeur /= 2;
                this.entree.neurones[i * 6 + j].valeur = float(this.entree.neurones[i * 6 + j].valeur);
                this.entree.neurones[i * 6 + j + 42].valeur = float(this.entree.neurones[i * 6 + j + 42].valeur);

        
                           

