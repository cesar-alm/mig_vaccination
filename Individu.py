import numpy as np

class Individu:
    
    def __init__(self, categorie_age, vaccin, confinement=0):
        self.categorie_age = categorie_age # 0 = <15 1 = 15-25 ; 2 = 26-34 ; 3 = 35-49 ; 4 = 50-65 ; 5 = >65
        self.vaccin = vaccin
        self.confinement=confinement #booléen 
        self.calculere()

    def beta(self):
        '''Nombre de personnes saines contaminées par personne contagieuse par jour (en jours^-1)'''
        if self.confinement == 1:
            B = [[1.2, 0.6, 1., 1., 0.8, 0.4, 0.4],
            [0.6, 2., 1.4, 1.4, 1.2, 0.4, 0.4],
            [1., 1.4, 1.4, 1.4, 1.2, 0.4, 0.4],
            [1., 1.4, 1.4, 0.8, 0.8, 0.4, 0.4],
            [0.8, 1.2, 1.2, 0.8, 0.8, 0.4, 0.4],
            [0.4, 0.4, 0.4, 0.4, 0.4, 0.9, 0.9],
            [0.4, 0.4, 0.4, 0.4, 0.4, 0.9, 0.9]]
        else:
            B=[[4., 1.7, 2.2, 2.2, 1.8, 1.7, 1.7],
            [1.7, 7.3, 7., 4.8, 2.5, 1.7, 1.7],
            [2.2, 7., 7.3, 4.8, 2.5, 1.7, 1.7],
            [2.2, 4.8, 4.8, 2.5, 2.2, 1., 1.7],
            [1.8, 2.5, 2.5, 2.2, 2., 1.9, 1.9],
            [1.7, 1.7, 1.7, 1., 1.9, 1., 1.],
            [1.7, 1.7, 1.7, 1., 1.9, 1., 1.]]
            
        beta = np.array(B)

        if self.confinement == 2:
            # Gestes barrières
            beta*=0.3

        return beta*self.d()

    def b(self):
        '''Retourne l'inverse de la valeur du temps moyen d'incubation'''
        return 1/4 #valeur moyenne trouvée sur le site du gouvernement
    
    def c(self): #age?
        '''Retourne la proportion de personnes en incubation qui développent une forme asymptomatique'''
        if self.vaccin != None:
            return 1-self.vaccin.efficacite_maladie
        return 0.243 #valeur publiée par SPF mais variable et on le sait parce que dans ceux qu'on considère asymptomatiques il y a forcément ceux qui sont dans une phase "pré-symptomatiques" et ceux qu'on ne teste pas => pourcentages de symptomatiques est alors de 75,7%""
    
    def d(self):
        '''Retourne l'inverse du temps caractéristique de la durée de la contagion (symptomatique ou asymptomatique)'''
        if self.vaccin != None:
            return 1/0.1
        return 1/14
    
    def calculere(self):
        '''Retourne la proportion de symptomatiques qui vont en réanimation'''
        rr=0.14/700 #proportion de personnes ayant été en réa sur le nombre total de symptomatiques, valeurs calculées à partir du rapport ICNARC => données en angleterre
        if self.categorie_age==4:
            rr*=10
        if self.categorie_age==5:
            rr*=35 #valeur de Santé Publique France
        if self.categorie_age==6:
            rr*=30

        if self.vaccin != None:
            rr *= self.vaccin.efficacite_rea
        
        self.e =  rr
         
    def f(self):
        '''Retourne l'inverse du temps caractéristique avant de développer une forme grave'''
        return 1/8.5

    def g(self):
        '''Proportion de personnes en réa qui décèdent'''
        if self.categorie_age == 5:
            return 0.2
        elif self.categorie_age == 6:
            return 0.4
        
        return 0.05    

    def h(self):
        '''Proportion des personnes symptomatiques qui meurent chez elles'''
        return 0.00052

    def i(self):
        '''Retourn l'inverse du temps caractéristique du temps en reanimation si décès'''
        return 1/9.5 #temps médian d'après ICNARC report 
    
    def j(self):
        '''Retourn l'inverse du temps caractéristique du temps en rea si survie'''
        return 1/12 #temps médian d'après ICNARC report 
    
    def k(self):
        '''Retourne l'inverse du temps caractéristique de perte d'immunité'''
        if self.vaccin != None:
            return 1/(self.vaccin.duree_protection)
        return 1/(6*30) 

    def l(self):
        '''Retourn la proportion d’immunisés qui perdent l’immunité'''
        if self.vaccin != None:
            return self.vaccin.prop_perte_protection
        return 1