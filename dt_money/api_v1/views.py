from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api_v1.authentication import ApiAuthentication
from api_v1.models import Owner, SysUser, Transaction
from api_v1.serializers import UserSerializer, TransactionSerializer
from utils.functions import response_message, get_error_dict, get_owner


# Create your views here.


class UserConfigView(viewsets.ViewSet):
    authentication_classes = [ApiAuthentication]

    serializer_class = UserSerializer
    queryset = ''

    def get(self, request):
        user = authenticate(username=request.headers.get('Username'), password=request.headers.get('Password'))

        if user:
            owner = get_object_or_404(Owner, user=user)
            sys_user = get_object_or_404(SysUser, owner=owner, user=user)

            message_dict = {
                'first_name': sys_user.user.first_name,
                'last_name': sys_user.user.last_name,
                'sys_user_uuid': str(sys_user.uuid),
                'status_code': 200
            }

            return response_message(message_dict)
        else:
            message_dict = {
                'message': 'Invalid username or password',
                'status_code': 400
            }

            return response_message(message_dict)

    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            validated_data: dict = serializer.validated_data

            if 'first_name' not in validated_data or 'last_name' not in validated_data:
                message_dict = {
                    'message': 'Missing first name or last name',
                    'status_code': 400
                }

                return response_message(message_dict)

            user_obj = User.objects.filter(username=validated_data.get('username')).first()

            if not user_obj:
                user = User.objects.create(
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    username=validated_data.get('username'),
                )

                user.set_password(raw_password=validated_data.get('password'))

                user.save()

                owner = Owner.objects.create(user=user)
                sys_user = SysUser.objects.create(user=user, owner=owner)

                message_dict = {
                    'message': 'User created successfully.',
                    'sys_user_uuid': str(sys_user.uuid),
                    'status_code': 200,
                }

                return response_message(message_dict)
        else:

            return get_error_dict(serializer, status_code=400)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, partial=True)

        success, owner = get_owner(request)

        if not success:
            return response_message(owner)

        if serializer.is_valid():
            validated_data: dict = serializer.validated_data

            username = request.headers.get('Username')
            user = User.objects.filter(username=username).first()

            if user:
                user.first_name = validated_data.get('first_name')
                user.last_name = validated_data.get('last_name')
                user.set_password(validated_data.get('password'))

                user.save()

                message_dict = {
                    'message': 'User updated successfully.',
                    'status_code': 200,
                }

                return response_message(message_dict)
            else:
                message_dict = {
                    'message': 'This user does not exists',
                    'status_code': 400
                }

                return response_message(message_dict)
        else:
            return get_error_dict(serializer, status_code=400)

    def delete(self, request, pk=None):
        success, owner = get_owner(request)

        if not success:
            return response_message(owner)

        sys_user = get_object_or_404(SysUser, uuid=request.headers.get('Sys-user-uuid'), owner=owner)

        if sys_user:
            sys_user.user.delete()

            message_dict = {
                'message': 'User deleted successfully',
                'status_code': 200
            }

        else:
            message_dict = {
                'message': 'This user does not exist',
                'status_code': 400
            }

        return response_message(message_dict)


class TransactionView(viewsets.ViewSet):
    authentication_classes = [ApiAuthentication]

    serializer_class = TransactionSerializer

    queryset = ''

    def list(self, request):
        success, owner = get_owner(request)

        if not success:
            return response_message(owner)

        transaction_list = Transaction.objects.filter(owner=owner)

        transaction_dict_list = []
        for transaction_temp in transaction_list:
            transaction_dict_list.append({
                'title': transaction_temp.title,
                'value': transaction_temp.value,
                'category': transaction_temp.category,
                'type': transaction_temp.type,
                'uuid': str(transaction_temp.uuid),
                'created': str(transaction_temp.created)
            })

        message_dict = {
            'message': '',
            'transaction_list': transaction_dict_list,
            'status_code': 200
        }

        return response_message(message_dict)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)

        success, owner = get_owner(request)

        if not success:
            return response_message(owner)

        if serializer.is_valid():

            transaction: Transaction = serializer.save(owner=owner)

            transaction_dict = {
                'title': transaction.title,
                'value': transaction.value,
                'category': transaction.category,
                'type': transaction.type,
                'uuid': str(transaction.uuid),
                'created': str(transaction.created)
            }

            return JsonResponse(transaction_dict)
        else:
            return get_error_dict(serializer, status_code=400)

    def delete(self, request, *args, **kwargs):
        success, owner = get_owner(request)

        if not success:
            return response_message(owner)

        transaction = Transaction.objects.filter(owner=owner, uuid=request.headers.get('Transaction-uuid')).first()

        if transaction:
            transaction.delete()

            message_dict = {
                'message': 'Transaction deleted successfully',
                'status_code': 200
            }
        else:
            message_dict = {
                'message': 'Transaction does not exist',
                'status_code': 400
            }

        return response_message(message_dict)
