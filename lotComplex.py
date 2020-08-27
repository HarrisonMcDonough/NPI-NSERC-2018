from cwComplexes import *

class LOTEdge:
    def __init__(self, source, dest, label):
        self.source = source
        self.dest = dest
        self.label = label


def lotComplex(onecell_list, edge_list):
    """Makes a LOT into a complex"""
    twocell_list = []

    count = 0
    for e in edge_list:
       twocell_list.append(TwoCell([(e.source, False), (e.label,False), (e.dest, True), (e.label, True)], count))
       count += 1
    #adds a two cell for each needed conjugation, inherited from edges in the LOT

    w = onecell_list[0].initZeroCell #acquiring the zero-cell
    return Complexes([w], onecell_list, twocell_list)		
