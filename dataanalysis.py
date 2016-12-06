def waterfallgraph(a):
    """Prend un tuple en entrée en sort une liste de tuple"""
    start = 0
    size = 0
    temp = 0
    result=[]
    for i in range(len(a)):
        if i == 0:
            start = 0
            size = a[i]
            temp=size
            result.append((start,size))
        elif i == len(a)-1:
            start = 0
            size = temp
            temp = 0
            result.append((start,size))
        else:
            start = temp
            size = a[i]
            temp = start + size
            result.append((start,size))
    return result

    def countrygraph():
        return None