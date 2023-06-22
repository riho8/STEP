# HW6 (6/16-)

## 宿題の概要

循環セールスマン問題に取り組み、より良いスコアを目指す

[サンプルプログラム](https://github.com/hayatoito/google-step-tsp)

[Visualizer](https://hkocinneide.github.io/google-step-tsp/visualizer/build/default/)

hw5-> [README](https://github.com/riho8/STEP/blob/master/L5/google-step-tsp/hw5.md) [hw5.py](https://github.com/riho8/STEP/blob/master/L5/google-step-tsp/hw5.py)

## [hw6.py](https://github.com/riho8/STEP/blob/master/L5/google-step-tsp/hw6.py)

### 実行方法

```python
# プログラムを実行し、outputファイルに実行結果を保存する
$ python3 hw6.py input_<number>.csv > output_<number>.py

# サーバーを立てる
$ python3 -m http.server

# 以下のリンクにアクセスする(visualizer)
http://localhost:8000/visualizer/build/default/index.html
```

- 以下のinputファイルが与えられます。
    - input_6.csv (N = 2048)
    - input_7.csv (N = 8192)
- 対応するoutputファイルに結果を保存します。

### 手法と性能

以下の手法で取り組みました

1. 初期経路： greedy (Nearest Neighbor)
2. 最適化：2-opt
3. 計算時間短縮 : 座標を4エリアに分割する

前回からの変更点

- 2-optの修正
- 座標を4分割して、それぞれの最適ルートを繋げる方法に変更

Best Score (avg)

|  | 6(N = 2048) | 7(N =8192) |
| --- | --- | --- |
| score | 43244.34 | 85371.16 |
| time | 1.67s | 45.48s |

### main()

1. csvファイルからそれぞれの点の座標(x,y)を持つリストcitiesを作る
2. get_tour_by_area()にcitiesを渡して経路を得る
3. 経路を出力する

### get_tour_by_area()

1. divide_cities()でそれぞれの点を右上、右下、左上、左下の4エリアに分割したsubcitiesを得る
    - subcities = [[TopLeft],[TopRight],[BottomRight],[BottomLeft]]
    - スタート位置をそのエリアの中で一番中心に近い点とする
2. それぞれのエリアに関して、solve()で最適解を得る
3. 最適解を繋げて一つの経路にする

### divide_cities()

1. x座標のリストとy座標のリストから、x軸(xの中心）とy軸(yの中心）を得る
2. x軸とy軸で分割された4つのエリアにそれぞれ含まれる点を新しいリストに入れていく

### solve()

1. それぞれの点の間の距離をdistに保存する
2. greedy()で初期経路を作成する
3. two_opt()で改良する

### greedy():

1. 現在位置から一番近い点へ移動していく

### two_opt()

1. 解が改善されなくなるまで以下を繰り返す
    1. スタート位置を固定するためindex = 0を除いた辺について、交換したときの距離が交換しなかった場合より短かった場合、辺を交換する。それ以外の場合何もしない。

### 考察/反省

- 試したこと
    - 4分割せず、四隅からスタートするプログラム(greey+2-opt)をC言語で書く
        - Cでも two_optの2重ループでかなり時間がかかったため、断念した
    - 4分割をさらに4分割して16エリア作る
        - それぞれのエリアをつなぐところで距離が間延びしてしまった。
        - 4分割のなかの4分割でも、それぞれのエリアのスタート位置が中心に一番近い点になるようにしていたため、そのスタート位置を変えたら距離を短縮できそう
- 計算時間短縮という面で、4分割をして良かった。ただ計算時間短縮に時間をかけすぎて肝心のスコアを伸ばすところに力を入れられなかった。
- or-optや2-opt近傍を組み合わせたり、この記事の2-opt ILSを試してみたい
    - [https://future-architect.github.io/articles/20211201a](https://future-architect.github.io/articles/20211201a/#Double-Bridge)

## Reference

[https://en.wikipedia.org/wiki/2-opt](https://en.wikipedia.org/wiki/2-opt)

[https://qiita.com/flowerrr__lily/items/6679f9496d0079fa0dd2](https://qiita.com/flowerrr__lily/items/6679f9496d0079fa0dd2)

[https://towardsdatascience.com/around-the-world-in-90-414-kilometers-ce84c03b8552](https://towardsdatascience.com/around-the-world-in-90-414-kilometers-ce84c03b8552)