# 塾の活動
## week5(10/31-)
### java チュートリアル 7h
動作確認まで完了。mvnarchetype:generateコマンドやMVCの基本を整理
sts4.xをインストールしていることに気づいて、sts3.xをインストール
ここで、立ち上がらない問題やrun on serverがでないなどのトラブルで時間をだいぶ使った。
javaのバージョンを変えたりstsのiniファイル編集したりして対応
serverがでなかったのはワークスペースの設定も悪かった？？

tutorialでドメイン部分の作成まで完了。Appの方も少しだけ作成して、一覧表示まではできた。
今までは何もわかっていなかったところからお作法とかは少しずつわかってきた。
細かいアノテーションの意味とかは調べつつ。。。わからないところはメモしている

![](img/20221104-1.png)

### AWS code artifact勉強(3h)
じつ業務の方で利用する機会があったので勉強した。  
jarファイルなどの成果物を共有することができるリポジトリ。   
curlコマンドでアップロードはできたが、mvn deployはできていない。
実際のアプリの時に使ってみて、使い方を整理したい。



### わからなかったこと
1. sts4でやったからか、run on serverがなくて困った【解決】
    - sts3をインストールし直して、javaのバージョンも1.8に変えた
    - PJを開く場所をデフォルトにしたらうまくいった
2. CodeArtifactへの登録をmvn deployからできなかった【宿題】
  - stsだとmvn deployはどこからするの？
3. repositoryとserviceで定義するメソッドについて【確認】
  - repositoryはCRUD処理のうちで使うもの
  - serviceは業務ロジックとして使うもの？チュートリアルはいいけど何を作るのかの定義が大事？
4. @injectって何？いくつか記事を読んでみたけど、まだよくわからない。【不明】
5. @modelAttributeでTodoFormの設定している部分はよくわからない【不明】  
　　@ModelAttributeでmodelを作成して、formというvalueがtodoFormとしてAttributeに追加されている。   
   このtodoFormはまだ使われていないだけ？


# TODO
## DONE
- sphinx環境構築
- githubアカウント作成
- javaspringは私用のパソコンでstsを構築
- dockerコンテナ環境構築
- java環境をdockerコンテナに固める手順整理
- 開発環境図整理
- H4B CICD
- CodeArtifactの勉強


## AWS
- H4B ECS 
- H4B SystemManager
- H4B AI Series
- [AWSで作るクラウドネイティブアプリケーションの基本](https://news.mynavi.jp/techplus/series/AWS/)
- [AWSで実践! 基盤構築・デプロイ自動化](https://news.mynavi.jp/techplus/series/AWSAuto/)


## java
- TERASOLNAのチュートリアル（私用
- SpringBootチュートリアル（社内環境