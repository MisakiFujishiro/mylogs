# MSK:Managed Streaming for Kafka
MSKはフルマネージドで可用性が高くセキュアなApache Kafka サービス  
以下のメリットがある。
- OSSのKafkaのAPIが利用可能
- BrokerやZookeeperインフラがマネージドで提供されている
- AWSサービスとの統合
    - IAM/権限管理
    - KMS/セキュアなデータのやり取り











## kafkaの概要
そもそもApache kafkaは、多くの導入実績があり、スケーラビリティに優れた、パブリッシュ・サブスクライブモデルの分散メッセージング基盤を提供する

### kafkaの役割
データソースから生成されるストリームデータを取り込んで永続化して、他のサービスへ連携することがkafkaの役割   

そもそもストリームデータとは、多数のデータソースによって継続的に生成されるデータであり、大量のデータを扱うためにkafkaには以下を満たす力がある。
- 拡張性
- スケーラビリティ
- 耐障害性
- 低遅延性

![](img/msk_mokuteki.png)


### kafkaの仕組み
Push型のキューシステムであり、pub-subモデルを採用している。
> Push型では、TopicからSubscriberへの配信は即時に行われる。
> Pull型では、キューからConsumerがメッセージを取り出す必要がある。

![](img/msk_pubsub.png)

kafkaでは、複数のサーバーでクラスタ構成をしており、スケーラビリティと可用性を確保している

#### kafka Cluster
kafkaのクラスターは以下の構成要素から成り立っている。
- ブローカー  
    クラスターとして動作してデータの受配信を担う
    クラスター構成のため、スケールアウトが可能
- パーティション  
    ブローカー上に分散配置されて、トピックのメッセージが実際に格納される分散キューにあたる
- トピック  
    メッセージを種別で管理する概念的な存在で、実態はpartitionをまとめたもの。
    Producer/Consumerはトピックを指定することができる
- ZooKeeper  
    トピックやパーティションのメタ情報を管理している

![](img/msk_cluster.png)



#### トピックとパーティション
トピックは概念的なものであり、メッセージを種別でまとめたもの。
実態としてはパーティションが存在しているだけ。

![](img/msk_topic_partition.png)

パーティションは可用性のために、ブローカーにレプリケーションを作成している。
- BrokerからLeader Replicaが選定される
- Producerがパーティションに書き込みを行う場合は、Leader Replicaに対してデータを書き込む

![](img/msk_pub.png)

-  Leader Replicaに書き込まれた内容はBrokerを超えてフォロワーレプリカに複製する（同期の確認はLeaderが行う）

![](img/msk_replicate.png)

-  Consumerのメッセージ読み込みもLeader Replicaに対して行う

![](img/msk_sub.png)


#### オフセット
メッセージがパーティションに書き込まれた際に付与されるシーケンシャルな番号を`offset`と呼ぶ

![](img/msk_offset.png)

パーティション単位で最後に取得したメッセージをzooKeeperもしくはkafka自体が保存して、Consumerにも連携しているこのオフセットにより、Consumerは継続的にメッセージのどこまでを読み出したかを管理している。

#### ハイウォーターマーク
レプリカによる複製が完了済みのオフセットのことを`ハイウォーターマーク`と呼び、Consumerはハイウォーターマークのデータのみを取得できる。
以下の図では、offset3までがConsumerが取得できるoffsetとなる。

![](img/msk_highwatermark.png)














## MSKの価値
■kafkaの課題  
kafkaは上記で述べてきたように非常に便利であるものの、分散メッセージ基盤であるため、環境構築において多くのサーバーに対する設定が必要となる。  
また、稼働後もブローカーやZookeeperの運用、スケールや監視などの作業が必要となる。


■MSKの価値  
MSKではこの問題に対応しており、MSKは一言で言うと
> MSKはフルマネージドで可用性が高くセキュアなApache Kafka サービス  

である。

MSKでは、以下を提供している
- MSKだからこそ容易に実行可能なコントロールプレーン  
    面倒なクラスターの作成、更新、削除をAPIやマネジメントコンソールから実行することができる  
    下図の紫色の枠をマネージドに作成・管理ができる

- Apache Kafkaを流用できるデータプレーン  
    トピックの作成、ProducerやConsumerからのデータのやり取りに関しては、Apache KafkaのAPIをそのままサポート  
    下図のオレンジ矢印の部分をApache kafkaを流用できる

![](img/msk_image.png)


