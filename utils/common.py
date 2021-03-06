import string
from pathlib import Path

PEOPLE_NAMES = list(set([i.rstrip() for i in open(Path(__file__).parent / "names.txt").readlines()]))
ANIMAL_NAMES = ['토끼', '개', '고양이', '강아지', '염소', '사슴', '사자', '호랑이', '얼룩말', '쥐',
                '뱀', '소', '원숭이', '닭', '돼지', '거북이', '말']
CONTAINERS = ['상자', '컵', '박스', '봉투', '가방', '통']
OBJECTS = ['공', '탁구공', '야구공', '종이컵', '초콜릿', '사탕', '캔디', '구슬', '지우개', '연필', '인형', '장난감',
           '공책', '펜', '색종이', '풀', '테이프', '색연필', '축구공', '사과', '배', '감', '빵', '끈', '리본',
           '참외', '수박', '메론', '귤', '포도', '농구공', '젓가락', '숟가락', '수저', '포크']
SUBJECTS = ['국어', '영어', '수학', '사회', '과학', '일본어', '독일어', '불어']
UNITS = ['개', '자루', '벌', '단', '채', '개비', '그루', '마리', '푼', '송이', '권', '명', '장', '척', '통', '병', '잔', '층', '쪽']
GANADAS = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
KR_NUMS = ['한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열']
DRINKS = ['물', '주스', '오렌지주스', '포도주스', '사과주스', '음료수', '차', '마테차', '매실차', '탄산음료', '콜라',
          '사이다', '닥터페퍼', '녹차', '루이보스티', '커피', '아메리카노', '블랙티', '라떼', '프라푸치노']
NUMBERS = '0123456789'
COLORS = ["빨간색", "파란색", "검은색", "흰색", "주황색", "노란색", "초록색", "보라색", "분홍색", "남색", "녹색", "청색", "핑크색"]
FAMILY_OBJ_DICT = {
    '과일': ['사과', '배', '감', '참외', '수박', '포도', '감', '메론', '딸기', '바나나', '귤', '키위'],
    '과목': ['국어', '영어', '수학', '과학', '사회', '도덕', '체육', '역사', '기술', '지리'],
    '동물': ANIMAL_NAMES,
}
VARIABLES = string.ascii_uppercase
NEWLINE = '\n'
ALPHABETS_FOR_PARTICLE = "LMNRlmnr"
SPACE4 = "    "
