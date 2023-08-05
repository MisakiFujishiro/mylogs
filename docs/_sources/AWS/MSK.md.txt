# MSK:Managed Streaming for Kafka
MSKはApache Kafkaを利用してストリーミングデータを処理するアプリケーションをの構築を可能とする、フルマネージドで可用性が高くセキュアなApache Kafka サービス  
以下のメリットがある。
- OSSのKafkaのAPIが利用可能
- BrokerやZookeeperインフラがマネージドで提供されている
- AWSサービスとの統合
    - IAM/権限管理
    - KMS/セキュアなデータのやり取り











## kafkaの概要
そもそもApache kafkaは、パブリッシュ・サブスクライブモデルの分散メッセージング基盤である。
LinkedInによって開発され、多くの導入実績があり、高スループット、リアルタイム性を有し、スケーラビリティに優れている。

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
ConsumerはPush型であり、ConsumerはPull型として動作する。

> Push型では、TopicからSubscriberへの配信は即時に行われる。
> Pull型では、キューからConsumerがメッセージを取り出す必要がある。

すなわち、Consumer側のタイミングでMessageを取得することができる。

![](img/msk_pubsub.png)

kafkaでは、複数のサーバーでクラスタ構成をしており、スケーラビリティと可用性を確保している

#### kafka Cluster
kafkaのクラスターは以下の構成要素から成り立っている。
- ブローカー  
    クラスターとして動作してデータの受配信を担う
    クラスター構成のため、スケールアウトが可能
- パーティション  
    ブローカー上に分散配置されて、トピックのメッセージが実際に格納される分散キューにあたる  
    Topicは複数のPartitionから成り立っており、それぞれのPartitionはBrokerに分散して配置される。
    ※Partition-Aは１つのPartitionに見えていても、実態は複数のブローカーに分散されており、レプリケーションされている
- トピック  
    メッセージを種別で管理する概念的なストレージで、実態はpartitionをまとめたもの。
    Producer/Consumerはトピックを指定して、Meaageの送受信を行う
- ZooKeeper  
    トピックやパーティションのメタ情報を管理している
- Message  
    kafka内で扱うデータの最小単位で、メッセージにはkey-valueを持たせることができる。

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

オフセットには以下の種類が存在し、Consumerが取得するメッセージの範囲やリトライ制御を行う
- Log-End-Offset  
    Partitionのデータの末尾（格納されたデータの数
- Current-Offset  
    Consumerが`どこまで読み込んだか`を示す
- Commit-Offset  
    Consumerが`どこまでコミットしたか`を示す



#### ハイウォーターマーク
レプリカによる複製が完了済みのオフセットのことを`ハイウォーターマーク`と呼び、Consumerはハイウォーターマークのデータのみを取得できる。
以下の図では、offset3までがConsumerが取得できるoffsetとなる。

![](img/msk_highwatermark.png)




#### Producer→Brokerの送信プロセス
At Least Oonceのために、Blockerは正しく受信できたことを示すためのAck（肯定応答）を行う。

また、どのパーティションに送信するかのパーティショニング機能が備わっている。

##### パーティショニング
Topicに対してメッセージを送付する際、Partitionに分散して、配置する。
ProducerからMessageを受け取る際に、Partitionerによって、どのようにMessageを配置するかを決定する
- ハッシュ：メッセージのkeyのハッシュを利用して配置する
- ラウンドロビン：順番にパーティションを配置する




#### Broker→Consumerの受信プロセス
成功した場合は以下のようにoffsetが更新される
1. ConsumerからBrokerにトランザクション開始のリクエスト
2. Consumerは取得対象のTopicに対してCurrent-Offsetを確認して、最新Messageを受信リクエストし、Current-Offsetを更新
3. 受信が無事成功
4. Commit-Offsetが更新され、Commit-OffsetとCurrent-Offsetが一致する

![](img/msk_consume_success.png)

失敗した場合は以下のようにoffsetが更新される
1. ConsumerからBrokerにトランザクション開始のリクエスト
2. Consumerは取得対象のTopicに対してCurrent-Offsetを確認して、最新Messageを受信リクエストし、Current-Offsetを更新
3. 受信が失敗
4. Current-Offsetがロールバックされ、Commit-OffsetとCurrent-Offsetが一致する

![](img/msk_consume_fail.png)



#### DLTについて
上記のoffsetによるkafka→Consumerの再送はConsumer側がトラブルなどでダウンしてしまった時のエラーハンドリング

一方でメッセージにトラブルがあり、処理できない場合はDLTを利用する。
SQSではマネージドなキューのためコンソール画面などからDLTの設定を行うことができた。具体的には、移動先のDLTとメッセージが読み込まれた回数を設定すると、限度の読み込み回数を超えた場合に自動でDLTに移動された。

