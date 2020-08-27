from cwComplexes import *
from presComplexBuilder import *
from newMaybeBacktrackTwoPointZero import *

str = "a, b, c | a b a b' a b"
c = prescomplex_builder(str)

b = backTrackSearch(c)
print(c, b)

