# QMWP: Qanda Math Word Problem Dataset Python

This dataset code generates mathematical question, python-code solution and answer pairs for different types of math word problems in Korean.

## Examples

```
# Arithmetic
Question: 지우개가 가방에 66개 들어있습니다. 유주가 38개 꺼내었습니다. 가방 안에 있는 지우개는 몇 개입니까?
Code: n0 = 66\nn1 = 38\nanswer = n0 - n1
Answer: 28

# Combination
Question: 1, 5, 3, 6, 0 중에서 3개
를 뽑아 한 번씩 사용하여 세 자리 수를 만들려고 합니다. 만들 수 있는 수 중에서 백의 자리 숫자가 6 인 가장 큰 수를 쓰시오.
Code: n0 = 1\nn1 = 5\nn2 = 3\nn3 = 6\nn4 = 0\nn5 = 3\nn6 = 1\nn7 = 3\nn8 = 100\nn9 = 6\nl0 = [1, 5, 3, 6, 0]\nnum_permutations(l0, n5)\nt0 = list(filter(lambda x: str(x)[-3] == str(n9), result))\nanswer = max(t0)
Answer: 653

# Comparison
Question: 소율이는 73과 45와 16과 2를 모았고, 지원이는 96을 모았습니다. 누가 모은 수가 더 작은가?
Code: n0 = 73\nn1 = 45\nn2 = 16\nn3 = 2\nn4 = 96\nt0 = dict()\nt0['소율'] = sum([n0, n1, n2, n3])\nt0['지원'] = sum([n4])\nanswer = min(t0, key=t0.get)
Answer: 지원

# Figure
Question: 길이가 784m인 철사로 직사각형을 만들었더니 철사가 남지도 모자라지도 않았고 직사각형의 세로 길이가 281m일 때, 가로 길이는 몇 m인지 알아보아라.
Code: n0 = 784\nn1 = 4\nn2 = 4\nn3 = 281\nt0 = n0 / 2\nanswer = t0 - n3
Answer: 111

# Number
Question: 어떤 수에 90을 뺀 결과에 240을 곱하면 8775일 때, 어떤 수의 값을 구하시오.
Code: n0 = 90\nn1 = 240\nn2 = 8775\nt0 = n2 / n1\nanswer = t0 + n0
Answer: 127

# Ordering
Question: 학생들이 한 줄로 서 있습니다. 아름이는 맨 뒤에 서 있습니다. 예찬이는 앞에서 14번째에 서 있습니다. 아름이와 예찬이 사이에 1명이 서 있을 때, 줄을 서 있는 학생은 모두 몇 명인지 구하여라.
Code: n0 = 14\nn1 = 1\nanswer = n0 + n1 + 1
Answer: 16
```

## How to Use

### Install Requirements

`pip install -r requirements.txt`

### Generate

in Python Console
```
from main import generate
# generate
data = generate(1000)

# to file
from main import generate_to_file
generate_to_file("filename.json", 1000)
```
