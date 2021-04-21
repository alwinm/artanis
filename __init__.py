import pylab as p
import numpy as n

def make_cdict1(children,parents):
    c_dict = {}
    # sort by parents so can loop through set 
    order = n.argsort(parents)
    uparents = n.unique(parents)
    indices = n.searchsorted(parents[order],uparents)
    for i in range(len(indices)-1):
        c_dict[uparents[i]] = children[indices[i]:indices[i+1]]
    return c_dict

def make_cdict2(children,parents):
    c_dict = {}
    for i in range(len(children)):
        if parents[i] in c_dict:
            c_dict[parents[i]].append(children[i])
        else:
            c_dict[parents[i]] = [children[i]]
    return c_dict

def process(children,parents,ydata):
    # children: N indices
    # parents: N indices
    # ydata: N floats
    
    # each parent needs to know all its children
    # so that the tree can be expanded in order 
    c_dict = make_cdict1(children,parents)
    counter = [0]    
    x_dict = {}

    # will be x positions of all children
    x_array = n.zeros(len(children))
    xmin_array = []
    xmax_array = []
    hparents = []
    def expand(index):
        if index not in c_dict:
            # index is not a parent
            counter[0] += 1
            xi = 1*counter[0]
        else:
            xs = [expand(child) for child in c_dict[index]]
            xmin_array.append(n.min(xs))
            xmax_array.append(n.max(xs))
            hparents.append(index)
            xi = n.mean(xs)
        x_array[n.searchsorted(children,index)] = xi
        return xi

    # make a call to expand the highest index
    ancestors = set(parents) - set(children)
    # parents that are not themselves children
    for ancestor in ancestors:
        expand(ancestor)

    hparents = n.array(hparents)
    xmin_array = n.array(xmin_array)
    xmax_array = n.array(xmax_array)

    # plot all vertical lines from child level to parent level
    p.vlines(x_array,ydata[children],ydata[parents],colors='k')
    # plot all horizontal lines representing merges (parents)
    p.hlines(ydata[hparents],xmin_array,xmax_array)
    
    
def test():
    children = n.array([0,1,2,3,4 ,5 ,6 ,7 ,8 ,9 ,10,11,12,13,14])
    parents  = n.array([8,8,9,9,10,10,11,11,12,12,13,13,14,14,15])
    ydata    = n.array([1,1,1,1,1,1,1,1,2,2,2,2,4,4,8,8,8,8,8,8,8])
    process(children,parents,ydata)
