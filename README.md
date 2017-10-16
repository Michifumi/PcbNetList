#"PcbNetList"について


Ａ.概要
 "PcbNetList.py"は、回路CADのネットリスト： Calay / CR-5000(CCF) / DK-Σ /  MM-2 / Telesis / PADS / Intergraph / KiCAD のフォーマットを双方向に変換できるサブプログラム(関数）です。
 そのサブプログラムを使って、OrCADのネットリストファイルを入力し、KiCADv4の基板設計ソフトPcbnew用ネットリストを出力できるにプログラムを提供する。


Ｂ.ファイル内容
1."Calay2Kicad.ipynb" ... OrCADからKiCAD用ネットリスト変換メインソフト
2."PcbNetList.py"     ... ネット変換用サブプログラム
3."01_DESIGN1.NET"    ... サンプルCalayネットリスト
4."01_DESIGN1.csv"    ... サンプル部品情報ファイル
5."Kicad2Pads.ipynb" ... KiCADネットリストを他ネットPadsへ変換する参考プログラム


Ｃ.動作環境
　Python3 (Jupyter Notebook) 


Ｄ.使用方法
1. OrCADのネットリストフォーマットを"Calay"選択し、ネットリストファイルを作成。
2. "Calay2Kicad.ipynb"と同じフォルダにそのファイルをコピーする。
3. "Calay2Kicad.ipynb"をJupyter Notebookでオープンする
4. 以下の内容にプログラムを変更する
  import PcbNetList as netlist
  net = netlist.Calay_Read('「OrCAD出力ネットリストファイル名」')
  netlist.Kicad_Write(net, '「出力ファイル名」')
5. プログラムを実行すれば、「出力ファイル名」で指名されたファイルが生成される。この時、生成されたファイルは、部品パッドが各部品最大ピン数のピンヘッダを自動的に割り当てられる。
6. Pcbnewを起動し、そのネットリストをインポートします。　その後、Pcbnewで部品パッドを変更すれば、基板設計できます。
7. この方法は部品一品毎に変更なので部品が多いと面倒です。それで、部番と部品パッド情報をcsvファイルで用意できれば、それを使っても、KiCAD用ネットリストを作成できる。
　それは、上記4.の３行目を
  netlist.Kicad_Write(net, '「出力ファイル名」','「部番と部品パッド情報のcsvファイル名」')
 へ変更して実行すると、部品パッドを変更したネットリストファイルが生成される。
 尚、「部番と部品パッド情報のcsvファイル名」は、"01_DESIGN1.csv"を参考にして作成してください。


