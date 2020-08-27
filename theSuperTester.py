from cwComplexes import *

def presComplexBuilder(pres_str):
    # Builds a presentation complex from a string description
    # The generators and the relators must be separated by a pipe,
    # generators and relators must be separated by commas,
    # and the different letters of a generator must be separated by a space

    (generator_str, relator_str) = pres_str.split("|", 2)
    generator_list = [s.strip(" ") for s in generator_str.split(",")] 
    relator_list = [s.strip(" ") for s in relator_str.split(",")] 

    z = ZeroCell("")
    onecell_dict = {}
    twocell_list = []

    for g in generator_list:
        onecell_dict[g] = OneCell(z, z, g)

    relator_count = 0
    for r in relator_list:
        if r=="":
            continue
        token_list = r.split(" ")
        boundary_map = []
        for t in token_list:
            t = t.strip(" ")
            inverse = False
            if (t[-1] == "'"):
                inverse = True
            generator = t.strip("'") #removes the apostrophe if necessary	
            if generator in onecell_dict:
                boundary_map.append((onecell_dict[generator], inverse))
            else:
                raise AttributeError('invalid generator in a relator')

        twocell_list.append(TwoCell(boundary_map, relator_count))
        relator_count += 1
    return Complexes([z], list(onecell_dict.values()), twocell_list)