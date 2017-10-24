#"Kicad2Pads.py"について


##Ａ.概要

+ "Kicad2Pads.py"は、KiCADv4の基板設計ソフトPcbnewで動作するマクロプログラムであり、KiCADのネットリストファイルを入力し、PADS用ネットリストを出力するソフトです。


##Ｂ.ファイル内容
+ "Kicad2Pads.py" ... KiCADからPADS用ネットリスト変換ソフト（マクロ）


##Ｃ.動作確認環境

+ KiCAD Ver4.07 on Windows7-64bit　/ Ubuntu14.04LTS-64bit  


##Ｄ.使用方法
1. Eeschemaを起動し、Pcbnew用のネットリストを作成する。
2. Pcbnewを起動し、Pythonコンソールを選択実行する。　
3. コンソール内で、「pwd」を実行し、出てきたフォルダ（普通は"C:\Program Files\KiCad")へ、本ソフト"Kicad2Pads.py"と**"PcbNetList.py"**をコピーする。
4. コンソール内で、「execfile("Kicad2Pads.py")」と入力、実行する。（入力ネットファイル名は、自動的に「プロジェクト名」+ ".net"に設定される）
5. Pads用ネットリスト"pads.net"ファイルが生成される。


##Ｅ.その他
1. 他に生成されるファイル"NET.TXT"は、ネットリストが正しく認識されたかを確認する為のものです。
2. "Kicad2Pads.py"の中に他のネットフォーマット： Calay / CR-5000(CCF) / DK-Σ /  MM-2 / Telesis / PADS / Intergraph の記述例が書かれています。　必要に応じてコメントアウトして使ってください。


##Ｆ.参考にさせて頂いたサイト
+ 「KiCad用のPythonスクリプト ～ ほぼ回路図の配置通りにフットプリントを予備配置する」
        <https://qiita.com/silvermoon/items/da4fcdba319f46570a60>


