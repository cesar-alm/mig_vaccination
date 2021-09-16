class Vaccin:
    
    def __init__(self, efficacite_maladie=0.042, efficacite_rea=0.01, duree_protection=365*2, prop_perte_protection=0.5):
        '''
        Efficacité réa = (proportion symptomatique qui vont en réa vacciné)/(proportion symtomatique qui vont en réa pas vaccinés)
        Efficacité maladie = (proportion des incubés qui développent des symptomes)
        '''
        self.efficacite_maladie = efficacite_maladie
        self.efficacite_rea = efficacite_rea
        self.duree_protection = duree_protection
        self.prop_perte_protection = prop_perte_protection