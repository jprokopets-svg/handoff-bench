from atoi_clone import *


assert my_atoi('42') == 42

assert my_atoi('   -42') == -42

assert my_atoi('4193 with words') == 4193

assert my_atoi('words and 987') == 0

assert my_atoi('-91283472332') == -2147483648

assert my_atoi('+1') == 1

assert my_atoi('') == 0

assert my_atoi('3.14') == 3