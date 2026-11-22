# 第4弾：Slack分析はいけるか ＋ 全プロダクトの競合調査

調査日: 2026-11-22

---

## 0. 結論

| 判定 | プロダクト |
|---|---|
| 🟢 **空きがある（勝負できる）** | 推し活の遠征エージェント／Slack分析（「監視」ではなく「つなぐ」方向・日本語特化）／友達の「お互い一致したら誘う」 |
| 🟡 **競合はいるが差別化の余地あり** | 社内シャッフルマッチング（Donutが強い）／旅行リマインダー（価格部分は大手、リマインド部分は空き）／デスクトップ常駐ゲーム |
| 🔴 **激戦（避けるか、機能の一つにとどめる）** | ミッション達成までSNSロック／写真でカロリー記録／AIフィットネスコーチ／健康経営の歩数チャレンジ |

---

## 1. Slack分析はできそうか

### 1-1. 技術的には？ → **作れる。ただし2025年のルール変更に要注意**

| 項目 | 内容 |
|---|---|
| **APIの制限（重要）** | 2025年5月から、**Slack Marketplaceの審査を通っていない外部配布アプリ**は、過去メッセージを取得するAPI（`conversations.history` / `replies`）が**1分に1回・15件まで**に制限された。過去ログを大量に読み込む分析は事実上できない |
| 対策① | **Marketplaceの審査を通す**（セキュリティ要件・審査期間あり） |
| 対策② | **Events API（新着メッセージのリアルタイム通知）でインストール後のデータを貯める**。過去ログは読まず、「導入した日から分析が始まる」設計にする |
| 対策③ | 本文を読まない**メタデータ分析**（誰が誰に返信したか、返信速度、深夜の投稿など）を中心にする |

### 1-2. 競合

| サービス | 内容 | 備考 |
|---|---|---|
| Slack標準のアナリティクス／Slack AI | チャンネル別の利用状況、要約 | 基本的な指標のみ。組織分析は弱い |
| **Aware** | 公開チャンネルの感情分析・コンプライアンス | 大企業向け |
| **Worklytics** | 組織の健全性・燃え尽きの兆候（深夜の活動など） | 大企業向け |
| **Flowtrace** | 関係マップ・サイロ（部署の孤立）の可視化。無料プランあり | 小さなチームにも対応 |
| **Compass** | コミュニケーションのネットワーク分析（有料） | Slack Marketplaceで公開 |
| **Count** | Slackデータの分析テンプレート | 分析者向け |
| **Chatacuity** | メンションと活動量の分析（公開チャンネルのみ） | |
| Officevibe | Slack上でのエンゲージメントサーベイ | サーベイ型 |
| Microsoft Viva Insights | Teams側の組織分析 | Microsoft 365向け |
| **日本製** | 今回の検索では、**Slack分析に特化した日本のサービスは見つからなかった**（カオナビなど人事システムのSlack連携はある） | **空いている可能性** |

### 1-3. 勝ち筋：「監視」ではなく「つなぐ」分析

感情分析や離職予兆は、**「会社に監視されている」と社員に嫌がられやすく**、しかも原因まではわからない（専門家の指摘）。そこで、方向を変える。

| 機能 | 内容 | 誰が喜ぶか |
|---|---|---|
| **「この話題ならこの人」マップ** | 公開チャンネルの発言から、誰が何に詳しいかを自動で地図にする | 全社員・新入社員 |
| **共通の話題でつなぐ** | 部署は違うが同じ話題（例：キャンプ、Rust、子育て）に反応している人同士を、ランチや1on1で引き合わせる → **「お互いが持っている話題」のアイデアそのもの** | 人事 |
| **新入社員の孤立検知** | 入社3か月で、誰ともやりとりが増えていない人を（中身を読まずに）人事にそっと知らせる | 人事・マネージャー |
| **部署間の壁の可視化** | 部署同士のやりとりの量をヒートマップにする | 経営者 |

- 価格の目安：1人あたり月¥300〜500。100人の会社30社で1000万円ペース
- プライバシー設計：公開チャンネルのみ、DMは読まない、個人ではなくチーム単位で見せる、社員側にも「自分のデータ」を見せる
- 第2弾の「社内シャッフルマッチング」と同じ商品にまとめられる（**分析でつなぐ相手を決める** → Donutとの差別化になる）

---

## 2. 各プロダクトの競合調査

### 2-1. 航空券の時期別価格×旅行リマインダー 🟡
| 競合 | 内容 |
|---|---|
| Google Flights | 無料で価格追跡・値上がり予測・メール通知 |
| Skyscanner | 価格アラート、月単位で最安を表示 |
| Hopper | 価格予測、価格を一時的に押さえる機能（有料） |
| Going | セール情報を有料で配信（英語圏） |
| トラベルコ | 1,500以上の旅行サイトを横断して比較 |
| エアトリ | 航空券＋ホテルのセット |
| LCC公式のメルマガ・SNS | セール情報 |

→ **価格の追跡そのものは大手に勝てない**。一方で、**「連休・有給の最適化」「行くまでのリマインド」**をしている大手は見当たらない。

