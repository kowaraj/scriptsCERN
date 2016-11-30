#/usr/bin/python

from matplotlib import pyplot as pl

def parse_csv(fd):

    xs = []
    ys = []
    while True:
        line = fd.readline()
        #print(line)
        if not line:
            break
        line = line.strip()

        if not ',' in line:
            continue


        x = int(float(line[:line.find(',')]))
        y = float(line[line.find(',')+1:])

        xs.append(int(x+1000))
        ys.append(y)


    return [xs,ys]


fd_csv = open('ffa-ftw-rffg.csv', 'r')
vals = parse_csv(fd_csv)

print([i for i in range(len(vals[0])) if vals[1][i] == 1.855455232e9])
print([i for i in range(len(vals[0])) if vals[0][i] > 7000])

xs = vals[0]
ys = vals[1]
pl.subplot(2,1,1)
print(len(xs))
print(len(ys))

pl.plot(xs, ys, c='r')


fd = open('fg.txt', 'r')
x = [int(x) for x in fd.readlines()]
pl.subplot(2,1,2)
pl.plot(x, c='b')
pl.show()

input()

