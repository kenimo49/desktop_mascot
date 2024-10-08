# desktop_mascot

## 目標フェーズ
v1: 
デスクトップマスコットとして、ペットとしての機能を持たせる

V2: 
デスクトップマスコットかつサポートキャラクターとして、PC使用者のサポートを行う
定期的に、名言を共有して、やる気をださせる。
タスク状況を報告して、仕事の進捗を確認する。
キーロガーの機能を使って、どの処理に時間がかかっているかを確認する & ゲーム等をしている場合は、注意を促す

vFinal: 
PCやEC2上で動かして人間は許可と確認だけして、actionはすべてサポートキャラクターにやらせる
之には、コーディングや設計、人とのコミュニケーション(連絡、指示)
投資に関しての根拠出しや操作も行う

やること

- [ ] 基本機能
  - [x] デスクトップマスコットを表示する
  - [ ] アイコンを設置する
  - [ ] パッケージ化する
    - バージョン管理を行う
  - [ ] インストールウィザードを用意する
- [ ] 会話機能
  - [x] テキストを表示する
  - [ ] 文字を入力できる
  - [ ] 音声を再生する
  - [ ] 音声を認識する
  - [x] 画像を表示できる
- [ ] デスクトップアプリの機能
  - [ ] キャラクターを選択できる
    - [ ] キャラクターを追加できる
    - [ ] キャラクターを削除できる
    - [ ] キャラクターを変更できる
    - [ ] キャラクターを複数選択して、ランダムで表示できる
  - [ ] レベルを上げれる 
  - [x] 動き回る機能を追加する
  - [x] 定期的につぶやく
    - [x] 登録できる
      - [x] テキストを登録できる
      - [x] 画像を登録できる
    - [x] 登録されているつぶやくの一覧を表示する
    - [x] 画像も登録されていればそれも一緒に表示する
    - [ ] URLが登録されていたら、それを開ける
    - [x] つぶやきを削除できる
    - [ ] つぶやく間隔を設定できる
    - [ ] つぶやく時間を設定できる
- [ ] 移動するときに、アニメーションをつける

- [ ] LLMと連携して会話を行う
- [x] databaseに保存できる
  - sqlalchemyで定義する
  - sqliteDBを使用する

- [ ] キーロガー的な機能
  - [x] キーボード何をしたのかアクションを記憶する
    - [ ] ブラウザで何をしたのかを把握する
      - どのブラウザ or アプリケーションなのか認識が上手くいかないので修正する
  - [ ] クリップボードにコピーしたときに理解する
  - [ ] 定期的なスクショ処理を行う

- ビジネス的な機能
  - [ ] ポイントを貯める機能(お得な)を追加する
  - [ ] 別のキャラクターと会話 or 連携 or 競争できる機能をつける
  - [ ] メルマガと連携して、その人が話しているように見える
- タスク管理
  - [ ] タスクを登録できる
  - [ ] 決まった時間にタスクの登録を要求する
  - [ ] 定期的にタスクの進捗を確認する
  - [ ] なにかと連携して、タスク管理をスマホ等でも可能にする


## ビジネスアイディア
* アプリをリリースした後に、追加機能をフィードバックで受信可能にする
  * この時に、お金を出してフィードバックした機能やお金を出すほどではないがやってほしいなど、分けることができるようにする
  * これにより、開発資金と実際にどのように使われているかを見えるかして、ユーザが使用者だけではなく、一緒に作っている仲間として誤認させる