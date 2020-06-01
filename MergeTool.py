def merge_the_tools(string, k):
    st =0
    end=k
    sublist =list()
    while st < len(string):
        val = string[st:end]
        st =  end
        end = end +k
        sublist.append(val)

    print (sublist)
    i=0
    mainli =list()
    for li in sublist:
        i=0
        templi = list()
        str=""
        while i < len(li):
            if li[i] not in templi:
                templi.append(li[i])
            i +=1
        val = str.join(templi)
        mainli.append(val)

    for lia in mainli:
        print(lia)

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)