### 2-2. 友達をこっそり誘う 🟢
| 競合 | 内容 |
|---|---|
| **Shirase**（日本） | 「暇」を特定の相手だけに知らせ、反応を待つ。断られる不安を減らす → **コンセプトが最も近い** |
| 今日ひま（日本） | 暇を友達限定で共有する |
| Digipals（YC 2025年秋） | 1人に1体のAIエージェントが会う機会を作る（英語圏） |
| Alfi（YC） | AIが参加するグループチャット |
| Sidekix | AIで日程を調整する |
| Dayli | 毎日1分の通話（方向転換した） |

→ 「暇を知らせる」系は日本にもある。ただし**「お互いが相手を指名して一致したら初めて通知」＋「AIが自然な口実（話題・イベント）まで用意する」**ものは見つからない。日本の勝者はまだいない。

### 2-3. AIが毎日のミッションを決めるfitアプリ 🔴
| 競合 | 内容 |
|---|---|
| Mission Fitness | 日替わりミッション |
| Kairos Coach | 天気・睡眠・体調から毎日のおすすめを出す（**アイデアにかなり近い**） |
| Kynetic / DAY 1 / WeekFit / microfit | HealthKitのデータから毎日のプランを作る |
| Finch | ペット育成×セルフケア（月約$100万の推計） |

→ **英語圏はすでに大量にある**。勝つには「運動だけでなく食事・生活・人間関係までまとめてミッションにする」「キャラ性（鬼コーチなど）」「日本語・日本の生活に合わせる」が必要。

### 2-4. ミッション達成までSNSロック 🔴
ScrollToll、Push Up Lock、FitScroll（年$39.99）、EarnScroll、RepLock、MonkeyLock、EarnIt、そして本家のOpal……**2026年は似たアプリが大量に出ている**。
→ 単体では出さない。fitアプリの一機能にとどめる。

### 2-5. 写真でカロリー記録（Cal AIの日本版） 🔴
Cal AI（**日本語対応済み**）、あすけん、カロミル、スマ食べ、EatPal、メシトラ、Nutrola……
→ 激戦。差別化は難しい。

### 2-6. 社内シャッフルマッチング（Slack） 🟡
| 競合 | 内容 |
|---|---|
| **Donut** | 2万社以上、1,000万件以上のつながりを生んだ定番 |
| 日本製の代替 | 今回の検索では目立つものは見つからなかった |

→ Donutは「ランダム」に引き合わせる。**「Slackの分析で、相性の良い・共通の話題がある人を選ぶ」**＋日本語の自然な誘い文なら差別化できる（1-3と合体）。

### 2-7. 健康経営の歩数チャレンジ 🔴
| 競合 | 内容 |
|---|---|
| サントリー「歩こうフェス」 | チーム対抗の歩数イベント。導入2,000社以上、基本料金35,000（単位は未確認） |
| 健康経営アプリ全般 | ランキングやチーム対抗はすでに標準機能 |

→ 大手と既存のサービスが多い。単独参入はおすすめしない。

### 2-8. 推し活の遠征エージェント 🟢
| 競合 | 内容 |
|---|---|
| エアトリプラス | 航空券＋ホテルのセット、推し活向けの訴求あり。調査では1回の遠征予算は5〜10万円が最多 |
| ANA「GOOD TRIP EXPRESS」 | 推し活旅行の特集（記事・プラン） |
| トラベルコ | 横断比較 |

→ 大手は**「推し活向けのマーケティング」**はしているが、**「公演日程に連動した価格監視・当落や入金締切のリマインド・同行者のマッチング」**をまとめてやる専用サービスは見つからなかった。**最も空いている**。
→ 将来はエアトリなどがアフィリエイト先・提携先にもなりうる。

### 2-9. デスクトップ常駐の作業用ゲーム 🟡
| 競合 | 実績 |
|---|---|
| Rusty's Retirement | **33万本以上**（$6.99） |
| Bongo Cat | 無料、同時接続約15万人。Steamのトップ10入り |
| Desktop Mate | Steamのチャート上位 |
| Tiny Pasture など | 「デスクトップ常駐」がSteamの公式タグになった |

→ 市場は実証済みだが、**ある週には放置ゲームが54本も出ていて、似たものだらけ**という報道がある。**「健康ミッション（水・ストレッチ・姿勢）」**という役に立つ要素で差別化する。

---

## 3. 優先順位（更新版）

| 順位 | プロダクト | 理由 |
|---|---|---|
| **1** | **推し活の遠征エージェント**（B2C・Web＋LINE） | 競合が最も薄い。旅行・リマインド・友達のアイデアがすべて活きる |
| **2** | **Slackの「つなぐ」分析＋相性マッチング**（B2B） | 日本製の競合が見当たらない。B2Bなので顧客数は少なくて済む。ただしMarketplaceの審査を前提に計画する |
| 3 | デスクトップ常駐の健康ミッションゲーム（Steam） | 市場は実証済み。上の2つと並行して小さく作れる |
| 保留 | fitアプリ・SNSロック・カロリー記録・健康経営 | 激戦。単独では出さない |