MSKでは、明示的にConsumerのソースコードの中に再実行の設定とエラーハンドリングとしてDLTへのメッセージ移動の処理を書く必要がある。再実行とDLTへの移動が完了したら、元のキューに対しては処理完了のコミットを行うことで処理自体としては正常終了したものとして扱う。



## MSKのメッセージ管理詳細
### group-id
MSKはPub-Subモデル（１つのメッセージに対して複数のConsumerが対応）を採用している。
ProducerはTopicに対してメッセージを送信するだけでよいが、Consumer側で'group-id'というものを指定する。
- group-idが同じConsumer同士は協調して、同じメッセージを重複処理しないようにする。
- groupidが異なるConsumer同士は、互いに独立してメッセージを処理する（同じメッセージが異なるグループで2回処理される）

### auto-offset-rest
Consumerが起動した際に、読み込むべき最初のオフセットをどのように指定するかの設定。

この設定が、反映されるのは以下の２パターン
- consumerが初めて起動した時（初めてTopicをSubscribeした時)
    - 挙動を見ていると、仮にmessageが0だったとしても__consumer_offsetsにoffset0として設定しているように見受けられる
- consumerが以前のoffset情報を失っているとき（offsets.retention.minutesを超えた時）

以下の3つの選択肢がある

- earliest   
    最も古いオフセットから読み込むので、全メッセージを消費することになる  
    普段は、前回のオフセットから実行されるがもし前回のオフセット情報などがない場合に関しては、一番最初から実行される
- latest  
    最新のオフセットを読み込む。すなわち、消費者が起動してから、追加されたメッセージを消化する
- none  
    Consumerが前回消費した最後のオフセットの次から読み込むが、そのオフセットが存在しない場合、例外がスローされる

### offset情報の管理
基本的に各Topicは、messageの情報をもつだけで、offset情報はtopicに記録されるわけではない。

offset情報は、`__consume_offsets`と呼ばれる特殊なトピックで管理され、記録は各Consumerが行うことになる。
これによって、Consumerがダウンしたとしてもoffsetの情報などは、__consumer_offsetsに管理され、前回に読み取った位置から再開することができる

従って、__consumer_offsetsには、各コンシューマーグループの各トピックの各パーティションについて最後に読み取ったオフセットを保持している。
具体的な__consumer_offsetsの中身は以下だが、これを直接参照することはkafkaのマネージド部分に影響をあたる可能性があるので非推奨
- コンシューマグループID： メッセージを消費するコンシューマグループの識別子
- トピック名： メッセージが消費される元のトピック名
- パーティション番号： 上記トピックの特定のパーティション
- オフセット： そのコンシューマグループが次に読み込むべきメッセージの位置。具体的には、最後に読み込まれたメッセージの次のメッセージの位置を示します。

MSKのメトリクスであるSumOffsetLagもこの__consuemr_offsetsを監視している。


### __consumer_offsetsの削除ポリシー
__consumer_offsetsには、すべてのConsumer Group、トピック、パーティションの組み合わせのオフセット情報を管理するため一般的に大量のデータを保持することになる。

そのため、クリーンアップポリシーを提供している。基本的にはcompactポリシーが適用されている。
- delete(log.retention.hours):特定の期間が経過したメッセージを自動削除する
- compact:各キーの最新のメッセージのみが保存され、それ以前のメッセージは削除される。

また、ある特定のConsumerGroupが一定期間活動がないと、そのConsumerグループに対するオフセット情報を削除することがある。  
これは、`offsets.retention.minutes`パラメータで設定されており、デフォルトで7日間（10080min)で設定されている。
消費者グループがこの期間以上メッセージを消費していないと、`__consumer_offsets`トピックからコンシューマーグループの情報を削除してしまう。

メッセージの消化がなかったとしても、Consumerが最新のオフセットを取得するような挙動をすれば情報が保持される可能性がある。

