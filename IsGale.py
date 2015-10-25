#################################################################
##                                                             ##
##  This program checks whether or not a point configuration   ##
##  is the Gale diagram of some polytope.                      ##
##                                                             ##
##  That is, whether for each hyperplane passsing through the  ## 
##  origin there are at least two points on either side of it. ## 
##                                                             ##  
#################################################################
from sympy import *
from fractions import Fraction
from itertools import *
from sys import exit

#####
#   This function checks some trivial cases
#   to see if it is possible for the point
#   configuration to be a Gale diagram.
#####
def dim_check(v, g):
    if min([v,g])<0:            # If either v, or g is negative,
        return 0                # then return a command to kill
                                # the program.
    else:                       
        if v in set([1,2,3]):   # All polytopes with 1, 2, or 3  
            if g==0:            # vertices are simplices, and 
                return 1        # therefore have a Gale diagram 
            else:               # of dimension 0.
                return 0
        else:
            if v-g-1>=2:        # In a general polytope P, 
                return 1        # dim(P)=v-g-1.  Already checked
            else:               # if it is a 0- or 1-polytope,
                return 0        # so this must be >=2.

#####
#   This function gets the vectors in the
#   configuration and puts them in a
#   (g)x(v) matrix.
#####
def get_matrix(height, width):
    M=Matrix(height, width, lambda i,j: 0)
    for j in range(width):
        print "Please input the coordinates of point %s: " % (j+1)
        for i in range(height):
            M[i,j]=Fraction(raw_input("    Entry %s: " % (i+1)))
    return M

#####
#   This function checks whether or not a
#   matrix M has rank rnk.
#####
def rank_ok(rnk, N):
    return len(N.rref()[1])==rnk


##########################
##########################
### Start the program. ###
##########################
##########################

# Get the dimension of the point confuguration
g = int(raw_input("Dimension of point configuration: "))
# Get the number of points in the configuration
v = int(raw_input("Number of points in the configuration: "))

if dim_check(v,g)==0:
    if v==1:
        print("There is no Gale Diagram with 1 point in a %s dimensional space." % (g))
        quit
    else:
        print("There is no Gale Diagram with %s points in a %s dimensional space." % (v,g))
        quit
else:
    M=get_matrix(g,v)
    print M
    #print M[1,2]
    if raw_input("Is this matrix correct?(y/n) " )!="y":
        quit
    else:
        if len(M.rref()[1])!=g:
            print "All of your points lie in a hyperplane."
        else:
            if g==1:                    # In the g=1 case,  
                pos=neg=0               # just need 2 points   
                for i in range(v):      # on either side of 
                    if M[i]>0:          # the origin.
                        pos+=1
                    elif M[i]<0:
                        neg+=1
                if pos>=2 and neg>=2:
                    print('This is the Gale diagram of a polytope of '
                             'dimension %s.' % (v-g-1))
                    quit
                else:
                    print('This is not the Gale diagram of a polytope.')
                    quit
            else:
                N=Matrix(g, g-1, lambda i,j:0)
                for comb in combinations(range(v),g-1):
                    for j in comb:
                        for i in range(g):
                            N[i,comb.index(j)]=M[i,j]
                    if len(N.rref()[1])!=g-1:
                        continue
                    else:
                        nml=Matrix(g,1, lambda i,j:0)
                        for d in range(g):
                            P=N.T
                            P.col_del(d)
                            nml[d]=(-1)**d*P.det()
                        pos=neg=0
                        for k in range(v):
                            ip=0
                            for b in range(g):
                                ip+=nml[b]*M[b,k]
                            if ip>0:
                                pos+=1
                            elif ip<0:
                                neg+=1
                        if pos<2:
                            print "The hyperplane perpendicular to"
                            print nml,
                            print "has an open half space with", pos,
                            print "point(s) contained in it."
                            exit
                        elif neg<2:
                            print "The hyperplane perpendicular to"
                            print nml,
                            print "has an open half space with", neg,
                            print "point(s) contained in it." 
                            exit
                print "This is the Gale diagram of a polytope of dimension",
                print v-g-1
