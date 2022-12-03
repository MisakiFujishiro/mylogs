## 作成するアプリケーション
![](img/tutorial11.4_arche.png)

- ログインページでID/Pass認証を行う。
- ID/PassはDBで管理しており、認証問い合わせを行う。(Spring Security)
- 認証しないとアクセスできないウェルカムページがある。
- ログアウトすることができる。(Spring Security)

## Spring Security
基本的な処理の流れは、
1. usernameを画面から受け取り、ユーザー情報を検索
2. ユーザー情報からusernameが見つかれば、passwordをハッシュ化したもので比較
3. パスワード比較が一致すれば認証、ユーザー情報がなかったり、パスワード一致しないと認証失敗

## アプリケーションの作成
プロジェクトを作成する。
DBを利用するのでmybatisのプロジェクトとする
```
mvn archetype:generate -B\
 -DarchetypeGroupId=org.terasoluna.gfw.blank\
 -DarchetypeArtifactId=terasoluna-gfw-web-blank-mybatis3-archetype\
 -DarchetypeVersion=5.7.0.RELEASE\
 -DgroupId=com.example.security\
 -DartifactId=first-springsecurity\
 -Dversion=1.0.0-SNAPSHOT
```

## ドメイン層の実装
Model/Repository/Serviceを作成する。

### Modelの作成
認証情報（usernameとpassword)を保持するAccountクラスを作成する。
`src/main/java/com/example/security/domain/model/Account.java`


### Repositoryの作成
Accountのオブジェクトをデータベースに問い合わせる処理を実装する。

まずは、Interfaceを実装する。
`src/main/java/com/example/security/domain/repository/account/AccountRepository.java`
```
package com.example.security.domain.repository.account;

import com.example.security.domain.model.Account;

import java.util.Optional;

public interface AccountRepository {
    Optional<Account> findById(String username);
}

```


次に、Implを実装する。Mybatisに問い合わせるSQLをMapperファイルに記述する。
`src/main/java/com/example/security/domain/reporitory/account/AccountRepository.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.security.domain.repository.account.AccountRepository">

    <resultMap id="accountResultMap" type="Account">
        <id property="username" column="username" />
        <result property="password" column="password" />
        <result property="firstName" column="first_name" />
        <result property="lastName" column="last_name" />
    </resultMap>

    <select id="findById" parameterType="String" resultMap="accountResultMap">
        SELECT
            username,
            password,
            first_name,
            last_name
        FROM
            account
        WHERE
            username = #{username}
    </select>
</mapper>
```
### Serviceの作成
ユーザー名から、Accountオブジェクトを取得する処理を実装する。
今回の処理は、SpirngSecurityの認証サービスから呼び出されるため、共通処理であるShareを名前につける

業務処理的な中身を記述するので、usernameが見つからなかった場合にエラーメッセージを発行する。

まずは、Interfaceを実装する。
`src/main/java/com/example/security/domain/service/account/AccountShareService.java`

次に、Implを実装する
`src/main/java/com/example/security/domain/service/account/AccountShareServiceImpl.java`
```
@Service
public class AccountSharedServiceImpl implements AccountSharedService {
    @Inject
    AccountRepository accountRepository;

    @Transactional(readOnly=true)
    @Override
    public Account findOne(String username) {
        // (1)
        return accountRepository.findById(username).orElseThrow(() -> {
            ResultMessages messages = ResultMessages.error();
            messages.add(ResultMessage.fromText(
                    "The given account is not found! username=" + username));
            return new ResourceNotFoundException(messages);
        });
    }
```

### 認証サービスの作成







### DB初期化スクリプト
本チュートリアルでは、インメモリDBを利用しているのでプロジェクト実行時に、毎回DBを作成する必要がある。
ブランクPJでは、`jdbc:initialize-database`が設定されているので、ここにDDLとDMLを設定すれば初期に実行される
`src/main/resources/META-INF/spring/first-springsecurity-env.xml`
```
<jdbc:initialize-database data-source="dataSource"
    ignore-failures="ALL">
    <jdbc:script location="classpath:/database/${database}-schema.sql" encoding="UTF-8" />
    <jdbc:script location="classpath:/database/${database}-dataload.sql" encoding="UTF-8" />
</jdbc:initialize-database>
```

`src/main/resouces/database/H2-schema.sql`にDDLを設定する。
`src/main/resouces/database/H2-dataload.sql`にDMLを設定する。



## アプリケーション層の実装





