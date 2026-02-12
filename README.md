# SCC Signs and Current Medical Complaints App

This project is created by copyright(c) 2026 Hans Hendrickx MD PhD. This is project in progress.

Codes: Django 5.2 lts, Python 3.12, Developed in W10, using VScode, 

Assistance: AI Deepseek, Perplexity and ChatGPT

Licence: MIT

Background: View this Github and search [Figshare+HansHendrickx]

# 🔍 The Folder Tree Reveals
✅ Django & DRF Setup Looks Solid
snippets/ app has models.py, serializers.py, views.py, permissions.py, and urls.py → you’re using ViewSets + ModelSerializer + custom permissions.

accounts/ app is present, which likely contains your custom user model and authentication logic (WV style).

templates/registration/ suggests you’re using django-allauth or a similar auth flow for the browsable API / admin.

SCC/urls.py probably includes path('api/', include('snippets.urls')) and path('accounts/', include('accounts.urls')).

permissions.py in snippets/ indicates you’ve implemented custom object-level permissions (e.g., IsOwnerOrReadOnly).

# ✅ Testing Structure Is Ready
snippets/tests.py and accounts/tests.py exist → you have test files waiting to be filled.

This is perfect: you already have the infrastructure for automated API tests.

# ✅ What Your settings.py Confirms
Aspect	Status	Implication
Django version	4.1 (docstring) / you mentioned 5.2 – fine, no conflict	Works either way.
Custom user model	❌ Not defined (AUTH_USER_MODEL absent)	You’re using Django’s default User. This simplifies testing.
DRF settings	Only pagination set	No global authentication/permission classes → defaults apply: SessionAuthentication, BasicAuthentication, and AllowAny.
Authentication backends	Default ModelBackend	Standard session/cookie auth. No token auth configured (yet).
Login/logout URLs	LOGIN_REDIRECT_URL = '/', LOGOUT_REDIRECT_URL = '/'	Matches WV tutorial style – login redirects to home.
Installed apps	rest_framework, snippets, pages, accounts	Clean, modular structure.
Templates	DIRS = [BASE_DIR / "templates"]	You have custom templates (e.g., for registration).
Key takeaway: Your API is currently open (AllowAny) unless you’ve overridden permissions in individual views. That’s fine for early development.

# 🔍 What I Still Need (To Understand Your “WV Authentication”)
You mentioned “WV authentication” – in Will Vincent’s tutorials, this usually means one of:

Django’s built-in session authentication with login templates (what you have now).

django-allauth for social/email login.

Token authentication (DRF’s TokenAuthentication) added later.

Your settings.py doesn’t include allauth or DRF token auth, so I suspect you’re using #1 (standard login views) – but I need to verify.

Please share these 3 files next (in order of priority):

File	Why It’s Critical
accounts/models.py	To confirm you’re not using a custom user model.
snippets/permissions.py	To see if you’ve implemented IsOwnerOrReadOnly or similar. This will dictate how we test object-level permissions.
snippets/views.py	To see if you’re using ModelViewSet (which respects DRF permissions) or function-based @api_view.
If you prefer, share them one by one – I’ll wait and analyse each.