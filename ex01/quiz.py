import datetime
import random

def syutudai():
    num = random.randint(0, 2)
    que = ["サザエの旦那の名前は?", "カツオの妹の名前は?", "タラオはカツオから見てどんな関係？"]
    ans = [["マスオ", "ますお"], ["ワカメ", "わかめ"], ["甥", "おい", "甥っ子", "おいっこ"]]
    print(f"問題: {que[num]}")
    kaito(ans[num])

def kaito(ans):
    if input() in ans:
        print("正解!")
    else:
        print("不正解")

if __name__ == "__main__":
    st = datetime.datetime.now()
    syutudai()
    ed = datetime.datetime.now()
    print(f"所要時間: {(ed-st).seconds}s")

# st = datetime.datetime.now()
# que = ["サザエの旦那の名前は?", "カツオの妹の名前は?", "タラオはカツオから見てどんな関係？"]
# ans = [["マスオ", "ますお"], ["ワカメ", "わかめ"], ["甥", "おい", "甥っ子", "おいっこ"]]
# num = round(random.random() * 3)

# print(que[num])
# if input() in ans[num]:
#     print("正解!")
# else:
#     print("不正解")

# ed = datetime.datetime.now()
# print(f"所要時間: {(ed-st).seconds}s")