# imports
IMPORT_MATH = "import math"


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
