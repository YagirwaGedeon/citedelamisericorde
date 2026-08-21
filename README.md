# Cité de la Miséricorde — Site web ASBL

Site officiel de l'ASBL **Cité de la Miséricorde** (Bukavu & Goma, RD Congo) : information, actualités, dons en ligne, espace d'administration.

---

## 1. Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python 3.14 / Django 6.x |
| Base de données | SQLite (développement) / PostgreSQL (production, via `.env`) |
| Frontend | HTML sémantique, Tailwind CSS 4 (CLI), JavaScript vanilla |
| Paiements | Stripe, PayPal, Mobile Money RDC (Flutterwave), passerelle **sandbox** de démo |
| Reçus de don | reportlab (PDF) + email de remerciement |
| PWA | `manifest.json`, `service-worker.js` (`/sw.js`), page `/offline/` |
| Anti-spam | reCAPTCHA v3 (formulaire de contact) |
| Import WordPress | commandes `manage.py wordpress_*` |

## 2. Prérequis

- Python 3.12+ (venv intégré : `.venv\Scripts\python.exe`)
- Node.js + npm (Tailwind CLI)
- Connexion internet pour les CDN (Leaflet, Google Fonts, reCAPTCHA)

## 3. Installation (première mise en route)

```powershell
# 1. Créer l'environnement virtuel et installer les dépendances
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Installer le frontend
npm install

# 3. Variables d'environnement
Copy-Item .env.example .env        # puis renseigner les valeurs (voir §6)

# 4. Base de données + données de référence
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_base       # contenus et données de référence
.venv\Scripts\python.exe manage.py createsuperuser # compte administrateur

# 5. Compiler le CSS Tailwind
npm run build
```

## 4. Démarrage

```powershell
# Développement (avec rechargement automatique)
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

# Recommandé ici (sans rechargement : les changements .py exigent un redémarrage)
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765 --noreload
```

Après chaque modification d'un fichier **Python ou template** : redémarrer le serveur.

```powershell
# Redémarrer le serveur (Windows PowerShell)
$conn = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if ($conn) { Stop-Process -Id $conn.OwningProcess -Force; Start-Sleep 2 }
Start-Process -FilePath "F:\SITE DE LA MISERICORDE\citedelamisericorde\.venv\Scripts\python.exe" `
  -ArgumentList "manage.py","runserver","127.0.0.1:8765","--noreload" `
  -WorkingDirectory "F:\SITE DE LA MISERICORDE\citedelamisericorde" -WindowStyle Hidden
```

Après chaque ajout de **classe CSS Tailwind** dans un template : `npm run build`.

## 5. Frontend (Tailwind)

```powershell
npm run build   # compilation unique (production)
npm run watch   # compilation continue pendant le développement
```

Fichiers : `static/css/input.css` (source) → `static/css/main.css` (compilé).
Les classes custom (`.btn`, `.nav-dropdown`, `.mobile-overlay`, `.card`, `.badge`…) sont définies dans `input.css` sous `@layer components`.

## 5bis. Multilingue (français / anglais / swahili)

- Sélecteur de langue **FR / EN / SW** dans la barre de navigation (desktop + mobile) : clic → POST `set_language` → cookie `django_language` → la page courante est rechargée dans la langue choisie.
- Catalogues : `locale/{fr,en,sw}/LC_MESSAGES/django.po`. La langue source est le français ; le menu, les boutons et les libellés d'interface sont traduits via `gettext_lazy` (Python) et `{% translate %}` (templates).
- **Ajouter/modifier une traduction** :
  1. Éditer les fichiers `.po` correspondants (`msgid "..."` / `msgstr "..."`),
  2. Recompiler les `.mo` (sans gettext, utilitaire inclus) :
     ```powershell
     .venv\Scripts\python.exe scripts\compile_po.py
     ```
  3. Redémarrer le serveur.
- Les **contenus édités dans l'admin** (articles, pages, projets…) sont rédigés dans une langue : la traduction complète de ces contenus est un chantier ultérieur (modèles bilingues) — le sélecteur bascule dès aujourd'hui l'interface et la navigation.

## 6. Configuration — fichier `.env`

Copier `.env.example` vers `.env` puis renseigner :

| Variable | Usage |
|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django (obligatoire, changer en production) |
| `DJANGO_DEBUG` | `True` en dev, **`False` en production** |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés (ex. `cite-misericorde.org`) |
| `DJANGO_EMAIL_BACKEND` | `console` en dev / SMTP en prod |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP (emails de remerciement, reset de mot de passe, newsletter) |
| `DEFAULT_FROM_EMAIL` | Expéditeur des emails |
| `RECAPTCHA_SITE_KEY`, `RECAPTCHA_SECRET_KEY` | reCAPTCHA v3 du formulaire de contact (vides = désactivé) |
| `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` | Paiements Stripe |
| `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MODE` | Paiements PayPal (`sandbox` / `live`) |
| `FLW_PUBLIC_KEY`, `FLW_SECRET_KEY`, `FLW_WEBHOOK_SECRET` | Mobile Money RDC (Flutterwave) |
| `ANALYTICS_GOOGLE_GA4` | Google Analytics 4 |
| `WORDPRESS_SITE`, `WORDPRESS_USERNAME`, `WORDPRESS_PASSWORD` | Import depuis WordPress |

**Ne jamais committer `.env`.** Il est ignoré par `.gitignore`.

## 7. Espace d'administration — `/admin/`

Comptes : superadmin `admin` ; utilisateurs créés dans « Utilisateurs » (rôle, photo, téléphone…).

