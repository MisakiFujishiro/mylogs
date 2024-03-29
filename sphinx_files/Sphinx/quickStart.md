# Sphinx プロジェクトの立ち上げ方
## Sphinxとは
python製のドキュメント生成ツール  
reSTやmarkdownで書かれたファイルをHTMLなどに変換する。  
github Pagesと連携することで、github上でドキュメントを公開できる。
  
## インストールとクイックスタート
python環境がインストールされていることが前提  
以下のコマンドでインストールされているか確認して、されていなければインストールする。
> $ python -V

pipでsphinxをinstall 
> $ pip install sphinx

sphinxのquickstarを実行。対話形式で設定
> $ sphinx-quickstart

Buildしてみる
> $ make html

build/html/index.htmlをブラウザで開くと、quickstartの画面が確認できる。




## mdファイルでドキュメント作成
まず事前準備として、myst-parserをインストール
> pip install --upgrade myst-parser

conf.pyを修正

以下を追加する
```
extensions = [
    'myst_parser'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
```

## テーマ変更
conf.pyの`html_theme`を変更することで、テーマを変えることができる。
以下のサイトが参考になる。2つ目のreadthedocsのテーマがカッコよくておすすめ。

- [テーマパターンと変更方法](https://sphinx-users.jp/cookbook/changetheme/index.html)
- [その他のパターン](https://planset-study-sphinx.readthedocs.io/ja/latest/06.html)



## ファイルの作成
### mdファイル
mdファイルはsource配下に記述していく

![ディレクトリの様子](img/sphinx_dir.png)

### index.rst
index.rstで構成を記載する。
セクション内で指定したDOCFILEがセクションのコンテンツになる。  
ファイルを指定する際は拡張子は不要  
maxdepthで指定された階層までのDOCFILEの階層が目次として出力される。

```
Sphinx
==================

.. toctree::
   :maxdepth: 2
   :caption: How to start
   :numbered:

   Sphinx/quickStart
   Sphinx/githubPages
```

![インデックスの様子](img/sphinx_index.png)




## 実行手順
make htmlを実行することで、更新される

### buildの簡略化
毎回make htmlを実行するのは大変なのでsphinx-autobuildを利用する

> pip install sphinx-autobuild     

以下を実行すると修正が自動反映される
> sphinx-autobuild -b html source build/html

## github pagesの公開
github pagesでは、docs配下のindex.htmlを参照しにいくので、出力先をbuildから変更する必要がある。

docsの配下に以下を追加する。
```
html: Makefile
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "docs" $(SPHINXOPTS) $(O)
```

対象のPJでgit initをして、リポジトリにpushし、公開設定する。


### CSS設定
github pagesでは以下を設定しないとCSSを読み込んでくれない
docsで.nojekyllファイルを作成

> touch .nojekyll 
