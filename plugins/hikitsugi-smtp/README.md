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
2. Domains → Add Domain → `hikitsugi.jp`
3. 表示されたDNSレコード（SPF用TXT、DKIM用TXT、MXまたはCNAME）を
   ドメインのDNSに追加する。**さくらのドメイン設定ではなく、
   `hikitsugi.jp` のネームサーバを管理している側で追加する**
4. Verified になるまで待つ（数分〜数時間）
5. API Keys → Create API Key（権限は Sending access のみで足りる）

送信元 `noreply@hikitsugi.jp` は実在するメールボックスである必要はない。
返信は CF7 が設定する Reply-To（管理者通知には問い合わせ者のアドレス、
自動返信には `ando@fuenn.co.jp`）に飛ぶ。

## 動作確認

```bash
ssh sakura
cd ~/www/aibpo
wp eval 'var_dump( wp_mail( "ando@fuenn.co.jp", "SMTP test", "test" ) );'
```

`bool(true)` なら成功。失敗時は `[hikitsugi-smtp] 送信失敗:` がPHPのエラーログに出る。
