def check(a: list, n:int):
    subsequence = 0
    subsequence1 = 0
    res = 0 
    for i in range(len(a)):
        for j in range(len(a)):
            if(a[i][j] == 0):
                subsequence += 1 
            elif(a[i][j] == 1):
                subsequence = 0
            if subsequence >= n:
                res += 1
            if(a[j][i] == 0):
                subsequence1 += 1 
            elif(a[j][i] == 1):
                subsequence1 = 0
            if subsequence1 >= n:
                res += 1
        subsequence = 0
        subsequence1 = 0
    return res

n = int(input())
m = int(input())
a = []

while m!=0:
    a = [list(map(int, input().split())) for _ in range(m)]
    print(check(a, n))
    m = int(input())