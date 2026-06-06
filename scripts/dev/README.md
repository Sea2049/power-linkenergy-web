# Locale 开发辅助脚本

此目录中的脚本仅用于维护 `assets/locales/*.json`，**不要上传到 OSS**。

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `build_locales.py` | 从 `data.js` 生成英文 locale 基准 |
| `build_translation_maps.py` | 构建翻译映射 |
| `apply_locale_translations.py` | 将映射应用到各语言 JSON |
| `translation_data_*.py` | 法语/俄语翻译字典 |

## 日常维护

正式流程请优先直接编辑 `assets/locales/en.json`、`zh.json`、`fr.json`、`ru.json`、`ar.json`，然后运行：

```bash
py -3 scripts/generate_static_pages.py
```

仅在需要批量重建或迁移翻译数据时，才使用本目录脚本。
