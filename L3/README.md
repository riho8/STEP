# HW3 (5/26-)

## 宿題の概要

1. [モジュール化した計算機プログラム](https://github.com/xharaken/step2/blob/master/modularized_calculator.py) を変更して、 * と / に対応する
2. 書いたプログラムをチェックするテストケースをrun_test()に追加する
3. プログラムを変更して、()に対応する

## hw3-1/3-2

### 実行方法

```python
$ python3 hw3-1.py
```

- まず `run_test()`が実行されます。`==Test Started==`　から `== Test Finished==` までの間、テストケースが緑色で`PASS!`と表示されれば成功、赤色で`FAIL!`と表示されたら失敗です。
- 次に入力待ち状態になるので、好きな式を入力すると、答えが返ってきます
    - 注意事項
        - スペースは入れないでください
        - {}や[]は使わないでください
    - 例
        
        ```python
        $> 1*2
        $answer = 2.000000
        ```
        

### 1. * と / のトークン化

- `read_multiply()`と `read_divide()`を追加する
- `tokenize()` に * と / をトークン化する条件分岐を追加する

### 2. read_number()を変更

- 一つ前のtokenにMINUSがあるとき、負の数として処理する。MINUSをPLUSに変える
- 一つ前のtokenにMINUS、二つ前にMULTIPLYかDIVIDEがあれば、負の数に変換してからMINUSを消す

### 3. evaluate_multiply_divide()を追加

- tokens[index]['type'] == 'NUMBER’ のとき、index-1がMULTIPLYかDIVIDEだったら計算して、tokensをアップデートする
- tokens[index]['type'] == 'NUMBER’ のとき、index-1がPLUSかMINUSだったらスキップ

### 4. evaluate()の変更

- 最初に`evaluate_multiply_divide()` を実行してから、`evaluate_plus_minus()`を呼び出し足し算と引き算の計算に移るように変更する。
- ダミーの＋を先頭に入れる処理を、`tokenize()`に移動。

### テストケースの追加

以下のテストケースを用意

- 数字のみ（計算なし）
- 整数のみの計算
- 整数と少数の計算
- 少数のみの計算
- 正の数と負の数の計算
- 負の数のみの計算
- 0を含む計算
- 少数、整数、四則演算を混ぜた計算
- 境界値の計算
    - `sys.maximize`の値を境界値とした

### 工夫した点

- -1など負の数に対応しました
- テストケースが見やすいように色をつけました

## hw3-3

### 実行方法

```python
$ python3 hw3-3.py
```

- （）を含んだテストケースを追加しました

### 1. ( と ) のトークン化

- `read_bracket_open()`と `read_bracket_close()`を追加する
- `tokenize()` に ( と ) をトークン化する条件分岐を追加する

### 2. evaluate_bracket()を追加

- tokensを前から見ていって、BRACKET_OPENがみつかったらそこからBRACKET_CLOSEを探す。OPENからCLOSEの間のtokenで新しいリストを作って、それを`evaluate()`に渡す
    - もしCLOSEを探している間に新しくOPENが見つかったら、OPENのインデックスを更新する
- tokensをアップデート: `evaluate()`の返り値をOPENのインデックスの場所に入れて、その次の要素～CLOSEまでを消す

### 3. evaluate()の変更

- 最初に`evaluate_bracket()` を実行するように変更する。

### 工夫した点

- openのインデックスを更新することで、二重のかっこにも対応した

## hw3-3_stack

### 実行方法

```python
$ python3 hw3-3_stack.py
```

### 1. convert()の追加

- tokensを逆ポーランド記法に変える関数
    - 例：1+2*3 → 1 2 3 + *
        - before [{'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}, {'type': 'MULTIPLY'}, {'type': 'NUMBER', 'number': 3}]
        - after [{'type': 'NUMBER', 'number': 1}, {'type': 'NUMBER', 'number': 2}, {'type': 'NUMBER', 'number': 3}, {'type': 'MULTIPLY'}, {'type': 'PLUS'}]
- tokensを保存していく`result`, 演算子を保存する`operators`, 演算子と()の優先度を保存した`priority`を用意する
- numberはresultに保存していく
- 演算子と()はoperatorsに保存
    - もし （　に当たったら operatorsに保存して進む
    - もし　）に当たったら、operatorsに（　が出てくるまで探す（operatorsの最後の要素から）
        - （　ではない演算子がでてきたらoperatorsからpopしてresultに追加する
    - もし＋－＊/に当たったら、operatorsにその演算子より優先度が低い演算子が出てくるまでoperatorからpopしてresultに追加する
- 最後にoperatorsの値をpopしてresultに入れる

### 2. evaluate()の変更

- `answer`というスタックを用意する
- numberはanswerに保存する
- 演算子に当たったら、answerから2回popする。popした値を演算子に合わせて計算する。
- 計算後の値をanswerにpushする
- 最後にanswerに残った値を計算結果として返す

### 3. read_number()とtokenize()の変更

- hw3-1で追加した負の数に変える処理を消した
- tokenize()で先頭にダミーのPLUSを追加した処理を消した

### 工夫した点

- 最初に上の方法で取り組みましたが、もっとシンプルにできないかと思いスタックを使う方法でも作ってみました。
- 逆ポーランド記法を取り入れたおかげで()や演算子の優先度を考える必要がなくなったので、stackを使ってevaluate()がシンプルになりました。
- ただ、今のプログラムだと負の値に対応できていないです。