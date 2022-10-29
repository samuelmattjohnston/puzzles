#!/usr/bin/env python3

#grab a number
# userNum=int(input("Enter Number"))
import argparse
parser = argparse.ArgumentParser(
    prog = 'Lagrange four-square solver',
    description = "Lagrange's four-square theoum states that any number can be reprsesented as the sum of 4 perfect roots."
)
parser.add_argument('userNum',type=int)
args=parser.parse_args()

# return a generator made of all the powers of two of a number
# def nextTwo(_bfNum):
#     return (int('0b1'+'0'*((i-1)//2),2) for i, digit in enumerate(reversed(_bfNum), 1) if digit=='1')

# Some dirty math to see if we can add some of these powers of two together and still be less than our original number
# it seems to be slow due to line 22, and I'm not sure how to test it otherwise. 
# def nearestTwoRoots(num):
#     bfNum=format(num,'b')
#     # powTwoHigh=sum((int('0b1'+'0'*((i-1)//2),2) for i, digit in enumerate(reversed(bfNum), 1) if digit=='1'))
#     powTwoHigh=2**((len((bfNum))+1)//2)
#     powTwoLow=0
#     getNext=nextTwo(bfNum)
#     nextPow=next(getNext,0)
#     rem=num
#     while nextPow > 0:
#         testPow=powTwoLow+nextPow
#         rem=num-(testPow*testPow)
#         if rem > 0:
#             powTwoLow = testPow
#         else:
#             break
#         bfNum=format(rem,'b')
#         getNext=nextTwo(bfNum)
#         nextPow=next(getNext,0)
#     return powTwoLow, powTwoHigh

def accPows(num, rootLow,rootHigh):
    testRoot=(rootLow+rootHigh)//2
    while rootHigh-rootLow > 1:
        if num < testRoot*testRoot:
            rootHigh = testRoot
            testRoot = (rootLow+rootHigh)//2
        else:
            rootLow = testRoot
            testRoot = (rootLow+rootHigh)//2
    return rootLow

def findBlindRoots(num, numRoots):
    res=[]
    rem=num
    for findRoot in range(numRoots):
        lenRem=len(format(rem,'b'))
        powHigh = int('0b1'+'0'*((lenRem+1)//2),2)
        powLow = int('0b1'+'0'*((lenRem-1)//2),2)
        #abaonded this, as it seemed to be slower than just using closest power of two
        # powLow, powHigh = nearestTwoRoots(rem)
        newPow=accPows(rem, powLow, powHigh)
        res.append(newPow)
        rem=max(rem-(newPow*newPow),0)
    return res, rem

# This function will gets the 4 roots that make up a number
def findRoots(num):
    roots, rem = findBlindRoots(num, 4)
    # if the function for grabbing higest roots blindly has a remainder, 
    # set first root to root-1, and incriment remainder by (2*root)-1
    # this is from properties of perfect roots, 
    # where any root is the sum of all odd numbers with n elements, where n=root
    while rem:
        rem+=(2*roots[0])-1
        roots[0]-=1
        rootsTwo, remTwo = findBlindRoots(rem, 3)
        # if there is still a remainder, try with the next two (This should be faster than the above)
        if remTwo:
            remTwo+=(2*rootsTwo[0])-1
            rootsTwo[0]-=1
            rootsThree, remThree = findBlindRoots(remTwo, 2)
            # Try with the last two roots, decrease by one, and solve for remainder
            if remThree:
                remThree+=(2*rootsThree[0])-1
                rootsThree[0]-=1
                rootsFour, remFour = findBlindRoots(remThree, 1)
                if not remFour:
                    # if no remainder, we found a solution, and we just return
                    return [roots[0],rootsTwo[0]]+rootsThree
                #if there is a remainder, rem is able to be increased, and rootsOne decremented 
                # at the beginning fo loop
            else:
                return [roots[0]]+rootsTwo
        else:
            return roots
    return roots
userRoots=findRoots(args.userNum)
print(f"Roots:\n{userRoots[0]}^2 ,{userRoots[1]}^2 ,{userRoots[2]}^2 ,{userRoots[3]}^2")
