# 回头记录工具 (Lookback Tracker)

课堂观察研究工具 — 记录和统计同学上课期间回头行为的次数、时长和间隔。

基于 [csTimer](https://github.com/cs0x7f/csTimer) 改造，移除了打乱、求解、DNF、+2 等魔方计时功能，保留并改造了计时和统计模块。

## 功能特性

- **开始上课**：点击"开始上课"按钮开始记录会话
- **长按记录**：统计人员在观察对象回头时长按屏幕，松开结束记录
- **实时计时**：显示当前回头时长和上课总时间
- **事件列表**：记录每次回头的开始时间、时长和间隔
- **统计指标**：
  - 回头次数
  - 全局平均回头时长
  - 全局平均回头间隔
  - AO12 时长（最近12次回头，去掉最长和最短的平均时长）
  - AO12 间隔（最近12次回头，去掉最长和最短的平均间隔）
  - 最长回头时长
- **CSV 导出**：上课结束自动生成 CSV 文件，也可手动导出
- **本地存储**：数据自动备份到浏览器 localStorage

## 部署指南

### 方式一：GitHub Pages 自动部署（推荐）

1. **Fork 本仓库**到你的 GitHub 账号

2. **启用 GitHub Pages**：
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"
   - 保存设置

3. **触发部署**：
   - 推送任何代码到 `master` 分支，或
   - 在 Actions 页面手动触发 "Deploy to Github Pages" 工作流

4. **访问应用**：
   - 部署完成后访问 `https://<你的用户名>.github.io/dstimer/`

### 方式二：直接打开 HTML 文件

应用是一个完全独立的 HTML 文件，无需服务器：

```bash
# 克隆仓库
git clone https://github.com/<你的用户名>/dstimer.git
cd dstimer

# 直接在浏览器中打开
open app/index.html        # macOS
xdg-open app/index.html    # Linux
start app\index.html       # Windows (CMD)
# PowerShell: Invoke-Item app\index.html
```

### 方式三：使用任意 Web 服务器

```bash
# 使用 Python 内置服务器
cd app
python3 -m http.server 8080
# 访问 http://localhost:8080

# 或使用 Node.js 的 http-server
npx http-server app -p 8080
# 访问 http://localhost:8080

# 或使用 PHP 内置服务器
php -S localhost:8080 -t app
# 访问 http://localhost:8080
```

### 方式四：部署到其他平台

#### Netlify
1. 登录 [Netlify](https://www.netlify.com/)
2. 将 `app` 文件夹拖拽到 Netlify 部署页面
3. 自动获得一个 HTTPS 链接

#### Vercel
```bash
npm i -g vercel
cd app
vercel
```

#### Cloudflare Pages
1. 连接你的 GitHub 仓库
2. 构建命令留空
3. 输出目录设为 `app`

## 使用说明

1. **开始记录**：点击"开始上课"按钮
2. **记录回头**：当观察对象回头看时，长按屏幕（触屏）或按住鼠标左键（电脑）
3. **结束回头**：观察对象转回时，松开手指/鼠标
4. **查看统计**：右侧/下方面板实时显示统计数据
5. **结束上课**：点击"结束上课"按钮，CSV 自动导出
6. **手动导出**：随时点击"导出 CSV"按钮导出当前数据

## 统计指标说明

| 指标 | 说明 |
|------|------|
| 回头次数 | 总共记录的回头次数 |
| 全局平均回头时长 | 所有回头时长的算术平均值 |
| 全局平均回头间隔 | 所有回头间隔的算术平均值（第一次为距上课开始的时间） |
| AO12 时长 | 最近12次回头时长，去掉最长和最短后的平均值 |
| AO12 间隔 | 最近12次回头间隔，去掉最长和最短后的平均值 |
| 最长回头 | 单次回头的最长时长 |

## CSV 输出格式

导出的 CSV 文件包含以下字段：

```
序号, 回头开始时间(ms), 回头结束时间(ms), 回头时长(ms), 回头间隔(ms), 回头开始时间, 回头时长(s), 回头间隔(s)
```

文件末尾附带统计摘要。

## 技术栈

- 纯 HTML + CSS + JavaScript（无需构建工具）
- 响应式设计，支持手机和电脑
- 数据本地存储（localStorage）
- GitHub Actions 自动部署

## 原项目

本项目基于 [csTimer](https://github.com/cs0x7f/csTimer)（专业魔方计时工具）改造。原项目的魔方计时器代码保留在 `src/` 目录中。
