# S3の処理
## S3とローカルディレクトリを同期する
AWS CLIを利用して、ローカルのディレクトリとS3のディレクトリを同期する

コマンドとしては左側から右側へコピーをする
```
aws s3 sync [FROM_DIR] [TARGET_DIR] --exact-timestamps
```
- `--exact-timestamps`を付与すると、タイムスタンプを見て、同期を判断する（デフォルトはファイルサイズ）
- `--delete`を付与するとコピー元にないファイルを削除しようとする


### S3にあるファイルをローカルに同期
```
aws s3 sync s3://[BUCKET_NAME] [LOCAL_DIR] --exact-timestamps
```


### ローカルにあるファイルをS3に同期
```
aws s3 sync  [LOCAL_DIR] s3://[BUCKET_NAME]　--exact-timestamps　--delete
```


### 参考文献
- [AWS CLIでS3操作(ls,mb,rb,cp,mv,rm,sync)](https://www.wakuwakubank.com/posts/642-aws-cli-s3/#index_id15)
- [syncのオプション](https://book.st-hakky.com/docs/aws-s3-sync/)










## ライフサイクルの設定
S3に格納されるオブジェクトに対して、ライフサイクルを設定することで、一定期間が経った段階でストレージクラスのレベルを変更したり、削除したりすることができる。


### ルールのアクション
ライフサイクルで設定することができるルールについて整理する。

![](img/s3_lifecycle_rule.png)

- オブジェクトの最新バージョンをストレージクラス間で移動  
    期限を迎えたオブジェクトをS3から別のストレージクラスに移動させる

- オブジェクトの非現行バージョンをストレージクラス間で移動  
    期限を迎えたオブジェクトの古いバージョンをS3から別のストレージクラスに移動させる（バージョニングが有効の場合のみ）

- オブジェクトの現行バージョンを有効期限切れにする  
    - バージョニングが有効：古いバージョンとなる
    - バージョニングが無効：削除される

- オブジェクトの非現行バージョンを完全に削除  
    期限を迎えたオブジェクトの古いバージョンを削除する


### 設定方法
対象のバケットを選択して`管理`タブを開き`ライフサイクルルールを作成`を選択

![](img/s3_lifecycle_setting.png)

ライフサイクルルール名を指定して、`プレフィックス`には、対象となるフォルダを記述する。  
※S3 バケットからのフルパスではなくて、対象のフォルダ名だけでOK


![](img/s3_lifecycle_prefix.png)


ライフサイクルのルールを設定して、ルールが適用される日数（作成されたからの日数）を指定する

![](img/s3_lifecycle_day.png)


### 設定確認
今回作成されたルールが各オブジェクトに適用されているかのルールを確認する。

設定したprefix配下のオブジェクトを選択し、プロパティの中に`オブジェクト管理の概要`という項目があり`有効期限ルール`の箇所に削除日時が表示されている。

![](img/s3_lifecycle_check.png)



### 削除タイミングについて
挙動としては、設定された日時を迎えたら9:00(JST)に非同期の削除バッチに追加されて、削除が開始される。
設定時に削除の期限を迎えていた場合は、次の9:00(JST)に削除バッチに追加される。

処理としては、非同期のバッチに入ってから削除されるので9:00に削除されるとは限らない。金額は設定時で換算される。


### 注意事項
ライフサイクルによって、フォルダ配下のファイルが全て削除されると、フォルダ自体も削除されてしまう点に注意。

データをアップロードするときにもパスを指定するとフォルダごと作成してくれるので、影響はないはず。


### 参考文献
- [S3のライフサイクルルールのアクションを理解する](https://www.capybara-engineer.com/entry/2021/09/16/151849)  
    設定できるルールのアクションについて解説している。

- [S3ライフサイクルルールで古いオブジェクトを自動削除する](https://nakada-r.com/2021/01/s3-lifecycle/)  
    一番丁寧に設定順序を整理してくれている

- [削除ルールを作成した時点ですでに期限が切れているオブジェクトを、ライフサイクルルールで削除するときの削除タイミングを教えてください](https://dev.classmethod.jp/articles/tsnote-tsexpiredobject-delete-timing/)  
    削除のタイミングについて解説している






## S3レプリケーション
S3のレプリケーションを利用することで、以下のようなメリットを享受できる
- バックアップのバケット複製
- ログの単一バケット集約
- 異なるアカウント間のオブジェクト連携

### クロスリージョン・同一リージョンのレプリケーション
S3のレプリケーションにはリージョン間でレプリケーションを行うCRR(Cross-Region Replication)と同一のリージョンでレプリケーションを行うSRR（Single-Region Replication)がある。

### 注意点
- レプリケーション設定前に存在しているオブジェクトはレプリケーションされない
- 双方のバケットでバージョニングの有効化が必要
- ライフサイクルのアクションなどはレプリケーションされない


### 通信経路について
明示的に記述はないが、SRRではAWS内部のトラフィックを利用しているので、料金に通信量などが書かれていない。
- [オブジェクトのレプリケーション](https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/replication.html#replication-configurations-rules-considerations)



### 同一リージョンで異なるアカウント間のS3でレプリケーション
手順は以下
- 事前準備
    - S3バケットの作成
    - バージョニングの有効化
    - リソースの格納
- レプリケーションルールの設定
- IAMポリシーの設定
- バケットポリシーの設定

### 事前準備
#### S3バケットの作成
Account-AとAccount-BでS3バケットを作成する。
- 両方を同一リージョン（ap-northeast-1)
- バージョングを有効化
- パブリックアクセスブロックを有効化

![](img/s3_replication_bucket_setting.png)

#### 送信元バケットのレプリケーション設定
S3バケットの設定タブからレプリケーションルールを作成する

![](img/s3_replication_make_rule.png)

具体的には以下の内容を設定
- 基本設定
    - ルール名：`myaccount_to_ma_replication_rule`
    - ステータス：有効

![](img/s3_replication_rule_setting_1.png)

- ソースバケット
    - スコープ：レプリケーション対象を限定可能だが、今回は全てを対象とする

![](img/s3_replication_rule_setting_2.png)


- 送信先
    - 別アカウントの場合、IDとバケット名を指定
    - 送信先のオブジェクトの所有者をバケットの所有者とする

![](img/s3_replication_rule_setting_3.png)

- IAMロール
    - 新しいIAMロールを作成する

![](img/s3_replication_rule_setting_4.png)

- 暗号化：今回はデフォルトのまま
- 送信先ストレージクラス：今回はデフォルトのまま
- 追加のレプリケーションオプション
    - レプリケーション時間のコントロール (RTC)を選択することで15分以内にコピーがされる

![](img/s3_replication_rule_setting_5.png)


#### 新規で作成されたIAMの確認
以下のポリシーが付与されている。
次の送信先の設定で利用するため、IAMロールのARNをメモしておく。
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket",
                "s3:GetReplicationConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectVersionTagging",
                "s3:GetObjectRetention",
                "s3:GetObjectLegalHold"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::＜送信元バケット＞",
                "arn:aws:s3:::＜送信元バケット＞/*",
                "arn:aws:s3:::＜送信先バケット＞",
                "arn:aws:s3:::＜送信先バケット＞/*"
            ]
        },
        {
            "Action": [
                "s3:ReplicateObject",
                "s3:ReplicateDelete",
                "s3:ReplicateTags",
                "s3:ObjectOwnerOverrideToBucketOwner"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::＜送信元バケット＞/*",
                "arn:aws:s3:::＜送信先バケット＞/*"
            ]
        }
    ]
}
```

#### 送信先バケットのポリシー設定
送信先バケットにて、バケットポリシーを編集する
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::＜送信元アカウントID＞:role/service-role/＜送信元IAMロール＞"
            },
            "Action": [
                "s3:ReplicateDelete",
                "s3:ReplicateObject",
                "s3:ReplicateTags",
                "s3:ObjectOwnerOverrideToBucketOwner"
            ],
            "Resource": "arn:aws:s3:::＜送信先バケット＞/*"
        }
    ]
}
```

#### 動作確認
送信元のバケットにオブジェクトを格納する。
アップロードしたオブジェクトのプロパティからレプリケーションステータスを確認するとレプリケーションの状況を確認することができる。

![](img/s3_replication_status_pending.png)

15分すると、送信先にオブジェクトがアップロードされる

![](img/s3_replication_status_complite.png)


#### S3レプリケーションをイベント契機にする場合
S3のレプリケーションによって、ファイルがアップロードされた場合のイベントは`S3:ObjectCreated:Put`であるので、注意。

ちなみに、S3 syncコマンドによるファイルアップロードは`S3:ObjectCreated:Copy`となる。



#### 参考文献
- [クラスメソッド](https://dev.classmethod.jp/articles/try-s3-cross-account-replication/)
- [S3 replictionにおけるイベント連携](https://dev.classmethod.jp/articles/s3event-difference-between-s3sync-and-s3replication/)
