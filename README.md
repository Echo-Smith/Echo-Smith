```text
$ whoami
> 一个碳基 prompt，正在被 AI 反向调教
$ uptime
> 模型越智能，我们做的越轻越薄 —— 这页也是
```

不写自我介绍。下面的看板是机器人每天自己刷新的，我连改数字的机会都没有。热力图？官方那张就在楼下。

### 📊 每日战报

<!-- 由 .github/workflows/dashboard.yml 每日自动填充，请勿手改 -->
<!-- DASH:START -->
<sub>🤖 GitHub Actions 每天自动刷新 · 最近一次：2026-10-28 UTC · 窗口：近 90 天 · 热力图请看楼下官方版</sub>

> 近况：最近 7 天在加速 🚀

| 指标 | 数值 | 点评 |
| --- | --- | --- |
| commit | **314** | 雨露均沾 |
| PR | **62** | 平均 1.5 天一个 |
| 有贡献的天数 | **53 / 90** | 一半时间在写，一半时间在想写什么 |
| 最长连更 | **8 天** | 第 9 天在睡觉 |
| 单日最高 | **34**（2026-10-25，周日） | 周日 = 本人战斗日 |

**commit 去哪了**

```text
LuminWrite-OSS          ████████████████████████  130
mirror-memory           ████████████████          89
Routekeeper             █████                     29
speak-to-questionnaire  █████                     26
其他公开仓库            ███████                   40
```

<sub>commit / PR 来自 GitHub contributionsCollection；天数与单日统计全部贡献类型。</sub>
<!-- DASH:END -->

### 🎒 当前装备（AI 相关）

```text
[主武器]  pi harness（pi-ai + pi-durable + chord）  // LuminWrite TS 重写版的 Agent 底座
[背包]    PGlite + pgvector                           // 把整个 Postgres 塞进进程，向量顺便带上
[护甲]    Hono + zod-openapi                          // 先写契约，再写接口
[饰品]    BYOK：OpenAI / Anthropic 兼容接口            // 你的 key 你做主，模型注册改编自 magpie
[法术]    MCP                                         // client / server / 沙箱都写过
[宠物]    Cursor cloud agents                         // LuminWrite 的 PR 大多出自 cursor/* 分支
[被动]    盲评 + 回归门禁                              // 硬失败不能被平均分抵消
```

### 🥚 彩蛋

- 🧠 一个被教会**怎么忘记**的 Agent 记忆：用户说"别再提了"，它就真不提，备份恢复之后也不会诈尸 → [mirror-memory](https://github.com/Echo-Smith/mirror-memory)
- 🧬 拿干细胞分化的思路做方案生成，然后在 README 里自己承认：多花约 47% token，还没证明更好 → [stemcell](https://github.com/Echo-Smith/stemcell)
- 🎙 对着问卷说"下一题"，它真的翻页 → [speak-to-questionnaire](https://github.com/Echo-Smith/speak-to-questionnaire)
- 🪆 管理开源版 / 商业版的小工具，被它大哥 [LuminWrite](https://github.com/Echo-Smith/LuminWrite-OSS) 用上了 → [open-pro](https://github.com/Echo-Smith/open-pro)

```diff
+ 测试通过 ≠ 模型是对的
+ 每次只改一个变量
- 一键生成
- 编数据（看板是机器人填的，想编也插不上手）
```