これらを踏まえ、たとえば[EC2上にKafkaを導入](https://aws.amazon.com/jp/blogs/news/best-practices-for-running-apache-kafka-on-aws/)する場合とMSKを利用する場合では以下のような差がある

![](img/msk_hikaku_manual.png)

### MSKのデプロイメント
MSKでは、AZ間でブローカーを均等にデプロイすると言うベストプラクティスを自動で適用してくれる。  
作成時に以下を設定する
- 適用するAZ
- AZあたりのブローカー数

### MSKのネットワーク
MSKでは、自動で作成したクラスターに対する接続はエンドポイントが払い出されるので、そのエンドポイントに対して、クライアントから通信すれば良い。

セキュリティグループはMSKクラスターで指定したセキュリティグループが適用されるが、クライアントと同じセキュリティグループにしておくと比較的簡単に通信ができるようになる。

![](img/msk_network.png)

### MSKの監視
MSKではAWSのCloudWatchと統合されており、メトリクスを取得可能
以下のメトリクスレベルを選択可能
- 基本モニタリング（DEFAULT）  
    基本的なクラスターレベルとブローカーレベルのメトリクス

![](img/msk_basic_monitering.png)

- 拡張ブローカーレベルモニタリング(PRE_BROKER)  
    基本モニタリングおよび拡張ブローカレベル(ブローカーごとも取得)

![](img/msk_broker_monitering.png)

- 拡張トピックレベルモニタリング(PER_TOPIC_PER_BROKER)  
    拡張ブローカーレベルおよび拡張トピックレベル（トピックごとも取得）

![](img/msk_topic_monitering.png)


### MSKのセキュリティ
大きく以下の４つの機能が存在し、今回は、データの保護、クライアント認証について整理
- ★データの保護
- ★クライアント認証
- IAMによる操作権限管理
- コンプライアンス

★データの保護  
データの保護については、大きく３つの対象が存在
1. 保存データの暗号化
2. ブローカー間の通信の暗号化
3. クライアントとブローカー間の通信

![](img/msk_security.png)


１、２に関しては、デフォルトでサーバー側暗号化が有効となる。  
３に関しては、TLSで暗号化した通信だけ許可することも可能だが、パフォーマンスが30%低下することに注意


★クライアント認証  
クライアント認証については、以下の手順を踏む
1. mskクラスターの作成時にACM Private Certificate AuthorityのプライベートCAを指定
2. クライアント側に証明書を設定する。
3. Kafka Autorization CLIを利用してトピックにアクセス権を設定

ブローカー側は
1. 先ほど説明したクライアントとブローカーの通信のTLS暗号化を有効化する
2. ブローカーはACMの証明書を利用
3. Amazon Trust Servicesを信頼する

![](img/msk_authenticate.png)


### MSKによるクラスターの更新
カスタム構成で、既存のクラスターを更新することが可能
1. kafkaの設定ファイルを作成
2. MSKのCOnfigurationを作成
3. MSKクラスターの更新

注意点として、Configurationを一度作成すると削除するAPIがない点やConfigurationを更新する方法がなく、新しく作成するしかない。クラスターの更新時にブローカーと接続断が発生する

デフォルトでは、以下の構成が採用されている

![](img/msk_default_conf.png)

カスタム構成では以下が設定可能

![](img/msk_custom_conf.png)


### MSKのスケーリング
大きく３つのスケーリングが可能
- ストレージの拡張:ブローカーのストレージを増やせる
- ブローカー数の拡張:AZあたりのブローカを増やせる
- ブローカーサイズの拡張:今後可能になる

![](img/msk_scaling.png)



























## 別サービスとの比較
### Amazon kinesis Data Streamsとの比較
kinesis Data Streamsも大量のストリームをリアルタイムで収集して処理するためのデータストリーミングサービスとなっている。

![](img/msk_kinesis_merit.png)


■API  
MSKは、オープンソース互換のAPIなのでKafkaのエコシステムを利用することができる。  
一方で、kinesisはAWSが提供するAPIを利用するため、他のAWSサービスとの連携が密となっている

■スケーリング  
MSKは、クラスターをプロビジョニングするため、シームレスなスケーリングは困難。  
一方で、kinesisでは、スループットをプロビジョニングするので、シームレスなスケーリングが可能

以下のように対応概念を見てみると、クラスターやブローカーという概念が存在しない。

![](img/msk_vs_kinesis.png)

また、構成を見ても、エンドポイントを通じて通信を行うので、バックエンドを意識しないですむ。

![](img/msk_vs_kinesis_arche.png)

■柔軟性  
MSKはkafkaのオープンソースを利用しているので、kafkaのエコシステムと互換性があるのがメリットになる。

MSKのメッセージ中執について、以下のようにSchema Registryを利用して、スキーマに応じた自動的なシリアライゼーションが可能となる

![](img/msk_schemaRegistry.png)









## MSKの実装

### MSKの採用
MSKを採用するか否かは以下のポイントから判断する
1. オンプレのApache Kafkaを移行したい
2. EC2のApache Kafkaを移行したい
3. Apache Kafkaの周辺ツールを利用する必要がある

上記以外の場合は、サーバーレスのメリットがあるので、Amazon Kinesis Data Streamsの利用が推奨



### ベストプラクティス
MSKを利用する場合は、[ベストプラクティス](https://docs.aws.amazon.com/ja_jp/msk/latest/developerguide/bestpractices.html)を参考にする

![](img/msk_best_practice.png)

#### クラスターサイズ
ブローカー１台あたりのパーティションの推奨数が定義されている
![](img/msk_partition_num.png)







