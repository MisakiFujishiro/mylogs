## java spring
### MVCとは
アプリケーションフレームワークの一つ。アプリケーションの処理を Model/View/Controllerの３つに分ける。
#### Model
データやDBへのアクセスなどを担う

#### View
クライアントからの入力やクライアントへの出力などを担う

#### Controller
ModelとViewをつなぐ。
Viewが受け取るクライアントからの入力をModelへ渡して処理を行い、Viewへ処理内容を連携する。

### Springとは
MVCの考え方からSpring MVCという考え方が生まれる。
SpringMVCはライブラリなどが多くて、扱いが難しかった。
SpringMVCを使いやすくしたフレームワークとしてSpringBootが生まれた。



## アノテーション
### @Controller
SpringBootにおいてControllerのクラスであることを認識させる

### @RequestMappng
クライアントからのリクエストに対して、メソッドなどの対応付ができる  
`return`で返却されるStringはViewResolverでファイル名に変換されてクライアントに返却される。


## References
- [MVCとSpring・コントローラーのアノテーション](https://qiita.com/TEBASAKI/items/267c261db17f178e33eb)