# Powerlink Energy README、404 与上线收尾实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 README 统一改为中文，补齐正式 404 页面，并整理可直接执行的最终上线文件清单与发布顺序。

**Architecture:** 继续沿用当前纯静态站点结构，不新增构建链路。404 页面直接复用现有 `assets/css/site.css`、`assets/js/site.js`、统一 header/footer 与按钮体系；README 负责项目摘要，详细上线步骤继续沉淀到独立部署文档。

**Tech Stack:** HTML、CSS、原生 JavaScript、Python 冒烟测试、阿里云 OSS、Cloudflare

---

## 文件结构

- **创建：** `404.html`
  - 新增正式品牌型 404 页面，复用站点头尾与现有按钮风格。
- **修改：** `README.md`
  - 统一改为中文，保留项目简介、本地预览、路由、部署摘要、Cases 维护说明。
- **修改：** `assets/css/site.css`
  - 增加 404 Hero 与辅助说明的少量样式。
- **修改：** `docs/deployment/cloudflare-oss-launch.md`
  - 明确最终上传文件清单、发布顺序、OSS 错误页配置为 `404.html`。
- **创建：** `tests/check_readme_404_launch.py`
  - 用于锁定 README 中文化、404 页面骨架和部署文档关键字段。

### 任务 1：先锁定 README、404 与发布文档要求

**Files:**
- Create: `tests/check_readme_404_launch.py`
- Test: `tests/check_readme_404_launch.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/check_readme_404_launch.py`：

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    readme = read("README.md")
    deployment = read("docs/deployment/cloudflare-oss-launch.md")
    page_404 = read("404.html")

    assert "## 项目简介" in readme, "README 仍未统一为中文结构"
    assert "## 本地预览" in readme, "README 缺少中文本地预览章节"
    assert "## 上线包摘要" in readme, "README 缺少上线包摘要"

    assert 'data-site-header' in page_404, "404 页面缺少统一站点头部挂载点"
    assert 'data-site-footer' in page_404, "404 页面缺少统一站点底部挂载点"
    assert 'href="/"' in page_404, "404 页面缺少返回首页入口"
    assert 'href="/solutions/"' in page_404, "404 页面缺少 Solutions 入口"
    assert 'href="/contact/"' in page_404, "404 页面缺少联系入口"

    assert "`404.html`" in deployment, "部署文档缺少 404 文件说明"
    assert "错误页指向 `404.html`" in deployment, "部署文档未切换到正式 404 配置"
    assert "发布顺序" in deployment, "部署文档缺少发布顺序章节"

    print("readme 404 launch hooks OK")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 运行测试并确认失败**

运行：

```bash
py -3 tests/check_readme_404_launch.py
```

预期：

```text
FileNotFoundError: [Errno 2] No such file or directory: '...\\404.html'
```

- [ ] **Step 3: 提交失败测试**

```bash
git add tests/check_readme_404_launch.py
git commit -m "test: add readme and 404 launch checks"
```

### 任务 2：实现中文 README 与品牌型 404 页面

**Files:**
- Modify: `README.md`
- Create: `404.html`
- Modify: `assets/css/site.css`
- Test: `tests/check_readme_404_launch.py`

- [ ] **Step 1: 将 README 改为中文结构**

把 `README.md` 改成下面这套中文结构：

```md
# Powerlink Energy 官网项目

## 项目简介

Powerlink Energy 官方网站静态站点项目，面向数据中心、通信、电池储能、逆变器及相关关键电力应用场景。

## 技术栈

- HTML
- CSS
- 原生 JavaScript

## 本地预览

使用 Python 在项目根目录启动本地静态服务：

```bash
py -3 -m http.server 8000
```

打开：

```text
http://127.0.0.1:8000/
```

## 主要页面路由

- `/`
- `/about/`
- `/contact/`
- `/solutions/`
- `/products/`
- `/cases/`
- `/404.html`

## 部署说明

项目上线采用阿里云 OSS + Cloudflare 架构。

- OSS 负责静态文件托管
- Cloudflare 负责 DNS、HTTPS、缓存和基础安全
- 详细发布步骤见 `docs/deployment/cloudflare-oss-launch.md`

## Cases 维护说明

- 在 `assets/js/data.js` 中新增或更新案例数据
- 为每个新案例创建 `cases/<slug>/index.html`
- 仅在拿到可验证素材后填写 `heroImage`、`gallery`、`galleryNote`
- 发布前至少检查一次案例概览页和一个详情页

## 上线包摘要

- 上传项目根目录中的正式静态文件
- 将 `index.html` 设为默认首页
- 将 `404.html` 设为正式错误页
- 更新后按范围清理 Cloudflare 缓存

## 注意事项

- 当前站点使用 CSS 文字 Logo
- 联系表单仍为静态邮件跳转方式
- 非正式交付文件如 `tests/`、`docs/superpowers/` 不参与上线
```

- [ ] **Step 2: 新建品牌型 `404.html`**

