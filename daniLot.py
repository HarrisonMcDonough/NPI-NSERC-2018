from lotComplex import *

def dani_lot():
    """ Dani's LOT example from the office"""
    z = ZeroCell('')
    o = {}
    
    for l in ['a','b','c','d','e']:
        o[l] = OneCell(z,z,l)
    
    edge_list = [
        LOTEdge(o['a'], o['b'], o['e']),
        LOTEdge(o['b'], o['c'], o['a']),
        LOTEdge(o['c'], o['d'], o['a']),
        LOTEdge(o['c'], o['e'], o['d'])
        ]
    
    return lotComplex(list(o.values()), edge_list)
