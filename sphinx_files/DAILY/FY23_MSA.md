# 塾の活動(FY23 上期)

## テーマ
「AWSメッセージングサービスの比較と適用ユースケースの整理」
### 背景  
- マイクロサービスにおけるメッセージングサービスの役割を言語化したい
- AWSのサービスとしてメッセージングサービスが複数ある中での特徴の把握をしたい
- 現在の案件でMSKを利用しているので、詳しくなりたい。  
### やる価値  
- MSAに止まらず、重要なメッセージングサービスのメリットデメリットを語れる人材になる
- メッセージングサービスを利用したアプリを開発できる人材になる
- AWSサービスの深掘りをする中で対外発表まで至れる人材になる




## 実行計画
■3月  
- テーマ検討

■4月  
- メッセージングサービス調査
- 環境構築

■5月  
- テーマ具体化と実装内容検討  
- テーマ深掘り
- 対象サービスの深掘り
- 実装開始

■6月  
- 実装継続
- 深掘りテーマの発見

■7月  
- 深掘りテーマの検証

■8月  
- バッファ
- 資料作成

■9月  
- 発表






## 活動履歴
### 4月上旬
- メッセージングサービス調査  
    Black Beltでサービスの特徴整理
    - [MQ](https://misakifujishiro.github.io/mylogs/AWS/MQ.html)【完了】
    - [SQS](https://misakifujishiro.github.io/mylogs/AWS/SQS.html)【完了】
    - [SNS](https://misakifujishiro.github.io/mylogs/AWS/SNS.html)【完了】
    - [MSK](https://misakifujishiro.github.io/mylogs/AWS/MSK.html)【完了】
    - [kinesis](https://misakifujishiro.github.io/mylogs/AWS/Streaming.html#kinesis-data-streams)【完了】
- 環境構築
    - workspaces（バーチャルディスプレイ環境）構築完了
    - Chrom/AWSCLI/IntelliJインストール完了
    - JDKのインストール完了
    - IntelliJのログイン完了
    - IntelliJでHello World（Spring versionに注意）
- AWS Summit  
    - メッセージキューなどについて色々AWS技術者に相談できてすごく有意義でした。来年も行きます。

### 5月
- 取り組みの全体像と実装内容検討【完了】  
    - [MIRO](https://miro.com/app/board/uXjVMTUlajs=/)で整理
        - 背景
        - メッセージキューの価値
        - キューの分類と対応するAWSサービスのメッセージキューサービスの使い分け
        - 実案件で困っている部分について
        - 実装による比較
        - 実装対象のリストアップ
- テーマ深掘り【完了】
    - キューイングの価値、マイクロサービスにおける重要性を[ドキュメント化](https://misakifujishiro.github.io/mylogs/microservice/queuing.html)
- 対象サービスの深掘り【完了】
    - SQSのメトリクスについて[調査](https://misakifujishiro.github.io/mylogs/AWS/SQS.html#id17)【完了】
    - MSKのメトリクスについて[調査](https://misakifujishiro.github.io/mylogs/AWS/MSK.html#id14)【完了】
    - オートスケーリングを設定するときに利用できそうなメトリクスを整理。溜まっているメッセージ数を利用するかCPUなどのメトリクスを見るか、どのような方針かも深掘りで整理したい。

- 実装【未着手】
    - SQSとMSKのセッティング
    - Lambdaからそれぞれを呼び出してみる


### 6月上旬
### 6月下旬


### 7月上旬
### 7月下旬


### 8月上旬
### 8月下旬



### 9月上旬