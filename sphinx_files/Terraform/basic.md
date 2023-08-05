# Terraformとは
IaCのためのツールであり、AWS/Azure/GCPなどで利用することができる。

## 公式ドキュメントの読み方
- [HCL2](https://developer.hashicorp.com/terraform/language)  
    基本的な記述方法
- [CLI](https://developer.hashicorp.com/terraform/cli)  
    terraformのコマンドの記述方法
- [provider](https://registry.terraform.io/browse/providers)  
    awsなどのproviderごとのリソースの記述方法
    - Example: 例
    - Argument: 引数
    - Attribute: 出力値



## Terraformの利用方法
### Terraformのインストールを行う
Terraform用のIAM Roleを作成し、profileに設定をしておく

### plan
ソースコードをもとにどのような変更が行われるかを確認することができる
```
terraform plan
```

### apply
tfファイルを作成して実行する。
```
terraform apply
```
でtfファイルを実行する
### 変更した場合(再作成なし)
変更を加えて、applyするだけで、`update`という確認がされて、更新がされる
これはtfstateという、terraformaを実行して、作成した状態を保存しているファイルがあるおかげである。

### 変更した場合(再作成あり)
EC2に対して、user_dataを追加するといった、EC2の再実行が必要な変更を加えてapplyする。
そうすると`replaced`という確認がされて、再作成がされる

### destory
```
terraform destory
```
で作成したものが削除される

### fmt
```
terraform fmt
```
を実行すると.tfファイルを整形してくれる




## 基本構文
HCL2(HashiCorpLanguage2)という独自言語を利用している

記述方法はjsonに似ているが以下が違う。
- コメント記述可能
- : ではなくて = でつなぐ
- 変数や関数を指定可能
- ブロックという単位でリソースを記述する

ブロックタイプと何を記述するかを学習していけばterraformを書いていくことができる

### locals,variablesブロック
ブロックとして、localsとvariablesがある
- locals: 外部から指定不可能
- variables:外部からデフォルトを上学ことができる

これらのブロックで指定した変数はコードないで参照される



### terraformブロック
terraform全体に関わる設定

terraformのバージョンとprovider(AWS/Azure/GCP)のバージョンを固定する


### profileブロック
AWSへアクセスするプロファイルやリージョンなどを設定することができる


### dataブロック
管理対象外のリソースや既存のリソースを読み込ませることができる。

対象のリソースによって、記載が異なる


### outputブロック
作成したリソースを外部参照させる。
このoutputリソースをdataブロックで読み込ませることができる。

### リソースブロック
作成するリソースを記述する。

ラベルを.でつなぐことで、作成しているリソース間を参照することができる

```
# ---------------------------------------------
# Terraform configuration
# ---------------------------------------------
terraform {
  required_version = ">=0.13" # terraformのバージョン
  required_providers { # awsのバージョン
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# ---------------------------------------------
# Provider
# ---------------------------------------------
# awsの基本設定
provider "aws" {
  profile = "terraform"
  region  = "ap-northeast-1"
}

# ---------------------------------------------
# Variables
# ---------------------------------------------
# 外から設定できる変数
variable "project" {
  type = string
}

variable "environment" {
  type = string
}
```

### データ型
HCL2では大きく3種類小さく8種類
- プリミティブ
    - str
    - num
    - bool
- 構造体
    - key-val
    - tuple: 順番と型がきまっている
- コレクション
    - list
    - 配列
    - set


### 組み込み関数
かなりたくさんの組み込み関数がある。

文字列操作や数字の切り捨てなど基本的な操作が可能

![公式ドキュメント](https://developer.hashicorp.com/terraform/language/functions)

## file分割
```
terraform apply
```
については、カレントディレクトリないの.tfファイル全てを読み込んで実行する。
注意点としては、サブディレクトリは読み込まない点に注意


