s = 8//2
print(s)
'''

import itertools

(K,N) = map(int,input().split())
li=list()
for i in range(K):
    l = list( map(int,input().split()))
    n= l[0]
    li.append(l[1:])
    assert len(li[i]) ==n

    max = 0
    limax = None

    for lis in itertools.product(*li):
        s= sum([x**2 for x in lis])%N

        if  s > max :
            max =s
            lmax =lis

print (max)
print(lmax)
'''