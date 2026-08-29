# 雾锁深楼 · RPG 推理游戏

一款网页端（纯 HTML + CSS + JS）的单人推理 RPG 游戏。

## 玩法特性

- **搜证系统**：在场景中拾取线索，累积观察力（触发机制解耦：不再依赖对白末尾放大镜台词，改为节点配置 `node.search` 显式标记；最后一句对白显示完毕后由玩家再点一次空白才触发搜证，以 toast 轻量提示代替对话框旁白）
- **盘问系统**：对嫌疑人提问，解锁证词与细节（choices≥4 条时自动隐藏底部对话框，避免遮挡下方选项）
- **时间线梳理**：按时间轴还原案发经过
- **推论系统**：根据已有线索锁定凶手，解锁对应结局
- **能力六维图**：观察力 / 直觉 / 勇气 / 推理力 / 共情力 / 洞察力
- **剧情脉络**：可视化展示已解锁节点和多结局分支；PC 鼠标滚轮缩放/拖拽平移，移动端单指拖拽 + 双指捏合缩放（放大上限 18 倍可看到单节点）
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

- **评分系统**：Cloudflare Workers + KV（namespace `RATING_KV`，key=`rating` → `{sum,count}`）实现真共享评分；Worker URL 在 `index.html` 的 `RATING_API`，源码在 `worker/worker.js`。Worker 不可达时回退到本地兜底数值显示。
- **访问统计**：GoatCounter 图片像素统计，代码在 `index.html` 的 `GoatCounter` 相关区块