---

## 出典
- Slack API: [2025年5月 規約・レート制限の変更FAQ](https://api.slack.com/changelog/2025-05-terms-rate-limit-update-and-faq) / [Rate limit changes for non-Marketplace apps](https://docs.slack.dev/changelog/2025/05/29/rate-limit-changes-for-non-marketplace-apps) / [日本語FAQ](https://docs.slack.dev/ja-jp/2025-05-terms-rate-limit-update-and-faq)
- Slack分析の競合: [HCA Mag: Employee listening](https://www.hcamag.com/us/specialization/transformation/employee-listening-ai-reads-your-slack-but-cant-say-why/594299) / [Mimecast: Slack sentiment analysis](https://mimecast.com/blog/slack-sentiment-analysis) / [Worklytics](https://www.worklytics.co/blog/slack-analytics-for-executives-how-to-measure-organizational-health) / [Flowtrace](https://flowtrace.co/collaboration-analytics-for-slack) / [Compass](https://slack.com/apps/A39JLCJVB-compass) / [Count](https://count.co/integration/slack/communication-network-analysis) / [Chatacuity](https://slack.com/marketplace/AKWJUT1T6-chatacuity) / [Slack: エンゲージメントアプリ](https://slack.com/intl/ja-jp/blog/collaboration/employee-engagement-apps) / [カオナビ Slack連携](https://www.kaonavi.jp/connected-partner/slack/)
- Donut: [Slack公式ブログ](https://slack.com/intl/ja-jp/blog/developers/donut-built-slack-first-business)
- 友達系: [Shirase](https://apps.apple.com/jp/app/shirase-%E3%83%BC%E3%81%95%E3%82%8A%E3%81%92%E3%81%AA%E3%81%8F%E5%8F%8B%E9%81%94%E3%82%92%E8%AA%98%E3%81%88%E3%82%8B%E3%82%A2%E3%83%97%E3%83%AA%E3%83%BC/id1594209501) / [今日ひま](https://apps.apple.com/us/app/-/id6689504007) / [Digipals](https://www.ycombinator.com/companies/digipals)
- fit・ロック系: [Kairos Coach](https://apps.apple.com/us/app/-/id6746157421) / [Mission Fitness](https://apps.apple.com/us/app/-/id6504419215) / [Kynetic](https://apps.apple.com/app/id6757194971) / [FitScroll](https://apps.apple.com/us/app/id6758033229) / [ScrollToll](https://play.google.com/store/apps/details?id=com.scrolltoll) / [EarnScroll](https://apps.apple.com/us/app/id6760631027)
- カロリー: [Cal AI（日本）](https://apps.apple.com/JP/app/id6480417616) / [スマ食べ](https://apps.apple.com/jp/app/%E3%82%B9%E3%83%9E%E9%A3%9F%E3%83%99-ai%E3%81%AB%E3%82%88%E3%82%8B%E9%A3%9F%E4%BA%8B%E5%88%86%E6%9E%90%E3%81%A8%E8%A8%98%E9%8C%B2/id6744808650) / [EatPal](https://apps.apple.com/jp/app/id6739669474)
- 健康経営: [サントリー 歩こうフェス](https://www.suntory.co.jp/softdrink/jihanki/solution/suntoryplus/aruko_fes/) / [一創: 健康経営サービスの選び方](https://www.issoh.co.jp/column/details/18530/) / [YuLife: 健康経営アプリ](https://yulife.com/jp/blog/corporate-health-apps-top5-2025)
- 推し活遠征: [エアトリ 推し活遠征調査](https://www.atpress.ne.jp/news/8907360) / [GOOD TRIP EXPRESS 推し活特集](https://www.oricon.co.jp/pressrelease/3014522/) / [トラベルコ](https://apps.apple.com/jp/app/id923916510)
- 航空券: [エアトリ: 安い時期](https://www.airtrip.jp/travel-column/22370) / [Skyscanner: 航空券価格の仕組み](https://www.skyscanner.jp/news/science-behind-flight-pricing-2)
- デスクトップ常駐: [GameDiscoverCo: Rusty's Retirement](https://newsletter.gamediscover.co/p/how-rustys-retirement-idle-farmed) / [PC Gamer: Bongo Cat](https://www.pcgamer.com/gaming-industry/game-development/top-10-steam-game-bongo-cat-is-actually-losing-us-money-says-dev-which-is-fine-because-its-been-great-for-business-before-we-knocked-on-50-doors-now-they-are-coming-to-us) / [PC Gamer: 1週間で54本の放置ゲーム](https://pcgamer.com/gaming-industry/steam-week-in-review-54-idle-games-released-on-steam-last-week-and-many-look-eerily-similar) / [Gamepressure: desktop buddies](https://www.gamepressure.com/newsroom/from-rustys-retirement-to-tiny-pasture-the-new-wave-of-desktop-bu/z679b4)

※ 「見つからなかった」は今回の検索範囲での話です。参入前には、App Store・Slack Marketplace・Xで改めて確認してください。
