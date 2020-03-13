import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import random
import os


class Person(object):                                    # class for one person
    def __init__(self, happiness_threshold=0.6):
        self.type = 0
        self.happiness_threshold = happiness_threshold   # happiness threshold
        r = random.randint(0, 100)
        if r <=50:                                       # equally division two type of agents
            self.type = 1
        else:
            self.type = -1

    def who(self):
        return self.type

    def thresh(self):
        return self.happiness_threshold


class City(object):                             # class for all city = square L by L
    def __init__(self,size=50, density=90):
        self.density = density                  # denisty of population
        self.size = size                        # size of square
        self.empty = []
        self.grid = np.zeros((size, size))      # grid to plot of results
        self.array = [[0 for i in range(size)] for j in range(size)]    # array of persons
        for i in range(size):
            for j in range(size):
                r = random.randint(0, 100)
                if r <= density:
                    self.array[i][j] = Person()
                else:
                    self.array[i][j] = 0
                    self.empty.append([i,j])
        self.next = []                          # table of nearest neighbours
        for i in range(size-1):                 # with boundary conditions
            self.next.append(i+1)
        self.next.append(0)
        self.previous = []
        self.previous.append(size-1)
        for i in range(1, size):
            self.previous.append(i-1)


    def plot(self, tekst):                          # make plot of the current state
        colors = ['#000000','#FFFFFF', '#969792']   # black, white and gray
        tmp = mpl.colors.ListedColormap(colors)
        for i in range(self.size):
            for j in range(self.size):
                if self.array[i][j] != 0:
                    self.grid[i][j] = self.array[i][j].who()
        plt.imshow(self.grid, cmap=tmp);
        plt.colorbar()
        plt.savefig(tekst)
        plt.close()



    def happy(self,x,y):    # is agent happy ?
        n = 0               # number of all neighbours
        t = 0               # number of neighbours the same type

        if self.array[self.next[x]][y] != 0:
            n+=1
            if self.array[self.next[x]][y].who() == self.array[x][y].who():
                t+=1
        if self.array[x][self.next[y]] != 0:
            n+=1
            if self.array[x][self.next[y]].who() == self.array[x][y].who():
                t+=1
        if self.array[x][self.previous[y]] != 0:
            n+=1
            if self.array[x][self.previous[y]].who() == self.array[x][y].who():
                t+=1
        if self.array[self.previous[x]][y] != 0:
            n+=1
            if self.array[self.previous[x]][y].who() == self.array[x][y].who():
                t+=1
        if self.array[self.previous[x]][self.previous[y]] != 0:
            n+=1
            if self.array[self.previous[x]][self.previous[y]].who() == self.array[x][y].who():
                t+=1
        if self.array[self.next[x]][self.previous[y]] != 0:
            n+=1
            if self.array[self.next[x]][self.previous[y]].who() == self.array[x][y].who():
                t+=1
        if self.array[self.next[x]][self.next[y]] != 0:
            n+=1
            if self.array[self.next[x]][self.next[y]].who() == self.array[x][y].who():
                t+=1
        if self.array[self.previous[x]][self.next[y]] != 0:
            n+=1
            if self.array[self.previous[x]][self.next[y]].who() == self.array[x][y].who():
                t+=1

        if n!= 0:
            if t/n < self.array[x][y].thresh():
                return False        # agent is unhappy
            else:
                return True         # agent is happy
        return False


    def simulation(self):
        iter = 0
        while iter < 50000:
            for i in range(self.size):
                for j in range(self.size):
                    if self.array[i][j] != 0:
                        if self.happy(i,j) == False:
                            r = random.choice(self.empty)
                            self.empty.remove(r)
                            self.array[r[0]][r[1]] = Person()
                            self.array[r[0]][r[1]].type = self.array[i][j].who()
                            self.array[i][j] = 0
                            self.empty.append([i,j])
            if iter%100 == 0:
                print(iter)
            iter+=1



def main():
    city = City()
    city.plot('before.png')
    city.simulation()
    city.plot('after.png')

if __name__ == '__main__':
    main()