Fonctionnalités :
- **Tableau de bord** : visiteurs du jour, dons (jour/mois/total), donateurs, projets, articles, messages non lus, graphique des dons sur 6 mois, dons par passerelle et par région, derniers dons/messages/articles, accès rapides.
- **Contenu (CMS)** : articles (éditeur rich-text avec aperçu : gras, titres, listes, liens, images, citations), pages, programmes, projets (statut dont « Urgent », progression), galerie, partenaires, témoignages, statistiques d'impact.
- **Dons** : donateurs, transactions (statuts Réussi / En attente / Échoué), export **CSV** (bouton dans la liste, avec accents corrects), reçus PDF.
- **Équipe** : membres de l'équipe dirigeante (photo, formation, ordre, publication).
- **Messages** : boîte de réception du formulaire de contact (spam géré par honeypot + reCAPTCHA).
- **Paramètres du site** : nom, slogan, adresses, réseaux sociaux, Google Analytics, thème PWA, maintenance.
- **Mon profil** : accessible dans le menu utilisateur (en haut à droite).

### Mot de passe oublié

Lien « Mot de passe oublié » sur la page de connexion → email de réinitialisation (console en dev, SMTP en prod).

## 8. Dons en ligne

Flux : **Formulaire** (`/dons/faire-un-don/`) → **Choix de la passerelle** (`/dons/checkout/<pk>/`) → **Paiement** (passerelle ou sandbox) → **Page de succès** avec reçu PDF et email de remerciement (envoyé une seule fois).

- Montants prédéfinis (10/20/50/100 USD) ou libre, don unique ou mensuel.
- Passerelles actives configurées dans l'admin (`Paiements → Passerelles`).
- **Sandbox** (« Mode démo ») : règle le don immédiatement — idéal pour tester sans clés.
- Les reçus PDF sont stockés dans `media/receipts/` et téléchargeables sur la page de succès.
- Aucune donnée bancaire n'est collectée ou stockée par le site.

## 9. PWA

- `manifest.json` et icônes dans `static/` (branchés dans `base.html`).
- Service worker servi à la racine : `/sw.js` (vue `service_worker`).
- Pré-cache des pages clés, stratégie *cache-first* pour les assets, page hors-ligne `/offline/`.
- Test : DevTools → Application → Service Workers.

## 10. Migration depuis WordPress

```powershell
# Voir le plan d'import sans rien écrire
.venv\Scripts\python.exe manage.py wordpress_import --dry-run

# Import complet (brouillons par défaut, images dédupliquées, URLs mappées)
.venv\Scripts\python.exe manage.py wordpress_import

# Options utiles
.venv\Scripts\python.exe manage.py wordpress_import --posts      # articles uniquement
.venv\Scripts\python.exe manage.py wordpress_import --pages      # pages uniquement
.venv\Scripts\python.exe manage.py wordpress_import --ids 256,209
.venv\Scripts\python.exe manage.py wordpress_import --publish    # publier directement
.venv\Scripts\python.exe manage.py wordpress_import --no-media   # sans télécharger les images

# Rapports
.venv\Scripts\python.exe manage.py wordpress_audit
.venv\Scripts\python.exe manage.py wordpress_report
```

Prérequis : identifiants WordPress dans `.env` (`WORDPRESS_USERNAME` / `WORDPRESS_PASSWORD`).

## 11. Tests automatisés

```powershell
.venv\Scripts\python.exe manage.py test
```

Suite de tests par application (`apps/*/tests.py`) : contact, donations, payments (reçus PDF), newsletter, migration, etc.

## 12. Sauvegarde

```powershell
# Base SQLite + fichiers téléversés
Copy-Item db.sqlite3 "backup-db-$(Get-Date -Format yyyyMMdd).sqlite3"
Copy-Item -Recurse media "backup-media-$(Get-Date -Format yyyyMMdd)"
```

En production (PostgreSQL) : `pg_dump`. Toujours sauvegarder aussi `media/` (photos, reçus PDF).

## 13. Mise en production — checklist

1. `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` rempli, `DJANGO_SECRET_KEY` forte.
2. `DJANGO_USE_POSTGRES=True` + variables `POSTGRES_*` renseignées.
3. `DJANGO_EMAIL_BACKEND` → SMTP réel, `DEFAULT_FROM_EMAIL` défini.
4. Clés de paiement réelles (Stripe/PayPal/Flutterwave) + webhooks configurés vers `/payments/webhook/<code>/`.
5. `DJANGO_SECURE_SSL_REDIRECT=True`, cookies sécurisés, HTTPS.
6. `manage.py collectstatic --noinput` et servir `static/` + `media/` (nginx/Apache/CDN).
7. `npm run build` (CSS minifié).
8. Remplir les paramètres du site (adresses, réseaux sociaux, reCAPTCHA, GA4).

## 14. Dépannage

| Problème | Solution |
|---|---|
| Port déjà occupé | `Get-NetTCPConnection -LocalPort 8765 -State Listen` puis `Stop-Process` |
| Styles non mis à jour | `npm run build` |
| Changements Python sans effet | Redémarrer le serveur (`--noreload`) |
| `NoReverseMatch` dans un template | Vérifier le nom de la route (`{% url 'app:name' %}`) |
| Email de remerciement absent | Vérifier `DJANGO_EMAIL_BACKEND` (console = sortie serveur) et l'adresse du donateur |
| reCAPTCHA bloque en dev | Laisser les clés vides (vérification désactivée) |
| 404 sur `/temoignages/` | Normal : pas de page publique dédiée (les témoignages sont sur la home et `/impact/`) |
| Mot de passe perdu | Lien « Mot de passe oublié » sur `/admin/login/` |