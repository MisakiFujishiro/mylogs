# チュートリアル11.1：TODOアプリケーション
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

※terminalで実行する場合は、¥で改行するようにしないとエラーが出た

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

```
src
  └pom.xml
  └main
      ├java・・・ソースコードを置くことがルール
      │  └com
      │    └example
      │      └todo
      │        ├ app ・・・アプリケーション層
      │        │   └todo・・・コントローラー
      │        └domain ・・・ドメイン層
      │            ├model ・・・モデル（データ定義
      │            ├repository ・・・リポジトリ（データにアクセス
      │            │   └todo
      │            └service ・・・サービス（業務処理
      │                └todo
      ├resources・・・設定ファイルをおくことがルール
      │  └META-INF
      │      └spring 
      └wepapp
          └WEB-INF
              └views ・・・jspなどのビュー
```
src/main/javaのフォルダとpom.xmlが上記なような構成があるだけで、mvnPJと呼ぶことができる。
昔は自由に決めることができていたけど、新規参画者が酷い目にあったので、ルールが画一化された。
結果として、mavenは自動で、src/main/java配下にあるソースをコンパイルしてくれる。


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
ドメイン層とアプリケーション層のステップで作成する。  

ドメイン層  
Model、Repository、Serviceを作成する。
- Modelは変数定義を記述 。
- RepositoryはInterfaceとImplementを作成して、中身としては業務を含まないデータへのアクセス処理を記述
- Serviceは業務まで含んだ、エラーメッセージのハンドリングまで含めて記述。

アプリケーション層  
ControllerとViewを作成する。
- Controllerでは、pathとメソッドの紐付け、viewとやり取りするためにmodelへのAttributeの追加などを記述。
- Viewでは、JSPなどを記述して画面表示する内容を記述。


### Domain層の作成
Model、Repository、Serviceを作成する。
- Modelは変数定義を記述 。
- RepositoryはInterfaceとImplementを作成して、中身としては業務を含まないデータへのアクセス処理を記述
- Serviceは業務まで含んだ、エラーメッセージのハンドリングまで含めて記述。



#### Model作成
src/main/java/com/example/todo/domain/model配下に作成

各プロパティとGetter・Setterを作成
- todoId：ID
- todoTitle：タイトル
- finished：完了フラグ
- createdAt：作成日

```
package com.example.todo.domain.model;

import java.io.Serializable;
import java.util.Date;

public class Todo implements Serializable {

    private static final long serialVersionUID = 1L;

    private String todoId;

    private String todoTitle;

    private boolean finished;

    private Date createdAt;

    public String getTodoId() {
        return todoId;
    }

    public void setTodoId(String todoId) {
        this.todoId = todoId;
    }

    public String getTodoTitle() {
        return todoTitle;
    }

    public void setTodoTitle(String todoTitle) {
        this.todoTitle = todoTitle;
    }

    public boolean isFinished() {
        return finished;
    }

    public void setFinished(boolean finished) {
        this.finished = finished;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }
}
```

#### Repository作成
##### Repository Interface作成
Interfaceから作成する

src/main/java/com/example.todo.domain.repository.todo配下にTodoRepository.javaを作成

各関数の引数と返り値のみが定義される。（中身はImplで作成）
記述する機能としては、業務とは独立したデータのCRUD処理のみ記述される
- findById
- findAll
- create
- update
- delete
- countByFinished

```
package com.example.todo.domain.repository.todo;

import java.util.Collection;
import java.util.Optional;

import com.example.todo.domain.model.Todo;

public interface TodoRepository {
    Optional<Todo> findById(String todoId);

    Collection<Todo> findAll();

    void create(Todo todo);

    boolean update(Todo todo);

    void delete(Todo todo);

    long countByFinished(boolean finished);
}
```

##### Repository Implementの作成
Implementを作成する

src/main/java/com/example.todo.domain.repository.todo配下にTodoRepositoryImpl.javaを作成

各関数の具体的な処理内容が記載される。
Interfaceで記述した機能について@Overrideして追記
- findById
- findAll
- create
- update
- delete
- countByFinished


★1  
Impl側に@Repositoryを記述する。

