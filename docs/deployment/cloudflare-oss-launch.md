# Cloudflare + OSS 发布指南

## 1. 最终上传文件清单

必须上传：

- `index.html`
- `404.html`
- `about/`
- `contact/`
- `products/`
- `solutions/`
- `cases/`
- `zh/`（含 `zh/404.html`、`zh/solutions/`、`zh/products/`、`zh/cases/`、`zh/about/`、`zh/contact/`）
- `fr/`（含 `fr/404.html` 及对应子路由）
- `ru/`（含 `ru/404.html` 及对应子路由）
- `ar/`（含 `ar/404.html` 及对应子路由）
- `assets/`（含 `assets/css/`、`assets/js/`、`assets/images/`，但不含 `assets/locales/`）
- `downloads/` 中被页面引用的文件
- `favicon.ico`
- `robots.txt`
- `sitemap.xml`
- `llms.txt`

不要上传：

- `tests/`
- `docs/superpowers/`
- `brainstorm/`
- `scripts/`
- `scripts/dev/`（locale 批量维护脚本，仅开发使用）
- `assets/locales/`（多语言源数据，仅用于本地生成，不参与线上运行时）
- 根目录 `.xlsx`、`.docx`、`.log`、`.txt` 业务文件
- `downloads/supplier_images/summary.md`
- `downloads/supplier_images/shortlist.md`
- `downloads/supplier_images/manifest.csv`
- 临时协作材料、规划草稿与本地校验脚本

## 2. 推荐发布顺序

1. 编辑 `assets/locales/{en,zh,fr,ru,ar}.json` 中的源数据，**不要直接手改 HTML 产物**
2. 运行 `py -3 scripts/generate_og_share_image.py` 刷新五语言 OG 分享图（仅 locale 文案变更时需要）
3. 运行 `py -3 scripts/generate_static_pages.py` 重新生成所有路由 HTML、`sitemap.xml` 及 `assets/js/data.js`
4. 使用 `py -3 -m http.server 8000` 在项目根目录启动本地预览
5. 本地检查英文首页、五语言首页、Reference Frameworks、Products、Solutions、各语言 `404.html`、`/zh/`、`/fr/`、`/ru/`、`/ar/` 主要路由
6. 运行发布前测试清单
7. 确认上线包只包含 allowlist 中的正式静态文件（特别确认 `assets/locales/` 和 `scripts/dev/` 未被打包）
8. 将正式静态文件上传到 OSS
9. 在 OSS 中将默认首页设置为 `index.html`
10. 在 OSS 中将错误页设置为 `404.html`
11. 在 Cloudflare 中完成 DNS、代理、HTTPS、缓存配置
12. 清理 Cloudflare 缓存（含 `/zh/*`、`/fr/*`、`/ru/*`、`/ar/*`）
13. 抽查线上首页、案例页、404 页面和静态资源

## 3. 阿里云 OSS 配置

1. 创建或打开正式站点使用的 Bucket。
2. 在 Bucket 设置中开启静态网站托管。
3. 默认首页指向 `index.html`。
4. 错误页指向 `404.html`。
5. 上传 allowlist 中的正式静态文件，并保留原始目录层级。
6. 上传完成后，先访问 OSS 提供的静态站点地址，确认首页和至少一个二级路由可打开。

## 4. Cloudflare 配置

1. 将业务域名接入 Cloudflare。
2. 在 DNS 中为 `www.power-linkenergy.com` 配置指向 OSS 源站的记录。
3. 打开 Cloudflare 代理，使外部访问先经过 Cloudflare 再回源到 OSS。
4. 在 SSL/TLS 中启用 HTTPS。
5. 按需开启 Brotli、缓存优化与基础安全规则。

上线前至少确认以下几点：

- `www.power-linkenergy.com` 为主访问域名
- Cloudflare 回源地址需与 OSS 公网访问地址一致
- 当前站点只支持**根路径**部署
- 页面资源请求不会被错误重写到不存在的路径
- 不要回退到 `index.html` 充当长期 404 方案，正式错误页应固定为 `404.html`

## 5. 日常发布与缓存建议

1. 将本次变更涉及的静态文件重新上传到 OSS。
2. 若更新首页、导航、共享资源或案例页，及时清理 Cloudflare 缓存。
3. 抽查首页、案例页、产品页、方案页与 `404.html`。
4. 确认页面样式、脚本、内部链接与静态资源均正常加载。

按影响范围选择刷新方式：

- 仅更新单页时，优先清理对应 URL
- 更新 `assets/css/site.css` 或 `assets/js/site.js` 后，建议清理共享资源缓存
- Cases 页面更新后，至少清理 `/cases/*` 路径缓存

缓存清理后，建议使用无痕窗口重新检查线上页面，避免被本地浏览器缓存干扰。

## 6. 新增案例时的维护提醒

1. 在 `assets/js/data.js` 中补充新的案例对象。
2. 创建对应的 `cases/<slug>/index.html` 路由文件。
3. 只有在拿到可验证项目素材后，才填写 `heroImage`、`gallery`、`galleryNote` 等字段。
4. 本地预览确认案例概览页和详情页渲染正常后，再上传到 OSS。
5. 上线后清理 Cloudflare 中与案例相关的缓存。

## 7. 最终上线检查清单

- OSS 静态网站托管已开启
- 默认首页已指向 `index.html`
- 错误页已指向 `404.html`
- Cloudflare DNS 和代理配置生效
- HTTPS 可正常访问
- 首页、案例页、产品页、方案页、404 页面均可打开
- 更新后缓存已清理
- 线上抽查无明显 404、样式丢失或脚本失效

## 8. 发布前测试清单

```bash
python tests/check_about_process_layout.py
python tests/check_about_contact_visual.py
python tests/check_home_advantage_cards.py
python tests/check_detail_card_system.py
python tests/check_cases_visual_system.py
python tests/check_contact_promise_cards.py
python tests/check_readme_404_launch.py
python tests/check_static_rendering.py
python tests/check_route_data_alignment.py
python tests/check_sitemap_routes.py
python tests/check_deployment_assumptions.py
python tests/check_public_artifact_hygiene.py
```

以上检查用于确认静态直出、404 策略、站点地图、文档边界和上线包卫生。
