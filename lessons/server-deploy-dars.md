# 🌐 Serverga Avtomatik Deploy — To'liq Dars

> **Maqsad:** GitHub'ga `git push` qilganingizda kod avtomatik tarzda serverga chiqib, sayt yangilanishini sozlash.

> **Oldindan:** [CI/CD asoslari darsi](./ci-cd-dars.md) ni o'qib chiqing.

---

## 📋 Mundarija

1. [Umumiy rasm](#1-umumiy-rasm)
2. [Kerakli fayllar](#2-kerakli-fayllar)
3. [SSH key — kalit yasash](#3-ssh-key--kalit-yasash)
4. [GitHub Secrets sozlash](#4-github-secrets-sozlash)
5. [Serverni tayyorlash](#5-serverni-tayyorlash)
6. [Deploy job qanday ishlaydi](#6-deploy-job-qanday-ishlaydi)
7. [Sinab ko'rish](#7-sinab-korish)
8. [Muammolarni hal qilish](#8-muammolarni-hal-qilish)

---

## 1. Umumiy rasm

Deploy — bu CI/CD ning **eng oxirgi bosqichi**. Test o'tdi, image yasaldi, Docker Hub'ga yuklandi... endi uni **serverga chiqarish** kerak.

```
   KOMPYUTERINGIZ          GITHUB ACTIONS            SERVERINGIZ
   ─────────────          ──────────────            ───────────
   git push  ───────────►  🧪 test
                           🏗️ build image
                           🚀 Docker Hub'ga push
                           🔑 SSH bilan ulanadi ──►  docker compose pull
                                                     docker compose up -d
                                                     ✅ sayt yangilandi!
```

> 💡 **Asosiy g'oya:** GitHub serverga xuddi siz kabi SSH orqali kiradi va bir nechta buyruq beradi. Faqat buni avtomatik, sizning aralashuvingizsiz qiladi.

---

## 2. Kerakli fayllar

| Fayl | Qayerda | Vazifasi |
|------|---------|----------|
| `docker-compose.yml` | lokal | `build: .` — o'zingiz build qilasiz |
| `docker-compose.prod.yml` | server | `image:` — Docker Hub'dan tortadi |
| `.github/workflows/ci-cd.yml` | repo | butun pipeline (test→build→push→deploy) |

### Lokal vs Server farqi

**Lokal** (`docker-compose.yml`):
```yaml
web:
  build: .              # ← kodni o'zi build qiladi
```

**Server** (`docker-compose.prod.yml`):
```yaml
web:
  image: giyos1/u11_django:latest   # ← tayyor image'ni tortadi
```

> ⚠️ Server `build` qilmaydi! U Docker Hub'dan tayyor image'ni oladi. Shuning uchun `docker compose pull` ishlaydi.

---

## 3. SSH key — kalit yasash

GitHub serverga kirishi uchun unga **kalit** kerak. Kalit ikki qismdan iborat:

- 🔓 **Public key** — serverga qo'yiladi ("eshik qulfi")
- 🔒 **Private key** — GitHub'ga qo'yiladi ("kalit")

### Kalit yasash (kompyuteringizda)

```bash
ssh-keygen -t ed25519 -C "github-deploy" -f deploy_key
```

(parol so'rasa, bo'sh qoldirib Enter bosing — avtomatik deploy uchun)

Natijada 2 ta fayl:

```
  🔒 deploy_key       (private)  →  GITHUB'ga   (SERVER_SSH_KEY secret)
  🔓 deploy_key.pub   (public)   →  SERVERGA    (~/.ssh/authorized_keys)
```

| Fayl | Bu nima | Kimga |
|------|---------|-------|
| `deploy_key` 🔒 | "kalit" (private) | GitHub Secret'ga |
| `deploy_key.pub` 🔓 | "qulf" (public) | Serverga |

> 🧠 **Eslab qolish oson:** Private (🔒) — kalit, faqat sizda. Public (🔓) — qulf, eshikka (serverga) o'rnatiladi. Kalit qulfni ochadi.

> ⚠️ Private key (`deploy_key`) ni **hech kimga bermang**, GitHub'ga ham faqat Secret sifatida qo'ying! Public key (`.pub`) ni esa bemalol tarqatsangiz bo'ladi.

---

### 🔄 Variant B: Key'ni to'g'ridan-to'g'ri SERVERDA yasash (qulayroq)

Local'da yasab, public'ni serverga ko'chirish o'rniga — hamma narsani serverning o'zida qilsangiz bo'ladi. Bu soddaroq, chunki public key'ni hech qayerga ko'chirmaysiz.

**1) Serverga kiring:**
```bash
ssh user@server-ip
```

**2) Serverda key yasang:**
```bash
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/deploy_key
```
(parol so'rasa — Enter bosing, bo'sh qoldiring)

**3) Public key'ni serverning o'ziga "ruxsat" qiling:**
```bash
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**4) Private key'ni ko'rsating va nusxalang:**
```bash
cat ~/.ssh/deploy_key
```
`-----BEGIN OPENSSH PRIVATE KEY-----` dan `-----END...` gacha **hammasini** nusxalab, GitHub'da `SERVER_SSH_KEY` secret'iga qo'ying.

**5) (Ixtiyoriy, xavfsizlik) Private'ni serverdan o'chiring:**
```bash
rm ~/.ssh/deploy_key      # GitHub'da nusxasi bor, serverda kerak emas
```
> ⚠️ Faqat `deploy_key` (private) ni o'chiring. `authorized_keys` ichidagi public key **qolishi shart** — aks holda GitHub kira olmaydi.

### 📊 Ikki variant taqqoslash

| | Local'da yasash (A) | Serverda yasash (B) |
|---|---|---|
| Public key | `ssh-copy-id` bilan yuborasiz | `>> authorized_keys` o'zi qo'shiladi |
| Qadam soni | ko'proq | kamroq ✅ |
| Natija | bir xil | bir xil |

Ikkalasi ham to'g'ri ishlaydi — qaysi qulay bo'lsa, o'shani tanlang.

---

## 4. GitHub Secrets sozlash

### Secrets qayerda turadi?

Maxfiy ma'lumotlar (parol, token, key) hech qachon kodга yozilmaydi! Ular GitHub'ning xavfsiz **Secrets** bo'limida saqlanadi.

```
1. GitHub'da repongni och
2. Yuqorida:  ⚙️ Settings   (repo settings — profil settings EMAS!)
3. Chap menyu:  🔒 Secrets and variables  →  Actions
4. Yashil tugma:  [ New repository secret ]
5. Name + Secret yozasan  →  [ Add secret ]
```

To'g'ridan-to'g'ri URL:
```
https://github.com/<username>/<repo>/settings/secrets/actions
```

> ⚠️ **Adashmang:** Yana `Settings → Deploy keys` degan bo'lim ham bor — u boshqa narsa (repo'ni o'qish uchun). Bizga **`Secrets and variables → Actions`** kerak.

### 5 ta secret qo'shing

Har birini alohida "New repository secret" bilan:

| Secret nomi | Qiymati | Qayerdan |
|-------------|---------|----------|
| `DOCKERHUB_USERNAME` | `giyos1` | Docker Hub username |
| `DOCKERHUB_TOKEN` | `dckr_pat_...` | ⬇️ pastdagi bo'limga qarang |
| `SERVER_HOST` | `123.45.67.89` | server IP yoki domen |
| `SERVER_USER` | `root` / `ubuntu` | SSH foydalanuvchi |
| `SERVER_SSH_KEY` | `-----BEGIN ...` | `deploy_key` faylining **to'liq** mazmuni |

### 🐳 DOCKERHUB_TOKEN qayerdan olinadi?

Docker Hub parolini emas, **access token** ishlatamiz (xavfsizroq).

```
1. https://hub.docker.com  →  login qil
2. O'ng yuqorida ismingni bos  →  Account Settings
3. Tab:  Security  (Personal access tokens)
4. [ New Access Token ]
5. To'ldir:
     - Description:  github-ci
     - Permissions:  Read & Write   ← MUHIM! (push uchun)
6. [ Generate ]
```

To'g'ridan-to'g'ri URL:
```
https://app.docker.com/settings/personal-access-tokens
```

> 🔴 **Diqqat:** Token faqat **bir marta** ko'rsatiladi (`dckr_pat_xxxx...`). Darhol nusxalab oling — sahifani yopsangiz, qayta ko'ra olmaysiz. Yo'qotsangiz — yangisini yasaysiz.

> 💡 Nega token, parol emas? Token faqat kerakli ruxsatni beradi va istalganda o'chirib tashlash mumkin. Parol esa butun akkauntga kirish beradi — xavfli.

### Private key'ni qanday nusxalash? (SERVER_SSH_KEY uchun)

```bash
cat deploy_key
```

`-----BEGIN OPENSSH PRIVATE KEY-----` dan `-----END OPENSSH PRIVATE KEY-----` gacha **hammasini** (shu qatorlar bilan) nusxalab, `SERVER_SSH_KEY` ga joylashtiring.

---

## 5. Serverni tayyorlash

Serverga bir marta kirib, tayyorlab qo'yamiz.

### a) Public key'ni serverga qo'shish (kompyuteringizdan)

```bash
ssh-copy-id -i deploy_key.pub user@server-ip
```

### b) Serverda Docker bor-yo'qligini tekshirish

```bash
ssh user@server-ip
docker --version          # bo'lmasa o'rnating
docker compose version
```

### c) Loyiha papkasini tayyorlash

```bash
mkdir ~/u11_django && cd ~/u11_django
```

Bu papkaga 3 ta narsa kerak:

1. **`docker-compose.yml`** (lokal `docker-compose.prod.yml` ning nusxasi)
2. **`nginx/default.conf`**
3. **`.env`** (productiongа moslangan)

### d) `.env` faylini productionga sozlash

```env
DEBUG=False
SECRET_KEY=kuchli-maxfiy-kalit
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=kuchli-parol
POSTGRES_HOST=db
POSTGRES_PORT=5432
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

### e) Birinchi marta qo'lda ko'tarish

```bash
docker compose up -d
docker compose ps        # hammasi "Up" bo'lsin
```

> ✅ Shu joygacha qilsangiz, sayt server IP'sida ochiladi. Endi avtomatlashtiramiz.

---

## 6. Deploy job qanday ishlaydi

`.github/workflows/ci-cd.yml` dagi deploy job:

```yaml
deploy:
  needs: build-and-push          # image tayyor bo'lsagina
  runs-on: ubuntu-latest
  steps:
    - uses: appleboy/ssh-action@v1
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd ~/u11_django
          docker compose pull      # yangi image'ni tort
          docker compose up -d     # qayta ishga tushir
          docker image prune -f    # eski image'larni tozala
```

### Qator-qator izoh

| Qator | Nima qiladi |
|-------|-------------|
| `needs: build-and-push` | Faqat image push bo'lsa ishlaydi |
| `appleboy/ssh-action` | Tayyor SSH action (marketplace) |
| `host/username/key` | Secret'lardan server ma'lumotlari |
| `docker compose pull` | Docker Hub'dan yangi image |
| `docker compose up -d` | Konteynerlarni yangi image bilan qayta ishga tushiradi |
| `docker image prune -f` | Disk to'lib ketmasligi uchun eski image'lar |

---

## 7. Sinab ko'rish

Hammasi tayyor bo'lsa:

```bash
# kodda biror o'zgarish qiling
git add .
git commit -m "test deploy"
git push
```

Keyin GitHub → **Actions** tab → ishlab turgan workflow'ni oching. Ko'rasiz:

```
✅ test
✅ build-and-push
✅ deploy          ← server'ga chiqdi!
```

Server IP'sini brauzerda oching — yangi kod ishlab turibdi! 🎉

---

## 8. Muammolarni hal qilish

| Muammo | Sabab | Yechim |
|--------|-------|--------|
| `Permission denied (publickey)` | SSH key noto'g'ri | Public key serverda `~/.ssh/authorized_keys` da-mi? Private key Secret to'g'ri-mi? |
| `docker: command not found` | Serverda Docker yo'q | Serverga Docker o'rnating |
| `no such file ~/u11_django` | Papka yo'q | Serverda papkani yarating va fayllarni qo'ying |
| `pull access denied` | Image private yoki nom xato | Image nomini tekshiring, Docker Hub login |
| Port 80 band | Boshqa nginx/apache ishlayapti | `sudo lsof -i :80` bilan tekshiring |

### Loglarni ko'rish (serverda)

```bash
cd ~/u11_django
docker compose logs -f web      # web loglar
docker compose logs -f nginx    # nginx loglar
docker compose ps               # holatlar
```

---

## 🎓 Xulosa

Endi sizda **to'liq avtomatik CI/CD** bor:

```
git push  →  test  →  build  →  Docker Hub  →  server  →  ✅ tirik sayt
```

Bir marta sozlaysiz — umrbod ishlaydi. Bu professional jamoalar ishlatadigan usul!

---

<div align="center">

### 🚀 Tabriklaymiz — siz DevOps asoslarini o'zlashtirdingiz!

</div>