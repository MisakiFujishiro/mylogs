# MSKのチュートリアル実装(CLI編)
MSKを利用したメッセージの送受信を行うために、MSKのクラスターを作成する。
その後、クラスターに対してキュートなるトピックを作成する。
最後に、EC2上からCLIを利用して、メッセージの送受信を行う。

- [クラスターの作り方](https://docs.aws.amazon.com/ja_jp/msk/latest/developerguide/getting-started.html)

## クラスターの作り方
基本的にMSKはマネージドなkafkaのクラスターを提供するサービスである。
そのため、kafkaのトピック作成やメッセージの送受信、メッセージの中身の確認といった部分のサポートは提供されていない。

MSKのコンソールからクラスターを作成を選択。カスタムを選択する

![](img/msk_cluster_setting2.png)

クラスター名を設定する。

![](img/msk_cluster_setting3.png)

クラスターのタイプはプロビジョンドを利用

![](img/msk_cluster_setting4.png)


ブローカーのインスタンスのファミリーのタイプを選択を行う。 (図では大きいファミリーだが小さいのでOK) 
ブローカーがどの程度分散されるかなどを設定できるか、AZに分散をするので、この後に設定するネットワークの設定と関連する。

![](img/msk_cluster_setting5.png)

ネットワークの設定を行う。  
事前に設定するVPC、AZ、セキュリティグループを作成しておく。
後ほど、EC2のクライアントと接続できるようにセキュリティグループの設定を行う。

![](img/msk_cluster_setting6.png)

セキュリティの設定を行う。一旦はIAMベースでのセキュリティやメッセージの暗号化について設定しておく

![](img/msk_cluster_setting7.png)

モニタリングの設定をする前にロググループを設定しておく

![](img/msk_cluster_setting8.png)

作成したロググループを使って、ログの出力を行う。ログのレベルはDEFAULTでOK

![](img/msk_cluster_setting9.png)

作成後に変更できる項目などの一覧は以下

![](img/msk_cluster_setting1.png)

## EC2の作成
### IAM Roleの作成
EC2に付与するMSKにアクセスすることができるポリシー及びロールを作成する

ポリシーを作成して、以下のポリシーに対して3点変更する
- Account-ID
- MSKTutorialCluster
- region
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:Connect",
                "kafka-cluster:AlterCluster",
                "kafka-cluster:DescribeCluster"
            ],
            "Resource": [
                "arn:aws:kafka:region:Account-ID:cluster/MSKTutorialCluster/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:*Topic*",
                "kafka-cluster:WriteData",
                "kafka-cluster:ReadData"
            ],
            "Resource": [
                "arn:aws:kafka:region:Account-ID:topic/MSKTutorialCluster/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:AlterGroup",
                "kafka-cluster:DescribeGroup"
            ],
            "Resource": [
                "arn:aws:kafka:region:Account-ID:group/MSKTutorialCluster/*"
            ]
        }
    ]
}
```

### EC2インスタンスの作成
MSKのクライアントをEC2で作成する。
簡単のためにMSKと同じVPC上にEC2を作成する。

名前とインスタンスの設定はデフォルト

![](img/msk-ec2-setting1.png)

ネットワークの設定はMSKと同じVPC内にEC2を作成する

![](img/msk-ec2-setting2.png)

作成が完了したら、セキュリティグループのルールの変更とIAMロールの付与を行う。

まず、セキュリティグループを修正するためVPCのコンソール画面からセキュリティグループの画面に移動する。  
- MSK側のSG  
    インバウンドルールを編集して`EC2のSG`からのすべてのトラフィックについて許可する。
- EC2側のSG  
    SSHの許可をする。ポート22に対してMyIPか3.112.23.0/29(AWSコンソールからの接続用)で許可する。

次に、EC2のコンソールから先ほど作成したIAM Roleの付与をする。


## トピックの作り方
EC2からインスタンスを選択して、接続する。

javaのインストール
> sudo yum -y install java-11

kafkaのダウンロードと解凍
> wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz  
> tar -xzf kafka_2.12-2.8.1.tgz

kafka_2.12-2.8.1/libsディレクトリに移動し、次のコマンドを実行して Amazon MSK IAM JAR ファイルをダウンロードします。Amazon MSK IAM JAR により、クライアントマシンはクラスターにアクセスできます。
> wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.1/aws-msk-iam-auth-1.1.1-all.jar

kafka_2.12-2.8.1/bin ディレクトリに移動します。次のプロパティ設定をコピーして、新しいファイルに貼り付けます。ファイルに client.properties という名前を付け、保存します。
```
security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

