import konlpy
from konlpy.tag import Kkma, Komoran, Okt, Hannanum

okt = Okt()
text = '코드잇에 오신 걸 환영합니다'

print(okt.nouns(text))
