def climbingLeaderboard(scores, alice):
    scores = sorted(list(set(scores)))
    index = 0
    rank_list = []
    n = len(scores)
    for i in alice:
        while (n > index and i >= scores[index]):
            index += 1
        rank_list.append(n+1-index)
    return rank_list
'''
def climbingLeaderboard(scores, alice):

   # print(scores)
   # print(alice)

    maillist = list()
    for i in range(len(scores)):
        if scores[i] not in maillist:
            maillist.append(scores[i])
    #print(maillist)
    score = list()
    for i in  range(len(alice)):
        val = getposistion(maillist,alice[i],0,len(maillist)-1)
        #print(val)
        score.append(val)

    return (score)

def getposistion(maillist,val,f,l):

    if f > l:
        return f+1

    mid = (f+l)//2

    if maillist[mid] == val:
        return mid+1
    elif maillist[mid] > val:
        if mid == len(maillist) -1:
            return len(maillist) + 1
        elif mid == 0:
            return 2
        else:
            return getposistion(maillist,val,mid+1 ,l)

    else:
        if mid == 0:
            return 1
        elif mid == len(maillist) -1 and f == len(maillist) -1  and l == len(maillist) -1:
            #return getposistion(maillist, val, f, mid - 1)
            return len(maillist)
        else:
            return getposistion(maillist, val, f, mid -1)

'''

if __name__ == '__main__':


    #scores_count = int(input())

    scores = list(map(int, input().split()))

    #alice_count = int(input())

    alice = list(map(int, input().split()))

    result = climbingLeaderboard(scores, alice)

    print('\n'.join(map(str, result)))

    #fptr.write('\n'.join(map(str, result)))
