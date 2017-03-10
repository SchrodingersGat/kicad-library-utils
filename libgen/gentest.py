from libgen import *

lib = DeviceLib("test")

desc = Description("BC022",keywords="one, two, three", datasheet="www.google.url")
cmp = Component(desc)

for i in range(10):
    p = Pin('pin_{n}'.format(n=i*2+1), i*2+1, 0, 300*i)
    cmp.addItem(p)

for i in range(25):
    l = Line()
    for j in range(i//5):
        l.addPoint(Point(i*70,j*25-30))
    cmp.addItem(l)


cmp.addItem(Rect(0,0,100,50,thickness='12',fill='F'))

lib.addComponent(cmp)

lib.save()
