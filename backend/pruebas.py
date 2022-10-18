'''s = 'fun {} {} {}'
c = '{}'
print(s.find(c))

s = 'fun {} {} {}'
c = '{}'
lst = []
for pos,char in enumerate(s):
    if(char == c):
        lst.append(pos)

print(lst)
x = ["my", "unlimited", "sadness"]
for i in range(len(x)-1, -1, -1):
    print(i, x[i])'''
tel = "aveces"

a = "Galleta"

print(a=="Galleta")