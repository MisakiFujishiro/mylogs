## Cognitoで認証をして、AWSのリソースにアクセスする
実施手順とポイント
1. ConitoでUser Poolを作成する
1. CognitoでIDPoolを作成する 
1. Cognitoの認証されたユーザーに対するIAM権限を設定する。
1. AWS CLIからログイン
1. Cognitoへ問い合わせしてクレデンシャルを取得する
1. クレデンシャルを登録して、AWS CLIからS3にアクセス
1. 【＋α】ルールベースでIAMロールを割り当てる



### 参考文献
- [クレデンシャルの取得方法](https://dev.classmethod.jp/articles/get-aws-temporary-security-credentials-with-cognito-id-pool-by-aws-cli/)  
：一番参考になるAWS CLIでCognitoのクレデンシャルを取得する方法から、ルールベースで付与するIAMを変更する手順が整理されている
- [Cognito を使ったユーザ認証で S3 にアクセスしてみる](https://www.aws-room.com/entry/cognito-s3)  
：pythonを利用して、cognitoから認証情報を受けてS3へのアクセス制御を検証している
- [PythonからCognitoのUSER_PASSWORD_AUTHとUSER_SRP_AUTHでのトークン取得](https://yomon.hatenablog.com/entry/2022/8/cognito_python)  
：pythonを利用してクレデンシャルを取得するところまで、クライアントシークレットを有効化している時に対応しているところまで整理してくれている
- [S3 の読み書きを Cognito で認証する方法](https://dev.classmethod.jp/articles/cognito-trigger-allow-access-per-identity-id/)  
：ディレクトリにユーザーIDを付与することで、認証したユーザーのIDを冠したディレクトリしかアクセスすることができなくなる。
- [外部ユーザが安全かつ直接的に Amazon S3 へファイルをアップロードできるようにする方法](https://aws.amazon.com/jp/blogs/news/allowing-external-users-to-securely-and-directly-upload-files-to-amazon-s3/)  
：amplifyを利用して、アップロードページをアップロードする方法


### Cognitoでユーザープールを作成
詳細は[別ページ](https://misakifujishiro.github.io/mylogs/Artifact/cognito.html#cognito)参照

この時に、アプリクライアントの設定で、`クライアントシークレットの作成`については無効化しておき、`ALLOW_ADMIN_USER_PASSWORD_AUTH`を有効化する  
また、test userも作成しておく（有効化してもなんとかなるけど、Cognitoへのログイン設定が面倒）

![](img/cognito_awscli_auth_point.png)


### CognitoでIDプールを作成
- idPool名  
    同じユーザー内で一意にする    
- 認証していないID  
    有効化すると、認証していないユーザーへの権限が設定可能
- 認証プロバイダ  
    前節で作成したCognitoのユーザープールの情報を設定

![](img/cognito_idpool_setting.png)

作成したIDプールのナビゲーションペインのサンプルコードからIDプールのIDを確認できる。
後から利用するので記録しておく。

![](img/cognito_idpool_id.png)



### 紐づくIAMの作成
作成したIDpool名を冠したIAMロールが存在するはずなので、そのロールのポリシーを編集していく。

![](img/cognito_idpool-iam.png)

ポリシーには、Cognitoで認証したユーザーごとのバケットの中でも`フェデレーティッドユーザーの ID${cognito-identity.:sub}`のディレクトリに紐づいたオブジェクトにのみアクセスできるポリシーを付与数r。
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::ma-fujishiroms-bucke"],
      "Condition": {"StringLike": {"s3:prefix": ["cognito/"]}}
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::ma-fujishiroms-bucket/cognito/${cognito-identity.amazonaws.com:sub}",
        "arn:aws:s3:::ma-fujishiroms-bucket/cognito/${cognito-identity.amazonaws.com:sub}/*"
      ]
    }
  ]
}
```

UnAuthユーザーには情報を付与しない。




### AWS CLIからのアクセス
#### ログイン
AWS CLIの場合は以下のコマンドでログインする  
Cognitoのユーザープールで動作確認用に2つのアカウントを作成しておく

初期設定
- USER_POOL_IDはCognitoのユーザープールの全般設定から取得
- CLIENT_IDはCognitoのユーザープールのアプリクライアントから取得
- IDENTITY_POOL_IDはCognitoのIDプールのサンプルコードから取得（前節でメモした）
```
USER_POOL_ID=ap-northeast-1_xxxxxxx
CLIENT_ID=xxxxxxxxxxxx
IDENTITY_POOL_ID=ap-northeast-1:xxxxxxxxxx
USER_NAME=YOUR_USER_NAME
USER_EMAIL=YOUR_MAIL_ADDRESS@gmail.com
REGION=ap-northeast-1
PASSWORD="Dummy456"
COGNITO_USER_POOL=cognito-idp.${REGION}.amazonaws.com/${USER_POOL_ID}
```

ログインして、ID Tokenの取得
(`USERNAME`はUSER＿NAMEでもUSER_EMAILでも認証が通った)
```
ID_TOKEN=$(aws cognito-idp admin-initiate-auth \
  --user-pool-id ${USER_POOL_ID} \
  --client-id ${CLIENT_ID} \
  --auth-flow ADMIN_NO_SRP_AUTH \
  --auth-parameters "USERNAME=${USER_NAME},PASSWORD=${PASSWORD}" \
  --query "AuthenticationResult.IdToken" \
  --output text) && echo ${ID_TOKEN}
```




#### クレデンシャルの取得
IDENTITY_IDを取得
```
IDENTITY_ID=$(aws cognito-identity get-id \
  --identity-pool-id ${IDENTITY_POOL_ID} \
  --logins "${COGNITO_USER_POOL}=${ID_TOKEN}" \
  --query "IdentityId" \
  --output text) && echo ${IDENTITY_ID}
```
Identify IDを利用して、`クレデンシャル`を取得
```
OUTPUT=$(aws cognito-identity get-credentials-for-identity \
  --identity-id ${IDENTITY_ID} \
  --logins "${COGNITO_USER_POOL}=${ID_TOKEN}") && echo ${OUTPUT}
```

返却されたクレデンシャルの`AccessKeyID`、`SecretKey`、`SessionToken`を環境変数に設定
```
AWS_ACCESS_KEY_ID=`echo $OUTPUT | jq -r '.Credentials.AccessKeyId'`
export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=`echo $OUTPUT | jq -r '.Credentials.SecretKey'`
export AWS_SECRET_ACCESS_KEY
AWS_SECURITY_TOKEN=`echo $OUTPUT | jq -r '.Credentials.SessionToken'`
export AWS_SECURITY_TOKEN
```

### S3バケットの作成
作成したIAMの権限に合わせて、S3バケットを作成する。
バケット内に作成するフォルダについても、`cognito/CognitoUserID`とする。
UserIDは先ほどの手順でログインすることでCognitoのID poolに追加されている値を利用する

![](img/cognito_idpool_added.png)

以下のようなディレクトリ構成となる
```
bucket
|
|--cognito
    |
    |--ap-northeast-1:xxxxxxxxx
    |
    |--ap-northeast-1:yyyyyyyyy
```

### 動作確認
xxxxxxxのクレデンシャルを環境変数に設定しているときとyyyyyyyyyのクレデンシャルを環境ヘンスに設定している時で、アクセスできるS3が異なることを確認する
```
aws s3 cp --region ap-northeast-1 s3://ma-fujishiroms-bucket/cognito/ap-northeast-1:xxxxxxxxx/alb_setting_basic.png ./


aws s3 cp --region ap-northeast-1 s3://ma-fujishiroms-bucket/cognito/ap-northeast-1:yyyyyyyyy/auth0_tenant.png ./
```






### ユーザーごとに紐づけるロールを変更する場合
#### IAMロールの作成
IAMのコンソール画面から、新しいロールを作成し、エンティティタイプをウェブアイデンティティにする。
プロバイダーとしてCognitoを選択して、IDプールのIDを書き込み、ポリシーを付与してロールを作成する

![](img/cognito_iam_setting.png)

#### IDプールでルールを設定
`IDプールの編集`から、認証プロバイダを選択して、`ルールを使用してロールを選択`するから、ルール設定
例えば、「emailにxxxxを含む」などの条件で付与するIAMを変更できる

![](img/cognito_iam_condition.png)