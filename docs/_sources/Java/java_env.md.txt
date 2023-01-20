# 環境構築手順
## STSのインストール（MAC）
### STSとは
Springの公式ツールでEclipseベースのIDE

### インストール
sts4.xは、[公式サイト](https://spring.io/tools)    
sts3.xは、[公式サイト](https://dist.springsource.com/release/STS/index.html)

### 3.xの場合
stsをDLして、展開すると３つappがあるので全部Applicationにいれる。

![](img/sts3_dl.png)

Applicationのstsを開こうとするとVMが作成できないエラーが出る場合がある。
sts.appを右クリック、パッケージ内容を表示して、` /Applications/STS.app/Contents/Eclipse/STS.ini `を編集

```
-vm
/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/bin
```

## javaのバージョン変更
[macでJDKのバージョンを切り替える方法-JAVA_HOME設定](https://amateur-engineer.com/mac-java-version/)を参考に以下の手順で変更する。

1. javaのバージョン確認
> /usr/libexec/java_home -V

2. javaの切り替え
> export JAVA_HOME=`/usr/libexec/java_home -v "1.8.0_292"`
> PATH=$JAVA_HOME/bin:$PATH

## serverの追加
### apache tomcat のDL
[macにtomcatをDL](https://blanche-toile.com/web/mac-tomcat)この記事を参考に実施


### STSへのServerの追加
[STSへTomcat9をインストール](https://iteng-pom.com/archives/129)この記事を参考に実施

## maven
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
#### mvn compile
src/main/java/配下のソースファイルのコンパイルが行われます。
コンパイルにより作成されたクラスファイルはtarger/classesディレクトリに出力されます。

#### mvn test
デフォルてで、以下のパターンにマッチするファイルが実行される
- ＊＊/Test＊.java
- ＊＊/＊Test.java
- ＊＊/＊TestCase.java

#### mvn packege
成功すると、targetディレクトリに**.jarファイルが作成される。  
作成されるjarファイルの名前はpom.xmlに記述されているartifactIdとversionできまる。



## 参考
- [Spring Tool Suite (STS)の環境構築(for Mac)](https://zenn.dev/nakohama/articles/7ed3953bae7f33)
- [Mavenとは何ぞや](https://qiita.com/ASHITSUBO/items/6c2aa8dd55043781c6b4)
- [初心者必見】Mavenまとめ](https://qiita.com/enzen/items/8546357f4e67357fe730)
- [java複数バージョンの切り替え](https://style.potepan.com/articles/16344.html)
- [pomの設定](http://www.code-magagine.com/?p=2346)