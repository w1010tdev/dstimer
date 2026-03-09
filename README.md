# 回头记录工具 (Lookback Tracker)

课堂观察研究工具 — 记录和统计同学上课期间回头行为的次数、时长和间隔。

## 功能特性

- **密码保护**：输入密码 `2427` 才能进入系统进行统计和上传
- **开始上课**：点击"开始上课"按钮开始记录会话
- **长按记录**：统计人员在观察对象回头时长按屏幕，松开结束记录
- **实时计时**：显示当前回头时长和上课总时间
- **事件列表**：记录每次回头的开始时间、时长和间隔
- **统计指标**：
  - 回头次数
  - **回头系数**（每分钟平均回头次数）
  - 全局平均回头时长
  - 全局平均回头间隔
  - AO12 时长（最近12次回头，去掉最长和最短的平均时长）
  - AO12 间隔（最近12次回头，去掉最长和最短的平均间隔）
  - 最长回头时长
- **CSV 导出**：上课结束自动生成 CSV 文件
- **后端同步**：CSV 自动上传到 Flask 后端服务器保存

## 项目结构

```
dstimer/
├── app/
│   └── index.html          # 前端页面（独立 HTML 文件）
├── server/
│   ├── app.py              # Flask 后端服务器
│   ├── requirements.txt    # Python 依赖
│   └── uploads/            # CSV 文件存储目录（自动创建）
├── .github/
│   └── workflows/
│       └── pages.yml       # GitHub Pages 自动部署
├── README.md
└── LICENSE
```

## 部署指南

### 一、前端部署

#### 方式 A：GitHub Pages 自动部署（推荐）

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

#### 方式 B：直接打开 HTML 文件

应用是一个完全独立的 HTML 文件，无需服务器即可使用基本功能：

```bash
# 克隆仓库
git clone https://github.com/<你的用户名>/dstimer.git
cd dstimer

# 直接在浏览器中打开
open app/index.html        # macOS
xdg-open app/index.html    # Linux
start app\index.html       # Windows (CMD)
```

### 二、后端部署（Flask 服务器）

后端用于接收和存储前端自动上传的 CSV 文件。

#### 环境要求

- Python 3.8+
- pip

#### 本地运行

```bash
# 进入 server 目录
cd server

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

服务器默认运行在 `http://0.0.0.0:5000`。

#### 配置前端连接后端

在前端页面底部的 **后端服务器地址** 输入框中填入后端地址，例如：
- 本地开发：`http://localhost:5000`
- 远程服务器：`http://your-server-ip:5000`

#### 生产环境部署

推荐使用 Gunicorn + Nginx：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动（4 worker 进程）
cd server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Nginx 反向代理配置示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 云平台部署

**Railway / Render / Fly.io 等平台：**

1. 将 `server/` 目录作为项目根目录
2. 启动命令：`gunicorn -w 2 -b 0.0.0.0:$PORT app:app`
3. 设置环境变量或直接使用默认配置

### 三、API 接口

| 接口 | 方法 | 参数 | 说明 |
|------|------|------|------|
| `/api/upload` | POST | `file` (CSV文件), `password` | 上传 CSV 文件 |
| `/api/files` | GET | `password` (查询参数) | 列出所有已上传的 CSV 文件 |
| `/api/files/<filename>` | GET | `password` (查询参数) | 下载指定 CSV 文件 |

所有接口都需要密码 `2427` 验证。

## 使用说明

1. **输入密码**：打开页面后输入密码 `2427`
2. **配置服务器**：在底部输入后端服务器地址（可选，不配置则仅本地导出）
3. **开始记录**：点击"开始上课"按钮
4. **记录回头**：当观察对象回头看时，长按屏幕（触屏）或按住鼠标左键（电脑）
5. **结束回头**：观察对象转回时，松开手指/鼠标
6. **查看统计**：右侧/下方面板实时显示统计数据
7. **结束上课**：点击"结束上课"按钮，CSV 自动导出并上传到后端
8. **手动导出**：随时点击"导出 CSV"按钮导出当前数据

## 统计指标说明

| 指标 | 说明 |
|------|------|
| 回头次数 | 总共记录的回头次数 |
| 回头系数 | 每分钟平均回头次数（回头次数 ÷ 已过分钟数）|
| 全局平均回头时长 | 所有回头时长的算术平均值 |
| 全局平均回头间隔 | 所有回头间隔的算术平均值 |
| AO12 时长 | 最近12次回头时长，去掉最长和最短后的平均值 |
| AO12 间隔 | 最近12次回头间隔，去掉最长和最短后的平均值 |
| 最长回头 | 单次回头的最长时长 |

## 技术栈

- **前端**：纯 HTML + CSS + JavaScript（无需构建工具）
- **后端**：Python Flask + Flask-CORS
- **部署**：GitHub Actions → GitHub Pages（前端）
