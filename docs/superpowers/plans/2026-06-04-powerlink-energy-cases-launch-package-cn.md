# Powerlink Energy Cases 上线包实施计划

> **给执行型代理：** 推荐按子任务逐项执行，并在每个任务完成后做一次测试与人工复核。

**目标：** 补强 Cases 首屏视觉、加入真实项目图片位与空状态模板，并整理 Cloudflare + 阿里云 OSS 上线说明。

**实现方式：** 继续沿用当前静态站点结构，在 `assets/js/data.js` 中补充案例媒体字段，在 `assets/js/site.js` 中扩展 Cases 渲染能力，在 `assets/css/site.css` 中补齐对应样式；部署说明以 Markdown 文档形式交付。

**技术栈：** HTML、CSS、原生 JavaScript、Python 冒烟测试、阿里云 OSS、Cloudflare

---

## 文件范围

- 修改 `assets/js/data.js`
  - 为现有 Cases 数据增加 `projectStatus`、`heroImage`、`gallery`、`galleryNote` 等可选字段
- 修改 `assets/js/site.js`
  - 新增 Cases 首屏、图片位、图库、空状态渲染
- 修改 `assets/css/site.css`
  - 新增 Cases 首屏布局、卡片媒体区、图库与空状态样式
- 修改 `cases/index.html`
  - 将简单首屏替换为 `cases-hero` 挂载点
- 修改 `tests/check_cases_visual_system.py`
  - 先写失败测试，再检查新增 Cases hooks
- 修改 `README.md`
  - 增加 Cases 维护说明与发布摘要
- 新增 `docs/deployment/cloudflare-oss-launch.md`
  - 输出完整上线步骤与缓存刷新说明

## 任务拆分

### 任务 1：锁定失败测试

- 先更新 `tests/check_cases_visual_system.py`
- 新增对 `renderCaseHero`、`renderCaseMedia`、`renderCaseGallery`、`.cases-hero`、`.case-gallery`、`.case-empty-state`、`id="cases-hero"` 的检查
- 运行：

```bash
py -3 tests/check_cases_visual_system.py
```

- 预期先失败在：

```text
AssertionError: missing cases overview hero renderer
```

### 任务 2：扩展 Cases 数据模型

- 在 `assets/js/data.js` 的 3 个案例对象中补充媒体字段
- 保持字段可选，不破坏现有渲染
- 再次运行失败测试，确认仍旧失败在缺少渲染函数，而不是数据结构错误

### 任务 3：实现 Cases 首屏与图片位

- 在 `cases/index.html` 中加入 `id="cases-hero"`
- 在 `assets/js/site.js` 中新增：
  - `renderCaseMedia`
  - `renderCaseHero`
  - `renderCaseGallery`
- 将 Cases 列表卡片接入顶部图片位
- 将 Cases 详情页接入 Hero 媒体位与 `Project Photos` 区块
- 在 `assets/css/site.css` 中补齐 Cases 首屏、卡片媒体区、图库与空状态样式
- 运行：

```bash
py -3 tests/check_cases_visual_system.py
py -3 tests/check_detail_card_system.py
```

### 任务 4：整理上线包文档并验收

- 更新 `README.md`
- 新增 `docs/deployment/cloudflare-oss-launch.md`
- 启动本地预览：

```bash
py -3 -m http.server 8013
```

- 检查：

```text
http://127.0.0.1:8013/cases/
http://127.0.0.1:8013/cases/small-data-center-backup-power/
```

- 验收点：
  - Cases 首屏更完整
  - Cases 卡片支持图片位与空状态
  - Cases 详情页出现 `Project Photos` 模块
  - Cloudflare + OSS 上线说明可直接交付使用

## 当前结果

- 以上 4 个任务已经完成
- Cases 相关测试与详情卡片回归测试已通过
- 浏览器已确认 Cases 概览页与详情页可正常打开
