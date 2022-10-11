from tkinter import filedialog
from tkinter import *
import tkinter as tk
import os
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
import io
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))


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
        admin_serializer = AdminSerializer(
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
        admin = Admin.objects.get(pk=pk)
        admin.delete()
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


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        print("------orginal_response-------"+str(orginal_response.data))
        body = {
            'message': 'User Logged in successfully',
            'result': orginal_response.data
        }
        return Response(body)


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
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'code': 1,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generatePDF(request, id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    # Inserting Logo into the Canvas at required position
    c.translate(10, 40)
    c.scale(1, 1)
    c.drawImage("YT 2.png", 10, 675, width=150, height=95)

    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1, 1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(50, 400)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold", 18)
    # Inserting the name of the company
    c.drawCentredString(315, 350, "YOUTH TECHNOLOGY PRIVATE LIMITED")
    # For under lining the title
    c.line(500, 340, 130, 340)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        300, 325, "Flat no-201,sec-10, beside good will arcade building,Nerul")
    c.drawCentredString(280, 310, "Navi Mumbai - 400709, India")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(280, 285, "GSTIN : 9876543210AABB")

    # Line Seprating the page header from the body
    c.line(520, 270, -15, 270)

    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold", 20)
    c.drawCentredString(215, 240, "TAX-INVOICE")

    # This Block Consist of Costumer Details
    # x-axis,y-axis,length,height,edges
    c.roundRect(-32, 100, 540, 125, 12, stroke=1, fill=0)
    c.setFont("Times-Bold", 15)
    c.drawRightString(200, 200, "INVOICE No.:YT001")
    c.drawRightString(200, 170, "DATE :10-10-2022")
    c.drawRightString(200, 140, "CUSTOMER NAME :John Doe")
    c.drawRightString(200, 110, "PHONE No. :9876543210")

    # This Block Consist of Item Description
    # x-axis,y-axis,length,height,edges
    c.roundRect(-32, -420, 540, 500, 12, stroke=1, fill=0)
    c.line(-32, -335, 508, -335)
    c.drawCentredString(8, 55, "SR No.")
    c.drawCentredString(170, 55, "ITEM")
    c.drawCentredString(340, 55, "PRICE")
    c.drawCentredString(400, 55, "QTY")
    c.drawCentredString(465, 55, "TOTAL")
    # Drawing table for Item Description
    c.line(-32, 45, 508, 45)  # horizontal line
    c.line(40, -371, 40, 80)  # vertical lines
    c.line(300, -371, 300, 80)  # vertical lines
    c.line(375, -371, 375, 80)  # vertical lines
    c.line(430, -371, 430, 80)  # vertical lines

    # Declaration and Signature ...
    c.line(-32, -370, 508, -370)
    c.line(250, -370, 250, -420)
    c.drawString(-25, -385, "We declare that above mentioned")
    c.drawString(-25, -400, "information is true.")
    c.drawString(-25, -415, "(This is system generated invoive)")
    c.drawRightString(450, -415, "Authorised Signatory")

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Invoice.pdf')


class ProductView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Main.objects.all()
    serializer_class = MainSerializer

    def get(self, request, *args, **kwargs):
        pro = Main.objects.all()
        pro_serializer = MainSerializer(pro, many=True)
        print("------pro_serializer-------"+str(pro_serializer))
        res = {
            'code': 1,
            'message': "Products List",
            "result": pro_serializer.data
        }
        return Response(data=res, status=status.HTTP_200_OK)


class DraftedView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Drafted.objects.all()
    serializer_class = DraftedSerializer

    def get(self, request, *args, **kwargs):
        draft = Drafted.objects.all()
        draft_serializer = DraftedSerializer(draft, many=True)
        print("------draft_serializer-------"+str(draft_serializer))
        res = {
            'code': 1,
            'message': "Drafted Products",
            "result": draft_serializer.data
        }
        return Response(data=res, status=status.HTTP_200_OK)


class PendingView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Pending.objects.all()
    serializer_class = PendingSerializer

    def get(self, request, *args, **kwargs):
        pending = Pending.objects.all()
        pending_serializer = PendingSerializer(pending, many=True)
        print("------pending_serializer-------"+str(pending_serializer))

        res = {
            'code': 1,
            'message': "Pending Products",
            "result": pending_serializer.data
        }
        return Response(data=res, status=status.HTTP_200_OK)


class CompletedView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Completed.objects.all()
    serializer_class = CompletedSerializer

    def get(self, request, *args, **kwargs):
        complete = Completed.objects.all()
        complete_serializer = CompletedSerializer(complete, many=True)
        print("------complete_serializer-------"+str(complete_serializer))
        res = {
            'code': 1,
            'message': "Completed Products",
            "result": complete_serializer.data
        }
        return Response(data=res, status=status.HTTP_200_OK)


class StoringPDFView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = StoringPDF.objects.all()
    serializer_class = StoringPDFSerializer

    def get(self, request, *args, **kwargs):
        storing_pdf = StoringPDF.objects.all()
        storing_pdf_serializer = StoringPDFSerializer(storing_pdf, many=True)
        print("------storing_pdf-------"+str(storing_pdf))
        res = {
            'code': 1,
            'message': "Storing PDF",
            "result": storing_pdf_serializer.data
        }
        return Response(data=res, status=status.HTTP_200_OK)

    def post(self, request):
        storing_pdf_serializer = StoringPDFSerializer(data=request.data)
        print("storing_pdf_serializer---------"+str(storing_pdf_serializer))
        if storing_pdf_serializer.is_valid():
            storing_pdf = storing_pdf_serializer.save()
            print("-----------storing_pdf---------"+str(storing_pdf))
            resp2 = {
                "code": 1,
                "message": "Storing PDF",
                "result": storing_pdf_serializer.data
            }
            return Response(data=resp2, status=status.HTTP_200_OK)
