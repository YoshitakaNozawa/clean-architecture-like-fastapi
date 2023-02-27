# clean-architecture-like-fastapi

## 内容
docker-composeでコンテナを立ち上げると以下2つのサービスが使えるようになります。

### FastAPI app
FastAPI app SwaggerUI (http://localhost:8000/docs)

実装されているAPIをSwaggerUIの画面が実行することができます。
これにより、開発しつつ動作確認も簡単にできるようになります。

![image](https://user-images.githubusercontent.com/55648865/186562567-b13a4a76-dcf3-4ad5-98d2-671348eeec07.png)

### phpMyAdmin
phpMyAdmin (http://localhost:8080)

mysqlサーバーにFastAPIとphpMyAdminから接続しており、phpMyAdminのGUIからデータを整形しつつ、開発をすすめることができるようにしています。
![image](https://user-images.githubusercontent.com/55648865/186562687-042c4ac4-8a38-4d5d-acc7-fa81dd19ca12.png)

## 使い方
root dirにて以下のコマンドを実行します。
```bash
$ docker-compose build
$ docker-compose up　# -dをつけてもOK
```

コンテナの削除は、コンテナをストップした後
```bash
$ docker-compose down
```

## フォルダ構成
クリーンアーキテクチャのような構成をとっています。
厳密なクリーンアーキテクチャは採用していません。

```
1. main.py (ルーターを起動)  → 2. drivers/router (各APIのエンドポイントを提供) → 3. usecase (ビジネスロジック) → 4. entities (クエリとか、コンポーネントとか、ビジネスロジックの変更の影響を受けにくい実装部を置く。)
```

の依存関係になっており、この順にコードを追えば、理解できる構成となっています。

```
.
|_ main.py # 各種ルーターを起動する。
|
|_ /drivers # driver層
|   |_ /router # 各APIのアクセスポイントを提供
|   |_ /db # DBへの接続情報
|
|_ /adapters # adapter層
|   |_ /presenter # ユーザーインターフェース（for フロントエンド）の設定
|
|_ /usecase # usecase層。APIのメインロジックはここに記述する。
|
|_ /entities
    |_ /dto # Request, Responseの型はここで定義する
    |_ /queries # SQLはここ
    |_ /component
```

## クリーンアーキテクチャについてざっくり説明
![image](https://user-images.githubusercontent.com/55648865/186561594-5539edf8-37e6-4134-b185-8984d9a92350.png)

### Frameworks & Drivers層 (青)
アプリケーション(API)に期待する処理、つまりビジネスロジックは、usecase（とEntities）に切り出し、切り出した処理は (あるWebフレームワークに依存する) routerから呼び出すようにします。
これにより、採用したいrouterを `main.py` で呼び出すだけで、アプリケーションに期待する処理を実行できるようになります。

アプリケーションに期待する処理の部分はrouterから独立しているので、フレームワークを柔軟に変更できる設計となります。
例えば、Flaskを使用していたが、やっぱりFastAPIを使いたいとなったときは、FastAPI用のrouterを用意し、main.pyではFlask用のrouterを呼び出していた部分をFastAPI用のrouterに置き換えればよいです。

⇒CleanArchitecture のルールの 1 つ、**フレームワーク独立**が実現。

ただ、弊アプリではフレームワーク独立は少し諦めています。
というのも、通常 `fastapi_router.py`, `falsk_router.py` というように、フレームワークごとにrouterを設けるべきなのですが、
すべてfastapiのrouterであると仮定して、機能区分ごとに `user_router.py`, `hoge_router.py`を分けています。
ですので、もしフレームワークを別のものに変更したいとなったときは、現状の構成
```
drivers
|_ /router
    |_ user_router.py
    |_ hoge_router.py
    |_ __init__.py 
```
これを
```
drivers
|_ /fastapi_router # fastapi用のルーター群
|   |_ user_router.py
|   |_ hoge_router.py
|   |_ __init__.py 
|
|_ /flask_router # flask用のルーター群
   |_ user_router.py
   |_ hoge_router.py
   |_ __init__.py 
```
という構成に修正し、`main.py` からの呼び出しをflask_routerに向き先を変えてあげる必要があります。

IDEを使えばこれくらいの変更は特に問題にはならないと思いますので、ちょっと頑張ればフレームワークの変更は可能になっています。

### Enterprise Business Rules層 & Application Business Rules層

“アプリケーションに本来期待する処理（ビジネスロジック）”（例えば、ユーザー情報を取得する処理とかのこと）は

- Enterprise Business Rules
- Application Business Rules

に分けられます。

前者が”アプリケーションにおける原則的な処理”で、後者が”それらを活用してアプリケーションの仕様を満たす流動的な処理”となります。
後者はビジネスロジックからカプセル化したもの、と説明できます。

このように分けることで、アプリケーションの仕様変更の際、既存の原則的な処理(Enterprise Business Rules)に影響を与えず、仕様を柔軟に修正・拡張できる設計になります。

### Interface Adapters層
アダプター（変換器）という名前の通り、ある型から別の型へ変換を行う潤滑油的な働きを行う層です。

この層を介入させることで、アプリケーションで受け入れ可能なリクエストの形式を変更する際に、Webフレームワークやビジネスルール側の修正をせずに、リクエストの形式を変更することが可能となります。

例えば、

既存の下記のようなform 形式での post リクエストしか受け付けていないとします。

`shell scriptcurl --location --request POST 'localhost:5000/memo/1' \--form 'memo=momomo'`

これを**JSON 形式で POST リクエストを受け付けるように仕様変更**したいとなったとしても、APIの処理が記述されているBusiness Rules層の修正は不要となるのが、Adapters層の役割です。

#### Controllers

Interface Adapters 層の Controller を活用することによって、更新頻度の高い、『外部からのリクエスト形式』を、実際の処理に適した形式に変更するという部分を、フレームワークから切り出すことができます。

これにより、アプリケーションで受け入れることのできるリクエストの形式を変更する際、既存のWebフレームワークやビジネスルールを考慮せずに、コードの修正を行うことができるようになります。

依存関係としては以下のようになる。

```
main.py -> drivers/router ->  <NEW!> adapters/controllers -> usecase
```

routerとusecaseの間に組み込まれており、routerとusecaseの仲介（Adapter: 変換器）となっています。

ただ、弊アプリでは、このcontrollerを作っていません！！
fastapiが優秀なので、このあたりの実装がなくてもいいという判断をとりました。
もし、flaskなどにフレームワークを変更する場合は、この層はあった方がいいと思います。
こういう意味でも、フレームワーク独立は諦めていると上で書きました。

#### Presenter

Presenterの存在により、UIを変更する際、既存のWebフレームワークや、ビジネスルールを考慮せず、UIのみを独立して変更できる設計になります。

このPresenterの導入により、CleanArchitecture のルール、UI独立が達成されます。

