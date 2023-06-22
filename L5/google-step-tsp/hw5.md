# HW5 (6/9-)

## 宿題の概要

巡回セールスマン問題(TSP Challenge)に取り組み、より良いスコアを目指す

[サンプルプログラム](https://github.com/hayatoito/google-step-tsp)

[Visualizer](https://hkocinneide.github.io/google-step-tsp/visualizer/build/default/)

## [hw5.py](https://github.com/riho8/STEP/blob/master/L5/google-step-tsp/hw5.py)

### 実行方法

```python
# プログラムを実行し、outputファイルに実行結果を保存する
$ python3 hw5.py input_<number>.csv > output_<number>.py

# サーバーを立てる
$ python3 -m http.server

# 以下のリンクにアクセスする(visualizer)
http://localhost:8000/visualizer/build/default/index.html
```

- 以下のinputファイルが与えられます。
    - input_0.csv (N = 5)
    - input_1.csv (N = 8)
    - input_2.csv (N = 16)
    - input_3.csv (N = 64)
    - input_4.csv (N = 128)
    - input_5.csv (N = 512)
    - input_6.csv (N = 2048)

## アルゴリズムと性能

以下の手法で取り組みました

1. 初期経路： greedy ( Nearest Neighbor)
2. 最適化：2-opt
3. ランダムにスタート位置を選択し、１と２で巡回路を生成し、その改善結果を記録するループを1000回繰り返す

### 性能比較

Best Score (avg)

|  | 0(N=5)  | 1(N=8) | 2(N=16) | 3(N=64) | 4(N=128) | 5(N=512) | 6(N = 2048) | Time complexity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| greedy | 3418.10 | 3832.29 | 5449.44 | 10519.16 | 12684.06 | 25331.84 | 49892.05 | O(N^2) |
| greedy + random starting point | 3418.10(3454.76) | 3832.29(4070.20) | 5065.58(5395.53) | 9276.22(10195.79) | 12084.32(12861.08) | 24191.6(25370.32) | 47822.41(49254.40) | O(N^2) |
| greedy + random starting point + 2-opt | 3291.62(3294.45) | 3778.72(3826.08) | 4494.42(4688.51) | 8309.83(9457.11) | 11606.27(12459.70) | 23697.62(25169.01) | 47811.95(49222.20) | O(N^2) |

<details>
<summary>詳細</summary>
    
    ### Greedy (greedy.py)
    
     0.  N = 5
    
        Result: 3418.1015991327063
    
    1. N = 8
        
        Result: 3832.2900939051947
        
    2. N = 16
        
        Result: 5449.435265220031
        
    3. N = 64
        
        Result: 10519.161145182472
        
    4. N = 128
        
        Result: 12684.059709833355
        
    5. N = 512
        
        Result: 25331.843307461648
        
    6. N = 2048
        
        Result: 49892.04939109294                                            
        
    
    ### Greedy + random starting point (greedy_random.py)
    
     0.  N = 5
    
        Average: 3454.757470828727
        Minimum: 3418.101599132713
        Maximum: 3518.528644875367
        Variance: 2337.587973759326
    
    1. N = 8
        
        Average: 4070.1972903499336
        Minimum: 3832.2900939051992
        Maximum: 4442.4080877369815
        Variance: 64262.649705978394
        
    2. N = 16
        
        Average: 5395.526137446038
        Minimum: 5065.575697525618
        Maximum: 5843.912855673055
        Variance: 40404.49005109236
        
    3. N = 64
        
        Average: 10195.797389853196
        Minimum: 9276.223768646349
        Maximum: 10831.085625290953
        Variance: 99601.02518983722
        
    4. N = 128
        
        Average: 12861.089106537394
        Minimum: 12084.319160687255
        Maximum: 13576.631405093052
        Variance: 83430.40572205061
        
    5. N = 512
        
        Average: 25370.32499412909
        Minimum: 24191.66096571249
        Maximum: 26765.98705946139
        Variance: 209940.73207004738
        
    6. N = 2048
        
        Average: 49254.397915139656
        Minimum: 47822.4134457014
        Maximum: 51408.67576718584
        Variance: 637420.8454696051
        
    
    ### Greedy + Random starting point +  2-opt (hw5.py)
    
    0.  N = 5
    
        Average: 3394.449861998392
        Minimum: 3291.6217214092458
        Maximum: 3418.101599132713
        Variance: 2432.0641512229304
        
    1. N = 8
        
        Average: 3826.0754313253774
        Minimum: 3778.7154164925378
        Maximum: 3832.2900939051997
        Variance: 294.32651196337963
        
    2. N = 16
        
        Average: 4688.510704416578
        Minimum: 4494.417962262893
        Maximum: 5160.837042299939
        Variance: 50338.672335484305
        
    3. N = 64
        
        Average: 9457.107004635409
        Minimum: 8309.832811152788
        Maximum: 10316.485353002585
        Variance: 95823.09048850952
        
    4. N = 128
        
        Average: 12459.695949359744
        Minimum: 11606.270255881205
        Maximum: 13272.492174238972
        Variance: 83812.15021479875
        
    5. N = 512
        
        Average: 25169.00956865462
        Minimum: 23697.615642377044
        Maximum: 26692.31095570941
        Variance: 232390.18490404254
        
    6. N = 2048
        
        Average: 49222.19565405332
        Minimum: 47811.94786520657
        Maximum: 51413.31162162608
        Variance: 621697.6953752141

</details>        

<br>

### main()

1. スタート位置をランダムに決める。
2. greedy()で初期経路を決める。
3. 2の経路をtwo_opt()で改良する。
4. 1~3を1000回繰り返し、一番良いスコアとルートを記録する

### greedy()

1. 現在位置から一番近い点へ移動していく

### two_opt()

1. ランダムに2つのインデックスを取得し、辺を繋ぎ変えるか判断する。
2. １を1000回繰り返す

### 考察

- Nが大きくなるとgreedy + random starting point + 2-opt と　greedy + random starting point　のBest Scoreの差がほぼ無くなる。
    - two_optの動きの確認と改良
- 現在のコードでは1000回のループが二つあり、Nが大きくなると1ループあたりの時間が長くなり全体として時間がかかってしまうので、ほかのアルゴリズムを組み合わせる方法を何個か試す
    - 焼きなまし法
    - 反復局所探索法