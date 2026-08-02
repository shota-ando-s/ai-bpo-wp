# ヒキツギAI SMTP送信

`wp_mail()` を Resend の SMTP 経由に切り替えるプラグイン。

## なぜ必要か

さくらのレンタルサーバのメールサーバが、PHPの `mail()` からの外部宛リレーを拒否する。

```
>>> RCPT To:<ando@fuenn.co.jp>
553 5.3.0 <ando@fuenn.co.jp>... User unknown, not local address
```

WordPressやCF7の問題ではない。素の `sendmail` を直接叩いても同じ（exit 67）。
この状態だとCF7の管理者通知も自動返信も一通も届かず、フォームは
`mail_failed`（「メッセージの送信に失敗しました」）を返す。

## 設定

**このリポジトリは公開されている。APIキーをGitに入れないこと。**
認証情報はサーバの `wp-config.php`（Git管理外）に置く。挿入位置は
`ABSPATH` 定義の直前。

```php
define( 'HIKITSUGI_SMTP_HOST',      'smtp.resend.com' );
define( 'HIKITSUGI_SMTP_PORT',      587 );
define( 'HIKITSUGI_SMTP_USER',      'resend' );
define( 'HIKITSUGI_SMTP_PASS',      're_xxxxxxxxxxxx' );   // ResendのAPIキー
define( 'HIKITSUGI_SMTP_FROM',      'noreply@send.hikitsugi.jp' );
define( 'HIKITSUGI_SMTP_FROM_NAME', 'ヒキツギAI（株式会社ふえん）' );
```

定数が揃っていなければプラグインは何もせず、管理画面に警告を出す。
「送っているつもりで一通も届いていない」状態に気づけるようにするため。

## Resendアカウントについて

`offboard-checklist` と**同じアカウント・同じAPIキーを共用**している。

**無料プランは検証済みドメインを1つしか持てない。** 2026-08-02 に
旧ドメイン `ai-bpo.site`（送信に使っているコードは無かった）を削除し、
`send.hikitsugi.jp` に入れ替えた。ドメインを増やしたい場合は
Resend Pro（月$20）が必要。

### ルートではなくサブドメインを使う理由

`hikitsugi.jp` には既にSPFレコードがある。

```
v=spf1 a:www3365.sakura.ne.jp mx ~all
```

**SPFレコードは1ドメインに1つしか置けない。** ルートドメインをResendに
登録するとSPFが2つになり、どちらも無効と判定されて逆に届かなくなる。
`send.hikitsugi.jp` を使えば既存のSPFに触らずに済む。

### DNSレコード

`hikitsugi.jp` のネームサーバは `ns1.dns.ne.jp` / `ns2.dns.ne.jp` ＝ **さくらのDNS**。
さくらのドメインコントロールパネル「ゾーン編集」で、以下を
`hikitsugi.jp` ゾーンに追加する（名前はゾーンからの相対表記）。

| 種別 | 名前 | 優先度 | 値 |
|---|---|---|---|
| TXT | `resend._domainkey.send` | — | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCXEmg13ntyJ3kuis3albTYJ2a8RVEunaTXr1Oi4T04whCRDLkEvglj/qmXNgI2oMCMLapvDVp5snRGyz+z3zgAlco5xrScJ87t4iyke8jivBXVl8Avts3or4n0hXwSExtKCE7rITMR9uH7U9EdqynhTiM51TEeQfreVglbGHXHiQIDAQAB` |
| MX | `send.send` | 10 | `feedback-smtp.ap-northeast-1.amazonses.com` |
| TXT | `send.send` | — | `v=spf1 include:amazonses.com ~all` |

`send.send` は誤記ではない。Resendは登録ドメイン（`send.hikitsugi.jp`）の
さらに `send.` サブドメインを Return-Path に使うため、
`hikitsugi.jp` から見ると `send.send.hikitsugi.jp` になる。

## 注意：offboard-checklist も送信できていない

チェックリスト側の `MAIL_FROM` は `hikitsugi@fuenn.co.jp` だが、
`fuenn.co.jp` はResendに登録されていない（SPFはZoho Mail）。
同じキーを使っているので、あちらも 550 で弾かれているはず。
直すならチェックリスト側の `MAIL_FROM` も `send.hikitsugi.jp` の
アドレスに変える必要がある。

## 動作確認

```bash
ssh sakura
cd ~/www/aibpo
wp eval 'var_dump( wp_mail( "ando@fuenn.co.jp", "SMTP test", "test" ) );'
```

`bool(true)` なら成功。失敗時は `[hikitsugi-smtp] 送信失敗:` がPHPのエラーログに出る。
SMTPの生のやり取りを見たい場合は `phpmailer_init` で `SMTPDebug = 2` を立てる。