```
package com.example.todo.domain.repository.todo;

import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Repository;

import com.example.todo.domain.model.Todo;

// ★★★★★1★★★★★
@Repository  
public class TodoRepositoryImpl implements TodoRepository {
    private static final Map<String, Todo> TODO_MAP = new ConcurrentHashMap<String, Todo>();

    @Override
    public Optional<Todo> findById(String todoId) {
        return Optional.ofNullable(TODO_MAP.get(todoId));
    }

    @Override
    public Collection<Todo> findAll() {
        return TODO_MAP.values();
    }

    @Override
    public void create(Todo todo) {
        TODO_MAP.put(todo.getTodoId(), todo);
    }

    @Override
    public boolean update(Todo todo) {
        TODO_MAP.put(todo.getTodoId(), todo);
        return true;
    }

    @Override
    public void delete(Todo todo) {
        TODO_MAP.remove(todo.getTodoId());
    }

    @Override
    public long countByFinished(boolean finished) {
        long count = 0;
        for (Todo todo : TODO_MAP.values()) {
            if (finished == todo.isFinished()) {
                count++;
            }
        }
        return count;
    }
}
```

#### Service作成
##### Service Interfaceの作成
Interfaceから作成する。

src/main/java/com/example/todo/service/todo配下にTodoService.javaを作成する。

各関数の引数と返り値のみが定義される。（中身はImplで作成）
- findAll
- create
- finish
- delete

記述する機能としては、アプリケーションとしての業務処理を行うメソッド

![todoApp](img/tutorial1_todoApp_archi.png)

```
package com.example.todo.domain.service.todo;

import java.util.Collection;

import com.example.todo.domain.model.Todo;

public interface TodoService {
    Collection<Todo> findAll();

    Todo create(Todo todo);

    Todo finish(String todoId);

    void delete(String todoId);
}
```


##### Service Implementの作成
Implementを作成する。

src/main/java/com/example/todo/service/todo配下にTodoServiceImpl.javaを作成する。

エラーメッセージのハンドリングなど、業務的なロジックについて実装している


★1  
ServiceImpl側でアノテーションを付与する

★2  
@Transactionalはトランザクション管理で、参照のみを行う処理にreadOnly=trueを付与する

★3  
@InjectでRepositoryで実装したメソッドのインスタンス注入されるので利用できるようになる。

```
package com.example.todo.domain.service.todo;

import java.util.Collection;
import java.util.Date;
import java.util.UUID;

import javax.inject.Inject;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.terasoluna.gfw.common.exception.BusinessException;
import org.terasoluna.gfw.common.exception.ResourceNotFoundException;
import org.terasoluna.gfw.common.message.ResultMessage;
import org.terasoluna.gfw.common.message.ResultMessages;

import com.example.todo.domain.model.Todo;
import com.example.todo.domain.repository.todo.TodoRepository;

// ★★★★★1★★★★★
@Service

// ★★★★★2★★★★★
@Transactional 
public class TodoServiceImpl implements TodoService {

    private static final long MAX_UNFINISHED_COUNT = 5;

    // ★★★★★3★★★★★
    @Inject
    TodoRepository todoRepository;

    @Override
    @Transactional(readOnly = true) 
    public Collection<Todo> findAll() {
        return todoRepository.findAll();
    }

    @Override
    public Todo create(Todo todo) {
        long unfinishedCount = todoRepository.countByFinished(false);
        if (unfinishedCount >= MAX_UNFINISHED_COUNT) {
            ResultMessages messages = ResultMessages.error();
            messages.add(ResultMessage
                    .fromText("[E001] The count of un-finished Todo must not be over "
                            + MAX_UNFINISHED_COUNT + "."));
            
            throw new BusinessException(messages);
        }

        
        String todoId = UUID.randomUUID().toString();
        Date createdAt = new Date();

        todo.setTodoId(todoId);
        todo.setCreatedAt(createdAt);
        todo.setFinished(false);

        todoRepository.create(todo);
        return todo;
    }

    @Override
    public Todo finish(String todoId) {
        Todo todo = findOne(todoId);
        if (todo.isFinished()) {
            ResultMessages messages = ResultMessages.error();
            messages.add(ResultMessage
                    .fromText("[E002] The requested Todo is already finished. (id="
                            + todoId + ")"));
            throw new BusinessException(messages);
        }
        todo.setFinished(true);
        todoRepository.update(todo);
        return todo;
    }

    @Override
    public void delete(String todoId) {
        Todo todo = findOne(todoId);
        todoRepository.delete(todo);
    }

    
    private Todo findOne(String todoId) {
        
        return todoRepository.findById(todoId).orElseThrow(() -> {
            ResultMessages messages = ResultMessages.error();
            messages.add(ResultMessage
                    .fromText("[E404] The requested Todo is not found. (id="
                            + todoId + ")"));
            return new ResourceNotFoundException(messages);
        });
    }
}
```

