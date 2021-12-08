# imports
IMPORT_MATH = "import math"
IMPORT_COMBINATIONS = "from itertools import combinations"


# local functions
IMPORT_NUM_PERMUTATIONS = "from utils.combinatorics import num_permutations"
IMPORT_COUNT_DIGIT = "from utils.combinatorics import count_digit"
IMPORT_FILTER_SUM = "from utils.combinatorics import filter_sum"


# lambda functions
IMPORT_NTH_SMALLEST = "nth_smallest = lambda l, i: sorted(l)[i-1]"
IMPORT_NTH_LARGEST = "nth_largest = lambda l, i: sorted(l, reverse=True)[i-1]"


# answer generation
ANSWER_ROUND_ZERO = "if answer - math.floor(answer) < 0.5:\n"\
                    "\tanswer = math.floor(answer)\n"\
                    "else:\n"\
                    "\tanswer = math.ceil(answer)"
ANSWER_ROUND_TWO = "answer = answer * 100\n"\
                   "if answer - math.floor(answer) < 0.5:\n"\
                   "\tanswer = math.floor(answer) / 100\n"\
                   "else:\n"\
                   "\tanswer = math.ceil(answer) / 100"
ANSWER_CHECK_CODE = "try:\n" \
                    "\tint(answer)\n" \
                    "\tif answer == int(answer):\n" \
                    "\t\tprint(0)\n" \
                    "\telse:\n" \
                    "\t\tprint(1)\n" \
                    "except:\n" \
                    "\tprint(2)\n"
