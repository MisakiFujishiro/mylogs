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
- 全体の計画
- 実装開始

■6月  
- 報告資料のイントロ部分作成・中間報告
- 実装
    - SQSのjavaでの実装
    - SQSのオートスケーリング検証

■7月  
- 実装
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
    - IntelliJをgitlabと連携＋codecommitとミラーリング【完了】
    - ProducerのPipeline作成（EC2に自動でデプロイ）【完了】
    - ConsumerのDockerコンテナ化【完了】
    - SQSのConsumerをECS上で実装【完了】
        - バッチ処理になっているので、うまく動かない修正は必要
    - ConsumerのPipeline作成（ECSに自動でデプロイ【完了】

---


### 6月上旬
- テーマ深掘り
    - 発表資料のイントロにドラフトを作成して整理してみる
- 実装
    - Producerのアプリ改修(まとめてメッセージを送信する)
    - Consumerの改修（常時起動でポーリングする）
    - オートスケーリングを設定して挙動を確認する
    - MSKについてJavaのコードで送受信
    - MSKについてメトリクスを取得

### 6月下旬
- テーマ深掘り
    - ドラフトを受けての追加調査ドラフト、オートスケーリングの結果を少し加えて23日の中間報告
- 実装
    - SQSのConsumerをECS上で実装
    - オートスケーリングを設定して挙動を確認する
    - 標準キューとFIFOキューの比較をする

### 7月上旬
- 実装
    - MSKについてJavaのコードで送受信（Producerはバッチなので作り切る→EC2上でOK）
    - MSKのConsumerをECS上で実装
    - オートスケーリングを設定して挙動を確認する
    - [塾長の実装](https://github.com/debugroom/sample-spring-cloud-stream)
### 7月下旬
- テーマ深掘り
    - MSKの結果を踏まえて、多重処理に関する整理
- 実装
    - SQS優先度の実装
    - MSK優先度の実装
### 8月上旬
- テーマ深掘り
    - 優先度に関して、結果を整理
    
### 8月下旬
- バッファ or さらなる深掘り


### 9月上旬
- 資料の最終調整・発表練習


## 相談事項
### 5月
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