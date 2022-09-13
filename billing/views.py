from django.shortcuts import render
from billing.models import *
from billing.serializers import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import ChangePasswordSerializer
from dj_rest_auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout

User = get_user_model()

class AdminRegisterView(generics.GenericAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Admin.objects.all()
    serializer_class = AdminRegistrationSerializer

    def get(self, request, *args, **kwargs):
        admin = Admin.objects.all()
        admin_serializer = self.get_serializer(admin, many=True)
        res2 = {
            'code': 1,
            'message': "GET List",
            "result": admin_serializer.data
        }
        return Response(data=res2, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("------serializer-------"+str(serializer))
        if serializer.is_valid():
            a = serializer.save()
            print("------a-------"+str(a))
            res = {
                'code': 1,
                'message': "Registered Successfully",
                "result": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res1 = {
                'code': 0,
                'message': "Not Registered",
                "result": serializer.errors
            }
            return Response(res1, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     # serializer = self.get_serializer(data=request.data)
    #     data = request.data
    #     data1 = data.copy()
    #     S = 24  # number of characters in the string.
    #     # call random.choices() string module to find the string in Uppercase + numeric data.
    #     ran = ''.join(random.choices(
    #         string.ascii_uppercase + string.digits, k=S))
    #     # data1['access_token'] = ran
    #     print("------data-------", str(data1))
    #     admin = Admin()
    #     admin.first_name = request.POST.get('FirstName')
    #     admin.last_name = request.POST.get('LastName')
    #     admin.mobile = request.POST.get('mobile')
    #     admin.email = request.POST.get('email')
    #     admin.password = request.POST.get('password')
    #     admin.gender = request.POST.get('gender')
    #     admin.access_token = ran
    #     admin.save()
    # # if data1.is_valid():
    # #     a = data1.save()
    # #     print("------a-------", str(a))
    #     return Response(admin, status=status.HTTP_201_CREATED)
    # # if serializer.is_valid():
    # #     a = serializer.save()
    # #     print("------a-------"+str(a))
    # #     data = request.data
    # #     print("------data-------"+str(data))

    # #     user = authenticate(
    # #         username=data['email'], password=data['password'])
    # #     print("------user-------"+str(user))

    # #     jwt_tokens = RefreshToken.for_user(user)

    # #     res = {
    # #         'code': 1,
    # #         'message': "Registered Successfully",
    # #         "status":True,
    # #         'refresh_token': str(jwt_tokens),
    # #         'access_token': str(jwt_tokens.access_token),
    # #         "result": serializer.data
    # #     }

    # #     return Response(res, status=status.HTTP_201_CREATED)
    # # else:
    # #     res1 = {
    # #         'code': 0,
    # #         'message': "Not Registered",
    # #         "result": serializer.errors
    # #     }
    # #     return Response(res1, status=status.HTTP_400_BAD_REQUEST)


class AdminDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        admin = Admin.objects.filter(pk=pk)
        print("------admin-------", admin)
        admin_serializer = AdminRegistrationSerializer(admin, many=True)
        print("------admin_serializer-------"+str(admin_serializer))
        resp4 = {
            "code": 1,
            "message": " Admin Detail",
            "result": admin_serializer.data
        }
        return Response(data=resp4, status=status.HTTP_200_OK)

    def put(self, request, pk):
        admin = Admin.objects.get(pk=pk)
        admin_serializer = AdminRegistrationSerializer(
            admin, data=request.data)
        if admin_serializer.is_valid():
            admin_serializer.save()
            resp4 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": admin_serializer.data
            }
            return Response(data=resp4, status=status.HTTP_200_OK)
        else:
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        resp6 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp6, status=status.HTTP_200_OK)


class MainView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MainSerializer
    queryset = Main.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            serializer = MainSerializer(data=request.data)
            print("------serializer-------"+str(serializer))
            if serializer.is_valid():
                a = serializer.save()
                print("------a-------"+str(a))
                res = {
                    'code': 1,
                    'message': "Registered Successfully",
                    "result": serializer.data
                }
                return Response(res, status=status.HTTP_201_CREATED)
        else:
            res1 = {
                'code': 0,
                'message': "Not Registered",
                "result": serializer.errors
            }
            return Response(res1, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        main = Main.objects.all()
        print("------main-------"+str(main))
        main_serializer = self.get_serializer(main, many=True)
        print("------main_serializer-------"+str(main_serializer))
        res2 = {
            'code': 1,
            'message': "GET List",
            "result": main_serializer.data
        }
        return Response(data=res2, status=status.HTTP_200_OK)


class MainDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        main = Main.objects.filter(admin_id=pk)
        print("------Main-------"+str(main))
        # tmpJson = serializers.serialize("json",main)
        # print("------tmpJson-------"+str(tmpJson))
        # tmpObj = json.loads(tmpJson)
        main_serializer = MainSerializer(main, many=True)
        print("------main_serializer-------"+str(main_serializer))
        resp4 = {
            "code": 1,
            "message": "Product Detail",
            "result": main_serializer.data
        }
        return Response(data=resp4, status=status.HTTP_200_OK)

    def put(self, request, pk):
        main = Main.objects.get(pk=pk)
        main_serializer = MainSerializer(main, data=request.data)
        if main_serializer.is_valid():
            main_serializer.save()
            resp4 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": main_serializer.data
            }
            return Response(data=resp4, status=status.HTTP_200_OK)
        else:
            return Response(main_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        main = Main.objects.get(pk=pk)
        main.delete()
        resp6 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp6, status=status.HTTP_200_OK)


class Sub_Title_One_View(generics.GenericAPIView):
    serializer_class = Sub_Title_One_Serializer
    queryset = Sub_Title_One.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = request.user
        # if user.is_admin:
        sub_title_one = Sub_Title_One.objects.all()
        print("sub_title_one---------"+str(sub_title_one))
        sub_title_one_serializer = Sub_Title_One_Serializer(
            sub_title_one, many=True)
        print("sub_title_one_serializer---------" +
              str(sub_title_one_serializer))
        resp1 = {
            "code": 1,
            "message": "Get List Success",
            "result": sub_title_one_serializer.data
        }
        return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.user
        # if user.is_admin:
        sub_title_one_serializer = Sub_Title_One_Serializer(data=request.data)
        print("sub_title_one_serializer---------" +
              str(sub_title_one_serializer))
        if sub_title_one_serializer.is_valid():
            title = sub_title_one_serializer.save()
            print("------title---------"+str(title))
            resp2 = {
                "code": 1,
                "message": "Posted Successfully",
                "result": sub_title_one_serializer.data
            }
            return Response(data=resp2, status=status.HTTP_200_OK)
        return Response(sub_title_one_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Sub_Title_One_DetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        sub_title_one = Sub_Title_One.objects.get(pk=pk)
        sub_title_one_serializer = Sub_Title_One_Serializer(
            sub_title_one, many=False)
        resp3 = {
            "code": 1,
            "message": "Detail",
            "result": sub_title_one_serializer.data
        }
        return Response(data=resp3, status=status.HTTP_200_OK)

    def put(self, request, pk):
        sub_title_one = Sub_Title_One.objects.get(pk=pk)
        sub_title_one_serializer = Sub_Title_One_Serializer(
            sub_title_one, data=request.data)
        if sub_title_one_serializer.is_valid():
            sub_title_one_serializer.save(one=request.user)
            resp4 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": sub_title_one_serializer.data
            }
            return Response(data=resp4, status=status.HTTP_200_OK)
        else:
            return Response(sub_title_one_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sub_title_one = Sub_Title_One.objects.get(pk=pk)
        sub_title_one.delete()
        resp5 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp5, status=status.HTTP_200_OK)


class Sub_Title_Two_View(generics.GenericAPIView):
    serializer_class = Sub_Title_Two_Serializer
    queryset = Sub_Title_Two.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub_title_two = Sub_Title_Two.objects.all()
        sub_title_two_serializer = Sub_Title_Two_Serializer(
            sub_title_two, many=True)
        resp1 = {
            "code": 1,
            "message": "Get List Success",
            "result": sub_title_two_serializer.data
        }
        return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request):
        sub_title_two_serializer = Sub_Title_Two_Serializer(data=request.data)
        print("sub_title_two_serializer---------"+str(sub_title_two_serializer))
        if sub_title_two_serializer.is_valid():
            title_two = sub_title_two_serializer.save()
            print("title_two---------"+str(title_two))
            resp2 = {
                "code": 1,
                "message": "Posted Successfully",
                "result": sub_title_two_serializer.data
            }
            return Response(data=resp2, status=status.HTTP_200_OK)


class Sub_Title_Two_DetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        sub_title_two = Sub_Title_Two.objects.get(pk=pk)
        sub_title_two_serializer = Sub_Title_Two_Serializer(
            sub_title_two, many=False)
        resp3 = {
            "code": 1,
            "message": "Product Detail",
            "result": sub_title_two_serializer.data
        }
        return Response(data=resp3, status=status.HTTP_200_OK)

    def put(self, request, pk):
        sub_title_two = Sub_Title_Two.objects.get(pk=pk)
        sub_title_two_serializer = Sub_Title_Two_Serializer(
            sub_title_two, data=request.data)
        if sub_title_two_serializer.is_valid():
            sub_title_two_serializer.save(two=request.user)
            resp4 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": sub_title_two_serializer.data
            }
            return Response(data=resp4, status=status.HTTP_200_OK)
        else:
            return Response(sub_title_two_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sub_title_two = Sub_Title_Two.objects.get(pk=pk)
        sub_title_two.delete()
        resp5 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp5, status=status.HTTP_200_OK)

# class MainGetView(generics.GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         main = Main.objects.all()
#         print("------main-------"+str(main))
#         main_serializer = MainSerializer(main, many=True)
#         print("------main_serializer-------"+str(main_serializer))
#         res2 = {
#             'code': 1,
#             'message': "GET List",
#             "result": main_serializer.data
#         }
#         return Response(data=res2, status=status.HTTP_200_OK)


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        print("------orginal_response-------"+str(orginal_response.data))
        body = {
            'message': 'User Logged in successfully',
            'result': orginal_response.data
        }
        return Response(body)


# class SignInAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         print("------serializer-------"+str(serializer))
#         serializer.is_valid(raise_exception=True)
#         print("------serializer-------"+str(serializer))
#         user = serializer.validated_data
#         print("------user-------"+str(user))
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)
#         })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'code': 1,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
