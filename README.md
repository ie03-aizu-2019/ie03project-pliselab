# ソフトウェア総合演習

## ジェネレーターの使用方法

`$ python3 generator.py`

道路の図と入力データが生成されます

`$ python3 generator.py -o {dir_path}`

道路の図と入力データを{dir_path}に保存します

- 以下のオプションで入力データの大きさなどの指定が可能です

  | オプション   | 意味                                                                                              |
  | :----------- | :------------------------------------------------------------------------------------------------ |
  | -n           | 端点の数。範囲指定可能。`{num}` or `{num1},{num2}`                                                |
  | -m           | 辺の数。範囲指定可能。`{num}` or `{num1},{num2}`<br>n 以上の値になった場合、自動で n-1 になります |
  | -p           | 追加点の数。範囲指定可能。`{num}` or `{num1},{num2}`                                              |
  | -q           | 経路の数。範囲指定可能。`{num}` or `{num1},{num2}`                                                |
  | -o, --output | 出力先ディレクトリ。未指定時はコンソールに入力データを出力。                                      |
  | --xymax      | XY 座標の最大値。                                                                                 |
  | --kmax       | 第何経路まで求めるかの最大値。                                                                    |

- 例

  `python3 generator.py -n 6 -m 5 -p 2 -q 4 -o ./data`

  `python3 generator.py -n 6,10 -m 5,9 -p 2 -q 4 -o ./data --xymax 10 --kmax 1`

## グラフジェネレーターの使用方法

`$ python3 graph_generator.py`

道路の図が生成されます

`$ python3 graph_generator.py -o {dir_path}`

道路の図と入力データを{dir_path}に保存します

- 例

  `cat ./input.txt | python3 graph_generator.py`

  `cat input.txt | python3 graph_generator.py -o ./data`
