# Powerlink Energy 官网项目

## 项目简介

Powerlink Energy 官方网站静态站点项目，面向数据中心、通信、电池储能、逆变器及相关关键电力应用场景。

站点支持 **英文（默认）**、**简体中文**、**法语**、**俄语** 四种语言。

## 技术栈

- HTML
- CSS
- 原生 JavaScript
- Python（仅用于静态页面生成，不参与线上运行时）

## 本地预览

使用 Python 在项目根目录启动本地静态服务：

```bash
py -3 -m http.server 8000
```

打开：

| 语言 | 地址 |
|------|------|
| 英文 | http://127.0.0.1:8000/ |
| 中文 | http://127.0.0.1:8000/zh/ |
| 法语 | http://127.0.0.1:8000/fr/ |
| 俄语 | http://127.0.0.1:8000/ru/ |
| 阿拉伯语 | http://127.0.0.1:8000/ar/ |

当前站点按**域名根路径**部署设计，英文页面位于根路径，其他语言位于 `/zh/`、`/fr/`、`/ru/`、`/ar/` 前缀下（阿拉伯语为 RTL 排版）。共享资源（CSS、JS、图片）仍从 `/assets/` 与 `/downloads/` 加载。

## 内容维护与页面生成

**不要直接手改各语言 HTML 页面。** 正确流程：

1. 编辑 `assets/locales/en.json`、`zh.json`、`fr.json`、`ru.json`、`ar.json`
2. 运行生成器：

```bash
py -3 scripts/generate_og_share_image.py
py -3 scripts/generate_favicon.py
py -3 scripts/generate_image_variants.py
py -3 scripts/generate_static_pages.py
```

`generate_og_share_image.py` 会生成五语言 OG 分享图（`assets/images/og-share*.jpg`）。更新 locale 文案后若需刷新分享图，先运行该脚本再运行页面生成器。

`generate_favicon.py` 会生成 `favicon.ico`、`favicon-16x16.png`、`favicon-32x32.png`、`apple-touch-icon.png`（基于品牌色和 "P" 字母 + 强调点）。仅当品牌视觉需要调整时重新生成。

`generate_image_variants.py` 会根据现有基础图生成 HTML 中引用的派生图变体（`012-hero-optimized.jpg`、`025-lineup-optimized.jpg`、`001-clean-optimized.jpg`）。这些是占位派生图，如果产生了正式的精修图片可以直接替换同名文件，脚本会自动跳过已存在文件。

依赖安装（使用 E 盘虚拟环境）：

```bash
py -3 -m venv E:\venvs\powerlink-web
E:\venvs\powerlink-web\Scripts\python.exe -m pip install Pillow
```

后续所有图片/页面生成脚本均使用 `E:\venvs\powerlink-web\Scripts\python.exe` 调用。

生成器会：

- 输出五语言全部 HTML 页面（首页、Solutions、Products、Cases、About、Contact 及详情页）
- 生成五语言 `404.html`（根目录 + 各语言前缀目录）
- 更新 `sitemap.xml`
- 将英文 locale 同步到 `assets/js/data.js`（兼容旧引用）

## 主要页面路由

英文（根路径）：

- `/`
- `/about/`
- `/contact/`
- `/solutions/`
- `/products/`
- `/cases/`
- `/404.html`

其他语言（以中文为例）：

- `/zh/`
- `/zh/about/`
- `/zh/contact/`
- `/zh/solutions/`
- `/zh/products/`
- `/zh/cases/`
- `/zh/404.html`

## 部署说明

项目上线采用阿里云 OSS + Cloudflare 架构。

- OSS 负责静态文件托管
- Cloudflare 负责 DNS、HTTPS、缓存和基础安全
- 详细发布步骤见 `docs/deployment/cloudflare-oss-launch.md`

## Cases 维护说明

1. 在 `assets/locales/*.json` 的 `cases` 数组中新增或更新案例数据（五种语言同步维护）
2. 运行 `py -3 scripts/generate_static_pages.py` 重新生成页面
3. 仅在拿到可验证素材后填写 `heroImage`、`gallery`、`galleryNote`
4. 发布前至少检查一次案例概览页和一个详情页（建议中英文各抽查一页）

## 上线包摘要

- 只上传正式静态网站文件，不要盲传整个仓库
- 将 `index.html` 设为默认首页
- 将根目录 `404.html` 设为 OSS 正式错误页
- 更新后按范围清理 Cloudflare 缓存（含 `/zh/*`、`/fr/*`、`/ru/*`、`/ar/*`）

建议上线包 allowlist：

- `index.html`
- `404.html`
- `about/`
- `contact/`
- `products/`
- `solutions/`
- `cases/`
- `zh/`（含 `zh/404.html`）
- `fr/`（含 `fr/404.html`）
- `ru/`（含 `ru/404.html`）
- `ar/`（含 `ar/404.html`）
- `assets/`（含 `assets/images/og-share.jpg` 及 `og-share-zh.jpg`、`og-share-fr.jpg`、`og-share-ru.jpg`、`og-share-ar.jpg` 社交分享图）
- `downloads/` 中被页面实际引用的图片文件
- `robots.txt`
- `sitemap.xml`

明确不要上传：

- `assets/locales/`（源数据，仅用于本地生成）
- `scripts/dev/`（locale 批量维护脚本，仅开发使用）
- 根目录 `.xlsx`、`.docx`、`.log`、`.txt` 业务文件
- `scripts/`
- `tests/`
- `brainstorm/`
- `docs/superpowers/`
- `downloads/supplier_images/summary.md`
- `downloads/supplier_images/shortlist.md`
- `downloads/supplier_images/manifest.csv`

## 注意事项

- 当前站点使用 CSS 文字 Logo
- 首页不再依赖外部 AI 首屏图
- 当前部分 Solutions 页面仍使用已下载的供应商参考图，发布前需确认授权与品牌可接受范围
- 联系表单仍为静态 `mailto:` 邮件跳转方式，Form endpoint 尚未接入；邮件主题与字段标签已按页面语言本地化
- 非正式交付文件如 `tests/`、`docs/superpowers/`、`assets/locales/` 不参与上线

## 测试说明

发布前至少运行以下检查：

```bash
py -3 tests/check_about_process_layout.py
py -3 tests/check_about_contact_visual.py
py -3 tests/check_home_advantage_cards.py
py -3 tests/check_detail_card_system.py
py -3 tests/check_cases_visual_system.py
py -3 tests/check_contact_promise_cards.py
py -3 tests/check_readme_404_launch.py
py -3 tests/check_static_rendering.py
py -3 tests/check_route_data_alignment.py
py -3 tests/check_sitemap_routes.py
py -3 tests/check_multilingual_integrity.py
py -3 tests/check_deployment_assumptions.py
py -3 tests/check_public_artifact_hygiene.py
py -3 tests/check_og_social_meta.py
```

这些检查覆盖静态内容、路由与数据对齐、多语言完整性、站点地图、404/部署文档以及上线包边界。
