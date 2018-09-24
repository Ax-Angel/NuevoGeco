
class CustomJWTSerializer(JSONWebTokenSerializer):
	username_field = 'username_or_email'

	def validate(self, attrs):

		password = attrs.get("password")
		user_obj = User.objects.filter(email=attrs.get("username_or_email")).first() or User.objects.filter(username=attrs.get("username_or_email")).first()
		if user_obj is not None:
			credentials = {
				'username':user_obj.username,
				'password': password
			}
			if all(credentials.values()):
				user = authenticate(**credentials)
				if user:
					if not user.is_active:
						msg = _('User account is disabled.')
						raise serializers.ValidationError(msg)

					payload = jwt_payload_handler(user)

					return {
						'token': jwt_encode_handler(payload),
						'user': user
					}
				else:
					msg = _('Unable to log in with provided credentials.')
					raise serializers.ValidationError(msg)

			else:
				msg = _('Must include "{username_field}" and "password".')
				msg = msg.format(username_field=self.username_field)
				raise serializers.ValidationError(msg)

		else:
			msg = _('Account with this email/username does not exists')
			raise serializers.ValidationError(msg)
