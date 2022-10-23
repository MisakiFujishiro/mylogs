# Code Series
ソースコードの反映をトリガーとして、ビルドデプロイといった一連のデリバリーを支援するサービス群  
ソースコード管理サービスのCode Commit、ビルドサービスのCode Build、デプロイサービスのCode Deploy、これらの一連の処理を連携するデリバリーサービスのCodePipelineの総称

## Code Commit
フルマネージドなソース管理（git repository）サービス  
メリットとして、スケーラブルでセキュアであり、既存のgitツールともシームレスに連携
### 設定手順
基本的には、リポジトリ名を作成するだけ  



## Code Build
ソースコードをコンパイル・テスト実行して、デプロイ可能なSWパッケージを作成するフルマネージドなビルドサービス  
メリットとして、ビルド用のサーバのプロビジョニング・管理が不要となる  
codebuildの成果物はartifactと呼ばれる。格納するS3バケットを作成しておく

### 設定手順
1. artifactの格納場所作成(S3のバケット作成
2. codebuildプロジェクトの設定
   - ソースプロバイダの設定  
   ソースコードのプロバイダでリポジトリやブランチ・タグなどを設定する  
   - buildの環境/ランタイムの設定する
   - アーティファクトの設定(S3で作成したバケットを指定)
   - ServiceRoleの設定  
   `AWSCodeDeployDeoloyerAccess`を付与する
   - buildspec.yamlの作成


フォルダ構成
```
|-src
|  |---index.html
|
|-buidlspe.yaml
```


buildspec.ymlの記載項目
  - version：buildspec.ymlファイルのバージョン指定0.2推奨
  - phases：ビルド実行時にCodeBuildが実行するコマンド
    - install：インストール時にCodeBuildが実行
    - pre_build：ビルド前にCodeBuildが実行（ECRへの認証など）
    - build：ビルド実行中にCodeBuildが実行
    - post_build：ビルド後にCodeBuildが実行(ECRへのpushなど)
  - artifacts：ビルドの出力結果の保存先
    - files：必須項目でデプロイする成果物を指定  
    '**/*'を指定するとディレクトリは以下全てをデプロイする資産として指定  
    - base-directory：デプロイ対象のルートディレクトリを指定

buildspec.yml
```
version: 0.2

phases:
  build:
    commands:
      - aws deploy push --application-name [YOUT_CODEDEPLOY_APPLICATION_NAME] --s3-location s3://[YOUR_BUCKT_NAME]/artifact.zip --source src
artifacts:
  files:
    - '**/*'
  base-directory: src
```


## Code Deploy
EC2・Lambdaに対してデプロイを行うサービス  
AutoScaling構成に対しても自動で反映してくれる

### 設定手順
1. codeDeploy用のRoleを作成する  
  IAM>ROLEの作成>ユースケースとしてCodeDeployを選択
2. codeDeployのアプリケーション作成
   - アプリケーション名やデプロイ先環境を設定（EC2/ECS/Lambda）
3. deploy Groupの作成
   - 事前に設定したサービスロールを選択
   - 環境設定でデプロイ対象を選ぶ（ターゲットグループやタグで対象を絞れる） 
4. appspec.ymlの作成  


フォルダ構成
```
|-src
|  |---index.html
|  |---appspec.yml
|
|-buidlspe.yaml
```

appspec.ymlの記載項目
- version：0.0のみ
- os：linux or Windows
- files：ビルドした結果をどこに配置するかの設定
- hook：インストール前後の処理

buildspec.yml
```
version: 0.0
os: linux
files:
  - source: index.html
    destination: /var/www/html/
```

## Code Pipeline
フルマネージドな継続的デリバリーサービス  
ソースコードの変更をトリガーとして、ビルド・デプロイといった一連の流れを自動的に実行する
### 設定手順
1. パイプライン名称  
パイプラインの構成を考慮の上セッティング
2. ソースステージ設定  
CodeCommitとの連携を設定し、検知するリポジトリやブランチ名を設定する

![](img/codepipelene_setting.png)

3. ビルドステージ設定  
   - デプロイプロバイダーにCodeBuild
   - 設定済のアプリケーションやデプロイグループを選択

4. デプロイステージ設定  
デプロイ先を設定する。 S3への直接デプロイや、ECS/EC2へのデプロイが可能


### S3へのCICD
- ビルドステージはスキップ
- デプロイステージでプロバイダーでS3を設定して、リージョンやバケットを選択

### EC2へのCICD
- EC2の作成
タグ名でCICDの対象を設定できるので、タグ名を設定しておくと良い

- EC2にcode deploy エージェントをインストールしておく  
[AWS Code Deploy エージェント](https://docs.aws.amazon.com/ja_jp/codedeploy/latest/userguide/codedeploy-agent-operations-install.html)のコマンドラインからのインストールを実行

> wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install



#### トラブルシューティング:codeBuildを手動で実行するとエラー
> [Container] 2022/10/23 13:46:20 Phase context status code: COMMAND_EXECUTION_ERROR Message: Error while executing command: aws deploy push --application-name h4b-cicd-codedeploy-application --s3-location s3://h4b-cicd-artifact-fujisiroms/artifact.zip --source src. Reason: exit status 255

appspec.ymlがsrcディレクトリは以下になかったことが原因

#### トラブルシューティング:codeDeployを手動で実行するとエラー
> The overall deployment failed because too many individual instances failed deployment, too few healthy instances are available for deployment, or some instances in your deployment group are experiencing problems.

appspec.ymlの文法がミスったまま、Deployしていたのが原因。appspec.ymlを修正してからbuildとdeployを実行


## githubとCodeCommitのミラーリング
- 公開鍵・秘密鍵の作成  
LocalPCで以下を実行
> ssh-keygen -t rsa -b 4096 -m PEM -C <メールアドレス>

作成された公開鍵と秘密鍵は以下コマンドでクリップボードにコピーすると扱いやすい
> pbcopy < ~/.ssh/id_rsa.pub

> pbcopy < ~/.ssh/id_rsa


- IAMユーザーに公開鍵を紐づける  
IAM>アクセス管理>ユーザー>AWS CodeCommitのSSHキーにパブリックキーをアップロード  
SSHキーの`ID`をメモしておく

![](img/codecommit_iam_setting.png)

- githubに秘密鍵をSecretes登録  
github>Setting>Secrets>Actions>New repository secrets  
以下の情報を登録
  - 秘密鍵
    - Name:CODECOMMIT_SSH_PRIVATE_KEY
    - Value:プライベートキーの中身
  - SSHキーID
    - Name：CODECOMMIT_SSH_PRIVATE_KEY_ID
    - Value：SSHキーのID


- githubとgitcommitを紐づける  
github>Actions>New Work Flow>set up a workflow

```
name: Mirroring

on: [ push, delete ]

jobs:
  to_codecommit:
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v1
      - uses: pixta-dev/repository-mirroring-action@v1
        with:
          target_repo_url:
            ssh://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/[YOUR REPOSITORY NAME]
          ssh_private_key:
            ${{ secrets.CODECOMMIT_SSH_PRIVATE_KEY }}
          ssh_username:
            ${{ secrets.CODECOMMIT_SSH_PRIVATE_KEY_ID }}
```

- 動作確認  
localにgithubのリポジトリをcloneして、新しいブランチを作ったり、ファイル編集してから、gitpushすると、codeCommitにまで反映されている  



## References
- [GitHubをCodeCommitにミラーリングする](https://chibinfra-techblog.com/github-with-aws-codecommit/)
- [buildspec.ymlコマンド](https://qiita.com/s_ryota/items/803b44caacac12fd2439)
- [Codebuild の buildspec.yaml](https://qiita.com/leomaro7/items/1eca2b814930f98f3ff9)
- [Codedeploy の 概要や appspec.yaml](https://qiita.com/leomaro7/items/40f126a4f0c23d511e88)
