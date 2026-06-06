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
    assert "assets/locales" in readme, "README 应说明 locale 源文件维护方式"

    assert 'data-site-header' in page_404, "404 页面缺少统一站点头部挂载点"
    assert 'data-site-footer' in page_404, "404 页面缺少统一站点底部挂载点"
    assert 'language-switcher' in page_404, "404 页面缺少语言切换器"
    assert 'href="/"' in page_404, "404 页面缺少返回首页入口"
    assert 'href="/solutions/"' in page_404, "404 页面缺少 Solutions 入口"
    assert 'href="/contact/"' in page_404, "404 页面缺少联系入口"
    assert (ROOT / "zh/404.html").exists(), "缺少中文 404 页面"

    assert "`404.html`" in deployment, "部署文档缺少 404 文件说明"
    assert "错误页指向" in deployment and "`404.html`" in deployment, "部署文档未切换到正式 404 配置"
    assert "发布顺序" in deployment, "部署文档缺少发布顺序章节"
    assert "generate_static_pages.py" in deployment, "部署文档应说明页面生成命令"
    assert "`zh/`" in deployment, "部署文档应包含中文目录"

    print("readme 404 launch hooks OK")


if __name__ == "__main__":
    main()