### アプリケーション層の作成 
ControllerとViewを作成する。
- Controllerでは、pathとメソッドの紐付け、viewとやり取りするためにmodelへのAttributeの追加などを記述。
- Viewでは、JSPなどを記述して画面表示する内容を記述。


#### Controllerの作成
src/main/java/com/example/todo/app/todo配下にTodoController.javaを作成する。

★1
@RequestMappngでTodoControllerで扱うパスの設定をしていく。
全ての処理はtodoの配下に設定される
```
package com.example.todo.app.todo;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
// ★★★★★1★★★★★
@RequestMapping("todo") 
public class TodoController {

}
```

#### Show all Todoの作成
新規作成フォームとTODOの全件表示の機能を実装

##### TodoFormを作成する。
Controllerで扱う、プロパティをここで定義して、最終的にはDomainに追加するような形。

src/main/java/com/example/todo/app/todo配下にTodoForm.javaを作成する。

内容としては todoTitleに関するプロパティ定義
```
package com.example.todo.app.todo;

import java.io.Serializable;

public class TodoForm implements Serializable {
    private static final long serialVersionUID = 1L;

    private String todoTitle;

    public String getTodoTitle() {
        return todoTitle;
    }

    public void setTodoTitle(String todoTitle) {
        this.todoTitle = todoTitle;
    }

}
```


##### Controllerの修正
@GetMappingで/todo/listへのGETメソッドに対しての処理を記述

★1  
@ModelAttributeを定義すると、クラス名を小文字化したもの（todoForm)をkey,返り値をvalueとして、modelに追加される。  
すなわち、TodoControllerの各処理で、model.Attribute("todoForm",form)を実装するのと同じ  
TodoFormの中身が、modelに追加される。


★2  
@GetMapping("list")の設定により todo/listへのアクセスがあると、list関数が走って、findallの結果をattributeに追加して、 todo/listに遷移させる。  


```
package com.example.todo.app.todo;

import java.util.Collection;

import javax.inject.Inject;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;

import com.example.todo.domain.model.Todo;
import com.example.todo.domain.service.todo.TodoService;


@Controller
@RequestMapping("todo")
public class TodoController {
    @Inject 
    TodoService todoService;
    
    // ★★★★★1★★★★★
    @ModelAttribute 
    public TodoForm setUpForm() {
        TodoForm form = new TodoForm();
        return form;
    }
    
    
    // ★★★★★2★★★★★
    @GetMapping("list") 
    public String list(Model model) {
        Collection<Todo> todos = todoService.findAll();
        model.addAttribute("todos", todos); 
        return "todo/list"; 
    }
}
```



##### jspの修正
Controllerjから受け取ったmodelの中身を使って、TODOのタイトルを表示する

src/main/webapp/WEB-INF-views/todo配下にlist.jspを作成する。

★1  
model.Attributeで渡されてtodosについてfor文で展開して、画面表示している。

```
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Todo List</title>
<style type="text/css">
.strike {
    text-decoration: line-through;
}
</style>
</head>
<body>
    <h1>Todo List</h1>
    <hr />
    <div id="todoList">
        <ul>
            <!-- ★★★★★1★★★★★-->
            <c:forEach items="${todos}" var="todo">
                <li><c:choose>
                        <c:when test="${todo.finished}">
                            <span class="strike">
                            ${f:h(todo.todoTitle)}
                            </span>
                        </c:when>
                        <c:otherwise>
                            ${f:h(todo.todoTitle)}
                         </c:otherwise>
                    </c:choose></li>
            </c:forEach>
        </ul>
    </div>
</body>
</html>
```
### Create Todoの作成
#### TodoFormの修正
TodoTitleについて、nullの禁止と文字数制限を設定
```
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
    @NotNull // ★★★★★
    @Size(min = 1, max = 30) // ★★★★★
    private String todoTitle;

```