これらの設定の詳細を解説しておくと
- security.protocol=SASL_SSL  
    クライアントとKafkaサーバー間の通信プロトコルを設定している（SASLを使用したSSLを指定）
- sasl.mechanism=AWS_MSK_IAM  
    SASL認証をどの方法を利用するかで、MSKのIAM認証を利用
- sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;  
    JAAS(Java Authentication and Authorization Service)の設定で、IAMを利用することを指定
- sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler  
    Callbackに関する設定


以下を実行するとTopicが作成される
```
bin/kafka-topics.sh --create --bootstrap-server BootstrapServerString --command-config bin/client.properties --replication-factor 2 --partitions 1 --topic MSKTutorialTopic
```


## メッセージの送信
```
<path-to-your-kafka-installation>/bin/kafka-console-producer.sh --broker-list BootstrapServerString --producer.config bin/client.properties --topic MSKTutorialTopic
```
コンソールが出力されるのでメッセージを記入

![](img/msk_producer.png)

## メッセージの受信
別のEC2を起動し、javaやkafkaのインストールをする。

以下のコマンドを実行すると、producerで送信されたメッセージが受信できる。
```
<path-to-your-kafka-installation>/bin/kafka-console-consumer.sh --bootstrap-server BootstrapServerString --consumer.config bin/client.properties --topic MSKTutorialTopic --from-beginning
```

![](img/msk_consumer.png)

## その他操作
Topic一覧表示
```
bin/kafka-topics.sh --list --zookeeper [ZookeeperServerString]
```

Topicの削除
```
bin/kafka-topics.sh --delete --zookeeper [ZookeeperServerString] --topic [TopicName]
```


