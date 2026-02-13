🏗️ Core Architecture Decision: Custom User Model First
The most critical decision is using a custom User model from the start. This is non-negotiable for the family role system you've described .

accounts/models.py:

python
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    # Extend the built-in User model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True)
    
    # Soft delete fields (GDPR compliance)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Age verification fields
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified_adult = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ("can_manage_children", "Can manage child accounts"),
            ("can_view_audit_logs", "Can view audit logs"),
        ]
👨‍👩‍👧‍👦 Family Role Implementation
Based on your age-based permission structure and the youth organization database patterns , here's the complete family account system:

accounts/models.py (continued):

python
from django.conf import settings
from django.db import models
import uuid

class UserProfile(models.Model):
    """Extended profile information for all users"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

class ChildParticipant(models.Model):
    """Represents a child who may not have their own login"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Who is responsible for this child
    supervised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,  # CRITICAL: Don't allow deletion if children exist
        related_name='supervised_children'
    )
    
    # Child's information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    # Contact info (children may not have email)
    email = models.EmailField(blank=True)  # Optional for children
    phone = models.CharField(max_length=20, blank=True)
    
    # Medical/Safety information
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    emergency_notes = models.TextField(blank=True)
    
    # Age-based permission level (derived from DOB, but cached for performance)
    age_group = models.CharField(max_length=20, choices=[
        ('0-11', '0-11 years'),
        ('12-15', '12-15 years'),
        ('16-17', '16-17 years'),
    ])
    
    # For proxy access (handicapped persons via proxy)
    requires_proxy_for_sharing = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete
    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['supervised_by', 'is_active']),
            models.Index(fields=['age_group']),
        ]
        permissions = [
            ("can_access_child_data", "Can access child participant data"),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (supervised by {self.supervised_by.username})"
    
    def get_age_group(self):
        """Calculate age group from date of birth"""
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        
        if age <= 11:
            return '0-11'
        elif 12 <= age <= 15:
            return '12-15'
        elif 16 <= age <= 17:
            return '16-17'
        else:
            return 'adult'  # Should not happen for ChildParticipant
🎭 Guest User Implementation (24-hour expiration)
For the guest accounts that expire after 24 hours, use the django-guest-user package which handles this elegantly .

Installation:

bash
pip install django-guest-user
settings.py:

python
INSTALLED_APPS = [
    # ...
    'guest_user',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guest_user.backends.GuestBackend',
]

# Guest user settings
GUEST_USER_MAX_AGE = 86400  # 24 hours in seconds
GUEST_USER_DELETE_INACTIVE_AFTER = 86400  # Delete after 24 hours

# Block bots from becoming guest users
GUEST_USER_BLOCKED_USER_AGENTS = [
    'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 'python-requests',
]

MIDDLEWARE = [
    # ...
    'guest_user.middleware.GuestMiddleware',  # Track guest activity
]
urls.py:

python
urlpatterns = [
    # ...
    path('guest/', include('guest_user.urls')),  # For guest conversion
]
Usage in views:

python
from guest_user.decorators import allow_guest_user

@allow_guest_user  # Automatically creates guest account for anonymous users
def emergency_view(request):
    # This view works for both guests and registered users
    return render(request, 'emergency.html')
For automatic cleanup of expired guest users, create a management command:

accounts/management/commands/cleanup_guests.py:

python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from guest_user.models import Guest

User = get_user_model()

class Command(BaseCommand):
    help = 'Delete expired guest users'
    
    def handle(self, *args, **options):
        expiry_time = timezone.now() - timedelta(seconds=86400)  # 24 hours
        expired_guests = Guest.objects.filter(
            user__date_joined__lt=expiry_time,
            converted_to_user__isnull=True
        )
        
        count = expired_guests.count()
        # This will cascade delete the associated User due to CASCADE
        expired_guests.delete()
        
        self.stdout.write(f'Deleted {count} expired guest users')
Add to cron or use django-cron to run this daily.

🔐 Security & Environment Variables
.env file (never commit to git):

bash
# Django
SECRET_KEY=your-very-long-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_NAME=scc_prod
DB_USER=scc_user
DB_PASSWORD=strong-database-password
DB_HOST=localhost
DB_PORT=5432

# Encryption for sensitive fields
ENCRYPTION_KEY=generate-a-32-byte-base64-key-here

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# QR Token Secret
QR_TOKEN_SECRET=another-secure-random-string
settings.py to load environment variables:

python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Encryption for sensitive fields
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
🔑 Token Generation for QR Codes
For the QR code functionality (children sharing data via QR), you need secure token generation:

accounts/utils/tokens.py:

python
import secrets
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

class QRTokenGenerator:
    """Generate secure tokens for QR code sharing"""
    
    @staticmethod
    def generate_child_access_token(child_id, expires_in_hours=24):
        """
        Generate a time-limited token for accessing child data via QR.
        Token includes child ID, expiration, and HMAC signature.
        """
        # Create payload
        expires = datetime.utcnow() + timedelta(hours=expires_in_hours)
        payload = {
            'child_id': str(child_id),
            'exp': expires.timestamp(),
            'purpose': 'child_data_access',
        }
        
        # Convert to JSON and encode
        payload_json = json.dumps(payload, separators=(',', ':'))
        payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
        
        # Create HMAC signature
        signature = hmac.new(
            settings.QR_TOKEN_SECRET.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()[:16]  # Truncate for QR readability
        
        # Combine: payload.signature
        return f"{payload_b64}.{signature}"
    
    @staticmethod
    def validate_child_access_token(token):
        """
        Validate token and return child_id if valid.
        Raises ValueError if invalid/expired.
        """
        try:
            payload_b64, signature = token.split('.')
            
            # Verify signature
            expected_sig = hmac.new(
                settings.QR_TOKEN_SECRET.encode(),
                payload_b64.encode(),
                hashlib.sha256
            ).hexdigest()[:16]
            
            if not hmac.compare_digest(signature, expected_sig):
                raise ValueError("Invalid signature")
            
            # Decode and parse payload
            payload_json = base64.urlsafe_b64decode(payload_b64.encode()).decode()
            payload = json.loads(payload_json)
            
            # Check expiration
            if datetime.utcnow().timestamp() > payload['exp']:
                raise ValueError("Token expired")
            
            return payload['child_id']
            
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid token: {e}")

# Alternative using Django's signing framework (simpler)
from django.core.signing import TimestampSigner, dumps, loads

signer = TimestampSigner(salt='child-access')

# Generate token
def generate_simple_token(child_id):
    """Generate simple signed token (easier but less customizable)"""
    return signer.sign(str(child_id))

def validate_simple_token(token, max_age=86400):
    """Validate token, returns child_id if valid"""
    try:
        return signer.unsign(token, max_age=max_age)
    except (BadSignature, SignatureExpired) as e:
        return None
QR code generation view:

python
from django.http import JsonResponse
import qrcode
from io import BytesIO
import base64

def generate_child_qr(request, child_id):
    """Generate QR code for child data sharing"""
    token = QRTokenGenerator.generate_child_access_token(child_id)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )
    qr.add_data(f"https://yourapp.com/access/{token}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in response
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return JsonResponse({
        'qr_code': f"data:image/png;base64,{img_str}",
        'token': token,
        'expires_in': '24 hours'
    })
🗑️ GDPR-Compliant Data Deletion
Implement proper soft delete with anonymization for GDPR compliance :

accounts/models.py - Add to User model:

python
def soft_delete(self, deleted_by=None, reason=""):
    """GDPR-compliant soft delete with anonymization"""
    self.is_deleted = True
    self.deleted_at = timezone.now()
    self.deleted_by = deleted_by
    
    # Anonymize personal data (GDPR requirement)
    original_email = self.email
    self.email = f"deleted-{self.id}@anonymous.local"
    self.first_name = "[deleted]"
    self.last_name = "[deleted]"
    
    # Store original email hash for audit if needed
    self.original_email_hash = hashlib.sha256(original_email.encode()).hexdigest()
    
    self.save()
    
    # Log deletion for audit trail
    AuditLog.objects.create(
        user_id=self.id,
        action='GDPR_DELETE',
        reason=reason,
        deleted_by=deleted_by.username if deleted_by else None
    )
accounts/models.py - Audit log model:

python
class AuditLog(models.Model):
    """Tamper-resistant audit log for GDPR compliance [citation:1]"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    user_id = models.UUIDField(db_index=True)  # Store even if user is deleted
    action = models.CharField(max_length=50)  # CREATE, READ, UPDATE, DELETE, GDPR_DELETE
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    
    # Store changes as JSON
    changes = models.JSONField(null=True, blank=True)
    
    # Who performed the action
    performed_by = models.CharField(max_length=150, null=True, blank=True)
    
    # Additional context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    reason = models.TextField(blank=True)
    
    # Cryptographic hash to detect tampering
    previous_hash = models.CharField(max_length=64, blank=True)
    current_hash = models.CharField(max_length=64, unique=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id', '-timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
        permissions = [
            ("can_view_audit_logs", "Can view audit logs"),
        ]
    
    def save(self, *args, **kwargs):
        """Generate hash chain for tamper resistance"""
        # Get last log for hash chaining
        last_log = AuditLog.objects.order_by('-timestamp').first()
        self.previous_hash = last_log.current_hash if last_log else '0' * 64
        
        # Create hash of this record
        hash_input = f"{self.timestamp}{self.user_id}{self.action}{self.previous_hash}{self.reason}"
        self.current_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        super().save(*args, **kwargs)
📝 Implementation Checklist
Priority	Task	Tools/Packages	Status
1	Set up custom User model	AbstractUser	⬜
2	Configure .env and encryption	python-dotenv, cryptography	⬜
3	Install and configure django-guest-user	PyPI package 	⬜
4	Create ChildParticipant model	Custom	⬜
5	Implement QR token system	secrets, hmac, qrcode	⬜
6	Add soft delete with anonymization	Custom + AuditLog	⬜
7	Set up cleanup cron job	django-cron or system cron	⬜
8	Create admin views with proper permissions	Django Admin	⬜
9	Add age verification logic	Custom	⬜
10	Test GDPR compliance flows	Manual + automated	⬜
🚀 Next Steps
Start with a new branch for this foundational work

Implement the custom User model first - this requires a fresh database

Configure environment variables and never commit .env

Add guest user functionality with 24-hour expiration

Build the child participant model with proper foreign key constraints (PROTECT not CASCADE for children) 

Implement QR token generation for secure sharing

Add audit logging for all data access

This foundation will give you a professional, GDPR-compliant application that properly handles all the family role scenarios you described. Once this is in place, building the emergency UI pages becomes straightforward—they'll just work with the solid authentication and data layer underneath.

Would you like me to elaborate on any specific component, or provide the complete code for a particular feature?