#### controllerの修正
##### beanMapperによるtodoFormオブジェクトをtodoオブジェクトに変換

★1  
todoFormは、todoTitleの情報を持っている。
Controller側でtodoTitleに関わる処理を終えたらtodoに変換する。  
これによって、todoTitleが入ったtodoオブジェクトを作って、次の createに流す。

```
@Inject
Mapper beanMapper;
// ★★★★★1★★★★★
Todo todo = beanMapper.map(todoForm, Todo.class);
```

##### postメソッドによるcreate処理

★1  
todo/createというパスのポストメソッドに対しては、createメソッドが走る。

★2  
TodoFormに対して、入力チェックが走る。

★3  
入力チェックの結果が格納される

★4  
正常に作成が完了すると、リダイレクトされる  
リダイレクト先への情報を格納するために、引数にRedirectAttributesを加える。

```
@PostMapping("create") // ★★★★★1★★★★★
public String create(@Valid TodoForm todoForm,// ★★★★★2★★★★★ 
                            BindingResult bindingResult, // ★★★★★3★★★★★
                            Model model, 
                            RedirectAttributes attributes// ★★★★★4★★★★★) { /

```

#### Create処理詳細
エラーがあれば一覧表示。エラーがなければ、正常終了でリダイレクト。

★1  
@validの部分でエラーがあった場合は一覧表示に戻る。  
JSP側で`<form:errors path="todoTitle" />`として、TodoFormのプロパティであるtodoTititleのエラーを表示させている。

★2  
todoServiceのcreateを呼び出して実行  
todoService→todoRepositoryのcreateが実行されて、Todo_Mapにtodoが追加される。

★3  
serviceに記述された個数の制限などに引っかかるとcatchされる。  
エラーメッセージはmodelに格納されるし、modelAttributeでmodelにtodoFornも格納されていると思う。

★4  
全ての処理がうまくいった場合は、ResultMessagesに成功のメッセージを追加して、listへリダイレクトする。


```
   // ★★★★★1★★★★★
    if (bindingResult.hasErrors()) {
        return list(model);
    }

    //★★★★★2★★★★★
    try {
        todoService.create(todo);
    } catch (BusinessException e) {
        // ★★★★★3★★★★★
        model.addAttribute(e.getResultMessages());
        return list(model);
    }

    // ★★★★★4★★★★★
    attributes.addFlashAttribute(ResultMessages.success().add(
            ResultMessage.fromText("Created successfully!")));
    return "redirect:/todo/list";
}

```


#### jspの修正
★1  
<t:messagesPanel />
org.terasoluna.gfw.common.message.ResultMessageに持っている情報を表示する。todoServiceで出力されたエラーか、正常終了のエラーが表示される。

★2  
modelAttributeには、@modelAttributeで指定した名前をつける

★3  
プロパティ名を指定するので、Formのプロパティ名を指定する。

★4  
入力エラーがあった場合に表示する。path属性の値は、Formのプロパティ名を指定


```
<div id="todoForm">
    <!-- ★1 -->
    <t:messagesPanel />

    <!-- ★2 -->
    <form:form
       action="${pageContext.request.contextPath}/todo/create"
        method="post" modelAttribute="todoForm">
        <!-- ★3 -->
        <form:input path="todoTitle" />
        <!-- ★4 -->
        <form:errors path="todoTitle" cssClass="text-error" />
        
        <form:button>Create Todo</form:button>
    </form:form>
</div>
```
### Finish Todoの作成
#### todoFormの修正
Finishの処理を追加する。FinishはtodoIdを使って、処理を行う。
CreateとFinishでは利用するプロパティが異なり、Createの時にはtodoTitleを使いFinishの時はtodoIdを使いたい。  
groups属性を利用して、入力チェックの制御を行う。


★1  
入力チェックのために、インターフェースを追加

★2  
todoIdはFinishで入力チェックをして、todoTitleはCreateで入力チェックをする。

