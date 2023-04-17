# awsses-mail-logger

SESで送信したメールに対するイベントを DynamoDB に保存するためのマイクロサービスを提供します。

## 前提条件

- 実行環境で `pipenv` , `pyenv` および `cdk` コマンドが実行可能にしておくこと
  - `pyenv` がない場合 python 3.9 が利用可能であること
- awscli の profile を設定済であること (ここでは `mail-logger` 仮定して説明する)
- SES の検証済 ID が既に登録されており、デフォルト Configuration Set を利用していないこと

## セットアップ

```bash
$ pipenv install
$ pipenv install --dev
```

### awscdk

```bash
$ cd awscdk
$ pipenv run cdk bootstrap --profile mail-logger

# 以下でどのような操作が行われるかを確認
$ pipenv run cdk diff --profile mail-logger

# 必要なリソースをデプロイ
$ pipenv run cdk deploy --all --profile mail-logger
```

### chalice

```bash
$ cd logger

# awscdk の実行結果を以下に反映する
$ vim chalicelib/env/prod.yaml
$ vim .chalice/config.json
$ vim .chalice/policy-prod.json

# デプロイを行う
$ pipenv run chalice deploy --stage prod --profile mail-logger
```

### 検証済IDへの設定

検証済IDのデフォルトセットとして、作成された Configuration Set を利用するようにする。


## License

Apache License 2.0
