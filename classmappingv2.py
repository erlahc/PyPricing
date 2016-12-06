from pony.orm import *
import csv
import os

def csvtolist(chemin):
    file = open(chemin)
    reader = csv.reader(file)
    data = list(reader)
    data.sort()
    return data

def ctevect(cte,vect):
    v1=[]
    for i in vect:
        v1.append(round(cte*i,2))
    return v1

def multvect(v1,v2):
    v3=[]
    if len(v1)==len(v2):
        for i in list(range(len(v1)-1)):
            v3.append(round(v1[i]*v2[i],2))
    return v3


db = Database("sqlite", "pony2.sqlite", create_db=True)

class Currency(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rate = Required(float)
    countrys = Set('Country')

class Country(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rate = Required(float)
    rate_sim = Required(float)
    junior = Optional(float)
    junior_sim = Optional(float)
    senior = Optional(float)
    senior_sim = Optional(float)
    manager = Optional(float)
    manager_sim = Optional(float)
    sm = Optional(float)
    sm_sim = Optional(float)
    director = Optional(float)
    director_sim = Optional(float)
    partner = Optional(float)
    partner_sim = Optional(float)
    expert = Optional(float)
    expert_sim = Optional(float)
    currency = Required(Currency)
    companys = Set('Company')

class Company(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    turnover = Required(float)
    manual = Optional(float)
    activity = Required('Activity')
    scope = Required('Scope')
    csp = Required('Csp')
    xworks = Set('Xwork')
    country = Required(Country)

class Activity(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    mini = Required(float)
    volume = Required(float)
    companys = Set(Company)
    structure = Required('Structure')

class Scope(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rate = Required(float)
    rate_sim = Required(float)
    companys = Set(Company)

class Csp(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rate = Required(float)
    rate_sim = Required(float)
    companys = Set(Company)

class Xwork(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    rate = Required(float)
    rate_sim = Required(float)
    companys = Set(Company)

class Structure(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    junior = Required(float)
    junior_sim = Required(float)
    senior = Required(float)
    senior_sim = Required(float)
    manager = Required(float)
    manager_sim = Required(float)
    sm = Required(float)
    sm_sim = Required(float)
    director = Required(float)
    director_sim = Required(float)
    partner = Required(float)
    partner_sim = Required(float)
    expert = Required(float)
    expert_sim = Required(float)
    activitys = Set(Activity)

db.generate_mapping(create_tables=True)

@db_session
def populate_permanent(cu,co,st,ac):
    #populate currencies
    for i in cu:
        Currency(name=i[0],rate=i[1])
    #populate countrys
    for i in co:
        o=select(p for p in Currency if p.name==i[3]).first()
        Country(name=i[0],rate=i[1],rate_sim=i[2],currency=o,\
            junior=i[4],junior_sim=i[5],\
            senior=i[6],senior_sim=i[7],\
            manager=i[8],manager_sim=i[9],\
            sm=i[10],sm_sim=i[11],\
            director=i[12],director_sim=i[13],\
            partner=i[14],partner_sim=i[15],\
            expert=i[16],expert_sim=i[17])
    #populate structures
    for i in st:
        Structure(name=i[0],\
            junior=i[1],junior_sim=i[2],\
            senior=i[3],senior_sim=i[4],\
            manager=i[5],manager_sim=i[6],\
            sm=i[7],sm_sim=i[8],\
            director=i[9],director_sim=i[10],\
            partner=i[11],partner_sim=i[12],\
            expert=i[13],expert_sim=i[14])
    #populate activitys
    for i in ac:
        s=select(p for p in Structure if p.name==i[2]).first()
        Activity(name=i[0],mini=i[1],structure=s,volume=i[3])

@db_session
def populate_company(com):
    for i in com:
        # Créer le scope si il n'existe pas
        if not(exists(p for p in Scope if p.name==i[6])):
            Scope(name=i[6],rate=0,rate_sim=0)
        sc=select(p for p in Scope if p.name==i[6]).first()
        # Créer le CSP si il n'existe pas
        if not(exists(p for p in Csp if p.name==i[5])):
            Csp(name=i[5],rate=0,rate_sim=0)
        cs=select(p for p in Csp if p.name==i[5]).first()
        # Vérifier si le pays existe
        if not(exists(p for p in Country if p.name==i[3])):
            print("Le pays de cette entite n'existe pas dans la base : " & i.name)
        else:
            co=select(p for p in Country if p.name==i[3]).first()

        # Interpoler la ligne d'abaque
        ac=select(p for p in Activity if p.name==i[1] and p.mini==max(p.mini for p in Activity if p.name==i[1] and p.mini<float(i[2]))).first()
        
        Company(name=i[0],turnover=i[2],activity=ac,scope=sc,csp=cs,country=co)
@db_session
def get_company_list():
    a=[]
    comp=select((x.name,y.name) for x in Company for y in x.country)[:]
    for i in comp:
        a.append((i[0],i[1],get_volumebase(i[0]),get_csp_impact(i[0]),get_scope_impact(i[0]),get_country_impact(i[0]),get_volumedriven(i[0])))
    return a

@db_session
def get_volumebase(comp=None):
    if comp==None:
        result=select(y.volume for x in Company for y in x.activity).sum()
    else:
        result=select(y.volume for x in Company for y in x.activity if x.name==comp).sum()
    return result
    
@db_session
def get_csp_impact(comp=None):
    if comp==None:
        csp_impact = select(y.rate*z.volume for x in Company for y in x.csp for z in x.activity).sum()
    else:
        csp_impact = select(y.rate*z.volume for x in Company for y in x.csp for z in x.activity if x.name==comp).sum()
    return round(-1*csp_impact/100,2)

@db_session
def get_csp_list():
    a=select((x.name,x.rate) for x in Csp)[:]
    return a

@db_session
def update_csp(x,y):
    a=select(a.id for a in Csp if a.name==x)[:]
    Csp[a[0]].rate=y

@db_session
def get_scope_impact(comp=None):
    if comp==None:
        scope_impact = select(y.rate*z.volume for x in Company for y in x.scope for z in x.activity).sum()
    else:
        scope_impact = select(y.rate*z.volume for x in Company for y in x.scope for z in x.activity if x.name==comp).sum()
    return round(scope_impact/100,2)

@db_session
def get_scope_list():
    a=select((x.name,x.rate) for x in Scope).order_by(1)[:]
    return a

@db_session
def update_scope(x,y):
    a=select(a.id for a in Scope if a.name==x)[:]
    Scope[a[0]].rate=y

@db_session
def get_country_impact(comp=None):
    if comp==None:
        country_impact = select(y.rate_sim*z.volume for x in Company for y in x.country for z in x.activity).sum() - \
        select(y.rate*z.volume for x in Company for y in x.country for z in x.activity).sum()
    else:
        country_impact = select(y.rate_sim*z.volume for x in Company for y in x.country for z in x.activity if x.name==comp).sum() - \
        select(y.rate*z.volume for x in Company for y in x.country for z in x.activity if x.name==comp).sum()
    return round(country_impact,2)

@db_session
def get_country_modified():
	a=[]
	country_modified = select((y.name,y.rate_sim-y.rate) for x in Company for y in x.country for z in x.activity)[:]
	for i in country_modified:
		if i[1]!=0:
			a.append(i)
	return a

@db_session
def get_country_default(co):
    a=select(x.rate for x in Country if x.name==co).first()
    return a

@db_session
def get_country_list():
    # a=select((x.name,x.rate_sim) for x in Country)[:]
    a=select((y.name,y.rate_sim) for x in Company for y in x.country)[:]
    return a

@db_session
def update_country(x,y):
    a=select(a.id for a in Country if a.name==x)[:]
    Country[a[0]].rate_sim=y

@db_session
def get_volumedriven(comp=None):
    if comp==None:
        result = get_volumebase()+get_csp_impact()+get_scope_impact()+get_country_impact()
    else:
        result = get_volumebase(comp)+get_csp_impact(comp)+get_scope_impact(comp)+get_country_impact(comp)
    return round(result,2)

@db_session
def get_volumesplited(comp):
    """ retourne une liste avec les volumes splités par grade """
    i=select((x.name,y) for x in Company for y in x.activity.structure if x.name==comp).first()
    a=[i[1].junior_sim,i[1].senior_sim,i[1].manager_sim,i[1].sm_sim,i[1].director_sim,i[1].partner_sim,i[1].expert_sim]
    result=ctevect(get_volumedriven(i[0]),a)
    return result

@db_session
def get_price(comp):
    """ Faux, il manque la durée de la journée de travail """
    i=select((z.rate,y)for x in Company for y in x.country for z in y.currency if x.name==comp).first()
    a=[i[1].junior,i[1].senior,i[1].manager,i[1].sm,i[1].director,i[1].partner,i[1].expert]
    result=ctevect(i[0],a)
    return result

@db_session
def get_volumepriced(vs,p):
    result=multvect(vs,p)
    print(sum(result))
    return result

if __name__ == '__main__':
    # cu=csvtolist('CURRENCY.CSV')
    # co=csvtolist('COUNTRY.CSV')
    # st=csvtolist('STRUCTURE.CSV')
    # ac=csvtolist('ACTIVITY.CSV')
    # com=csvtolist('DB.CSV')
    # populate_permanent(cu,co,st,ac)
    # populate_company(com)
    a=get_country_list()
    print(a)