```
package com.example.todo.app.todo;

import java.io.Serializable;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

public class TodoForm implements Serializable {
    
    // ★★★★★1★★★★★
    public static interface TodoCreate {
    };
    public static interface TodoFinish {
    };

    private static final long serialVersionUID = 1L;

    // ★★★★★2★★★★★
    @NotNull(groups = { TodoFinish.class })
    private String todoId;

    // ★★★★★2★★★★★
    @NotNull(groups = { TodoCreate.class })
    @Size(min = 1, max = 30, groups = { TodoCreate.class })
    private String todoTitle;

    public String getTodoId() {
        return todoId;
    }

    public void setTodoId(String todoId) {
        this.todoId = todoId;
    }

    public String getTodoTitle() {
        return todoTitle;
    }

    public void setTodoTitle(String todoTitle) {
        this.todoTitle = todoTitle;
    }

}
```

#### todoControllerの修正
groups属性を追加したので@Validではなく、@Validatedを利用する。

★1  
グループ化した入力チェックルールを適用するために、@Validアノテーションを@Validatedアノテーションに変更する
適用する入力チェックルールのグループ(グループインタフェース)を指定する。
Default.classは、グループ化されていない入力チェックルールを適用するために用意されているグループインタフェースである

★2  
PostMappping("finish")でtodo/finishへのPOSTメソッドに対する処理を記載する。
基本的な処理はcreateと同じで、エラーを捌きつつ、正常終了したら、Service→Repositoryで定義されたfinishを実行する。
処理の中身としては、対象のIdのfinishフラグの値を変更して、updateをかける。


```
@PostMapping("create")
public String create(
        // ★★★★★1★★★★★
        @Validated({ Default.class, TodoCreate.class }) TodoForm todoForm, 
        BindingResult bindingResult, Model model,
        RedirectAttributes attributes) {

// ★★★★★2★★★★★
@PostMapping("finish") 
public String finish(
        @Validated({ Default.class, TodoFinish.class }) TodoForm form, 
        BindingResult bindingResult, Model model,
        RedirectAttributes attributes) {
    if (bindingResult.hasErrors()) {
        return list(model);
    }
    try {
        todoService.finish(form.getTodoId());
    } catch (BusinessException e) {
        model.addAttribute(e.getResultMessages());
        return list(model);
    }
    attributes.addFlashAttribute(ResultMessages.success().add(
            ResultMessage.fromText("Finished successfully!")));
    return "redirect:/todo/list";
}
```

#### jspファイルの変更
hiddenでtodoのtodoIdをPOSTする。
```
<!-- (1) -->
<form:form
    action="${pageContext.request.contextPath}/todo/finish"
    method="post"
    modelAttribute="todoForm"
    cssClass="inline">
    <!-- (2) -->
    <form:hidden path="todoId"
        value="${f:h(todo.todoId)}" />
    <form:button>Finish</form:button>
</form:form>
```

### Delete Todoの作成
Finishと基本的には同じ修正を加える。

## MyBatis3を利用したTODOアプリ
### プロジェクトの作成
以下を実行（別のフォルダで）
```
mvn archetype:generate -B¥
 -DarchetypeGroupId=org.terasoluna.gfw.blank¥
 -DarchetypeArtifactId=terasoluna-gfw-web-blank-mybatis3-archetype¥
 -DarchetypeVersion=5.7.0.RELEASE¥
 -DgroupId=com.example.todo¥
 -DartifactId=todo¥
 -Dversion=1.0.0-SNAPSHOT
```

すでに作成した、src配下のRepositoryImpl以外のファイルをコピーしてくる。
- domain/model/Todo.java
- domain/repository/todo/TodoRepository.java
- domain/service/todo/TodoService.java
- domain/service/todo/TodoServiceImpl.java
- app/todo/TodoController.java
- app/todo/TodoForm.java
- src/main/webapp/WEB-INF/views/todo/list.jsp