创建 `404.html`：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>404 | Powerlink Energy</title>
  <meta name="description" content="The page you are looking for does not exist or has been moved.">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  <div data-site-header></div>
  <main>
    <section class="page-hero page-hero--404">
      <div class="container not-found">
        <p class="eyebrow">Page Not Found</p>
        <h1>404</h1>
        <p>你访问的页面不存在、链接已更新，或当前地址暂时不可用。你可以返回首页、查看方案页面，或直接联系 Powerlink Energy。</p>
        <div class="button-row">
          <a class="button button--primary" href="/">返回首页</a>
          <a class="button button--ghost" href="/solutions/">查看 Solutions</a>
          <a class="button button--ghost" href="/contact/">联系我们</a>
        </div>
        <div class="not-found__note">
          <p>如果你是通过旧链接进入本站，建议从首页重新进入或直接向我们发送需求。</p>
        </div>
      </div>
    </section>
  </main>
  <div data-site-footer></div>
  <script src="/assets/js/data.js"></script>
  <script src="/assets/js/site.js"></script>
</body>
</html>
```

- [ ] **Step 3: 在 `assets/css/site.css` 中补充 404 样式**

把下面这段样式加到现有 hero 相关区域附近：

```css
.page-hero--404 {
  padding: 88px 0 96px;
}

.not-found {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 18px;
  min-height: 420px;
  justify-content: center;
}

.not-found h1 {
  margin: 0;
  font-size: clamp(72px, 12vw, 160px);
  line-height: 0.95;
}

.not-found > p {
  max-width: 760px;
  color: rgba(255, 255, 255, 0.82);
}

.not-found__note {
  margin-top: 6px;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.not-found__note p {
  margin: 0;
  color: rgba(255, 255, 255, 0.78);
}
```

- [ ] **Step 4: 运行测试并确认通过**

运行：

```bash
py -3 tests/check_readme_404_launch.py
```

预期：

```text
readme 404 launch hooks OK
```

- [ ] **Step 5: 检查样式文件诊断**

检查：

```text
assets/css/site.css
```

预期：

```text
无新增诊断错误
```

- [ ] **Step 6: 提交页面与 README 更新**

```bash
git add README.md 404.html assets/css/site.css tests/check_readme_404_launch.py
git commit -m "feat: add branded 404 page and chinese readme"
```

### 任务 3：补齐最终上线文件清单与发布顺序，并完成预览验收

**Files:**
- Modify: `docs/deployment/cloudflare-oss-launch.md`
- Test: `tests/check_readme_404_launch.py`
- Test: 浏览器预览

- [ ] **Step 1: 重写部署文档中的发布顺序章节**

确保 `docs/deployment/cloudflare-oss-launch.md` 至少包含这两段内容：

```md
## 1. 最终上传文件清单

必须上传：

- `index.html`
- `404.html`
- `about/`
- `contact/`
- `products/`
- `solutions/`
- `cases/`
- `assets/`
- `downloads/` 中被页面引用的文件
- `robots.txt`
- `sitemap.xml`

不要上传：

- `tests/`
- `docs/superpowers/`
- brainstorming、临时协作材料
```

```md
## 2. 推荐发布顺序

1. 本地预览检查首页、Cases、Products、Solutions 和 `404.html`
2. 将正式静态文件上传到 OSS
3. 在 OSS 中将默认首页设置为 `index.html`
4. 在 OSS 中将错误页设置为 `404.html`
5. 在 Cloudflare 中完成 DNS、代理、HTTPS、缓存配置
6. 清理 Cloudflare 缓存
7. 抽查线上首页、案例页、404 页面和静态资源
```

- [ ] **Step 2: 保留并补强 Cloudflare/OSS 关键配置说明**

在文档中明确以下文字：

```md
- `www.power-linkenergy.com` 为主访问域名
- Cloudflare 回源地址需与 OSS 公网访问地址一致
- 更新 `assets/css/site.css` 或 `assets/js/site.js` 后，建议清理共享资源缓存
- Cases 页面更新后，至少清理 `/cases/*` 路径缓存
```

- [ ] **Step 3: 再次运行文档与 404 测试**

运行：

```bash
py -3 tests/check_readme_404_launch.py
```

预期：

```text
readme 404 launch hooks OK
```

- [ ] **Step 4: 启动本地预览**

运行：

```bash
py -3 -m http.server 8013
```

预期：

```text
Serving HTTP on 0.0.0.0 port 8013
```

- [ ] **Step 5: 浏览器检查首页与 404 页面**

打开：

```text
http://127.0.0.1:8013/
http://127.0.0.1:8013/404.html
```

预期：

- 首页正常打开
- 404 页面加载统一 header/footer
- 404 页面显示 3 个 CTA：返回首页、查看 Solutions、联系我们

- [ ] **Step 6: 提交上线文档更新**

```bash
git add docs/deployment/cloudflare-oss-launch.md
git commit -m "docs: finalize launch checklist and publish order"
```
