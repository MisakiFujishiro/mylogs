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
- テーマ検討【完了】

■4月  
- メッセージングサービス調査【完了】
- 環境構築【完了】

■5月  
- テーマ具体化と実装内容検討【完了】
- テーマ深掘り【完了】
- 対象サービスの深掘り【完了】
- 全体の計画【完了】
- 実装開始【完了】

■6月  
- 報告資料のイントロ部分作成・中間報告【完了】
- 実装
    - SQSのjavaでの実装【完了】
    - SQSの詳細設定調整【完了】
    - SQSCloudWatchのメトリクス確認とアラームの設定

■7月  
- 実装
    - SQSのオートスケーリング検証
    - MSKのjavaでの実装
    - MSKのオートスケーリング検証
- オートスケーリングの検証結果について整理


■8月  
- 実装
    - 優先度について実装
- 優先度の検証結果について整理
- 資料全体調整
- バッファ

■9月  
- 発表練習






## 活動履歴
### 4月
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

### 5月上旬
- 取り組みの全体像と実装内容検討【完了】  
    - [MIRO](https://miro.com/app/board/uXjVMTUlajs=/)で整理
        - 背景
        - メッセージキューの価値
        - キューの分類と対応するAWSサービスのメッセージキューサービスの使い分け
        - 実案件で困っている部分について
        - 実装による比較
        - 実装対象のリストアップ
- テーマ深掘り【継続】
    - キューイングの価値、マイクロサービスにおける重要性を[ドキュメント化](https://misakifujishiro.github.io/mylogs/microservice/queuing.html)
- 対象サービスの深掘り【完了】
    - SQSのメトリクスについて[調査](https://misakifujishiro.github.io/mylogs/AWS/SQS.html#id17)【完了】
    - MSKのメトリクスについて[調査](https://misakifujishiro.github.io/mylogs/AWS/MSK.html#id14)【完了】
    - オートスケーリングを設定するときに利用できそうなメトリクスを整理。溜まっているメッセージ数を利用するかCPUなどのメトリクスを見るか、どのような方針かも深掘りで整理したい。

### 5月下旬
- 今期のWBSをざっくり作成【完了】
- SQSの調査
    - [SQSディベロッパーガイド](https://docs.aws.amazon.com/ja_jp/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- 実装【実施中】
    - SQSとMSKのセッティング【完了】
    - CLIから送受信【完了】
    - [IntelliJに慣れる](https://misakifujishiro.github.io/mylogs/Java/intelliJ.html)【完了】
    - SQSについてJavaのコードで送受信【完了】
    - SQSについてメトリクスを取得【完了】
    - SQSとMSKのJava開発環境のCICD構築【完了】
        - SQSとMSKのProducerのPipeline作成（EC2に自動でデプロイ）【完了】
        - SQSとMSKのConsumerのPipeline作成（ECSに自動でデプロイ【完了】
            - ConsumerのDockerコンテナ化【完了】
            - SQSのConsumerをECS上で実装【完了】



### 6月上旬
- テーマ深掘り
    - 発表資料のイントロにドラフトを作成して整理してみる【完了】
- 実装
    - SQSの開発
        - SQSのProducerのアプリ改修(まとめてメッセージを送信する)【完了】
        - SQSのConsumerをECS上で実装【完了】

### 6月下旬
- テーマ深掘り
    - 最終報告のドラフトも検討【完了】
    - 最終報告資料でも使えるくらいの資料にブラッシュアップ【完了】
    ---
- 実装
    - Consumerの改修（常時起動でポーリングする）
    - SQSオートスケーリングを設定して挙動を確認する

### 7月上旬
- 実装
    - MSKについてJavaのコードで送受信
    - MSKについてJavaのコードで送受信（Producerはバッチなので作り切る→EC2上でOK）
    - MSKのConsumerをECS上で実装
    - オートスケーリングを設定して挙動を確認する
### 7月下旬
- テーマ深掘り
    - MSKの結果を踏まえて、多重処理に関する整理
- 実装
    - SQS.fifoについて[クラスメソッド](https://dev.classmethod.jp/articles/sqs-new-fifo/#toc-16)
### 8月上旬
- テーマ深掘り
    - FIFOキューの実装比較
    
### 8月下旬
- バッファ or さらなる深掘り


### 9月上旬
- 資料の最終調整・発表練習


## 相談事項
### 検証について
- SQSの検証環境について
    - Pipelineまで作成したので、コンパイルして、pushすれば、EC2上にデプロイまでしてくれるので、それを実行している
    - ローカル環境ではクレデンシャルの未設定でエラーになってしまう。
    - クレデンシャルはなるべく払い出したくないので、どうすれば良い？
```
Exception in thread "main" com.amazonaws.SdkClientException: Unable to load AWS credentials from any provider in the chain: [EnvironmentVariableCredentialsProvider: Unable to load AWS credentials from environment variables (AWS_ACCESS_KEY_ID (or AWS_ACCESS_KEY) and AWS_SECRET_KEY (or AWS_SECRET_ACCESS_KEY)), SystemPropertiesCredentialsProvider: Unable to load AWS credentials from Java system properties (aws.accessKeyId and aws.secretKey), WebIdentityTokenCredentialsProvider: To use assume role profiles the aws-java-sdk-sts module must be on the class path., com.amazonaws.auth.profile.ProfileCredentialsProvider@12eedfee: Unable to load credentials into profile [default]: AWS Access Key ID is not specified., com.amazonaws.auth.EC2ContainerCredentialsProviderWrapper@574a89e2: The requested metadata is not found at http://169.254.169.254/latest/meta-data/iam/security-credentials/]
```

- 選択肢
    - [ローカルスタック](https://itneko.com/localstack-sns-sqs/)で模擬的なSQSを構築する
    - 処理前にCognitoで一時認証を取得する