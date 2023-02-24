# Amazon CognitoとSpring Securityを利用したOAuth2ログイン
塾長の記事[AWSで作るマイクロサービス](https://news.mynavi.jp/techplus/series/aws_2/)を参考に認証認可の仕組みを実装する。
図は[ドラフト版](https://debugroom.github.io/mynavi-doc-draft/index.html)の方が見やすい
- [Cognitoの設定①](https://news.mynavi.jp/techplus/article/techp5319/)
- [Cognitoの設定②](https://news.mynavi.jp/techplus/article/techp5368/)
- [Lambda関数の設定①](https://news.mynavi.jp/techplus/article/techp5466/)
- [Lambda関数の設定②](https://news.mynavi.jp/techplus/article/techp5496/)
- [Spring Securityの設定①](https://news.mynavi.jp/techplus/article/aws_2-19/)
- [Spring Securityの設定②](https://news.mynavi.jp/techplus/article/aws_2-20/)
- [Spring Securityの設定③](https://news.mynavi.jp/techplus/article/aws_2-21/)



## Cognitoの設定
CognitoはAWSの認証/認可のサービス

ユーザープールとIDプールという２つの大きな機能を提供する
- ユーザープール（ユーザー情報データベース）  
    - ユーザー情報やユーザー属性を定義可能
    - ユーザーの作成やサインイン管理    
    - サードパーティとの連携
    - MFAの設定が可能   
- IDプール（認可情報機能を提供する）  
    認証されたユーザーに対して、Tokenを検証して、一時的な認可情報を付与する





### Cognitoのユーザープールの作成
以下の項目を設定していく
- 名前  
    userpoolの名前
- 属性  
    ログインIDなど、ログインユーザーの情報に関しての設定
- ポリシー  
    パスワードに関するポリシーを設定
- MFAとアカウント回復  
    MFAの設定やアカウントの回復方法の設定
- メッセージのカスタマイズ  
    ユーザーに発出するメールに関する設定
- タグ  
    Cognitoに関するタグの設定
- デバイス  
    一度ログイン完了したブラウザ情報を通じてログインを継続する機能
- アプリクライアント  
    アプリクライアントの設定を行い、クライアント名ややりとりするトークンの設定、クライアントシークレットに関する設定を行う。
- トリガー  
    ユーザープールにおけるイベントを契機として実行するLambdaの設定を行う


![](img/cognito_userpool_settings.png)

#### 名前の設定
userpoolの名前を設定する

![](img/cognito_userpool_name.png)

#### 属性
ログインユーザーのIDや基本設定を定義する

- ユーザー名  
    サインイン時の識別子IDについて設定  
    今回は検証した（ユーザーからの応答があった）Eメールを設定
- Eメール・電話番号  
    Eメールや電話番号自体をユーザーIDにする場合に設定するオプション
- 大文字小文字の区別  
    大文字小文字の区別設定で、区別を推奨している
- 標準属性  
    標準で準備されている、ユーザープールで保持する属性情報（今回は氏名と名前）
- カスタム属性  
    開発者がカスタムで設定できる、ユーザープールで保持する属性情報（今回はログインIDと管理者フラグ）

![](img/cognito_zokusei.png)



#### ポリシー
パスワードに関するポリシーを設定
- パスワード強度  
    文字数などを設定
- 自己サインアップ  
    管理者だけが、ユーザー登録できるか、一般ユーザーが自分でできるか
- 有効期限  
    ユーザー作成時の一時パスワードについての有効期限で、これを過ぎるとユーザーの作り直しとなる。

![](img/cognito_password.png)



#### MFAとアカウント回復
MFAの設定とパスワードを忘れたときなどのアカウントの回復方法を定義する

- MFAの有効  
    Cognitoを利用したサインアップ・サインインについてMFAを利用するかの設定（今回は不要）
- 回復方法  
    パスワードを忘れたときのリセット方法としてEメールや電話が利用できる
- 確認する属性  
    サインアップやリセット時に確認する属性情報を設定
- SMSのロール  
    MFAや回復にはSMSを利用するので、そのためのロールを作成する（デフォルトでOK）

![](img/cognito_mfa.png)

#### メッセージのカスタマイズ
Cognitoから発出するメールの設定を行う

- Eメールアドレスのカスタマイズ  
    発信リージョンは限られているが、利用しているリージョンと異なっていても特に問題はない  
    発信元のメール設定やリプライ先について設定可能
- SESによるメール発信設定  
    大規模なユーザーに向けて、サービスを提供する場合はEメール対応のための設定（今回は不要）
- Eメール検証メッセージ設定  
    検証メールのカスタマイズ
- ユーザー招待メッセージ設定  
    初回ログイン時の招待メールのメッセージをカスタマイズ

![](img/cognito_email.png)

![](img/cognito_message.png)

#### タグ
Cognitoリソースに対するタグ設定を必要に応じて実施

#### デバイス
ブラウザやデバイス情報を記憶して、ログインを保持する、Remembermeサービス設定を必要に応じて設定

![](img/cognito_device.png)


#### アプリクライアント
ユーザープールを利用するアプリクライアントの設定や、やりとりするトークンやクライアントシークレットの設定を行う。
- アプリクライアント名  
    Cognitoへアクセスするアプリケーションクライアントの設定（適当なものを設定）
- トークンの有効期限  
    リフレッシュトークンの有効期限で、30days
- アクセストークンの有効期限  
    アクセストークン（認可情報）の有効期限で、60minがデフォルト
- IDトークンの有効期限  
    IDトークン（認証情報）の有効期限で、60minがデフォルト
- クライアントシークレットの生成  
    アプリクライアントの正当性を確認するパスワードのようなもので、サーバーサイド側でやりとりするべき情報  
    JSやモバイルアプリケーションは脆弱性に直結するので利用しない点に注意
- 認証フローの設定  
    OAuth2の認証フローではなくて、ユーザーサインアップ時のユーザー認証フローを指しており、以下の5つから設定する
    - ALLOW_ADMIN_USER_PASSWORD_AUTH  
        CLIやSDKを利用して、管理者ユーザーとして認証を処理する
    - ALLOW_CUSTOM_AUTH  
        Lambdaでカスタム認証を行う
    - ALLOW_USER_PASSWORD_AUTH  
        CLIやSDKを利用して、一般ユーザーとして処理を行うオプション
    - ALLOW_USER_SRP_AUTH  
        Saltやチャレンジレスポンスなど、パスワード交換の安全性を高めた方法
    - ALLOW_REFRESH_TOKEN_AUTH(必須)  
        リフレッシュトークンを利用した、認証
- セキュリティ設定  
    ユーザーが存在しない時のエラーに対応（デフォルトでOK
- 高度なトークン設定  
    個別にリフレッシュトークンを無効化することが可能になるらしい

![](img/cognito_app_client.png)

#### トリガー
ユーザープールにおけるイベントを契機として実行するLambdaの設定を行う(今回はデフォルト)

![](img/cognito_trigger.png)




### CognitoのIDプールの作成
OAuth2Loginに向けて、アプリクライアントの設定とユーザープールで発行したトークンを検証するIDプールを作成する。

#### アプリクライアントの設定
Cognitoのユーザープールの画面のナビゲーションペインから`アプリクライアントの設定`を選択


以下の項目を選択していく
- 有効なIDプロバイダ  
    プロバイダとして利用するユーザーディレクトリ
- サインインとサインアウトのURL  
    - コールバックURL  
        アプリクライアントからリダイレクトされたCognitoで認証が完了した後、アプリクライアントへ再度リダイレクトするURL  
        Spring Securityでリダイレクトを受け入れるURLは`https://domain_name/context_path/login/oauth2/code/provice_name`  
        今回はローカルで実行されるアプリケーション向けに`http://localhost:8080/frontend/login/oauth2/code/cognito`とする。  
        この設定が、正しく一致しないと動作しないので注意
    - サインアウトURL   
        サインアウト後にリダイレクトするアプリケーションのクライアントURL  
        今回は`http://localhost:8080/frontend`
- OAuth2.0のフローとスコープ  
    - OAuthの認可フロー  
        セキュリティ的な安全性が担保されている`Authorization code grant`が推奨
    - スコープ  
        OAuth2.0では、保護されたリソースに対するアクセス制御する方法としてスコープという概念を使用している。  
        Cognitoが保護されたリソースへのアクセス権を指定する。（認可の指定)    
        今回は以下を許可する
        - openid: IDトークン
        - aws.cognito.signin.user.admin: ユーザープールのAPIオペレーション
        - profile: ユーザー情報へのプロファイルアクセス

![](img/cognito_app_client_setting.png)


#### ドメインの設定
Cognitoのユーザープールの画面のナビゲーションペインから`ドメイン名`を選択して、ドメイン名を設定

![](img/cognito_domain.png)



#### IDプールの設定
Cognitoのコンソール画面から、IDプールの管理>IDプールを作成を選択

- IDプール名  
    MA-fujishiroms-idpool
- ユーザープールID  
    ユーザープールの全般設定にある
- アプリクライアントID  
    ユーザープールのアプリクライアントの設定の一番上にある




## Auth0の設定
### Auth0にサインアップ
[Auth0](https://auth0.com/signup)

### テナントの作成
リージョンとテナント名を指定して、テナントを作成

![](img/auth0_tenant.png)

### アプリケーションの作成
作成したテナントからアプリケーションを選択して、アプリケーションの作成

![](img/auth0-app-create.png)

アプリケーションの名前を設定して、`SIngle Page Web Application`を選択してCreate

![](img/auth0-app-setting.png)

作成した、アプリケーションのSettingから以下の情報を控えておく
- Name
- Domain
- Client ID
- Client Secret

![](img/auth0-info.png)

許可されたコールバックURLで以下のドメインを設定しておく（以下の形式に従う必要がある）
> https://<cognito-domain>.auth. <region>.amazoncognito.com/oauth2/idpresponse

> https://ma-fujishiroms-domain.auth. ap-northeast-1.amazoncognito.com/oauth2/idpresponse




## Lambdaの構築
Cognitoの初期化処理を自動化するLambda関数を構築
- アプリクライアントのクライアントシークレットをSystems Managerに登録する
- CognitoのユーザープールにOAuth2Login用のユーザーを作成
- OAuth2 Loginユーザーのサインアップステータスを変更する


## Springの設定
あんまり難しく考えないで、SpringSecurityを利用して、ログイン画面を作成する


### Spring Securityの実装（フロントエンド）
#### Spring Securityとは？
Spring Frameworkを用いいてWebAppを作成する場合に認証にか処理を簡単に実装できるフレームワーク

セキュリティ対策は難解であるものの、SpringSecurityを利用することで少量のコーディングで多様なセキュリティ対策処理を実装可能
- サーブレットフィルタリングによる、リクエスト処理の正当性チェック
- 不正リクエストのブロック
- パスワードのハッシュ化、暗号化
- OAuth2を使ったトークン検証など

#### 作成するアプリケーション
- WebApp  
    SpringBootAppを実行する起動クラス   
- MvcConfig  
    SpringMVCの設定クラス    
- SecurityConfig     
    SpringSecurityの設定クラス   
- SampleController     
    ログイン画面やログイン後にポータル画面に遷移するよう定義するクラス   
- CustomUserDetails     
    SpringSecurityでユーザー情報を表すモデルオブジェクトを継承したカスタムクラス   
- CustomeUserDetailServiece     
    CustomUserDetailsを取得するためのカスタムクラス   
- LoginSuccessHandler     
    ログインが成功したのちに実行されるハンドラクラス   
- SessionExpiredDetectingLoginUrlAuthenticationEntryPoint     
    セッションが無効になったことを検出してログイン画面へ遷移するためのハンドラクラス   

```
src/main/java/***/frontend
|
|-- app/web
|   |
|   |-- SampleController
|   |
|   |-- security
|        |
|        |-- CustomUserDetails
|        |
|        |-- CustomUserDetailsService
|        |
|        |-- LoginSuccessHandler
|        |
|        |-- SessionExpiredDetectingLoginUrlAuthenticationEntryPoint
|
|
|-- congig
     |
     |-- MvcConfig
     |
     |-- SecurityConfig
     |
     |-- WebApp

```
#### 静的ファイルのコピー
staticやresources配下のhtmlファイルなどはgithubからコピーしておく

#### SecurityConfig
以下の内容など、Secruty関連の内容を指定していく
- SpringSecurityの対象外のパス
- ログインログアウト処理を行うURIのパス

#### CustomUserDetails
送信されたID/Passwordを検証するロジック

SpringSecurityによる、ログイン処理では、リクエストパラメータとして送信されたIDとパスワードを検証するロジックが必要。

このロジックは既に実装されており、org.springframework.security.core.userdetails.UserDetailsを使って実装する。


#### CustomUserDetailsService
CustomUserDetailsを実装するためには、org.springframework.security.core.userdetails.UserDetailsServiceのインターフェースを実装しておく必要があるので、実装する。

UserDetailsServiceでは、loadUserByUserNameメソッドを実装し、 UserDetailsインターフェースが実装したクラスを返却する。
このオブジェクトを利用して、SpringSecurtyが検証を行う。




#### トラブルシュート①: SpringSecurityのモジュールインポートエラー
pomでSpringbootを指定したところ、以下のモジュールが見つからないエラーが発生した
> import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

SpringSecurtityでは、[5.4〜6.0でセキュリティ設定の書き方が大幅に変わる](https://qiita.com/suke_masa/items/908805dd45df08ba28d8)
いので、pomで明示的にバージョンを5.4になるように指定
```
	<properties>
		<spring-security.version>5.3.4.RELEASE</spring-security.version>
	</properties>

```

#### トラブルシュート②：　javaxのimportエラー
SampleControllerでjavaxのimportがエラー
> import javax.servlet.http.HttpSession;


pomで依存関係を追加してあげることで解決
```
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>javax.servlet-api</artifactId>
			<version>4.0.0</version>
			<scope>provided</scope>
		</dependency>
```

#### トラブルシュート③：循環？
```

***************************
APPLICATION FAILED TO START
***************************

Description:

The dependencies of some of the beans in the application context form a cycle:

┌──->──┐
|  securityConfig (field org.springframework.security.crypto.password.PasswordEncoder org.debugroom.mynavi.sample.ecs.backendforfront.config.SecurityConfig.passwordEncoder)
└──<-──┘


Action:

Relying upon circular references is discouraged and they are prohibited by default. Update your application to remove the dependency cycle between beans. As a last resort, it may be possible to break the cycle automatically by setting spring.main.allow-circular-references to true.


```

PasswordEncoderフィールドに対して、@Autowiredと@Beanの定義をしているせいで循環してしまっているっぽい。

SecurityConfigの@AutoWired部分を削除して、Beanを直接指定するように変更

削除
```
@Autowired
    PasswordEncoder passwordEncoder;
```

修正
```
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth
                .userDetailsService(userDetailsService())
                .passwordEncoder(passwordEncoder());
    }


```

※application.ymlで、重複を許可してしまうやり方もある
```
  spring:
    main:
      allow-circular-references: true
```


#### トラブルシュート④：javax.servlet.Filterをcastできない
実行すると以下のエラーが発生。

SpringSecurityのフィルターチェーンの構成が正しくできていない原因っぽい。
WebSecurityConfigurationがjavax.servlet.Filterインターフェースをcastできていないっぽい

```
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'springSecurityFilterChain' defined in class path resource [org/springframework/security/config/annotation/web/configuration/WebSecurityConfiguration.class]: Failed to instantiate [javax.servlet.Filter]: Factory method 'springSecurityFilterChain' threw exception with message: class org.springframework.security.web.access.ExceptionTranslationFilter cannot be cast to class javax.servlet.Filter (org.springframework.security.web.access.ExceptionTranslationFilter and javax.servlet.Filter are in unnamed module of loader 'app')

//omit

Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [javax.servlet.Filter]: Factory method 'springSecurityFilterChain' threw exception with message: class org.springframework.security.web.access.ExceptionTranslationFilter cannot be cast to class javax.servlet.Filter (org.springframework.security.web.access.ExceptionTranslationFilter and javax.servlet.Filter are in unnamed module of loader 'app')
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:171) ~[spring-beans-6.0.4.jar:6.0.4]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:653) ~[spring-beans-6.0.4.jar:6.0.4]
	... 21 common frames omitted
Caused by: java.lang.ClassCastException: class org.springframework.security.web.access.ExceptionTranslationFilter cannot be cast to class javax.servlet.Filter (org.springframework.security.web.access.ExceptionTranslationFilter and javax.servlet.Filter are in unnamed module of loader 'app')
	at org.springframework.security.config.annotation.web.builders.FilterComparator.compare(FilterComparator.java:57) ~[spring-security-config-5.3.4.RELEASE.jar:5.3.4.RELEASE]
	at java.base/java.util.TimSort.countRunAndMakeAscending(TimSort.java:355) ~[na:na]
```

[参考サイト](https://stackoverflow.com/questions/39849534/maven-cannot-be-cast-to-javax-servlet-filter)のpom.xmlでprovideを追加するという対策をしてみたが、変化なし。。。    
```
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>4.0.0-b01</version>
    <scope>provided</scope>
</dependency>
```

[参考サイト](https://qiita.com/ponsuke0531/items/608d074b7e106c7fd1a0)では、微妙に違うエラーだが、tomcatのバージョンが10だからとあった。
今回利用しているのもtomcat10だった。
```
[Apache Tomcat/10.1.5]
```

tomcatのバージョンを変えてみた。pomでインストール済みのtomcat9を指定
```
<properties>
    <java.version>17</java.version>
    <spring-security.version>5.3.4.RELEASE</spring-security.version>
        <tomcat.version>9.0.71</tomcat.version>
</properties>
```

結果、違うエラーが発生した。
トラブルシュート⑤⑥を試しても結局改善せず、、、

[stack overflow](https://stackoverflow.com/questions/74769168/org-springframework-beans-beaninstantiationexception-failed-to-instantiate-jav)
に同じエラーの質問があり、spring Boot3はspring security6とjakartaを使えとのこと・・・



#### トラブルシュート⑤：jakartaがない
`jakarta/servlet/ServletException`とあるので、jakakrtaが利用できていない？
```
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'securityConfig' defined in file [/Users/misakifujishiro/java_workspaces/mynavi-sample-aws-ecs-backend-for-front/target/classes/org/debugroom/mynavi/sample/ecs/backendforfront/config/SecurityConfig.class]: Failed to instantiate [org.debugroom.mynavi.sample.ecs.backendforfront.config.SecurityConfig$$SpringCGLIB$$0]: Constructor threw exception

Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.debugroom.mynavi.sample.ecs.backendforfront.config.SecurityConfig$$SpringCGLIB$$0]: Constructor threw exception
	at org.springframework.beans.BeanUtils.instantiateClass(BeanUtils.java:223) ~[spring-beans-6.0.4.jar:6.0.4]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:87) ~[spring-beans-6.0.4.jar:6.0.4]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateBean(AbstractAutowireCapableBeanFactory.java:1300) ~[spring-beans-6.0.4.jar:6.0.4]
	... 16 common frames omitted


Caused by: java.lang.NoClassDefFoundError: jakarta/servlet/ServletException
```

pomでjakartaを追加
```
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>5.0.0</version>
    <scope>provided</scope>
</dependency>			
```

SampleControllerでjakartaをimportする形に変更
```
import jakarta.servlet.http.HttpSession;
```

次なるエラーが発生

#### トラブルシュート⑥：クラスが存在しない？


```
***************************
APPLICATION FAILED TO START
***************************

Description:

An attempt was made to call a method that does not exist. The attempt was made from the following location:

    org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory.configureContext(TomcatServletWebServerFactory.java:378)

The following method did not exist:

    'void org.apache.catalina.Context.addServletContainerInitializer(jakarta.servlet.ServletContainerInitializer, java.util.Set)'

The calling method's class, org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory, was loaded from the following location:

    jar:file:/Users/misakifujishiro/.m2/repository/org/springframework/boot/spring-boot/3.0.2/spring-boot-3.0.2.jar!/org/springframework/boot/web/embedded/tomcat/TomcatServletWebServerFactory.class

The called method's class, org.apache.catalina.Context, is available from the following locations:

    jar:file:/Users/misakifujishiro/.m2/repository/org/apache/tomcat/embed/tomcat-embed-core/9.0.71/tomcat-embed-core-9.0.71.jar!/org/apache/catalina/Context.class

The called method's class hierarchy was loaded from the following locations:

    org.apache.catalina.Context: file:/Users/misakifujishiro/.m2/repository/org/apache/tomcat/embed/tomcat-embed-core/9.0.71/tomcat-embed-core-9.0.71.jar


Action:

Correct the classpath of your application so that it contains compatible versions of the classes org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory and org.apache.catalina.Context


```

[このサイト](https://stackoverflow.com/questions/66336509/im-having-a-problem-of-dependency-with-springboot-web-embed-tomcat-it-gives-me-t)的には、tomcat9を利用しているのが原因？？
だが、tomcat10に戻すとjavax.servlet.Filterをcastできないエラーに逆戻り・・・




## SpringSecurityとCognitoの連携
### ユーザープールを利用した認証




### アクセストークンを利用した認可の設定











## CognitoとAuth0の連携
以下を参考に設定
- [Auth0 を Amazon Cognito ユーザープールの OIDC プロバイダーとして設定するにはどうすればよいですか?](https://aws.amazon.com/jp/premiumsupport/knowledge-center/auth0-oidc-cognito/)を参考にする。
- [Auth0 を Amazon Cognito ユーザープールの OIDC プロバイダーとして設定するにはどうすればよいですか?](https://aws.amazon.com/jp/premiumsupport/knowledge-center/auth0-oidc-cognito/)
- [Cognito の OIDC プロバイダに Auth0 を設定](https://tech-blog.s-yoshiki.com/entry/284)


### CognitoでAuth0をSAML IdPとして設定
ユーザープール>IDプロバイダーから、OpenID Connectを選択して以下を設定
- プロバイダー名：任意
- クライアントID：Auth0で控えたClientID
- クライアントシークレット：Auth0で控えたClient Secret
- 属性のリクエストメソッド:GET
- 認証のスコープ:openid
- 発行者URL: Auth0で作成したアプリのドメイン（https://xxxxxxx.auth0.com)
- 属性マッピング: email=email

![](img/cognito_auth0_setting.png)

### クライアントアプリの設定
ユーザープール>クライアントアプリの設定から、OpenIDが選択可能となっている。

##　ユーザーの統合？