# 雾锁深楼 · RPG 推理游戏

一款网页端（纯 HTML + CSS + JS）的单人推理 RPG 游戏。

## 玩法特性

- **搜证系统**：在场景中拾取线索，累积观察力
- **盘问系统**：对嫌疑人提问，解锁证词与细节
- **时间线梳理**：按时间轴还原案发经过
- **推论系统**：根据已有线索锁定凶手，解锁对应结局
- **能力六维图**：观察力 / 直觉 / 勇气 / 推理力 / 共情力 / 洞察力
- **剧情脉络**：可视化展示已解锁节点和多结局分支
- **多结局**：6 种结局（真结局 / 伪真相 / 放弃 / 伪善等）

## 运行方式

直接用浏览器打开 `index.html` 即可游玩。

> 如果需要托管：上传到任何静态页面托管（GitHub Pages、Vercel、Netlify），访问根目录下的 `index.html`。

## 文件结构

```
.
├── index.html              主页面（UI、游戏逻辑、样式）
├── game-script.js          剧情节点、对白、线索、角色、BGM 配置
├── compress_assets.py      资源压缩脚本（Pillow + FFmpeg）
├── assets/
│   ├── bgm/                背景音乐 MP3（7 首）
│   ├── backgrounds/        场景背景图（JPG）
│   ├── characters/         角色头像/立绘（JPG + PNG）
│   └── clues/              线索卡图片（JPG）
└── SKILL.md                RPG 游戏制作沉淀工作流
```

## 第三方接入（可选）

- **评分系统**：jsonbin.io 存放累计评分 `sum/count`，ID 在 `index.html` 的 `JSONBIN_BIN_ID`
- **访问统计**：GoatCounter 图片像素统计，代码在 `index.html` 的 `GoatCounter` 相关区块
