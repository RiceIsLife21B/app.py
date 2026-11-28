"""Local browser regression: uv run --no-project --with playwright python tests/browser_remember_device.py"""

import ast
import os
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from remembered_sessions import COOKIE_NAME  # noqa: E402

PASSWORD = "local-browser-test-only"


def copy_fixture(directory):
    # Exercise the checked-out app without typing or logging its live password.
    source = (ROOT / "app.py").read_text()
    assignment, = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "STAFF_PASSWORD" for target in node.targets)
    ]
    lines = source.splitlines(keepends=True)
    lines[assignment.lineno - 1:assignment.end_lineno] = [f"STAFF_PASSWORD = {PASSWORD!r}\n"]
    (directory / "app.py").write_text("".join(lines))
    shutil.copyfile(ROOT / "remembered_sessions.py", directory / "remembered_sessions.py")


@contextmanager
def run_app(directory, port, url):
    python = os.getenv("STREAMLIT_PYTHON", str(ROOT / ".venv/bin/python"))
    tls_options = []
    health_tls = None
    if url.startswith("https://"):
        tls_options = ["--server.sslCertFile=cert.pem", "--server.sslKeyFile=key.pem"]
        # Only the disposable local fixture uses a self-signed certificate.
        health_tls = ssl._create_unverified_context()
    with (directory / "streamlit.log").open("w+") as log:
        app = subprocess.Popen(
            [python, "-m", "streamlit", "run", "app.py", "--server.headless=true",
             f"--server.port={port}", "--server.address=127.0.0.1",
             "--browser.gatherUsageStats=false", *tls_options],
            cwd=directory, stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            for _ in range(100):
                if app.poll() is not None:
                    break
                try:
                    with urlopen(f"{url}/_stcore/health", timeout=1, context=health_tls) as response:
                        if response.read() == b"ok":
                            break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Timed out waiting for the local Streamlit server")
            if app.poll() is not None:
                raise RuntimeError("Local Streamlit server exited before the tests")
            yield
        except Exception:
            log.seek(0)
            print(log.read(), file=sys.stderr)
            raise
        finally:
            if app.poll() is None:
                app.terminate()
                try:
                    app.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    app.kill()
                    app.wait()


def login(page, *, remember=False, password=PASSWORD):
    page.get_by_placeholder("Enter password").fill(password)
    if remember:
        page.get_by_text("Remember this device", exact=True).click()
        expect(page.get_by_role("checkbox", name="Remember this device")).to_be_checked()
    page.get_by_role("button", name="Log In", exact=True).click()


def check_logged_in(page):
    expect(page.get_by_role("button", name="Log Out", exact=True)).to_be_visible()
    expect(page.get_by_placeholder("Enter password")).to_have_count(0)


def check_logged_out(page):
    expect(page.get_by_placeholder("Enter password")).to_be_visible()
    expect(page.get_by_role("button", name="Log Out", exact=True)).to_have_count(0)


def check_error(page, message):
    alert = page.get_by_role("alert").filter(has_text=message)
    expect(alert).to_be_visible()
    expect(alert).to_have_css("color", "rgb(255, 128, 136)")
    expect(alert).to_have_css("background-color", "rgb(45, 17, 23)")
    expect(alert).to_have_css("text-align", "center")


def cookie(context, url):
    return next((item for item in context.cookies(url) if item["name"] == COOKIE_NAME), None)


def main():
    chrome = os.getenv("CHROME_BINARY") or shutil.which("google-chrome") or shutil.which("chromium")
    with socket.socket() as candidate:
        candidate.bind(("127.0.0.1", 0))
        port = candidate.getsockname()[1]
    hostname = os.getenv("OMAI_TEST_HOST", "localhost")
    use_https = os.getenv("OMAI_TEST_HTTPS") == "1"
    scheme = "https" if use_https else "http"
    url = f"{scheme}://{hostname}:{port}"
    with tempfile.TemporaryDirectory(prefix="omai-browser-") as scratch, sync_playwright() as pw:
        fixture = Path(scratch)
        copy_fixture(fixture)
        profile = fixture / "browser-profile"
        if use_https:
            subprocess.run(
                ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
                 "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
                 "-keyout", "key.pem", "-out", "cert.pem"],
                cwd=fixture, check=True, capture_output=True,
            )

        def open_browser():
            if os.getenv("OMAI_TEST_BROWSER") == "webkit":
                context = pw.webkit.launch_persistent_context(profile, ignore_https_errors=use_https)
            else:
                context = pw.chromium.launch_persistent_context(
                    profile, executable_path=chrome, ignore_https_errors=use_https,
                )
            page = context.pages[0]
            page.goto(url)
            return context, page

        with run_app(fixture, port, url):
            context, page = open_browser()
            check_logged_out(page)
            expect(page.get_by_role("checkbox", name="Remember this device")).not_to_be_checked()
            login(page, remember=True, password="wrong-browser-test-password")
            check_error(page, "Incorrect password.")
            assert cookie(context, url) is None
            page.reload()
            login(page)
            check_logged_in(page)
            assert cookie(context, url) is None
            page.reload()
            check_logged_out(page)
            print("PASS: wrong password and unchecked login do not persist")

            login(page, remember=True)
            check_logged_in(page)
            if os.getenv("OMAI_EXPECT_COOKIE_BLOCKED") == "1":
                check_error(page, "This browser could not save the sign-in cookie.")
                assert cookie(context, url) is None
                check_logged_in(page)
                page.reload()
                check_logged_out(page)
                context.close()
                print("PASS: blocked cookie shows a warning and does not persist login")
                return
            page.wait_for_function("name => document.cookie.includes(name + '=')", arg=COOKIE_NAME, timeout=5000)
            saved = cookie(context, url)
            assert saved and saved["secure"] and saved["sameSite"] == "Lax" and saved["path"] == "/"
            assert 0 < saved["expires"] - time.time() <= 86405
            assert saved["value"] != PASSWORD
            page.reload()
            check_logged_in(page)
            new_tab = context.new_page()
            new_tab.goto(url)
            check_logged_in(new_tab)
            context.close()
            context, page = open_browser()
            check_logged_in(page)
            print("PASS: remembered login survives refresh, new tab, and browser relaunch")

            page.get_by_role("button", name="Log Out", exact=True).click()
            check_logged_out(page)
            page.wait_for_function("name => !document.cookie.includes(name + '=')", arg=COOKIE_NAME)
            assert cookie(context, url) is None
            page.reload()
            check_logged_out(page)
            context.add_cookies([saved])
            page.reload()
            check_logged_out(page)
            print("PASS: logout clears the cookie and invalidates its token on the server")

            login(page, remember=True)
            check_logged_in(page)
            page.wait_for_function(
                "([name, old]) => document.cookie.split('; ').some(c => c.startsWith(name + '=') && c !== name + '=' + old)",
                arg=[COOKIE_NAME, saved["value"]],
            )
            context.close()

        with run_app(fixture, port, url):
            context, page = open_browser()
            assert cookie(context, url) is not None
            check_logged_out(page)
            context.close()
            print("PASS: server restart rejects the still-present remembered cookie")


if __name__ == "__main__":
    main()