[公式ドキュメント](https://kafka.apache.org/documentation/)この説明を見ると、consumerの処理がずっとなかったとしても、定期的にサブスクライブをしていれば大丈夫そう
```
offsets.retention.minutes
For subscribed consumers, committed offset of a specific partition will be expired and discarded when 
1) this retention period has elapsed after the consumer group loses all its consumers (i.e. becomes empty); 
2) this retention period has elapsed since the last time an offset is committed for the partition and the group is no longer subscribed to the corresponding topic. 

For standalone consumers (using manual assignment), offsets will be expired after this retention period has elapsed since the time of last commit. 
Note that when a group is deleted via the delete-group request, its committed offsets will also be deleted without extra retention period; 
also when a topic is deleted via the delete-topic request, upon propagated metadata update any group's committed offsets for that topic will also be deleted without extra retention period.
```

また、起動すると、subscribeしているっぽいlogがある
```
@timestamp,@message
2023-07-28 16:02:32.512,"2023-07-29 01:02:32.511  
INFO 7 --- [           main] o.a.k.clients.consumer.KafkaConsumer     : [
    Consumer clientId=consumer-CG-P5_1_1week_latest_wakeup-1, 
    groupId=CG-P5_1_1week_latest_wakeup] 
    Subscribed to topic(s): Topic_P5_1_1week_latest_wakeup"
```






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
[詳細は公式°キュtメント参照](https://docs.aws.amazon.com/ja_jp/msk/latest/developerguide/msk-configuration-properties.html)



## MSKのメトリクス
MSKではAWSのCloudWatchと統合されており、メトリクスを取得可能  
基本、拡張ブローカー、拡張トピックの3つのメトリクスレベルがあり、取得できるメトリクスについては、Amazon CloudWatchと連携して、モニタリングが可能。 詳細は[公式ドキュメント](https://docs.aws.amazon.com/ja_jp/msk/latest/developerguide/metrics-details.html)を参照されたい。

代表的なものを紹介する
- 基本モニタリング（DEFAULT）  
    基本的なクラスターレベルとブローカーレベルのメトリクス  

![](img/msk_basic_monitering.png)

- 拡張ブローカーレベルモニタリング(PRE_BROKER)  
    基本モニタリングおよび拡張ブローカレベル(ブローカーごとも取得)  

![](img/msk_broker_monitering.png)

- 拡張トピックレベルモニタリング(PER_TOPIC_PER_BROKER)  
    拡張ブローカーレベルおよび拡張トピックレベル（トピックごとも取得）  

![](img/msk_topic_monitering.png)

- 拡張トピックレベルモニタリング(PER_TOPIC_PER_PARTITION)
    拡張ブローカーレベルおよび拡張パーティションレベル（パーティションごとも取得）  




## USEメソッドに関連するメトリクス
USEメソッド（利用度、飽和度、エラー数）とその他に分けて、メトリクスを紹介する。

#### Utilization(使用度)
どれだけキューが利用されているかを確認するためのメトリクス

- BytesInPerSec(DEFAULT)  
    Producerから受信したメッセージのバイト数
- BytesOutPerSec(DEFAULT)  
    Consumerへ送信したメッセージのバイト数
- MemoryUsed(DEFAULT)  
    ブローカーのメモリの使用率
- NetworkRxPackets(DEFAULT)  
    ブローカーが受信したデータ数
- MessagesInPerSec(PER_TOPIC_PER_BROKER)  
    1秒あたりに受信したメッセージ数


#### Satulation(飽和度)
どれだけキューにメッセージが溜まり、システムが正しく処理を捌き切れているかを確認するためのメトリクス
- sumoffsetlag(DEFAULT)    
    トピックごとの処理されていないメッセージの総数
- OffsetLag(PER_TOPIC_PER_PARTITION)  
    パーティションごとの処理されていないメッセージの総数
- EstimatedMaxTimeLag(DEFAULT)  
    トピックごとの現在の最後のメッセージが処理されるまでの必要な時間の推定値
- EstimatedTimeLag(PER_TOPIC_PER_PARTITION)  
    パーティションごとの現在の最後のメッセージが処理されるまでの必要な時間の推定値


#### Errors(エラー数)
キューにおける失敗したメッセージを確認するメトリクス。
- NetworkRxErrors(DEFAULT)    
  ブローカーのネットワーク受信エラーの数
- NetworkTxDropped(DEFAULT)    
    ブローカーのネットワーク送信エラーの数。





### オートスケーリングに利用するメトリクス
MSKのメトリクスを利用する際の注意点は、各メトリクスが取得できるタイミングに幾つかのパターンがある。
- クラスターが ACTIVE 状態になった後
- トピックを作成した後
- プロデューサー/コンシューマーが立ち上がった後
- コンシューマーグループがトピックから消費した後

上記の条件を満たしてからでないと、オートスケーリングのルール設定でメトリクスを選択できないので注意する。

MSKのメトリクスを監視して、Consumerのオートスケーリングを行う場合に利用できるメトリクスの候補は以下
- BytesInPerSec  
    どれだけのメッセージサイズがMSKに流入しているかから判断する
- MessagesInPerSec  
    どれだけのメッセージ数をMSKが受信しているかから判断する
- sumoffsetlag  
    どれだけのメッセージがMSKに溜まっているかから判断する
- EstimatedMaxTimeLag  
    メッセージが処理されるまでにどの程度かかるかから判断する






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

MSKのメッセージ抽出について、以下のようにSchema Registryを利用して、スキーマに応じた自動的なシリアライゼーションが可能となる

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










## MSK Serverles
2021年に新規発表された







## 参考サイト
- [black belt](https://aws.amazon.com/jp/events/aws-event-resource/archive/?cards.sort-by=item.additionalFields.SortDate&cards.sort-order=desc&awsf.tech-category=*all&cards.q=msk&cards.q_operator=AND)
- [qiita Apache Kafkaについてまとめる](https://qiita.com/hirooka0527/items/d15e479fa2ded428834d)
- [Apache Kafka の基本](https://tutuz-tech.hatenablog.com/entry/2019/03/16/155501)


