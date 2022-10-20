# 環境構築手順
## STSのインストール（MAC）
### STSとは
Springの公式ツールでEclipseベースのIDE

### インストール
[公式サイト](https://spring.io/tools)からDL  

## mavenのインストール
### mavenとは
POM(Project Object Model)という考え方に基づいて、プロジェクトのビルド、テスト、ドキュメンテーション、成果物の配備などプロジェクトのライフサイクルを管理するもの。
プロジェクトに関わる情報はPOMに集約する。
### インストール
インストールできるApach Maveを確認
> brew search maven

インストール

> brew install maven

動作確認
> mvn --version

### mavenの各コマンド
> mvn packege

成功すると、targetディレクトリに**.jarファイルが作成される。  
作成されるjarファイルの名前はpom.xmlに記述されているartifactIdとversionできまる。

## 参考
- [Spring Tool Suite (STS)の環境構築(for Mac)](https://zenn.dev/nakohama/articles/7ed3953bae7f33)
- [Mavenとは何ぞや](https://qiita.com/ASHITSUBO/items/6c2aa8dd55043781c6b4)
- [初心者必見】Mavenまとめ](https://qiita.com/enzen/items/8546357f4e67357fe730)
