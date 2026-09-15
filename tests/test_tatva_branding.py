import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
PRODUCT_NAME = "Tatva Voice Studio"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_visible_product_identity_is_tatva():
    tauri = json.loads(read("frontend/src-tauri/tauri.conf.json"))
    assert tauri["productName"] == PRODUCT_NAME
    assert tauri["app"]["windows"][0]["title"] == PRODUCT_NAME
    assert f"<title>{PRODUCT_NAME}</title>" in read("frontend/index.html")
    assert PRODUCT_NAME in read("frontend/src/pages/SetupWizard.jsx")
    assert PRODUCT_NAME in read("frontend/src/components/settings/AboutTab.jsx")


def test_bootstrap_title_is_tatva_in_every_locale():
    locales = sorted((ROOT / "frontend/src/i18n/locales").glob("*.json"))
    assert len(locales) == 21
    for locale in locales:
        assert json.loads(locale.read_text(encoding="utf-8"))["bootstrap"]["title"] == PRODUCT_NAME


def test_default_theme_uses_tatva_tokens():
    css = read("frontend/src/index.css")
    for token in ("#1a1a2e", "#1fb8ff", "#0077c2", "#f7941d", "#f8fafc"):
        assert token in css
    for declaration in (
        "--primary: #1fb8ff;",
        "--primary-hover: #0077c2;",
        "--accent: #f7941d;",
        "--text-primary: #f8fafc;",
        "--chrome-bg:            #1a1a2e;",
        "--chrome-fg:            #f8fafc;",
    ):
        assert declaration in css
    assert "--color-bg:            #1a1a2e;" in css
    assert "--bg: #1a1a2e;" in css
    assert "<body style=\"background:#1a1a2e\">" in read("frontend/index.html")
    appearance = read("frontend/src/components/settings/AppearancePanel.jsx")
    assert "{ id: 'gruvbox', label: 'Tatva', dot: '#1fb8ff' }" in appearance


def test_compatibility_identity_stays_upstream():
    tauri = json.loads(read("frontend/src-tauri/tauri.conf.json"))
    assert tauri["identifier"] == "com.debpalash.omnivoice-studio"
    assert "debpalash/VoiceStudio/releases/latest" in read(
        "frontend/src-tauri/tauri.conf.json"
    )
    assert "OMNIVOICE_DATA_DIR" in read("backend/core/config.py")
