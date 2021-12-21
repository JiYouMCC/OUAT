from .models import Token
import uuid

def create_token(user):
    clear_token(user)
    token = Token(user=user, token=uuid.uuid4().hex)
    token.save()
    return token.token

def clear_token(user):
    Token.objects.filter(user=user).delete()

def get_user_by_token(token):
    token = Token.objects.filter(token=token)[0]
    if token:
        return token.user
    else:
        return None

