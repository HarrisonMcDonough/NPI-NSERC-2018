from cwComplexes import *
from presComplexBuilder import *
from maybeBacktrackTwoPointZero import *

str = "1, 2, 3, 4, 5 | 2' 1' 1' 1' 1' 3 1 2'"
c = prescomplex_builder(str)

b = backTrackSearch(c)
print(c, b)

