

from sort import Sort
from bulbs import Bulbs
from remote import RemoteDriver
import time

class QuickSort(Sort):
    def __init__(self, bulbs):
        super(QuickSort, self).__init__(bulbs)

    def dim_light(self, idx):
        (r, g, b, a) = self.lights[idx]
        self.lights[idx] = (r, g, b, 20)
    
    def brighten_light(self, idx):
        (r, g, b, a) = self.lights[idx]
        self.lights[idx] = (r, g, b, 200)

    # From Wikipedia's pseudo code of an in-place quicksort
    def partition(self, left, right, pivot_idx): 
        pivot_value = self.lights[pivot_idx]
        self.swap(pivot_idx, right)
        if pivot_idx != right:
            self.render()
        tmp_idx = left
        for i in range(left, right):
            # flash compare
            self.dim_light(i)
            self.dim_light(right)
            self.render()
            time.sleep(0.05)
            
            self.brighten_light(i)
            self.brighten_light(right)
            
            if self.freq(self.lights[i]) < self.freq(pivot_value):
                self.swap(i, tmp_idx)
                if i != tmp_idx:
                    self.render()
                    time.sleep(0.05)
                tmp_idx += 1

        self.swap(tmp_idx, right)
        if tmp_idx != right:
            self.render()
            time.sleep(0.05)

        return tmp_idx 
    
    def quicksort(self, left, right):
        if left < right:
            pivot_idx = (left + right)/2     # play with different pivot selection
            pivot_new_idx = self.partition(left, right, pivot_idx)
            self.quicksort(left, pivot_new_idx - 1)
            self.quicksort(pivot_new_idx + 1, right)

    def sort(self):
        self.quicksort(0, 99)
        

if __name__=="__main__":
    print 'waiting...'
    d = RemoteDriver("QuickSort")
    print 'our turn'
    
    sorter = QuickSort(Bulbs(d))
    sorter.sort()
    
    # Leave the sorted list up
    d.busy_wait()
    
    
