import datetime
import random

pn = 10     # 対象文字数
fn = 2      # 欠損文字数
count = 0   # 繰り返し回数
limit = 3   # 上限

def makelis():
    lis = []
    while True:
        if pn <= len(lis):
            break        
        num = random.randint(65, 90)
        if num not in lis:
            lis.append(num)
    plis = [chr(x) for x in sorted(lis)]    # 対象文字
    flis = []                               # 欠損文字
    for _ in range(fn):
        flis.append(chr(lis.pop()))
    flis.sort()
    qlis = [chr(x) for x in lis]            # 表示文字
    return [plis, flis, qlis]

def que():
    global count
    while True:
        # 回数上限チェック
        if limit-1 < count:
            print("gameover")
            break        
        # 問題表示
        question_list = makelis()
        text_list = ["対象文字", "欠損文字", "表示文字"]
        text_index = [0, 2]                 # 表示指定
        # text_index = [0, 1, 2]            # デバック用
        for i in text_index:
            print(f"{text_list[i]}\n" + " ".join(question_list[i]))
        check = kaito("\n欠損文字はいくつあるでしょうか?: ", [str(fn)]) 
        # 判定
        if not check:
            print(f"不正解です。\n"+"-"*10)
            count += 1
            continue
        else:
            print("正解です。それでは、具体的に欠損文字を1つずつ入力してください")
            for i in range(fn):
                check = kaito(f"{i+1}つ目の文字を入力してください: ", question_list[1])
                if not check:
                    print(f"不正解です。\n"+"-"*10)
                    count += 1
                    break
                else:
                    question_list[1].remove(check)
            else:
                print("パーフェクト！")
                break
            continue            

def kaito(text, ans):
    # 入力した文字がans内にあるならcheckに代入して返す
    # なければNone
    check = None
    ip = input(text)
    if ip in ans:
        check = ip
    return check

if __name__ == "__main__":
    st = datetime.datetime.now()
    que()
    ed = datetime.datetime.now()
    print(f"所要時間: {(ed-st).seconds}s")