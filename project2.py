FIELD = 931312417536517329027114974149 #random 30 digit prime
AShares = [] #list of all shares 
total = 0 #global sum total

import random
from phe import paillier
import secrets
import time
import numpy as np


def randomlist(n):
    # function generates a list of n random numbers 
    randoml = random.sample(range(0, 10000), n)
    return randoml

def noprivacy(randoml):
    # computes average of n numbers without any privacy 
    return sum(randoml)/ len(randoml)

def pallierz(randoml, n):
    # implements palliers to compute average of n numbers 
    secretsGenerator = secrets.SystemRandom()
    random_number = secretsGenerator.randint(0, FIELD)
    pub_key,priv_key = paillier.generate_paillier_keypair()
    enc = []
    dec = []
    sums = 0
    for i in randoml:
        encr = pub_key.encrypt(i, r_value= random_number)
        enc.append(encr)
        sums = sums + encr
    avg = sums
    for s in enc:
        decr = priv_key.decrypt(s)
        dec.append(decr)
    dd = priv_key.decrypt(avg)/ n
    
    return dd

def secretz(k):   
    # generates the secret using l(i)
    global total
    jkl = 1
    l, br = sumz(k)
    for b in range(0,k):
        li = larange(jkl,l)
        fx  = li * br[b]
        total += fx
        jkl +=1
        
def larange(i, K):
    # calculates l(i) for Shamir's 
    s = 1
    for j in K:
        if(j==i):
            continue
        u = pow(i-j,-1,FIELD)*(-1*j)
        s = u * s
    return s
        
def coeff(secret, t, n):
    # coefficient generator for polynomial
    cx = [random.randrange(0, FIELD) for x in range(t-1)]
    cx.append(secret)
    sharesz(cx, n)
    
def sharesz(cx, n):
    # generating shares for secrets 
    z = np.poly1d(cx) 
    s = []
    for i in range(1,n+1):
        s.append(z(i)%FIELD)
    AShares.append(s)
    
def sumz(k):
    # calculating the sum of all shares i.e f(i)= f1(i) + f2(i)+... 
    global total
    gg = []
    le = list(range(1, k+1))
    for i in le:
        su = 0
        for row in AShares:
            ro = row[i-1]
            su = su + ro
        gg.append(su)
    return le, gg

def dp(rlist, epsilon, n):
    # implementing differential privacy 
    sums = sum(rlist)
    b = 10000/n
    noise = np.random.laplace(0,b)
    result = sums + noise
    avg = result/n
    return avg


def oneS(r):
    # measuring time taken to run NO PRIVACY
    start = time.time()
    fi = noprivacy(r)
    end = time.time()
    T = end-start
    return fi, T

def twoS(r,n):
    # measuring time taken to run PALLIER
    start = time.time()
    fi = pallierz(r, n)
    end = time.time()
    T = end-start
    return fi, T

def threeS(r, t, n):
    # measuring time taken to run SHAMIR'S
    k = t + 1
    start = time.time()
    for s in r:
        coeff(s,t,n)
    secretz(k)
    fi = (total % FIELD)/n
    end = time.time()
    T = end-start
    return fi, T

def fourS(r, epsilon, n):
    # measuring time taken to run DIFFERENTIAL PRIVACY
    start = time.time()
    fi = dp(r, epsilon, n)
    end = time.time()
    T = end-start
    return fi, T

def howaccurate(actual,calculated): 
    # calculating the pecentage relative error
    c = (actual - calculated)
    n = (c/actual) * 100
    return n

def oneA(r):
    # measuring accuracy of NO PRIVACY
    a = noprivacy(r)
    fi = noprivacy(r)
    g = howaccurate(a, fi)
    return a, fi, g

def twoA(r,n):
    # measuring accuracy of PALLIERS
    a = noprivacy(r)
    fi = pallierz(r, n)
    g = howaccurate(a, fi)
    return a, fi, g

def threeA(r, t, n):
    # measuring accuracy of SHAMIRS
    a = noprivacy(r)
    k = t + 1
    for s in r:
        coeff(s,t,n)
    secretz(k)
    fi = (total % FIELD)/n
    g = howaccurate(a, fi)
    return a, fi, g

def fourA(r, epsilon, n):
    # measuring accuracy of DIFFERENTIAL PRIVACY
    a = noprivacy(r)
    fi = dp(r, epsilon, n)
    g = howaccurate(a, fi)
    return a, fi, g


def main():
    n = 5
    #n = 50
    #n = 100
    #n = 500
    #n = 1000
    #n = 5000
    t = round(n//2)
    epsilon = 1.0
    r2 = randomlist(n)
    
    #box 1
    """
    a = oneS(r2) 
    b = twoS(r2,n)
    c = threeS(r2, t, n)
    d = fourS(r2, epsilon, n)
    print('No privacy (Avg. calculated, Time taken): ', a)
    print('Pallier (Avg. calculated, Time taken): ', b)
    print('Shamir (Avg. calculated, Time taken): ', c)
    print('Differential Privacy (Avg. calculated, Time taken): ', d)
    """
    
    #box 2
    """
    W = oneA(r2) 
    X = twoA(r2,n)
    Y = threeA(r2, t, n)
    Z = fourA(r2, epsilon, n)
    print('No privacy (actual, calculated, percentage relative error): ', W)
    print('Pallier (actual, calculated, percentage relative error): ', X)
    print('Shamir (actual, calculated, percentage relative error): ', Y)
    print('Differential Privacy (actual, calculated, percentage relative error): ', Z)
    """
main()