### DataBaseのセットアップ
APサーバ起動時にH2 Database上にテーブルが作成されるようにする。
TBLを作成するためのDDLは以下
```
create table if not exists todo (
    todo_id varchar(36) primary key,
    todo_title varchar(30),
    finished boolean,
    created_at timestamp
)
```
これを `src/main/resources/META-INF/spring/todo-infra.properties`に追加。
```
database=H2

# (1)
database.url=jdbc:h2:mem:todo;DB_CLOSE_DELAY=-1;INIT=create table if not exists todo(todo_id varchar(36) primary key, todo_title varchar(30), finished boolean, created_at timestamp)

database.username=sa
database.password=
database.driverClassName=org.h2.Driver
# connection pool
cp.maxActive=96
cp.maxIdle=16
cp.minIdle=0
cp.maxWait=60000
```

### インフラストラクチャ層の実装
RepositoryImplにあたる部分を作成する。  
RepositoryImplを作成するのではなく、Repositoryインターフェースが呼び出された時に、実行するSQLを定義するためのMapperファイルを作成する。

`todo/src/main/resources/com/example/todo/domain/repository/todo`配下に`TodoRepository.xml`を作成する。


★1  
RepositoryのインターフェースのFQCNを指定する

★2  
今回の検索結果(ResultSet)とDomain/modelの紐付けをおこなっている。
Repository内部で指定するtodoResultMapと、domain/model配下のtodo.javaの紐付けを行うという宣言。

★3  
idでの指定はPrimaryKeyの指定している。
Repositoryの変数todoIdとテーブルのtodo_idを紐付けている。

★4  
resultの指定はそのほかの要素に関する指定
Repositoryの変数todoTitleとテーブルのtodo_titleなどを紐付けている。

★5-10  
処理自体はSQLとして記述している。
idの部分で、Repositoryインターフェースのメソッドとのマッピングをしている。


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!-- ★★★★★1★★★★★ -->
<mapper namespace="com.example.todo.domain.repository.todo.TodoRepository">

    <!-- ★★★★★2★★★★★ -->
    <resultMap id="todoResultMap" type="Todo">
        <!-- ★★★★★3★★★★★ -->
        <id property="todoId" column="todo_id" />
        <!-- ★★★★★4★★★★★ -->
        <result property="todoTitle" column="todo_title" />
        <result property="finished" column="finished" />
        <result property="createdAt" column="created_at" />
    </resultMap>

    <!-- ★★★★★5★★★★★ -->
    <select id="findById" parameterType="String" resultMap="todoResultMap">
    <![CDATA[
        SELECT
            todo_id,
            todo_title,
            finished,
            created_at
        FROM
            todo
        WHERE
            todo_id = #{todoId}
    ]]>
    </select>

    <!-- ★★★★★6★★★★★ -->
    <select id="findAll" resultMap="todoResultMap">
    <![CDATA[
        SELECT
            todo_id,
            todo_title,
            finished,
            created_at
        FROM
            todo
    ]]>
    </select>

    <!-- ★★★★★7★★★★★ -->
    <insert id="create" parameterType="Todo">
    <![CDATA[
        INSERT INTO todo
        (
            todo_id,
            todo_title,
            finished,
            created_at
        )
        VALUES
        (
            #{todoId},
            #{todoTitle},
            #{finished},
            #{createdAt}
        )
    ]]>
    </insert>

    <!-- ★★★★★8★★★★★ -->
    <update id="update" parameterType="Todo">
    <![CDATA[
        UPDATE todo
        SET
            todo_title = #{todoTitle},
            finished = #{finished},
            created_at = #{createdAt}
        WHERE
            todo_id = #{todoId}
    ]]>
    </update>

    <!-- ★★★★★9★★★★★ -->
    <delete id="delete" parameterType="Todo">
    <![CDATA[
        DELETE FROM
            todo
        WHERE
            todo_id = #{todoId}
    ]]>
    </delete>

    <!-- ★★★★★10★★★★★ -->
    <select id="countByFinished" parameterType="Boolean"
        resultType="Long">
    <![CDATA[
        SELECT
            COUNT(*)
        FROM
            todo
        WHERE
            finished = #{finished}
    ]]>
    </select>

</mapper>
```


## References
- [mvn archetype:generateコマンド](https://shunyaueta.com/posts/2021-07-18/)
- [javaPJの構成](https://qiita.com/aaaaaayyymmm/items/f5458d2302c11202136d)