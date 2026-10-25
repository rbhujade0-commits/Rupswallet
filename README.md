# RupsWallet

Personal expense tracker: glass UI, fingerprint lock, dashboard charts, and
cloud backup/sync with Firebase (anonymous sign-in + Firestore). Installable
as an Android app (PWA) and packageable as an APK.

## Project layout
| Path | What it is |
|---|---|
| `index.html` | The compiled app. This is what gets deployed. |
| `src/index.src.html` | Editable source (React/JSX inline). |
| `tools/build.py` | Compiles `src/` into `index.html`. |
| `manifest.webmanifest`, `sw.js`, `icons/` | PWA / installable-app files. |
| `firestore.rules` | Firestore security rules (publish these in Firebase). |
| `netlify.toml` | Netlify headers/config. |

## Firebase setup (once)
1. Firebase console > **Authentication > Sign-in method > Anonymous > Enable**.
2. **Firestore Database > Create database**, then **Rules** tab: paste `firestore.rules` > Publish.
3. **Authentication > Settings > Authorized domains**: add your Netlify / GitHub Pages domain.
4. Your web config lives at the top of `src/index.src.html` (`FIREBASE_CONFIG`).
   Firebase web keys are not secrets; the Firestore rules are what protect the data.

## Deploy
**Netlify (from GitHub):** New site > Import from Git > pick this repo. Build command: *(none)*, publish directory: `.`

**GitHub Pages:** Settings > Pages > Source: **GitHub Actions** (workflow included). Site URL: `https://<user>.github.io/<repo>/`

## Edit the app
```bash
npm i -g typescript        # one time
# edit src/index.src.html
python tools/build.py      # regenerates index.html
git add -A && git commit -m "Update" && git push
```

## Build the APK on GitHub (no Netlify needed)
The repo contains a native Android wrapper (`android/`) that bundles the app inside the APK, with real
Android fingerprint unlock and backups saved to `Downloads/RupsWallet`.
1. Push this repo to GitHub.
2. Go to the **Actions** tab > **Build Android APK** > **Run workflow**.
3. When it finishes (about 5 minutes), open the run and download **RupsWallet-apk** from *Artifacts*. Unzip it to get `RupsWallet.apk`.
4. Copy it to your phone and install it (allow "Install unknown apps" for your file manager/browser).

**Release link:** push a tag (`git tag v1.0 && git push origin v1.0`) and the APK is also attached to a GitHub Release.

**Stable signing key (recommended, so updates install over the old app):**
```bash
keytool -genkeypair -v -keystore release.jks -alias rupswallet -keyalg RSA -keysize 2048 -validity 10000
base64 -w0 release.jks      # copy the output
```
Repo > Settings > Secrets and variables > Actions > add: `KEYSTORE_BASE64` (that output), `KEYSTORE_PASSWORD`, `KEY_ALIAS` (rupswallet), `KEY_PASSWORD`.
Back up `release.jks`; never commit it. Without these secrets the workflow builds a debug-signed APK, which works fine but cannot be updated in place by a later build (uninstall first, then export a Backup from the app).

Before the APK works with cloud sync, finish the Firebase setup above (Anonymous sign-in + Firestore rules).

## Android app (PWA alternative)
- **Install now:** open the site in Chrome on Android > menu > **Install app**.
- **APK:** go to https://www.pwabuilder.com, paste your site URL > **Package for Android**.
  Keep the generated signing key safe (never commit it).

## Notes
- Anonymous accounts are tied to one browser/device. Clearing site data loses access to the cloud copy; use Backup/Restore (JSON) to move data.
- Opened as a downloaded file (not http/https) the app runs local-only.
