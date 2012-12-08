from remote import RemoteDriver
from bulbs import Bulbs
import random
import time
import colorsys
import sys
import math

sleep_time = .3

colors = [(15, 0, 0), \
            (15, 3, 0), \
            (15, 15, 0), \
            (0,   15,   0), \
            (0,   0, 15), \
            (4,  14, 13), \
            (14, 0, 14) ]

class MergeSort(object):
    def __init__(self, bulbs, driver):
        self.driver = driver
        self.bulbs = bulbs
        self.lights = [(0,0,0,0)]*100
        self.mylist = []
        for i in range(50):
            (r, g, b) = colors[random.randint(0, len(colors)-1)]
            self.lights[i+25] = (r, g, b, 200)
            self.mylist.append((r,g,b,200))

    def freq(self, color):
        r, g, b, a = color
        return colorsys.rgb_to_hsv(r/15.0, g/15.0, b/15.0)[0]

    # lol = list of lists
    def display_lol(self, lol, sleep = sleep_time, test_print = False):
        offInterval = 50 / (len(lol) + 1)
        listWritten = 0
        i = 0
        roundNum = 0
        listWritten = 0
        print "length of lol: ", len(lol)
        while roundNum < len(lol) or i < 100:
            counter = 0
            while i < 100 and counter < offInterval:
                self.lights[i] = (0, 0, 0, 0)
                counter += 1
                i += 1
            if roundNum < len(lol):
                for element in lol[roundNum]:
                    print i, roundNum, len(lol)
                    self.lights[i] = element
                    i += 1
                    listWritten += 1
                roundNum += 1
            
        if listWritten != 50:
            print "error"
            print listWritten
        self.driver.write_led(100, 0, 0, 0, 0)
        self.render()
        if test_print:
            print self.lights
        time.sleep(sleep)

        # This can represent end goal
        return self.lights

    
    def render(self):
        for i in range(100):
            self.bulbs.set(i, self.lights[i])
        #print self.bulbs.frame
        r = random.randint(0,2)
        if r == 0:
            self.bulbs.render(True)
        else:
            self.bulbs.render()
            

    # Recursive merge sort
    # def sort(self, sub, leftMostPosition, bins):
    #     if len(sub) <= 1:
    #         # List is sorted
    #         return sub
        
    #     # Must continue sorting
    #     middle = len(sub) / 2
    #     left = []
    #     right = []
    #     for i in range(len(sub)):
    #         if i < middle:
    #             left.append(sub[i])
    #         else:
    #             right.append(sub[i])
        
        
    #     left = self.sort(left, leftMostPosition, bins * 2)
    #     #self.display_list(bins)
    #     #print bins
    #     right = self.sort(right, middle, bins * 2)
        
    #     mergedList = self.merge(left, right, leftMostPosition)
    #     #self.partialSortMyList(mergedList, leftMostPosition)
    #     self.display_list(bins)
    #     print bins
    #     self.check_list(mergedList)
    #     return mergedList

    def breakdown_list(self, l, storage, level):
        lol = []
        if len(l) <= 1:
            return [l]
        middle = len(l) / 2
        left = l[:middle]
        right = l[middle:]
        storage[level].append(left)
        storage[level].append(right)
        lol.extend(self.breakdown_list(left, storage, level+1))
        lol.extend(self.breakdown_list(right, storage, level+1))

        return lol
        
    def breakdown_list2(self, l):
        middle = len(l) / 2
        left = l[:middle]
        right = l[middle:]
        for i in range(6):
            l.append(left)
            l.append(right)

    def iter_sort(self):
        #working list of lists
        storage = [[],[],[],[],[],[]] 
        wlol = self.breakdown_list(self.mylist, storage, 0)
        print "storage", storage[5]

        for s in storage:
            self.display_lol(s)

        lollen = 1
        while lollen <= len(self.mylist):
            new_wlol = []
            i = 0
            while i < len(wlol)-1:
                new_wlol.append(self.merge(wlol[i], wlol[i+1], 0))
                i += 2
            #odd number of merges
            if i == len(wlol)-1:
                new_wlol.append(wlol[i])

            if new_wlol:
                # new working list of lists is instantiated on each iteration
                wlol = new_wlol

            lollen *= 2
            self.display_lol(wlol)

        print "wlol", wlol
        print "lollen", lollen
        self.check_list(wlol[0])
        return wlol

    def check_list(self, someList):
        if len(someList) < 2:
            return True
        for i in range(len(someList)-1):
            if self.freq(someList[i]) > self.freq(someList[i+1]):
                print someList
                for i in someList:
                    print i, self.freq(i)
                sys.exit(1)

    def partialSortMyList(self, mergedList, leftMostPosition):
        for i in range(len(mergedList)):
            self.mylist[i+leftMostPosition] = mergedList[i]
        
    def merge(self, left, right, leftMostPosition):
        totalLength = len(left) + len(right)
        lPtr = 0
        rPtr = 0
        mergedList = []
        for i in range(totalLength):
            if lPtr >= len(left):
                mergedList.append(right[rPtr])
                rPtr += 1
            elif rPtr >= len(right):
                mergedList.append(left[lPtr])
                lPtr += 1

            elif self.freq(left[lPtr]) <= self.freq(right[rPtr]):
                mergedList.append(left[lPtr])
                lPtr += 1
            else:
                mergedList.append(right[rPtr])
                rPtr += 1

        return mergedList

if __name__=="__main__":    
    d = RemoteDriver("MergeSort")
    print 'our turn!'

    # init
    b = Bulbs(d)
    merger = MergeSort(b, d)
    #for i in range(49):
    #    merger.display_list(i+1)
    #merger.mylist = merger.sort(merger.mylist, 0, 1)
    finalList = merger.iter_sort()
    #merger.check_list(finalList)
    merger.display_lol(finalList, .4, True)
    #print merger.mylist

    d.busy_wait()
