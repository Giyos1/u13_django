# 🚀 CI/CD — To'liq Dars

> **Maqsad:** Dars oxirida siz CI/CD nima ekanini tushunasiz, GitHub Actions yordamida o'z loyihangizga avtomatik test va deploy o'rnatasiz.

---

## 📋 Mundarija

1. [CI/CD nima va nega kerak?](#1-cicd-nima-va-nega-kerak)
2. [CI vs CD — farqi](#2-ci-vs-cd--farqi)
3. [Pipeline (quvur) tushunchasi](#3-pipeline-quvur-tushunchasi)
4. [GitHub Actions bilan tanishuv](#4-github-actions-bilan-tanishuv)
5. [Workflow fayl anatomiyasi](#5-workflow-fayl-anatomiyasi)
6. [Amaliyot: bizning loyiha uchun pipeline](#6-amaliyot-bizning-loyiha-uchun-pipeline)
7. [Secrets — maxfiy ma'lumotlar](#7-secrets--maxfiy-malumotlar)
8. [Tez-tez beriladigan savollar](#8-faq)
9. [Vazifa](#9-uyga-vazifa)

---

## 1. CI/CD nima va nega kerak?

### Muammo 🤔

Tasavvur qiling, jamoada 5 ta dasturchi bor. Har biri kod yozadi va serverga yuklaydi. Natijada:

- ❌ Birovning kodi boshqasinikini buzadi
- ❌ "Mening kompyuterimda ishlayapti-ku!" muammosi
- ❌ Serverga qo'lda yuklash — uzoq va xatoga moyil
- ❌ Test qilishni unutib qo'yish
- ❌ Bitta xato butun saytni o'chiradi

### Yechim ✅

**CI/CD** — bu kod yozishdan to serverga chiqishgacha bo'lgan jarayonni **avtomatlashtirish**.

> 💡 **Oddiy ta'rif:** CI/CD — bu "robot yordamchi". Siz kod yozasiz, u esa avtomatik tarzda: tekshiradi → test qiladi → build qiladi → serverga yuklaydi.

**CI/CD** = **C**ontinuous **I**ntegration / **C**ontinuous **D**elivery (yoki **D**eployment)

O'zbekcha: *"Uzluksiz integratsiya / Uzluksiz yetkazib berish"*

---

## 2. CI vs CD — farqi

Bu ikkalasi alohida tushuncha, lekin birga ishlatiladi:

### 🔵 CI — Continuous Integration (Uzluksiz integratsiya)

Kod yozilganda **avtomatik tekshirish va test qilish**.

Nima qiladi:
- Kod to'g'ri yozilganmi? (linting)
- Testlar o'tdimi?
- Kod build bo'ladimi?

> **Maqsad:** Xatolarni serverga chiqishidan **oldin** topish.

### 🟢 CD — Continuous Delivery / Deployment

Test o'tgan kodni **avtomatik tarqatish/joylashtirish**.

| Tur | Ma'nosi |
|-----|---------|
| **Continuous Delivery** | Tayyor qiladi, lekin chiqarish uchun odam tugma bosadi |
| **Continuous Deployment** | Hammasi avtomatik — odam aralashmaydi |

### 📊 Yonma-yon

| | CI 🔵 | CD 🟢 |
|---|---|---|
| **Nima qiladi** | Test va tekshirish | Build va deploy |
| **Qachon** | Har push'da | CI o'tgandan keyin |
| **Maqsad** | Xato topish | Mahsulotni yetkazish |
| **Natija** | "Kod sog'lommi?" | "Kod serverda!" |

---

## 3. Pipeline (quvur) tushunchasi

**Pipeline** — bu kodingiz bosib o'tadigan **bosqichlar zanjiri**. Suv quvurdan oqqandek, kod ham bosqichma-bosqich o'tadi.

```
  Kod yozdim          Robot ishga tushdi
  git push  ───────►  ┌──────────────────────────────────────┐
                      │                                        │
                      │  1️⃣ CHECKOUT   →  Kodni yuklab oladi   │
                      │       ↓                                 │
                      │  2️⃣ INSTALL    →  Kutubxonalarni o'rnatadi │
                      │       ↓                                 │
                      │  3️⃣ TEST       →  Testlarni ishlatadi  │
                      │       ↓                                 │
                      │  4️⃣ BUILD      →  Docker image yasaydi │
                      │       ↓                                 │
                      │  5️⃣ PUSH       →  Docker Hub'ga yuklaydi│
                      │       ↓                                 │
                      │  6️⃣ DEPLOY     →  Serverda ishga tushadi│
                      │                                        │
                      └──────────────────────────────────────┘
                                    ↓
                              ✅ Sayt yangilandi!
```

> ⚠️ **Muhim qoida:** Agar biror bosqich **xato** bersa, keyingilari **ishlamaydi**. Masalan, test o'tmasa — deploy bo'lmaydi. Bu bizni buzuq kodni serverga chiqarishdan saqlaydi.

---

## 4. GitHub Actions bilan tanishuv

CI/CD qiladigan ko'plab vositalar bor: Jenkins, GitLab CI, CircleCI, Travis CI... Biz **GitHub Actions** ishlatamiz, chunki:

- ✅ GitHub ichida — alohida narsa o'rnatmaysiz
- ✅ Bepul (public repo'lar uchun cheksiz)
- ✅ Sodda YAML sintaksis
- ✅ Tayyor "action"lar ko'p (marketplace)

### Asosiy tushunchalar

| Tushuncha | Ma'nosi | Hayotiy o'xshatma |
|-----------|---------|-------------------|
| **Workflow** | Butun jarayon (1 ta `.yml` fayl) | Retsept kitobi |
| **Event (trigger)** | Nima ishga tushiradi (push, PR...) | "Mehmon kelganda" |
| **Job** | Bir guruh vazifa | Bir taom tayyorlash |
| **Step** | Bitta qadam | "Sabzini to'g'rash" |
| **Action** | Tayyor qadam (boshqalar yozgan) | Tayyor sous |
| **Runner** | Kod ishlaydigan kompyuter | Oshxona |

### Fayl qayerda turadi?

Workflow fayllar **doim** shu manzilda bo'lishi shart:

```
loyiha/
└── .github/
    └── workflows/
        └── ci-cd.yml      ← shu yerda
```

---

## 5. Workflow fayl anatomiyasi

Keling, har bir qismni ko'rib chiqamiz:

```yaml
# 1) Workflow nomi
name: CI/CD Pipeline

# 2) QACHON ishga tushadi? (trigger)
on:
  push:
    branches: [ "main" ]      # main'ga push bo'lganda

# 3) JOBLAR (vazifalar)
jobs:
  test:                       # job nomi
    runs-on: ubuntu-latest    # qaysi OS'da ishlaydi

    steps:                    # qadamlar
      - name: Kodni olish
        uses: actions/checkout@v4   # tayyor action

      - name: Python o'rnatish
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Test qilish
        run: python manage.py test   # oddiy terminal buyrug'i
```

### Har bir kalit so'z

| Kalit | Vazifasi |
|-------|----------|
| `name` | Workflow nomi (GitHub'da ko'rinadi) |
| `on` | **Qachon** ishga tushishi (trigger) |
| `jobs` | Bajariladigan vazifalar ro'yxati |
| `runs-on` | Qaysi mashina (ubuntu, windows, macos) |
| `steps` | Job ichidagi qadamlar |
| `uses` | Tayyor action ishlatish |
| `run` | Terminal buyrug'i ishlatish |
| `with` | Action'ga parametr berish |
| `needs` | Boshqa job'ga bog'liqlik |
| `if` | Shart (faqat shu holatda ishla) |

---

## 6. Amaliyot: bizning loyiha uchun pipeline

Bizning loyiha — **Django + Docker + Postgres**. Maqsadimiz:

1. 🧪 Har push'da testlarni ishlatish (CI)
2. 🚀 Test o'tsa, Docker image yasab Docker Hub'ga yuklash (CD)

To'liq fayl `.github/workflows/ci-cd.yml` da. Asosiy g'oya:

```yaml
jobs:
  # 1-JOB: Test
  test:
    runs-on: ubuntu-latest
    services:
      postgres:               # test uchun vaqtinchalik baza
        image: postgres:15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: python manage.py test

  # 2-JOB: Build & Push (faqat test o'tsa)
  build-and-push:
    needs: test               # ← test'ga bog'liq!
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v3       # Docker Hub login
      - uses: docker/build-push-action@v6  # build + push
```

> 🔑 **Eng muhim qator:** `needs: test` — bu "build faqat test o'tgandan keyin ishlasin" degani. Test yiqilsa, image yuklanmaydi.

---

## 7. Secrets — maxfiy ma'lumotlar

Docker Hub parolini kodga **hech qachon** yozmaymiz! Buning o'rniga GitHub **Secrets** ishlatamiz.

### Qanday qo'shiladi?

1. GitHub repo → **Settings**
2. Chap menyu → **Secrets and variables** → **Actions**
3. **New repository secret** tugmasi
4. Ikkita secret qo'shing:

| Nomi | Qiymati |
|------|---------|
| `DOCKERHUB_USERNAME` | `giyos1` |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token |

### Token qayerdan olinadi?

Docker Hub → **Account Settings** → **Security** → **New Access Token**

1. https://app.docker.com/settings/personal-access-tokens
2. **New Access Token** → Description: `github-ci`
3. Permissions: **Read & Write** ← push uchun majburiy!
4. **Generate** → token `dckr_pat_...` ko'rinishida chiqadi

> 🔴 Token faqat **bir marta** ko'rsatiladi — darhol nusxalab oling! Yo'qotsangiz yangisini yasaysiz.

### Kodda qanday ishlatiladi?

```yaml
with:
  username: ${{ secrets.DOCKERHUB_USERNAME }}
  password: ${{ secrets.DOCKERHUB_TOKEN }}
```

> 🔒 `${{ secrets.NOMI }}` — bu maxfiy qiymatni xavfsiz oladi. GitHub uni loglarda ham `***` qilib yashiradi.

---

## 8. FAQ

**❓ Workflow qachon ishga tushadi?**
`on:` blokida belgilangan hodisa yuz berganda. Masalan `git push` qilganda.

**❓ Tekin bo'ladimi?**
Public (ochiq) repo'lar uchun cheksiz tekin. Private uchun oyiga ma'lum daqiqa tekin.

**❓ Workflow xato bersa nima bo'ladi?**
GitHub sizga email yuboradi, repo'da ❌ qizil belgi chiqadi. Keyingi bosqichlar ishlamaydi.

**❓ Bir nechta job parallel ishlaydimi?**
Ha! Agar `needs` bilan bog'lanmagan bo'lsa, joblar bir vaqtda ishlaydi.

**❓ Loglarni qayerdan ko'raman?**
GitHub repo → **Actions** tab → workflow'ni bosing.

---

## 9. Uyga vazifa

### ⭐ Daraja 1 (oson)
O'z loyihangizga `.github/workflows/ci.yml` yarating. U faqat:
- Kodni checkout qilsin
- Python o'rnatsin
- `pip install -r requirements.txt` qilsin

### ⭐⭐ Daraja 2 (o'rta)
Yuqoridagiga **test** bosqichini qo'shing (`python manage.py test`).

### ⭐⭐⭐ Daraja 3 (qiyin)
To'liq CI/CD yozing:
- Test o'tsa → Docker image build qiling
- Docker Hub'ga push qiling
- Secrets ishlating

---

## 📚 Foydali havolalar

- [GitHub Actions rasmiy hujjat](https://docs.github.com/actions)
- [GitHub Marketplace (tayyor action'lar)](https://github.com/marketplace?type=actions)
- [YAML sintaksis](https://yaml.org)

---

<div align="center">

### 🎓 Dars tugadi!

**Savollar bo'lsa — so'rang. Omad!** 🚀

</div>