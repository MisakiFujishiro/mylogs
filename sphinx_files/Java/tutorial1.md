# チュートリアル１：TODOアプリケーション
[実施内容](http://terasolunaorg.github.io/guideline/5.7.0.RELEASE/ja/Tutorial/index.html)

## 環境構築
### PJの作成
`mvn archetype:generate`コマンドは設定したフォーマットのjavaのプロジェクトのひな壇を作成してくれる。
フォーマットを作成することもでき、ベストプラクティスに従った構成を素早く作成できる。

オプションの意味は以下
- archetypeGroupId:テンプレートの提供元ID
- archetypeArtifactId:今回利用するテンプレートのID
- archetypeVersion:テンプレートのバージョン
- groupId:PJの識別子
- artifactId:作成するJavaPJの名称
- version:PJのバージョン名

```
mvn archetype:generate -B\
 -DarchetypeGroupId=org.terasoluna.gfw.blank\
 -DarchetypeArtifactId=terasoluna-gfw-web-blank-archetype\
 -DarchetypeVersion=5.7.0.RELEASE\
 -DgroupId=com.example.todo\
 -DartifactId=todo\
 -Dversion=1.0.0-SNAPSHOT
```

### STSでのPJ立ち上げ
STSでImportする。  
詳細は[チュートリアル](http://terasolunaorg.github.io/guideline/5.7.0.RELEASE/ja/Tutorial/TutorialTodo.html#id13)に有り

### PJ構成
javaのPJ構成とそれぞれの役割
- src/main/java：ここにModel操作やControllerのjavaクラスを格納
- src/main/resources：Viewに当たるリソースを置く
  - static:cssやjsを置く
  - template:htmlを置く
  - application.proparties：ポートの設定など
```
src
  └main
      ├java... (1)
      │  └com
      │    └example
      │      └todo
      │        ├ app 
      │        │   └todo
      │        └domain 
      │            ├model 
      │            ├repository 
      │            │   └todo
      │            └service 
      │                └todo
      ├resources... (2)
      │  └META-INF
      │      └spring 
      └wepapp
          └WEB-INF
              └views 
```

### PJの動作確認
`src/main/java/com/example/todo/app/welcome/HelloController.java`のプロジェクトはトップページが準備されている。

★1
@ControllerのアノテーションによりControllerであることを認識させる

★2
@RequestMappingにより`/`のGETとPOSTに対してhomeというメソッドを紐付け。
処理内容はログの出力、日時の取得、日時情報をモデルに引き渡し、Viewへの連携

★3
ModelにAttribute（変数）を引き渡している。
model側でserverTimeという変数名が使える。

★4
viewのファイル名で、画面を表示先を指定  
ViewResolverで`src/main/webapp/WEB-INF/views/welcome/home.jsp`配下のファイルが指定されている


```

/**
 * Handles requests for the application home page.
 */
 
// ★★★★★1★★★★★
@Controller
public class HelloController {

    private static final Logger logger = LoggerFactory
            .getLogger(HelloController.class);

    /**
     * Simply selects the home view to render by returning its name.
     */

    // ★★★★★2★★★★★
    @RequestMapping(value = "/", method = {RequestMethod.GET, RequestMethod.POST})
    public String home(Locale locale, Model model) {

        logger.info("Welcome home! The client locale is {}.", locale);

        Date date = new Date();
        DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG,
                DateFormat.LONG, locale);

        String formattedDate = dateFormat.format(date);

        // ★★★★★3★★★★★
        model.addAttribute("serverTime", formattedDate);

        // ★★★★★4★★★★★
        return "welcome/home";
    }

}
```



## Todoアプリケーションの作成

## データベースアクセスを伴うインフラストラクチャ

## References
- [mvn archetype:generateコマンド](https://shunyaueta.com/posts/2021-07-18/)
- [javaPJの構成](https://qiita.com/aaaaaayyymmm/items/f5458d2302c11202136d)