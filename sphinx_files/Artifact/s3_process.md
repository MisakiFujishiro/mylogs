## S3の処理
### S3とローカルディレクトリを同期する
AWS CLIを利用して、ローカルのディレクトリとS3のディレクトリを同期する

コマンドとしては左側から右側へコピーをする
```
aws s3 sync [FROM_DIR] [TARGET_DIR] --exact-timestamps
```
- `--exact-timestamps`を付与すると、タイムスタンプを見て、同期を判断する（デフォルトはファイルサイズ）
- `--delete`を付与するとコピー元にないファイルを削除しようとする


#### S3にあるファイルをローカルに同期
```
aws s3 sync s3://[BUCKET_NAME] [LOCAL_DIR] --exact-timestamps
```


#### ローカルにあるファイルをS3に同期
```
aws s3 sync  [LOCAL_DIR] s3://[BUCKET_NAME]　--exact-timestamps　--delete
```


### 参考文献
- [AWS CLIでS3操作(ls,mb,rb,cp,mv,rm,sync)](https://www.wakuwakubank.com/posts/642-aws-cli-s3/#index_id15)
- [syncのオプション])(https://book.st-hakky.com/docs/aws-s3-sync/)
