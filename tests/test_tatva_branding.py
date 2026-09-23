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


def test_customer_demo_shell_uses_the_tatva_name_everywhere():
    header = read("frontend/src/components/Header.jsx")
    bootstrap = read("frontend/src/components/BootstrapSplash.jsx")
    first_run = read("frontend/src/components/FirstRunSetup.jsx")
    setup = read("frontend/src/pages/SetupWizard.jsx")
    info_plist = read("frontend/src-tauri/Info.plist")
    native_shell = read("frontend/src-tauri/src/lib.rs")
    blank_guard = read("frontend/src-tauri/src/blank_guard.rs")
    per_user = json.loads(read("frontend/src-tauri/tauri.per-user.conf.json"))

    assert PRODUCT_NAME in header
    assert f"t('bootstrap.title', '{PRODUCT_NAME}')" in bootstrap
    assert f"t('firstrun.title', 'Set up {PRODUCT_NAME}')" in first_run
    assert f"'Improve {PRODUCT_NAME}'" in setup
    assert f"{PRODUCT_NAME} needs microphone access" in info_plist
    assert f"{PRODUCT_NAME} may use the camera" in info_plist
    assert per_user["productName"] == f"{PRODUCT_NAME} (Current User)"
    for label in (
        f"Open {PRODUCT_NAME}",
        f"Show {PRODUCT_NAME}",
        f"Quit {PRODUCT_NAME}",
    ):
        assert label in native_shell
    assert f"<title>{PRODUCT_NAME}</title>" in blank_guard
    assert f"{PRODUCT_NAME} could not display its interface" in blank_guard

    for locale in sorted((ROOT / "frontend/src/i18n/locales").glob("*.json")):
        copy = locale.read_text(encoding="utf-8").replace("VoiceStudio@palash.dev", "")
        assert "VoiceStudio" not in copy, locale


def test_customer_demo_shell_hides_developer_chrome_without_removing_diagnostics():
    header = read("frontend/src/components/Header.jsx")
    app = read("frontend/src/App.jsx")
    settings = read("frontend/src/pages/Settings.jsx")

    assert "reloadAfterApplicationPersistence" not in header
    assert "<LogsFooter" not in app
    assert "case 'logs':" in settings
    assert "<LogsTab" in settings


def test_customer_demo_copy_does_not_make_unsupported_language_claims():
    launchpad = read("frontend/src/pages/Launchpad.jsx")
    english = read("frontend/src/i18n/locales/en.json")
    models = read("backend/config/models.yaml")

    assert "values={{ count: 646 }}" not in launchpad
    assert "646 languages" not in english
    assert "human-level quality" not in english
    assert "600+ languages" not in models
    assert 'label: "Tatva Voice Studio TTS (k2-fsa/OmniVoice, multilingual, zero-shot)"' in models


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
