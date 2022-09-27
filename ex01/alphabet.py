import datetime
import random

pn = 10     # 対象文字数
fn = 2      # 欠損文字数
count = 0   # 繰り返し回数

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
        origin = makelis()
        plis = [chr(x) for x in sorted(origin)] # 対象文字
        flis = []                               # 欠損文字
        for _ in range(fn):
            flis.append(chr(origin.pop()))
        flis.sort()
        qlis = [chr(x) for x in origin]         # 表示文字
        
        print("対象文字")
        print(" ".join(plis))
        print("欠損文字")
        print(" ".join(flis))
        print("表示文字")
        print(" ".join(qlis))
        check = kaito("欠損文字はいくつあるでしょうか?: ", [str(fn)])
        if not check:
            print("不正解です。\n")
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
                print("正解です")
                break
            continue

            

def kaito(text, ans):
    check = None
    ip = input(text)
    if ip in ans:
        check = ip
    return check

que()