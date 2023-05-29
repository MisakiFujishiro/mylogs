# SQSのチュートリアル実装(CLI編)
以下の内容に関して理解するためにチュートリアルを行う
- キューの作り方
- DLTの設定方法
- メッセージの送受信方法

参考にしたサイト
- [CLIで作成・送受信](https://weblabo.oscasierra.net/aws-sqs-tutorial/)




## キューの作り方
SQSのキューの作成方法について整理する
### CLIで作成する場合
まずは、キューが存在するかの確認。以下コマンドで、現在のキューを確認できる。何もない場合は返値なし
```
$ aws sqs list-queues
```

キューの作成はcreate-queueコマンド（以下は標準キューを作成する場合）
```
$ aws sqs create-queue --queue-name [YOUR_QUEUE_NAME]
{
    "QueueUrl": "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]"
}
```
FIFOキューを作成する場合は、キュー名の最後に`.fifo`を追加して、FifoQueue=Trueのオプションを追加する
```
$ aws sqs create-queue --queue-name [YOUR_QUEUE_NAME].fifo --attributes FifoQueue=true
```

改めて、キューの確認を行うと作成したキューが確認できる
```
$ aws sqs list-queues
{
    "QueueUrls": [
        "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]"
    ]
}
```

また、作成したキューについての詳細を`get-queue-attributes`で表示させることができる
```
$ aws sqs get-queue-attributes --attribute-names All --queue-url https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME] 

{
    "Attributes": {
        "QueueArn": "arn:aws:sqs:ap-northeast-1:[AWS_ACCOUNT_ID]:[YOUR_QUEUE_NAME]",
        "ApproximateNumberOfMessages": "0",
        "ApproximateNumberOfMessagesNotVisible": "0",
        "ApproximateNumberOfMessagesDelayed": "0",
        "CreatedTimestamp": "1683331260",
        "LastModifiedTimestamp": "1683331260",
        "VisibilityTimeout": "30",
        "MaximumMessageSize": "262144",
        "MessageRetentionPeriod": "345600",
        "DelaySeconds": "0",
        "ReceiveMessageWaitTimeSeconds": "0",
        "SqsManagedSseEnabled": "true"
    }
}
```
得られる属性値のうち、キューの状態を表すものは以下
- ApproximateNumberOfMessages  
    未処理のメッセージの数
- ApproximateNumberOfMessagesNotVisible  
    Consumerが取得したが、処理完了していないメッセージ数（処理中のメッセージ数）
- ApproximateNumberOfMessagesDelayed  
    遅延時間が設定されているメッセージ数（Consumer処理可能になるまで待機しているメッセージ数）

得られる属性値のうち、キューの設定値を表すものは以下
- VisibilityTimeout  
    可視性タイムアウト（他のConsumerにメッセージが見えるようになるまでの時間）
- DelaySeconds  
    遅延時間（受信してから、Consumerがメッセージが見えるようになるまでの時間）  
    この遅延時間はキュー全体に対して適用される。
- ReceiveMessageWaitTimeSeconds     
    メッセージがポーリングされる際の最大待機時間
- MessageRetentionPeriod  
    メッセージが保管される期間

コンソールから確認すると以下

![](img/sqs_setting.png)

### GUIで作成する場合
キュータイプと名前を指定する

![](img/sqs_setting_manual1.png)

キューに対する遅延時間や可視性タイムアウトを設定する

![](img/sqs_setting_manual2.png)

暗号化とアクセスポリシーを設定する

![](img/sqs_setting_manual3.png)



## DLTの設定方法
CLIから作成する場合は、`RedrivePolicy`をオプションとして指定することで作成することができるが、詳細は[公式ドキュメント](https://docs.aws.amazon.com/cli/latest/reference/sqs/create-queue.html)を参照されたい。

コンソール画面からは、キューを作成や更新する際に指定することができる。注意点として、DLQは送信元のキューと同じキュータイプ（標準・FIFO）を設定する必要がある。

![](img/sqs_dlq_setting.png)


最大受信数に設定した回数、、キューが失敗した場合にDLQに送信される。










## メッセージの送受信方法
### CLIで送信
`send-message`を利用してメッセージを送信するとメッセージIDとメッセージのハッシュが返却される
```
aws sqs send-message --queue-url "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]" --message-body "hello world"
{
    "MD5OfMessageBody": "5eb63bbbe01eeed093cb22bb8f5acdc3",
    "MessageId": "1db7869e-5ca0-4e97-810c-bb7b7b7522bc"
}
```


### コンソールから送信
SQSのコンソールから、キューを選択しメッセージを送受信を選択

![](img/sqs_txrx_console.png)

メッセージを送信タブから、メッセージ本文を記載して送信する

![](img/sqs_tx_console.png)

### 送信の確認
CLIから`ApproximateNumberOfMessages`を確認する
```
$ aws sqs get-queue-attributes --attribute-names ApproximateNumberOfMessages  --queue-url "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]" 
{
    "Attributes": {
        "ApproximateNumberOfMessages": "2"
    }
}
```

もしくは、コンソールから`利用可能なメッセージ`を確認する

![](img/sqs_message_num.png)






### コンソールで受信確認
まず、コンソールからキュー内のメッセージを受信することができる。
注意点は、SQSはメッセージを受信しただけではなく、削除までする必要があるので、このオペレーションを繰り返すと、受信回数が増えてDLQに移動してしまうこと。

SQSのコンソールから、キューを選択しメッセージを送受信を選択

![](img/sqs_txrx_console.png)

メッセージを受信タブから、メッセージをポーリングする

![](img/sqs_rx_console1.png)

ポーリングの結果得られたメッセージを押下すると、本文などが確認できる。

![](img/sqs_rx_console2.png)

ポーリングをDLQで設定した回数分行うとDLQに移動する



### CLIでメッセージ受信と削除
次に、メッセージをコンソールから受信し、その上で削除を行う。

メッセージの受信は`receive-message`を利用する。メッセージは複数格納されていても、1つのメッセージだけが受信される
```
$ aws sqs receive-message --queue-url "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]" 
{
    "Messages": [
        {
            "MessageId": "698a7959-7d80-4125-9ccf-2a1a52334606",
            "ReceiptHandle": "AQEBQfRoUCKb74uFFlmZT~~~~",
            "MD5OfBody": "11b1d675d840f10f85fed95d4af7264a",
            "Body": "message_from_console1"
        }
    ]
}
```

SQSではメッセージの処理が完了したら、明示的にメッセージの削除を行う必要がある。
メッセージの削除は`delete-message`を利用する。また、メッセージを指定するために受信した際に受け取った`ReceiptHandle"を指定して削除するメッセージを決める
```
$ aws sqs delete-message --queue-url "https://sqs.ap-northeast-1.amazonaws.com/[AWS_ACCOUNT_ID]/[YOUR_QUEUE_NAME]" --receipt-handle "AQEBQfRoUCKb74uFFlmZT~~~~"
```

削除されたことで、メッセージキューにも、DLQにもメッセージが存在しないことが確認できる。















# SQSのチュートリアル実装(Java編)
参考サイト
- [JavaからAmazon SQSのメッセージ送受信を行う](https://www.stsd.co.jp/dev-blog/send_and_receive_amazon_sqs_messages_from_java.html)
- [JavaでAmazon SQSのメッセージを送受信するチュートリアル](https://weblabo.oscasierra.net/aws-sqs-tutorial-java-1/)


## SQSの作成
SQSは別資料で作成した標準キューを再利用する


## EC2の作成
基本的にはデフォルトでEC2を作成。

IAMについては以下のポリシーを持つIAMポリシーを作成しておき付与する
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage",
                "sqs:SendMessage"
            ],
            "Resource": "arn:aws:sqs:ap-northeast-1:[アカウントID]:[SQS_NAME]"
        }
    ]
}

```

## Javaのプログラム作成（Producer
JavaからSQSへのアクセスには、AWS公式のライブラリ`aws-java-sdk-sqs`を利用することとする。pomに以下を追加する。

pom.xml
```
<dependency>
  <groupId>com.amazonaws</groupId>
  <artifactId>aws-java-sdk-sqs</artifactId>
  <version>1.12.116</version>
</dependency>
```

### config
src/main/javaの配下にconfigのディレクトリを作成して、`sqsConfig`を作成する

```
package com.msa.aws.sqs.sqs_producer.config;

import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class sqsConfig {
    @Bean
    public AmazonSQS amazonSQSClient(){
        return AmazonSQSClientBuilder.defaultClient();
    }
}
```
- @configurationにより、設定クラスであることを宣言
    - 設定クラスではSpringがDIするためのBeanの定義を行う
- @Beanにより、メソッドがDIコンテナによって管理させるBeanを作成することを宣言
    - AmazonSQSClient()メソッドにより、SQSのクライアントを生成する
    - defaultClient() メソッドは、既定の設定を使用して AmazonSQS クライアントのインスタンスを作成します。


### MessageSender
```
package com.msa.aws.sqs.sqs_producer;

import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.model.SendMessageRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class MessageSender {
    @Autowired
    private AmazonSQS amazonSQSClient;

    public void sendMessage(){
        String url = "https://sqs.ap-northeast-1.amazonaws.com/626394096352/MA-fujishiroms-sqs-standard";

        String message = "hello SQS!! FROM JAVA";

        SendMessageRequest request = new SendMessageRequest()
                .withQueueUrl(url)
                .withMessageBody(message)
                .withDelaySeconds(5);
        amazonSQSClient.sendMessage(request);
    }
}

```

ここで指定している`withDelaySeconds`はメッセージに対する遅延時間。
SQSのコンソール画面から設定した、`DelaySeconds`はキュー全体に対する遅延時間。


### main
```
package com.msa.aws.sqs.sqs_producer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class SqsProducerApplication {

    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(SqsProducerApplication.class, args);
        MessageSender sender = context.getBean(MessageSender.class);
        sender.sendMessage();
    }

}

```


## Javaのプログラム作成（Consumer
### Config
```
package com.msa.aws.sqs.sqs_consumer.config;

import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class sqsConfig {
    @Bean
    public AmazonSQS amazonSQSClient(){
        return AmazonSQSClientBuilder.defaultClient();
    }
}

```

### MessageReceiver
```
package com.msa.aws.sqs.sqs_consumer;

import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.model.Message;
import com.amazonaws.services.sqs.model.ReceiveMessageRequest;
import com.amazonaws.services.sqs.model.ReceiveMessageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class MessageReceiver {
    @Autowired
    private AmazonSQS amazonSQSClient;


    public void receiveMessage(){
    String url = "https://sqs.ap-northeast-1.amazonaws.com/626394096352/MA-fujishiroms-sqs-standard";

    ReceiveMessageRequest request = new ReceiveMessageRequest()
                .withQueueUrl(url)
                .withWaitTimeSeconds(5)
                .withMaxNumberOfMessages(5);

    ReceiveMessageResult result = amazonSQSClient.receiveMessage(request);

    for (Message msg : result.getMessages()) {
        // 受信したメッセージの情報を表示
        System.out.println("["+msg.getMessageId()+"]");
        System.out.println("  Message ID     : " + msg.getMessageId());
        System.out.println("  Receipt Handle : " + msg.getReceiptHandle());
        System.out.println("  Message Body   : " + msg.getBody());
        System.out.println();

        // 受信したメッセージを削除
        amazonSQSClient.deleteMessage(url, msg.getReceiptHandle());
        }
    }
}

```

### frontend
ECSに載せるための動作確認用とhelthcheck用に文字列を返すControllerを作成しておく
```
package com.msa.aws.sqs.sqs_consumer;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class frontendController {

    @RequestMapping(value="/sqs-consumer", produces = "text/plain")
    public String frontend(){
        return "Hello sqs-consumer!";
    }
}

```

### main
```
package com.msa.aws.sqs.sqs_consumer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class SqsConsumerApplication {

	public static void main(String[] args) {
		ApplicationContext context = SpringApplication.run(SqsConsumerApplication.class, args);
		MessageReceiver receiver = context.getBean(MessageReceiver.class);
		receiver.receiveMessage();

	}
}

```



## EC2からの実行
### jarファイルを移動させる
- キーペアのコピー
    - 作成した、キーペアをworkspacesにコピーしておく（ファイルのコピーはできないので、テキストベースでコピーする。

- 権限付与
```
chmod 600 XXXX.pem 
```

- ファイルコピーコマンド実行
```
scp -i 'EC2秘密鍵' 'ローカルの転送したいファイル' 'EC2ユーザー名@IPアドレス:ファイル配置先 

EX)scp -i .ssh/XXX.pem TEST.txt ec2-user@12.34.567.890:/home/
```


### javaのインストール
EC2にjavaをインストールして、jarファイルを実行する

javaのインストール
```
sudo yum install java-11-amazon-corretto
```

実行
```
java -jar XXX.jar
```

### 結果
Producer側のjarファイルを実行

![](img/sqs_tutorial_producer.png)

Consumer側のjarファイルを実行すると、メッセージを取得することができる

![](img/sqs_tutorial_consumer.png)

CloudWatchでApproximateNumberOfMessagesVisibleを確認するとConsumer側ではメッセージを削除するので、Produceした分増えた後、Consumeした分減る

![](img/sqs_tutorial_metrix.png)







# SQSの開発環境構築
## ProducerのCICD
Producer側はバッチで処理を流すので、CodeDeployでEC2上にjarファイルをデプロイする
1. [IntelliJとGithubを連携](https://misakifujishiro.github.io/mylogs/Java/intelliJ.html#intellijgithub)
2. [GithubとCodeCommitのミラーリング](https://misakifujishiro.github.io/mylogs/AWS/CodeSeries.html#code-commit)
3. CodeDeoloyの準備
3. CodeDeployの設定
4. CodePipelineの作成

### CodeDeployの準備
- appspec.ymlをJava PJのルートディレクトリに配置する

```
version: 0.0
os: linux
files:
  - source: target/sqs_producer-0.0.1-SNAPSHOT.jar
    destination: /home/ec2-user/
permissions:
  - object: /home/ec2-user/sqs_producer-0.0.1-SNAPSHOT.jar
    mode: 755
```

- EC2にcodedeployエージェントをインストール
```
sudo yum -y update
sudo yum install -y ruby
sudo yum install -y aws-cli
wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
```

- EC2に必要なポリシーを追加  
`AmazonEC2RoleforAWSCodeDeploy`のポリシーをEC2に付与したRoleに追加

![](img/codedeploy_ec2_role.png)


- CodeDeployのIAM Roleの作成  
Roleを作成する際にCodeDeployを選択する

![](img/coddedeploy_role.jpeg)


### CodeDeployの設定
- Code Deployのコンソール画面>アプリケーション>アプリケーションの作成
    - アプリケーション名を入力
    - コンピューティングプラットフォームに'EC2'を選択

![](img/codedeploy_app.png)

- アプリケーションが作成できたら、そのままデプロイグループを作成する
    - デプロイグループの名前を入力
    - サービスロールは事前に作成したもの
    ![](img/codedeploy_setting1.png)

    - デプロイのグループはキーを利用するのでデプロイ先のEC2のタグを指定する
    ![](img/codedeploy_setting2.png)

    - DodeDeployエージェントのインストールは完了しているので、対応なし
    ![](img/codedeploy_setting3.png)


### CodePipelineの作成
- Pipelineの作成
    - パイプライン名を入力
    - サービスロールは新規で作成する
    ![](img/codepipeline_sqs_producer.png)
- ソースプロバイダーは事前作成したCodeCommit
- ビルドステージはスキップ
- デプロイステージは事前に作成したCodeDeploy

![](img/codepipeline_sqs_producer_overview.png)






## ConsumerのECSデプロイとCICD
Consumerは最終的にオートスケーリングを行うことを考えて、ECSでのデプロイを目指す。
1. [IntelliJとGithubを連携](https://misakifujishiro.github.io/mylogs/Java/intelliJ.html#intellijgithub)
2. [GithubとCodeCommitのミラーリング](https://misakifujishiro.github.io/mylogs/AWS/CodeSeries.html#code-commit)
3. DockerFileの作成
4. ECRの設定
5. buildspec.ymlの作成
6. CodeBuildの設定
7. ECSの設定
8. Pipelineの作成(Deployまで)


### Dockerfileの作成
javaの環境構築済みのコンテナを起動し、githubからspringプロジェクトをcloneして、コンテナを起動する。
```
# Docker Imageとしてadoptopenjdk11を使用
FROM adoptopenjdk:11-jdk-hotspot

# git などのインストール
RUN apt-get update && apt-get install -y \
       wget tar iproute2 git

# mavenのインストール
RUN apt-get install -y maven

# PJのコピー
RUN git clone https://github.com/[YOUR_GITHUB_URL]

# プロジェクトのビルド
RUN mvn install -DskipTests=true -f /sqs_consumer/pom.xml

# タイムゾーンの変更
RUN ln -sf  /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# コンテナのポート解放
EXPOSE 8080

# Javaの実行
CMD java -jar sqs_consumer/target/sqs_consumer-0.0.1-SNAPSHOT.jar

```

試しに以下のコマンドでカレントディレクトリのDockerfileを利用したdocker imageが作成されるか確認する
```
sudo docker built -t [YOUR_IMAGE_TAG] .
```

### ECRの設定
パブリックで、ECRを作成しておく。


### Buildspec.ymlの作成
codeBuildで作成したDockerFileを利用してDockerImageを作成し、そのDocker ImageをECRへpushするように設定する
```
version: 0.2
phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - $(aws ecr get-login --no-include-email --region ap-northeast-1)
      - AWS_ACCOUNT_ID=$(echo ${CODEBUILD_BUILD_ARN} | cut -f 5 -d :)
      - REPOSITORY_URL=${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/ma-fujishiroms-sqs-consumer
      - IMAGE_TAG=$(echo ${CODEBUILD_RESOLVED_SOURCE_VERSION} | cut -c 1-7)

  build:
    commands:
      - echo Building the Docker image on `date`
      - docker build --no-cache -t ma-fujishiroms-sqs-consumer:${IMAGE_TAG} .
      - docker tag ma-fujishiroms-sqs-consumer:${IMAGE_TAG} ${REPOSITORY_URL}:${IMAGE_TAG}
  post_build:
    commands:
      - echo Pushing the Docker image on `date`
      - docker push ${REPOSITORY_URL}:${IMAGE_TAG}
      - printf '[{"name":"MA-fujishiroms-container-sqs-consumer","imageUri":"%s"}]' $REPOSITORY_URL:$IMAGE_TAG > imagedefinitions.json
artifacts:
  files: imagedefinitions.json
```

### CodeBuildの設定
CodeBuildを設定することで、buildspec.ymlが実行され、gitlabにコミットすると、Docker ImageがECRにPushされるようになる。

CodeBuildのコンソールからビルドプロジェクトを作成開始
- PJ名の入力
![](img/sqs_consumer_codebuild1.png)
- ソースはCodeCommitのmainブランチ（ここのルートのbuildspecを見る）
![](img/sqs_consumer_codebuild2.png)
- 環境を設定する
- dockerを利用する場合は特権付与にチェックを入れる
- サービスロールは新規で作成するが、後ほどECRへの権限を付与する
![](img/sqs_consumer_codebuild3.png)
- buidspec.ymlがルートディレクトリにある場合はデフォルトでOK
![](img/sqs_consumer_codebuild4.png)


- IAM Roleは新規作成した後に`AmazonEC2ContainerRegistryPowerUser`を付与する

![](img/sqs_consumer_codebuild5.png)


この時点でCodeBuildまでのCodePipelineを作成すると、ECRへのpushが行われる

![](img/codepipeline-sqs-consumer-build.png)

buildspecで設定した通り、イメージタグにIDが振られている(Latestにならない)

![](img/ecr-sqs-consumer.png)



### ECSの設定
#### タスク定義の設定
ECRを設定する。
今回はFargateで設定するため、ネットワークモードがawsvpcになっており、ホストポートを設定しない。

![](img/ecs-taskdefinition1.png)

![](img/ecs-taskdefinition2.png)

ここで、設定したタスクロールにはSQSへのアクセス権限を付与しておく
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage",
                "sqs:SendMessage"
            ],
            "Resource": "arn:aws:sqs:ap-northeast-1:[アカウントID]:[SQS_NAME]"
        }
    ]
}

```


#### サービスの設定
今回はFargateで作成するので起動タイプをFargateとする。
作成したタスク定義を指定することで、起動時のコンテナの設定を行う。

![](img/sqs-consumer-ecs-service-setting1.png)

ネットワークモードとして、VPCやサブネットを選択する。
設定するセキュリティグループの注意点として、コンテナポートに接続できるように設定を行う。（今回は8080にアクセスできるようにインバウンドルールを修正しておく）

![](img/sqs-consumer-ecs-service-setting2.png)

ロードバランサーの設定はサービスを作成する際にしか設定できない点に注意。

事前に作成したALBを指定して、ロードバランス用のコンテナとして、TGの作成などをこの場で設定することができる。
こちらで設定すれば、TGの作成およびTGとALBの紐付けを行うことができる。

![](img/sqs-consumer-ecs-service-setting3.png)


### CodeDeployの設定
CodePipelineを修正し、Deployステージを設定する。

まず、Code Buildのステージで出力アーティファクトを追加する。

![](img/codebuild-artifact.png)


次に、Deployステージを追加し、入力アーティファクトにBuildの出力ステージを追加し、対象となるクラスターやサービス名を指定する。

この設定を行うことで、gitlabの修正から、ECRへのpush、ECSのデプロイを自動化することができる。

![](img/codedeploy-sqs-consumer.png)

![](img/sqs-consumer-pipiline-all.png)

無事ECSが起動できたら、ALBのDNSの後ろに`/sqs-consumer`でアクセスして文字列が表示されるか確認する。


# SQSの本格実装(Java編)
## Producerの改善

## Consumerの改善
- 常時起動するようにする
- 受け取った数字分待機するようにする
- メトリクスの挙動を確認する


