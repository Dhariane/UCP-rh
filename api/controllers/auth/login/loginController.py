from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.auth.login.loginModel import Login
from api.services.auth.login.loginService import LoginService
from api.dto.auth.login.loginDto import LoginDTO

class LoginController(APIView):
    
    def get(self, request, id=None):
        if id:
            try:
                data = LoginService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Login retrieved successfully",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Login.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Login not found for id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = LoginService.getAllDto().data
            response = {
                "status": "success",
                "message": "List of Logins retrieved successfully",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        # Utilisation du DTO pour valider les données entrantes (email, role)
        # Note: Le mot de passe sera généré dans le service
        serializer = LoginDTO(data=request.data)
        
        if not serializer.is_valid():
            errors_list = [f"{field}: {error}" for field, field_errors in serializer.errors.items() for error in field_errors]
            errors_str = "; ".join(errors_list)
            
            response = {
                "status": "error",
                "message": errors_str,
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Appel au service pour la création (incluant la génération de mdp et le hachage)
        login_obj = LoginService.create(
            serializer.validated_data['email'], # L'objet Personnelle
            
        )
        
        response = {
            "status": "success",
            "message": "Login created successfully",
            "data": LoginDTO(login_obj).data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        serializer = LoginDTO(data=request.data)
        
        if not serializer.is_valid():
            errors_list = [f"{field}: {error}" for field, field_errors in serializer.errors.items() for error in field_errors]
            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            login_obj = LoginService.update(
                id=id,
                email_id=serializer.validated_data['email'],
                role=serializer.validated_data['role']
            )
            response = {
                "status": "success",
                "message": "Login updated successfully",
                "data": LoginDTO(login_obj).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Login.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Login not found for id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)