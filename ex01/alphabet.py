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
    return lis

def que():
    global count
    while True:
        # 回数上限チェック
        if limit < count:
            print("gameover")
            break
        
        # 問題生成
        origin = makelis()
        plis = [chr(x) for x in sorted(origin)] # 対象文字
        flis = []                               # 欠損文字
        for _ in range(fn):
            flis.append(chr(origin.pop()))
        flis.sort()
        qlis = [chr(x) for x in origin]         # 表示文字

        # 問題表示
        text_list = [["対象文字", plis], ["欠損文字", flis], ["表示文字", qlis]]
        text_index = [0, 2]         # 表示指定
        # text_index = [0, 1, 2]    # デバック用
        for i in text_index:
            print(f"{text_list[i][0]}\n" + " ".join(text_list[i][1]))
        check = kaito("\n欠損文字はいくつあるでしょうか?: ", [str(fn)]) 

        # 判定
        if not check:
            print(f"不正解です。\n"+"-"*10)
            count += 1
            continue
        else:
            print("正解です。それでは、具体的に欠損文字を1つずつ入力してください")
            for i in range(fn):
                check = kaito(f"{i+1}つ目の文字を入力してください: ", flis)
                if not check:
                    print(f"不正解です。\n"+"-"*10)
                    count += 1
                    break
                else:
                    flis.remove(check)
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