from collections import OrderedDict

def wordorder(n,li):
    sum =0
    st1 = set()
    dic =OrderedDict()
    if 1<= n and n<= 10**5:
        for val in li:
            sum = sum + len(val)
            st1.add(val)


        if sum <= 10**6:
            for vall in li:
                cnt = 0
                print(vall)
                if  vall in dic.keys():
                    dic[vall] += 1
                else:
                    dic[vall]= 1


    print(len(st1))
    for i in dic.values():
        print(i, end =" ")


if __name__ == '__main__':
    noofword = int(input())
    inputs =[]
    for i in range(noofword):
        inputs.append(input())

    wordorder(noofword,inputs )