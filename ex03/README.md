# 第 3 回

## 迷路ゲーム(ex03/maze.py)

### ゲーム概要

- 迷路に沿ってこうかとんを移動させるゲーム。
- ex03/maze.py を実行すると、1500×900 のウィンドウとメッセージボックスが立ち上がる。
- ok ボタンを押すとゲームスタート。
- 初期状態として周囲 3×3 のブロック範囲しか表示されません。
  - 移動することで表示範囲を広げることができます。
- 実行するたびに迷路は変わります。
- スタート位置は左上固定、但しゴールは右上、右下ランダムに変わります。
- クリアするとメッセージボックスが表示され、ok ボタンを押すと終了します。

### 操作方法

- 矢印キー又は WASD キーでこうかとんを上下左右に移動する

### 追加機能

- 操作方法に WASD キーを追加
- スタート、ゴールの追加
- ゴールにメッセージボックス(ゲーム終了機能)を追加
- タイマーを追加
- こうかとんの周囲 3 ブロック以外は非表示にする機能
  - 一度表示された場所は表示されたまま

### 備考

- main 関数内で tkm.showinfo を動かすとメインのゲームが動かなくなる。
- threading で対処できる(並列処理)
