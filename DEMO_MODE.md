# SHELESTFIT demo mode

Current public version is a portfolio demonstration. It does not accept service inquiries, orders or payments. Do not restore intake or analytics by running old one-off builders.

The active build is `python3 build_seo.py`. It applies `demo_mode.demo_html` before validation and writing every generated landing page. After editing legacy HTML, run `python3 demo_mode.py`, then `python3 build_seo.py --check` and the release audit. The original verification documents must stay unchanged.

Keep CSP with connect-src none, form-action none, frame-src none and self-hosted assets. UI theme choices stay in document memory, without localStorage. Contact on the project notice is for privacy/project questions only, not coaching intake. Do not claim that GitHub hosting logs or past processing cease to exist because of demo mode.

Rollback: revert this release in Git and redeploy only after the owner explicitly authorizes resuming a working service. Do not restore the previous business version as a routine visual rollback.
