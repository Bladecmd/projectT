from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from rest_framework.authtoken.models import Token
# import from the Users model in the data_api_app project
from data_api_app.models import Author

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'username', 'email', 'password']
        
    # override default save to include token
    def save(self, **kwargs):
        new_author = Author.objects.create_user(
            username = self.validated_data["username"],
            email = self.validated_data["email"],
            password = self.validated_data["password"],
        )
        
        new_author.save()
        
        new_token = Token.objects.create(user=new_author)
        