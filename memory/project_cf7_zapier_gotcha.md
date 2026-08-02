---
name: project_cf7_zapier_gotcha
description: cf7-to-zapierがCF7のメール送信を止める・Webhook失敗でmail_failedに塗り替える。設定は_ctz_zapier。
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b79467e-9d8e-4ddf-889d-5165b10777ed
  modified: 2026-08-02T06:02:11.468Z
---

LPのお問い合わせフォーム（CF7 ID 1092）は `cf7-to-zapier`（CFTZ）が挙動を握っている。設定は post meta `_ctz_zapier`（シリアライズ配列）。

**罠1: `send_mail=0` だとCF7のメールを1通も送らない。** CFTZは `wpcf7_skip_mail` フィルタで `return empty($properties['send_mail'])` を返す。管理者通知も自動返信も飛ばず、しかもCF7は `mail_sent` を発火するので気づきにくい。

**罠2: Webhook失敗が成功ステータスを塗り替える。** CFTZは `wpcf7_mail_sent` でWebhookを叩き、例外時に `$submission->set_status('mail_failed')` を実行する。メールが正常に送れていてもフォームは「送信に失敗しました」と表示する。

**罠3: Slack Incoming Webhook には `custom_body` が必須。** 空だと生のフォームデータをPOSTしてSlackが `400 no_text` を返す。`{"text":"..."}` 形式のテンプレートを `custom_body` に入れる（`[フィールド名]` で置換される）。checkboxは配列のまま `["a"]` に展開されJSON文字列内に置くと壊れるので、Slack本文にはスカラー項目だけ載せている。

**Why:** 2026-08-02、フォームが `mail_failed` を返す原因を追ったとき、CF7やSMTPを疑って長時間かかった。実際はCFTZの設定2つ（send_mail と custom_body）が原因だった。

**How to apply:** フォームの送信結果がおかしいときは、SMTPを疑う前に `wp post meta get 1092 _ctz_zapier` を見る。`update_post_meta` は値に `wp_unslash()` をかけるので、JSONを保存するときは `wp_slash()` を通すこと（`\n` が `n` に潰れる）。関連 [[project_mail_smtp]]
