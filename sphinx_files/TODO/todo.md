# 塾の活動
## week5(10/31-)
### java チュートリアル 7h
動作確認まで完了。mvnarchetype:generateコマンドやMVCの基本を整理
sts4.xをインストールしていることに気づいて、sts3.xをインストール
ここで、立ち上がらない問題やrun on serverがでないなどのトラブルで時間をだいぶ使った。
javaのバージョンを変えたりstsのiniファイル編集したりして対応
serverがでなかったのはワークスペースの設定も悪かった？？

tutorialでドメイン部分の作成まで完了。Appの方も少しだけ作成して、一覧表示まではできた。
今までは何もわかっていなかったところからお作法とかは少しずつわかってきた。
細かいアノテーションの意味とかは調べつつ。。。わからないところはメモしている

![](img/20221104-1.png)

### AWS code artifact勉強(3h)
じつ業務の方で利用する機会があったので勉強した。  
jarファイルなどの成果物を共有することができるリポジトリ。   
curlコマンドでアップロードはできたが、mvn deployはできていない。
実際のアプリの時に使ってみて、使い方を整理したい。
### わからなかったこと
1. sts4でやったからか、run on serverがなくて困った【解決】
    - sts3をインストールし直して、javaのバージョンも1.8に変えた
    - PJを開く場所をデフォルトにしたらうまくいった
2. CodeArtifactへの登録をmvn deployからできなかった【宿題】
  - stsだとmvn deployはどこからするの？
3. repositoryとserviceで定義するメソッドについて【解決】→[アプリケーションのレイヤと役割](https://terasolunaorg.github.io/guideline/5.5.1.RELEASE/ja/Overview/ApplicationLayering.html)
  - repositoryはCRUD処理のうちで使うもの
  - serviceは業務ロジックとして使うもの？チュートリアルはいいけど何を作るのかの定義が大事？
4. @injectって何？いくつか記事を読んでみたけど、まだよくわからない。【解決】→- [DIとAOPの神動画](https://www.youtube.com/watch?v=LGtdpsmMfvI)


---
## week6(11/4-)
### 全体の計画見直し

チュートリアル【10-12月】
1. java tutorial（11月中）
   - TODO App 【完了】
   - TODO App REST【実施中】
   - TODO App Security【実施中】
   - TODO App Sesstion【実施中】

2. Spring TUtorial【スキップ？】

3. AWS Handson(11月中)
   - cicd【完了】
   - ecs【完了】
   - AI + Lambda

4. 塾長のWeb記事「クラウドネイティブアプリケーションの基本【スキップ？】

5. 塾長のWeb記事「AWSで実践! 基盤構築・デプロイ自動化【12-1月】


アプリケーション検討【12-2月】
1. 使ってみたいサービスリストアップ
   - Cognito
   - AWS CodeArtifact
2. アプリケーション検討
3. 全体構成検討
4. CICD基盤作成
5. アプリケーションの本格作成



報告準備【3月】


2月くらいから準備して、３月に頑張る。


### java チュートリアル (7h)
DIとAOPの理解
[動画](https://www.youtube.com/watch?v=LGtdpsmMfvI)見てだいぶスッキリした。  
DIはコンテナでBean（インスタンス）を管理して、インスタンスの受け渡しを担うことでメソッド間を疎結合にする。という理解。  
あとは、実際に使いながら理解を深める

TODOアプリの作成
実装完了(MyBatisを利用したインフラ層実装まで)  

![](img/20221104-2.png)


### AWS ECSのH4B
今までもやったことがあったが、良い復習になった。
fargateからの起動方法が新規で理解できた。
task定義とサービス定義でFargateで起動する設定を行う。

### わからなかったところ
#### Mapper beanMapperの役割について  
TodoControllerの実装中で登場するbeanMapper君が何者かわからない。


多分処理的には、object型の変換をしている
todoFormはtodoTitleを持っていて、Todo.classにもあるからObjectを変換している。
他のプロパティは空っぽで変換してくれて、後続のcreateメソッドでプロパティを追加しているっぽい。  

Q1.なんでInjectしているのか不明。。。import で使うのとは別なの？？
```
@Inject
 Mapper beanMapper;

  Todo todo = beanMapper.map(todoForm, Todo.class);

```

#### Controllerとjspでの変数のやり取りについて

①titleのnullチェックは文字数チェックのエラー結果はbindingResultにある
```
bindingResult.hasErrors()
```

②serviceに書かれた業務エラー（５個以上のTodo）はmodelにある  
Q2.modelってkey-valueな気がするのに、keyを指定しない理由がわからない

```
try {
   todoService.create(todo);
} catch (BusinessException e) {
   // (7)
   model.addAttribute(e.getResultMessages());
   return list(model);
}
```

③処理成功はattributesにある  
```
// (8)
attributes.addFlashAttribute(ResultMessages.success().add(
       ResultMessage.fromText("Created successfully!")));
return "redirect:/todo/list";
}
```

jsp側での処理では、messagePanelがResultMessagesを表示させるので、②と③は表示されるらしい。
```
<t:messagesPanel />
```
Q3. modelとAttribute違う場所にあるけど、jspに渡ってきているの？
しかも異なる変数のなか（modelとattribute)にあるResultMessagesから勝手にみてきてくれるの？



①の表示はform:errorsが担っているっぽい
```
<form:errors path="todoTitle" /><!-- (4) -->
```
@modelAttributeで指定したtodoFormのプロパティにtodoTitleがある。

Q4.todoTitleのValidチェックがform:errorsでエラーで結果を表示できるの？？



#### Mybatsを利用した実装  
RepositoryImplでは@RepositoryでBeanにしていたからコンテナでDIしてくれていたけど、

Q5. Repository.xmlでは@付与をしていないのでは？勝手にBeanにしてくれるの？


TodoServiceImplでInjectしているけど、@Repositoryがなくなったので、
コンポーネントスキャンされていない。
DIコンテナの中にBeanがないのではないか？
```
 @Inject// (3)
 TodoRepository todoRepository;
```

ここの部分は、SQLの結果とDomain/modelのプロパティを紐づけているだけっぽいし
```
 <resultMap id="todoResultMap" type="Todo">
        <id property="todoId" column="todo_id" />
        <result property="todoTitle" column="todo_title" />
        <result property="finished" column="finished" />
        <result property="createdAt" column="created_at" />
    </resultMap>
```
この辺の処理は、Interfaceとの紐付けをおこなっているだけっぽい。
```
<select id="findById" parameterType="String" resultMap="todoResultMap">
```



# TODO
## DONE
- sphinx環境構築
- githubアカウント作成
- javaspringは私用のパソコンでstsを構築
- dockerコンテナ環境構築
- java環境をdockerコンテナに固める手順整理
- 開発環境図整理
- H4B CICD
- CodeArtifactの勉強
- H4B ECS 

## AWS
- H4B S3+AI+Lambda Series
- AutoScaling
- [AWSで作るクラウドネイティブアプリケーションの基本](https://news.mynavi.jp/techplus/series/AWS/)
- [AWSで実践! 基盤構築・デプロイ自動化](https://news.mynavi.jp/techplus/series/AWSAuto/)


## java
- TERASOLNAのチュートリアル（私用
- SpringBootチュートリアル（社内環境