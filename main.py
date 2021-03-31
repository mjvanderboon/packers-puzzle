from copy import deepcopy
import random
from datetime import datetime as dt

TOP = True
BOTTOM = False

HELM = "helm"
SHIRT = "shirt"
LOGO = "logo"
PACKERS = "packers"

class Icon:
    def __init__(self,name,dir):
        self.name = name
        self.dir = dir

    def __eq__(self,icon):
        if icon.name==self.name and icon.dir!=self.dir:
            return True
        return False

    def __cmp__(self,icon):
        return not self.__eq__(icon)

HelmTop = Icon(HELM,TOP)
HelmBottom = Icon(HELM,BOTTOM)
ShirtTop = Icon(SHIRT,TOP)
ShirtBottom = Icon(SHIRT,BOTTOM)
LogoTop = Icon(LOGO,TOP)
LogoBottom = Icon(LOGO,BOTTOM)
PackersTop = Icon(PACKERS,TOP)
PackersBottom = Icon(PACKERS,BOTTOM)

class Grid:
    def __init__(self):
        self.item00 = None
        self.item01 = None
        self.item02 = None
        self.item10 = None
        self.item11 = None
        self.item12 = None
        self.item20 = None
        self.item21 = None
        self.item22 = None

    def __getitem__(self,pos):
        x,y = pos
        if x==0 and y==0:
            return self.item00
        elif x==1 and y==0:
            return self.item01
        elif x==2 and y==0:
            return self.item02
        elif x==0 and y==1:
            return self.item10
        elif x==1 and y==1:
            return self.item11
        elif x==2 and y==1:
            return self.item12
        elif x==0 and y==2:
            return self.item20
        elif x==1 and y==2:
            return self.item21
        elif x==2 and y==2:
            return self.item22
        raise IndexError(f"No index {x},{y} in Grid")

    def __setitem__(self,pos,item):
        x,y = pos
        x,y = pos
        if x==0 and y==0:
            self.item00 = item
        elif x==1 and y==0:
            self.item01 = item
        elif x==2 and y==0:
            self.item02 = item
        elif x==0 and y==1:
            self.item10 = item
        elif x==1 and y==1:
            self.item11 = item
        elif x==2 and y==1:
            self.item12 = item
        elif x==0 and y==2:
            self.item20 = item
        elif x==1 and y==2:
            self.item21 = item
        elif x==2 and y==2:
            self.item22 = item
        else:
            raise IndexError(f"No index {x},{y} in Grid")

    def show(self):
        for x in range(0,3):
            for y in range(0,3):
                item = self[x,y]
                print(f"({x},{y}): {item.id}, {item.cw}")

class Item:
    def __init__(self,id,top,right,bottom,left,cw=0):
        self.id = id
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.cw = cw

    def rotate_cw(self):
        return Item(id=self.id,
                    top=self.left,
                    right=self.top,
                    bottom=self.right,
                    left=self.bottom,
                    cw=self.cw+1)

def possible(grid,item,i,j):
    # Check if item is already in grid
    for x in range(0,3):
        for y in range(0,3):
            _item = grid[x,y]
            if _item is None:
                continue
            if _item.id == item.id:
                return False

    # Validate neighbours
    for x in range(i-1,i+2):
        if x<0 or x>2:
            # Continue if we are out of bounds
            continue
        for y in range(j-1,j+2):
            if y<0 or y>2:
                # Continue if we are out of bounds
                continue
            _item = grid[x,y]
            if _item is None:
                continue
            if x==i and y==j:
                continue
            if x==i and y>j:
                # Top
                if item.bottom != _item.top:
                    return False
            elif x>i and y==j:
                # Right
                if item.right != _item.left:
                    return False
            elif x==i and y<j:
                # Bottom
                if item.top != _item.bottom:
                    return False
            elif x<i and y==j:
                # Left
                if item.left != _item.right:
                    return False
    return True


def solve():
    #global grid
    for x in range(0,3):
        for y in range(0,3):
            # print(x,y)
            if grid[x,y] is None:
                for item in items:
                    if possible(grid,item,x,y):
                        grid[x,y] = item
                        solve()

                        # Reset
                        grid[x,y] = None
                # No item fits here
                #print("Nope")
                return
    # We're done!
    grid.show()
    raise ValueError()

item1 = Item(
    id=1,
    top=ShirtBottom,
    right=LogoTop,
    bottom=HelmTop,
    left=PackersTop
)
item2 = Item(
    id=2,
    top=PackersBottom,
    right=LogoTop,
    bottom=ShirtTop,
    left=HelmBottom
)
item3 = Item(
    id=3,
    top=LogoBottom,
    right=ShirtTop,
    bottom=ShirtTop,
    left=PackersBottom
)
item4 = Item(
    id=4,
    top=LogoBottom,
    right=PackersTop,
    bottom=HelmTop,
    left=ShirtTop
)
item5 = Item(
    id=5,
    top=ShirtBottom,
    right=LogoBottom,
    bottom=PackersTop,
    left=HelmTop
)
item6 = Item(
    id=6,
    top=ShirtBottom,
    right=LogoBottom,
    bottom=HelmBottom,
    left=PackersBottom
)
item7 = Item(
    id=7,
    top=ShirtTop,
    right=LogoTop,
    bottom=PackersTop,
    left=HelmBottom
)
item8 = Item(
    id=8,
    top=PackersTop,
    right=HelmTop,
    bottom=LogoBottom,
    left=HelmBottom
)
item9 = Item(
    id=9,
    top=LogoBottom,
    right=ShirtBottom,
    bottom=HelmTop,
    left=PackersTop
)

grid = Grid()
originals = [item1,item2,item3,item4,item5,item6,item7,item8,item9]
items = []
for original in originals:
    items.append(original)
    iter_original = deepcopy(original)
    for i in range(1,4):
        iter_original = iter_original.rotate_cw()
        items.append(iter_original)

# random.shuffle(items)

if __name__=="__main__":
    # Note: recursive solving only works when there
    # exists at least 1 solution. Otherwise it will
    # get stuck.
    t1 = dt.now()
    try:
        solve()
    except:
        pass
    print(dt.now()-t1)