---
name: project_mail_smtp
description: さくらのmail()は外部宛リレー不可。メール送信はhikitsugi-smtpプラグイン経由（wp-config.phpに定数）。
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b79467e-9d8e-4ddf-889d-5165b10777ed
  modified: 2026-08-02T01:16:11.469Z
---

さくらのレンタルサーバは PHP の `mail()` からの外部宛リレーを拒否する（`553 5.3.0 ... User unknown, not local address` / sendmail exit 67）。WordPress・CF7とは無関係のサーバ側制約で、素の `sendmail` を直接叩いても同じ。

このため 2026-08-02 に `plugins/hikitsugi-smtp/` を追加し、`wp_mail()` をSMTP経由に切り替えた。認証情報は**リポジトリが公開されているため絶対にGitに入れない**。サーバの `wp-config.php`（Git管理外）に `HIKITSUGI_SMTP_*` 定数として置く。定数が無ければプラグインは何もせず管理画面に警告を出す。

**Why:** メールが届かない症状を見ると真っ先にCF7やフォームの実装を疑いたくなるが、原因はサーバ側にある。切り分けは `ssh sakura` して `sendmail` を直接叩くのが最短。

**How to apply:** 「フォームからメールが届かない」と言われたら、まず `wp-config.php` にSMTP定数が入っているか、`hikitsugi-smtp` が有効かを確認する。DNSは さくらのDNS（ns1.dns.ne.jp）管理で、`hikitsugi.jp` には既にSPFがあるためSPFの二重登録に注意。詳細は `plugins/hikitsugi-smtp/README.md`。関連 [[project_domain_migration]]
