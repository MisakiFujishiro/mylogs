# MSKにおけるメッセージの優先順位について
kafkaに送信されたメッセージに対して、優先順位をつけて優先度の高いメッセージを優先して処理させたい。

Apache kafkaは公式にはそのような機能を提供していないので、いくつかの実装例を調査









## 優先度付きのトピックを作成
[Kafkaはトピックまたはメッセージの優先度をサポートしていますか？](https://www.web-dev-qa-db-ja.com/ja/apache-kafka/kafka%E3%81%AF%E3%83%88%E3%83%94%E3%83%83%E3%82%AF%E3%81%BE%E3%81%9F%E3%81%AF%E3%83%A1%E3%83%83%E3%82%BB%E3%83%BC%E3%82%B8%E3%81%AE%E5%84%AA%E5%85%88%E5%BA%A6%E3%82%92%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%81%8B%EF%BC%9F/1053263533/)

■手順  
1. 優先度に応じたTopicを作成する。
2. Consumerでは、優先度に応じたトピック順にメッセージを確認する

■懸念点  
優先度が低いメッセージが大量に送信されているときに、優先度高いメッセージを優先してくれるか。

■確認事項
1. ConsumerのTopicを読み込むプロセスがどのタイミングになっているか確認する必要がある
2. Consumerが2つのTopicをよみこむプロセスを確認する必要がある











## メッセージの中に優先度のキーを追加
Topicを共通として、Producer側でメッセージに対して優先度を付与する
```
kafka-console-producer.sh --broker-list localhost:9092 --topic test \
--property "parse.key=true" \
--property "key.separator=:"
> high_priority_key:{"priority": "high", "data": "some_data"}
> low_priority_key:{"priority": "low", "data": "some_other_data"}

```
Consumer側で優先度を比較する。


■懸念点  
Consumer側でまとめてPartitionのメッセージを読み込んで、優先度の高いメッセージを探すように見える
今はConsumer側で1つのメッセージを受け取っているような印象。
ここから検証が必要か。

次のセクションで説明するkafka ストリームで特定メッセージをフィルターして別トピックに格納する方法が対応の一つだが、それなら元々別トピックに書き込むのと同じ。
今回はProducerからして違うので、Topicを変更するのが一番良い。





## kafkaストリームの利用
[Kafka Streams](https://qiita.com/41semicolon/items/60f92a1db6dfce4303c5)
を利用すると、特定のメッセージをフィルタリングすることが可能なようには見える。

特定のキーを持つメッセージだけをConsumeする場合、Kafka Streamsのfilter()関数を使用して、指定されたキーを持つメッセージだけをストリームからフィルタリングすることが可能に見える。

■懸念点  
filterした後は別のTopicに書き込む処理のようなので、そもそもTopicを書き分ける方が直接的な印象。  
filterしたものを処理するフローも書けるのかもしれないが、処理しなかった方のメッセージがどうなるか不明瞭

```
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Predicate;

KStream<String, String> inputStream = builder.stream("input-topic");
KStream<String, String> filteredStream = inputStream.filter(new Predicate<String, String>() {
  @Override
  public boolean test(String key, String value) {
    // フィルタ条件を記述する
    // 例えば、valueが"important"であるレコードのみをフィルタする場合は
    // return value.equals("important");
    // のように記述します
  }
});
filteredStream.to("output-topic");
```








## schema Registryの利用
[Schema Registry簡易テスト](https://qiita.com/tomotagwork/items/5e456400197457cc4291)

ProducerとConsumerのやり取をSchema Registryを介して行う

![](img/msk_schemaRegistry.png)

### メッセージ送信時(Producer)
1. メッセージフォーマットを示すschemaを準備
2. SchemaをRegistryに登録する
3. RegistryからIDが返却される
4. idとデータセットをTopicに送信する

### メッセージ受信時(Consumer)
1. Consumer側でschemaに問い合わせて優先度の高いものを確認
2. 優先度の高いidを抽出して処理

■懸念点  
結局Consumer側で優先順位順に処理するロジックがあれば、わざわざschema Resitryは不要な印象
Resistry側で処理済み、未処理のチェックをしているのかが不明（何回も処理指定しまう？）








## Decatonの利用 
優先度をつけたメッセージを優先的に処理はできるらしい。
ただ、Decaton自体は、並列処理を実行するが目的に見えるように見える。
優先順を付与するだけのためにdecatonまで導入するかは要相談
※どれだけドキュメントが充実しているかなどが定かではない・・・・

■懸念点  
改めて、kafkaストリームについて習得する必要があり、難易度が高い可能性あり  
トラブルシューティング時に、Decaton含めて調査が必要