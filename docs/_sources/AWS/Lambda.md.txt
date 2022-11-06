# Lambda
サーバーのプロビジョニングや管理なしでプログラムを実行できるサービス

## Lambdaのメリット
コードの実行やスケーリングをLambada側で実施するので、開発者はコーディングに集中できる。

## Lambdaの呼び出しかた分類
Lambdaは呼び出し元のサービスによって、呼び出され方が異なる。

![](img/lambda_call.png)

４つの種別については、以下のような分類がある。

![](img/lambda_call_detail.png)
大きな分類手である、ポーリングとはLambdaがイベントを取りに行くのか、呼ばれるのかの分類である。

### ①Lambda関数を同期的に呼び出す
Lambdaを呼び出したら、その実行が完了するのを待つ。  
イベント元に実行結果を返す。

### ②Lambda関数を非同期的に呼び出す
Lambdaを呼び出すと、一旦LambdaないのQueueに格納されてからLambdaが実行される。
イベントソースには、キューへの格納成功だけが返されるので、結果は返されない。
エラー時の挙動はリトライ設定ができる。


![](img/lambda_call_ansync.png)

### ③Lambdaがイベントを読み取る
Lambdaが新しいイベントがないがないかポーリングする。


## Lambdaと各種AWSサービスの連携

### H4b
[H4B：AWS LambdaとAWS AI Servicesを組み合わせて作る音声文字起こし&感情分析パイプライン](https://pages.awscloud.com/JAPAN-event-OE-Hands-on-for-Beginners-Serverless-3-2022-confirmation_772.html)
の内容を踏まえてLambadaの手順などを整理する。

#### 全体構成
S3に音声データをアップロードするとS3のイベントが発出され、Lambdaがそれを受け取る。  
LambdaがTranscribeを呼び出して、テキストデータに変換し、そのデータをS3にアップロードする。  
テキストのアップロードを契機として、再度Lambdaを呼び出して、ポジネガ判定を行う。

- Polly:テキストから音声を生成するAIサービス
- Transcribe:音声からテキストを生成するAIサービス
- comprehend:文章のポジネガ判定を行うAIサービス

- ![](img/lambda_archie.png)

#### S3とLambdaの連携
[S3の手順書](./S3.md)に記載

