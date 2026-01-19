from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout ,get_user_model  # ✅ added logout + authenticate
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .tokens import account_activation_token  # custom token generator
from django.http import HttpResponse
from django.conf import settings
import random
from .models import PasswordResetOTP  # model to store OTPs
from django.contrib.auth.hashers import make_password
from .models import Profile

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    from .forms import ProfileForm  # Import here to avoid circular import
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def auth_toggle(request):
    if request.method == "POST":
        # If user is already logged in -> logout
        if request.user.is_authenticated:
            logout(request)
            return redirect('note_list')   # redirect to notes after logout

        # Otherwise -> login attempt
        if 'login' in request.POST:  # login form
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(request, "Please activate your account via email first.")
                    return redirect('auth_toggle')

                login(request, user)
                return redirect('note_list')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('auth_toggle')

        elif 'register' in request.POST:  # registration form
            # registration logic
            pass

    return render(request, 'registration/auth_toggle.html')

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email:
            messages.error(request, "Username and email are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)

        # Send activation email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = request.build_absolute_uri(reverse('activate', args=[uid, token]))

        subject = "Activate your StudySetU account"
        message = render_to_string('accounts/activation_email.txt', {
            'user': user,
            'activation_link': activation_link,
        })

        try:
             send_mail(subject, message, None, [email])
        except Exception as e:
             print("Email error:", e)

        messages.success(request, "Check your email to activate your account.")
        return redirect('auth_toggle')
    return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and account_activation_token.check_token(user, token):
        if user.is_active:
            messages.info(request, "Your account is already activated. Please log in.")
            return redirect('auth_toggle')
        
        user.is_active = True
        user.save()
        
        # Ensure profile exists (should be created by signal, but just in case)
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        
        messages.success(
            request,
            "Your email has been verified successfully. Please log in to continue."
        )
        return redirect('auth_toggle')

    messages.error(request, "Activation link is invalid or expired.")
    return redirect('auth_toggle')

def send_otp_view(request):
    # Clear any previous debug OTP
    # if "debug_otp" in request.session:
    #     del request.session["debug_otp"]
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "accounts/forgot_password.html")
        
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  # 6-digit OTP

            # Save new OTP in DB
            PasswordResetOTP.objects.create(user=user, otp=otp)

            # Send OTP via email
            try:
                send_mail(
                    subject="StudySetU - Password Reset OTP",
                    message=f"Hello {user.username},\n\nYour password reset OTP is: {otp}\n\nThis code will expire in 5 minutes.\n\nIf you didn't request this, please ignore this email.\n\nBest regards,\nStudySetU Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                request.session["reset_user"] = user.id  # store user in session
                messages.success(request, f"OTP has been sent to {email}. Please check your inbox.")
                return redirect("verify_otp")
            except Exception as email_error:
                # If email fails, still save OTP and show it (for development/testing)
                # In production, you might want to handle this differently
                error_msg = str(email_error)
                
                # For development: if console backend, OTP is printed to console
                if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
                    print(f"\n{'='*50}")
                    print(f"PASSWORD RESET OTP for {user.username} ({email}): {otp}")
                    print(f"{'='*50}\n")
                    request.session["reset_user"] = user.id
                    messages.warning(request, f"Email sending failed (using console backend). OTP: {otp} - Check console/terminal for OTP.")
                    return redirect("verify_otp")
                else:
                    # For production: show error with helpful message
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Email sending error: {error_msg}")
                    
                    # Provide helpful error message based on common issues
                    if "authentication failed" in error_msg.lower() or "535" in error_msg:
                        error_display = "Email authentication failed. Please check your Gmail App Password."
                    elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                        error_display = "Could not connect to email server. Please check your internet connection."
                    elif "550" in error_msg or "relay" in error_msg.lower():
                        error_display = "Email relay error. Please check email configuration."
                    else:
                        error_display = f"Email error: {error_msg[:100]}"  # Limit error message length
                    
                    messages.error(request, error_display)
                    # Still save OTP in session for manual testing if needed
                    request.session["reset_user"] = user.id
                    request.session["debug_otp"] = otp  # Store OTP in session for debugging (remove in production)
                    return render(request, "accounts/forgot_password.html")
                
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
            return render(request, "accounts/forgot_password.html")
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in send_otp_view: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}. Please try again later.")
            return render(request, "accounts/forgot_password.html")
    
    return render(request, "accounts/forgot_password.html")

def verify_otp_view(request):
    user_id = request.session.get("reset_user")
    if not user_id:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect("forgot_password")
    
    if request.method == "POST":
        otp_entered = request.POST.get("otp", "").strip()
        if not otp_entered:
            return render(request, "accounts/varify_otp.html", {"error": "Please enter the OTP."})

        try:
            user = User.objects.get(id=user_id)
            otp_obj = PasswordResetOTP.objects.filter(user=user).order_by('-created_at').first()

            if otp_obj and otp_obj.otp == otp_entered and otp_obj.is_valid():
                request.session["otp_verified"] = True
                messages.success(request, "OTP verified successfully!")
                return redirect("reset_password")
            else:
                return render(request, "accounts/varify_otp.html", {"error": "Invalid or expired OTP. Please request a new one."})
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("forgot_password")
        except Exception as e:
            return render(request, "accounts/varify_otp.html", {"error": "An error occurred. Please try again."})
    
    return render(request, "accounts/varify_otp.html")

def reset_password_view(request):
    if not request.session.get("otp_verified"):
        messages.error(request, "Please verify OTP first.")
        return redirect("forgot_password")
    
    if request.method == "POST":
        new_pass = request.POST.get("password", "").strip()
        confirm_pass = request.POST.get("confirm_password", "").strip()
        user_id = request.session.get("reset_user")
        
        if not user_id:
            messages.error(request, "Session expired. Please start again.")
            return redirect("forgot_password")
        
        if not new_pass or not confirm_pass:
            return render(request, "accounts/reset_password.html", {"error": "Both password fields are required."})
        
        if new_pass != confirm_pass:
            return render(request, "accounts/reset_password.html", {"error": "Passwords do not match."})
        
        if len(new_pass) < 6:
            return render(request, "accounts/reset_password.html", {"error": "Password must be at least 6 characters long."})
        
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_pass)  # Use set_password instead of make_password
            user.save()
            
            # Delete used OTP
            PasswordResetOTP.objects.filter(user=user).delete()
            
            # Clear session
            request.session.pop("otp_verified", None)
            request.session.pop("reset_user", None)
            
            messages.success(request, "Password reset successfully! Please login with your new password.")
            return redirect("auth_toggle")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("forgot_password")
        except Exception as e:
            return render(request, "accounts/reset_password.html", {"error": "An error occurred. Please try again."})
    
    return render(request, "accounts/reset_password.html")
def create_admin_once(request):
    User = get_user_model()

    if User.objects.filter(username="admin").exists():
        return HttpResponse("Superuser already exists")

    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="StrongPassword@123"
    )
    return HttpResponse("Superuser created successfully")