# MSKの開発環境の構築
## ProducerのCICD
MSKは依存関係などが重くなることが見込まれるので、ECS上に構築することにする。
[SQSのConsumer](https://misakifujishiro.github.io/mylogs/HandsOn/SQS.html#id12)と同様の手順で構築する

## ConsumerのCICD
基本的には[SQSのConsumer](https://misakifujishiro.github.io/mylogs/HandsOn/SQS.html#id12)と同様

- Spring側でapplication.ymlを作成してportを8081に変更する
- DockerFileをmskに変えて、Portも8081とする




# MSKのチュートリアル実装(Java編)
## Producerの設定
### pomの設定

以下の依存関係を追加する
- kafka:kafka-clients  
    Apache KafkaのJavaクライアントライブラリで、ProducerとConsumerを設定するためには必要
- kafka:spring-kafka  
    SpringBootフレームワークが提供するkafkaとの統合をサポートするライブラリで、送受信を行う
- awssdk:kafka  
    AWS SDK for javaの一部で、MSKのクラスタに対するAPIリクエストを行うために利用される
- msk:aws-msk-iam-auth  
    AWS MSK IAM Java Authenticationというライブラリで、MSKへのIAM認証を実施してくれる
- aws-sdk-java  
    springプロジェクトがAWS JAVA SDKを利用してAWSのサービスにアクセスするための依存関係の設定


```
<dependency>
    <groupId>software.amazon.msk</groupId>
    <artifactId>aws-msk-iam-auth</artifactId>
    <version>1.1.0</version>
</dependency>

<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>kafka</artifactId>
    <version>2.20.98</version>
</dependency>

<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>

<!-- https://mvnrepository.com/artifact/software.amazon.awssdk/aws-sdk-java -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>aws-sdk-java</artifactId>
    <version>2.20.98</version>
    <scope>provided</scope>
</dependency>
```

### application.yml
msk-producerは8082のポートを利用するため、application.yamlで以下を設定する
```
server:
  port: 8082
```


kafkaを利用するためにapplication.yamlで以下の設定を行う。これはcliから実行した時はclient.propertiesに設定してたもの
- producer
    - bootstarap-servers: ブートストラップのエンドポイントを指定する（MSKクラスタより取得）
    - key-serializer: producerがキーを送信する際にバイトに変換するための設定
    - value-serializer: producerが値を送信する際にバイトに変換するための設定
- properties
    - security.protocol: kafkaへの接続に使用するセキュリティプロトコルの設定
    - sasl.mechanism: saslのメカニズム設定で、今回はIAMを利用するための設定が行われている
    - sasl.jaas.config: JAASの設定で、MSKのIAMログインモジュールを利用
    - sasl.client.callback.handler.class: SASLのコールバックを指定する
```
spring:
  kafka:
    producer:
      bootstrap-servers: <YOUR_BOOTSTRAP>
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
    properties:
      security.protocol: SASL_SSL
      sasl.mechanism: AWS_MSK_IAM
      sasl.jaas.config: software.amazon.msk.auth.iam.IAMLoginModule required;
      sasl.client.callback.handler.class: software.amazon.msk.auth.iam.IAMClientCallbackHandler
```



### フロントエンドの作成
前提としてalbのパスルーティングを行う際に、`msk-producer*`というパスをルーティングするので、全てのパスはmsk-producerから始まるようにする。
msk-producerにアクセスすると、index.htmlにリダイレクトしてindex.htmlからmessageをmskにpostするという全体像。

![](img/msk_alb_rule.png)


以下2つのフロントエンドの実装を行う。  
- ヘルスチェック用のフロント
- 画面を表示して、メッセージをMSKに送信するフロント


■ヘルスチェック用  
TGで設定するALBからのヘルスチェックのエンドポイントとして利用する。
```
@RestController
public class HealthCheckController {
    @GetMapping("/msk-producer-healthCheck")
        public ResponseEntity<String> healthCheck() {
            return ResponseEntity.ok("Healthy");
    }
}
```

![](img/msk_tg.png)


■表示する画面のhtml  
src/main/java/resourcesの配下にmsk-producer-index.htmlを作成する
```
<!DOCTYPE html>

<html lang="ja">
<head>
    <title>Send Message</title>
</head>
<body>
<form action="/msk-producer-send" method="post">
    <label for="message">Message:</label><br>
    <input type="text" id="message" name="message"><br>
    <input type="submit" value="Submit">
</form>
</body>
</html>
```

msk-producerへのアクセスをindex.htmlにリダイレクトするためにWebConfig.javaを実装する
```
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addRedirectViewController("/msk-producer", "/msk-producer-index.html");
    }
}
```

### Controller
フロントエンドで受け取ったメッセージをmsk-producer-sendにpostするためのControllerクラスを作成する。

```

@RestController
public class FrontendController {
    private final MessageSender messageSender;

    @Autowired
    public FrontendController(MessageSender messageSender) {
        this.messageSender = messageSender;
    }

    @PostMapping("/msk-producer-send")
    public ResponseEntity<String> sendMessage(@RequestParam("message") int message) {
        if (message <= 0) {
            return ResponseEntity.badRequest().body("Invalid message value. Only positive integers are allowed.");
        }

        messageSender.sendRandomMessages(message);
        return ResponseEntity.ok("Messages sent: " + message);
    }
}

```


### MessageSender
メッセージを送るMessageSenderを作成する

spring-kafkaで提供されているKafkaTemplateを利用して、kafkaへの送信をおこなっている
```

@Component
public class MessageSender {
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final String topic;

    @Autowired
    public MessageSender(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
        this.topic = "Topic_from_java"; // 送信先のトピック名
    }

    public void sendMessage(String message) {
        kafkaTemplate.send(topic, message);
    }

    public void sendRandomMessages(int num) {
        Random rand = new Random();
        System.out.print(num);
        for (int i = 0; i < num; i++) {
            int randomNum = rand.nextInt(11);
            System.out.print(randomNum);
            kafkaTemplate.send(topic, String.valueOf(randomNum));
        }
    }
}
```


## Consumerの設定
### application.yaml
msk-consumerは8081のポートを利用するため、application.yamlで以下を設定する
```
server:
  port: 8081
```

kafkaを利用するためにapplication.yamlで以下の設定を行う。これはcliから実行した時はclient.propertiesに設定してたもの
- producer
    - group-id  
        これはConsumer側で自身が所属するグループを指定するための値。  
        この値を利用することで、Pub-Subモデルのメッセージキューにすることができる。
        - 異なるグループのConsumerはそれぞれ独立して、メッセージをConsumeする。
        - 同じグループのConsumerは、お互いにoffset情報をやり取りして、メッセージが適切に分配されることを保証する
    - auto-offset-reset  
        Consumerが消費者が読み込むべき最初のオフセットをどのように決定するかを指定する。
        - earliest: 最も古いオフセットから読み込むので、全メッセージを消費することになる
        - latest: 最新のオフセットから読み込む、Consumerが起動した時点からTopicに追加されたメッセージを消費する
        - none: Consumerが前回消費した最後のオフセットの次から読み込むが、そのオフセットが存在しない場合、例外がスローされる

- propertiesはProducerと同様

```
spring:
  kafka:
    consumer:
      bootstrap-servers: b-2.mafujishiromsmsk.2mkkld.c2.kafka.ap-northeast-1.amazonaws.com:9098
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      group-id: group_id
      auto-offset-reset: earliest
    properties:
      security.protocol: SASL_SSL
      sasl.mechanism: AWS_MSK_IAM
      sasl.jaas.config: software.amazon.msk.auth.iam.IAMLoginModule required;
      sasl.client.callback.handler.class: software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

### MessageReceiver
以下のMessageReciverクラスを作成する
- @Component  
    Springのコンポーネントスキャンにより、自動的にコンポーネントとして検出され、springによりインスタンスが生成される
- @KafkaLister  
    このメソッドはTopicからのメッセージ受信するためのリスナーメソッドになる
- ConsumerRecord  
    kafkaから受信したメッセージ
```

@Component
public class MessageReceiver {

    @KafkaListener(topics="Topic_from_java")
    public void receiveMessage(ConsumerRecord<String, String> record){
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        System.out.println("PROCESSING START =======================================================" );

        //処理開始時間の表示
        LocalDateTime now_bf = LocalDateTime.now();
        System.out.println("START TIME：" + formatter.format(now_bf)+" & MESSAGE key： "+record.key());
        System.out.println("START TIME：" + formatter.format(now_bf)+" & MESSAGE Value： "+record.value());
        System.out.println("START TIME：" + formatter.format(now_bf)+" & MESSAGE partition： "+record.partition());
        System.out.println("START TIME：" + formatter.format(now_bf)+" & MESSAGE Offset： "+record.offset());

        int waitTime = Integer.parseInt(record.value()) * 1000;
        System.out.println("wait time: " + waitTime);
        waitInMilliseconds(waitTime);

        //処理完了時間の表示
        LocalDateTime now_af = LocalDateTime.now();
        System.out.println("END TIME： " + formatter.format(now_af) +" & MESSAGE ID： "+record.key());
        System.out.println("PROCESSING END =======================================================" );

    }
    //数字を受け取って、その時間待機するためのメソッド
    private void waitInMilliseconds(int milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            e.printStackTrace();
        }
    }

}

```

これだけで、メッセージを送信すると、Consumerで受信することができる。


### 結果
ALB_URL/msk-producerにアクセスすると以下画面が表示される。

![](img/msk_producer_frontend.png)

画面から数字を入力すると、Consumer側でその数だけメッセージを受け取ってシリアルに待機することを確認

![](img/msk_consumer_log.png)

# MSKのオートスケーリング設定
## 基本方針
- 監視
    CloudWatchで`SumoffsetLag`を監視する。
    (処理済みと未処理のoffsetの差分)
- オートスケール
    - キューが溜まったら、スケールアウトして8台になる
    - 5分間連続でメッセージ数が0になったらスケールインする
- 確認事項
    - 件数と処理数が多い場合に、働かないConsumerが発生して、減り方が漸減する
    - 最初はpartitionに偏りがない
    - 後半にpartitionに偏りが発生する
    - partition数を増やすことで、偏りが減るかを確認する

## 監視設定
メトリクスの各種設定はSQSと同様

![](img/msk_sumoffsetlag.png)

スケールアウトの設定

![](img/msk_scaleout_alarm_setting.png)

スケールインの設定

![](img/msk_scalein_alarm_setting.png)


## オートスケール設定
基本的にはSQSの設定と同様にする。

スケールアウトの設定

![](img/msk_scaleout_policy.png)

スケールインの設定

![](img/msk_scalein_policy.png)


## 検証結果
あんまりうまくいかなくなってしまった。要調査
### partitionが1でscaleoutする場合
100件データを送信したところ、アラームが検知

![](img/msk_alarm.png)


Consumerも8台起動（IPの関係で7台起動）

![](img/msk_scaleout_num.png)

ただし、parttiionが1で作成されているため、分散されないで時間がかかる。  
ログを確認してみても、partitionが0になっている

![](img/msk_partition1_consumer_7_log.png)


### partitionがscaleout台数と同じ場合


### partitionがscaleout台数より多い場合