import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
import random
import os


class Person():
    def __init__(self):
        # random division between two type of agents
        self._type = random.choice([1,-1])

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if(value not in (-1,0,1)):
            raise ValueError("Value Range Error")
        self._type = value

    @type.deleter
    def type(self):
        del self._type



class City():
    def __init__(self, happiness_threshold: float, size: int, density: int, trials: int):
        self.happiness_threshold = happiness_threshold
        self.density = density
        self.trials = trials
        self.size = size


    def __repr__(self):
       return f"thresh: {self._happiness_threshold}; size: {self._size}; density: {self._density}; trials: {self._trials}"


    def _initial_configuration(self):
        self._people_array = [[0 for i in range(self._size)] for j in range(self._size)]
        self._empty = []
        for i in range(self._size):
            for j in range(self._size):
                r = random.randint(0, 100)
                if r <= self._density:
                    self._people_array[i][j] = Person()
                else:
                    self._people_array[i][j] = 0
                    self._empty.append([i,j])


    def _is_agent_happy(self, x, y):
        # number of all neighbours
        [all, the_same] = [0, 0]

        if self._people_array[self._next[x]][y] != 0:
            all += 1
            if self._people_array[self._next[x]][y].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[x][self._next[y]] != 0:
            all += 1
            if self._people_array[x][self._next[y]].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[x][self._previous[y]] != 0:
            all += 1
            if self._people_array[x][self._previous[y]].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[self._previous[x]][y] != 0:
            all += 1
            if self._people_array[self._previous[x]][y].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[self._previous[x]][self._previous[y]] != 0:
            all += 1
            if self._people_array[self._previous[x]][self._previous[y]].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[self._next[x]][self._previous[y]] != 0:
            all += 1
            if self._people_array[self._next[x]][self._previous[y]].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[self._next[x]][self._next[y]] != 0:
            all += 1
            if self._people_array[self._next[x]][self._next[y]].type == self._people_array[x][y].type:
                the_same += 1
        if self._people_array[self._previous[x]][self._next[y]] != 0:
            all += 1
            if self._people_array[self._previous[x]][self._next[y]].type == self._people_array[x][y].type:
                the_same += 1

        # agent is unhappy / happy
        if all!= 0:
            return False if the_same/all < self._happiness_threshold else True
        return False


    def simulation(self):
        self._initial_configuration()
        iter = 0
        while iter < self._trials:
            for i in range(self._size):
                for j in range(self._size):
                    if self._people_array[i][j] != 0:
                        if self._is_agent_happy(i,j) == False:
                            _ = random.choice(self._empty)
                            self._empty.remove(_)
                            self._people_array[_[0]][_[1]] = Person()
                            self._people_array[_[0]][_[1]].type = self._people_array[i][j].type
                            self._people_array[i][j] = 0
                            self._empty.append([i,j])
            if iter%100 == 0: print(f'trial: {iter}')
            iter+=1


    # plot of the current state
    def plot(self, tekst):
        # grid to plot of results
        plotGrid = np.zeros((self._size, self._size))
        # black, white and gray
        colors = ['#969792','#FFFFFF','#000000']
        cmap = {0: '#FFFFFF', 1:'#000000', -1:'#969792'}
        labels = {0:'empty', 1:'A type', -1:'B type', }
        patches = [mpatches.Patch(color=cmap[i],label=labels[i]) for i in cmap]
        tmp = mpl.colors.ListedColormap(colors)

        for i in range(self._size):
            for j in range(self._size):
                if self._people_array[i][j] != 0:
                    plotGrid[i][j] = self._people_array[i][j].type

        plt.imshow(plotGrid, cmap=tmp)
        plt.legend(handles=patches,shadow=True, facecolor='#6A6175',
                    bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(tekst)
        plt.close()


    ############################################################################
    # GETTERS & SETTERS & DELETERS                                             #
    ############################################################################

    @property
    def happiness_threshold(self):
        return self._happiness_threshold

    @happiness_threshold.setter
    def happiness_threshold(self, value):
        if(value < 0 or value > 1):
            raise ValueError("Value Range Error")
        self._happiness_threshold = value

    @happiness_threshold.deleter
    def happiness_threshold(self):
        del self._happiness_threshold
    ############################################################################


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if(value < 0):
            raise ValueError("Value Range Error")
        self._size = value
        # table of nearest neighbours, with boundary conditions
        self._next = [i+1 for i in range(self._size-1)]
        self._next.append(0)
        self._previous = [self._size-1]
        for i in range(1, self._size):
            self._previous.append(i-1)

    @size.deleter
    def size(self):
        del self._size
        del self._people_array
        del self._next
        del self._previous
    ############################################################################


    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        if(value < 0 or value >= 100):
            raise ValueError("Value Range Error")
        self._density = value

    @density.deleter
    def density(self):
        del self._density
    ############################################################################


    @property
    def trials(self):
        return self._trials

    @trials.setter
    def trials(self, value):
        if(value < 0):
            raise ValueError("Value Range Error")
        self._trials = value

    @trials.deleter
    def trials(self):
        del self._trials
    ############################################################################
