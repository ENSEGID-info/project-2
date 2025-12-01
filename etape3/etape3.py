from numpy import *
import math as m

e=[4,5,6,7,8,9,4,6,8,2]
a=[12,11.5,10.5,10,9,8.5,8,7.5,7,6.5]

def epaisseur_fact(n,alpha):

    return pow(m.sin(m.radians(alpha)),(n/(n+2)))


def etape3_main(n):
    r=[]
    for k in range(len(e)):
        t=e[k] * epaisseur_fact(n,a[k])
        r.append(t)

    return r





