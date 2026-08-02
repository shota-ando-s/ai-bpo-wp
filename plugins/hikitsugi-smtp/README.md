# ヒキツギAI SMTP送信

`wp_mail()` をSMTP経由に切り替えるプラグイン。

## なぜ必要か

さくらのレンタルサーバのメールサーバが、PHPの `mail()` からの外部宛リレーを拒否する。

```
>>> RCPT To:<ando@fuenn.co.jp>
553 5.3.0 <ando@fuenn.co.jp>... User unknown, not local address
```

この状態だとCF7の管理者通知も自動返信も一通も届かず、フォームは
`mail_failed`（「メッセージの送信に失敗しました」）を返す。

## 設定

**このリポジトリは公開されている。APIキーをGitに入れないこと。**
認証情報はサーバの `wp-config.php`（Git管理外）に書く。

```php
define( 'HIKITSUGI_SMTP_HOST',      'smtp.resend.com' );
define( 'HIKITSUGI_SMTP_PORT',      587 );
define( 'HIKITSUGI_SMTP_USER',      'resend' );
define( 'HIKITSUGI_SMTP_PASS',      're_xxxxxxxxxxxx' );   // ResendのAPIキー
define( 'HIKITSUGI_SMTP_FROM',      'noreply@hikitsugi.jp' );
define( 'HIKITSUGI_SMTP_FROM_NAME', 'ヒキツギAI' );
```

`/* That's all, stop editing! */` の**前**に置く。

定数が揃っていなければプラグインは何もせず、管理画面に警告を出す。

## Resend側の準備

1. https://resend.com でサインアップ
2. Domains → Add Domain → **`send.hikitsugi.jp`**（サブドメイン推奨。理由は下記）
3. 表示されたDNSレコードを追加する。`hikitsugi.jp` のネームサーバは
   `ns1.dns.ne.jp` / `ns2.dns.ne.jp`＝**さくらのDNS**なので、
   さくらのドメインコントロールパネルの「ゾーン編集」で追加する
4. Verified になるまで待つ（数分〜数時間）
5. API Keys → Create API Key（権限は Sending access のみで足りる）

### ルートではなくサブドメインを使う理由

`hikitsugi.jp` には既にSPFレコードがある。

```
v=spf1 a:www3365.sakura.ne.jp mx ~all
```

**SPFレコードは1ドメインに1つしか置けない。** ルートドメインをResendに
登録するとSPFが2つになり、どちらも無効と判定されて逆に届かなくなる。
`send.hikitsugi.jp` を使えば既存のSPFに触らずに済む。

どうしてもルートで送りたい場合は、追加ではなく既存レコードに
`include:amazonses.com` を**マージ**すること。

```
v=spf1 a:www3365.sakura.ne.jp mx include:amazonses.com ~all
```

サブドメインを使う場合、`HIKITSUGI_SMTP_FROM` は
`noreply@send.hikitsugi.jp` にする。

送信元アドレスは実在するメールボックスである必要はない。
返信は CF7 が設定する Reply-To（管理者通知には問い合わせ者のアドレス、
自動返信には `ando@fuenn.co.jp`）に飛ぶ。

## 動作確認

```bash
ssh sakura
cd ~/www/aibpo
wp eval 'var_dump( wp_mail( "ando@fuenn.co.jp", "SMTP test", "test" ) );'
```

`bool(true)` なら成功。失敗時は `[hikitsugi-smtp] 送信失敗:` がPHPのエラーログに出る。
