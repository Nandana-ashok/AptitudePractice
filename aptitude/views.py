from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from aptitude.serializers import AptitudeSerializer,AptitudeSubmissionSerializer
from rest_framework.response import Response
from aptitude.models import AptitudeQuestion,AptitudeSubmission

# Create your views here.

class AptitudeQuestionCreateListView(APIView):

    def get(self,request):

        qs = AptitudeQuestion.objects.all().values()
        serializer_instance = AptitudeSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    
    def post(self,request):

        form_data = request.data
        serializer_instance = AptitudeSerializer(data=form_data)

        if serializer_instance.is_valid():

            actual_data = serializer_instance.validated_data
            AptitudeQuestion.objects.create(**actual_data)
            return Response({"Message":"Aptitude question added successfully..."})
        else:
            return Response(data=serializer_instance.errors)


class AptitudeRetrievalUpdateDeleteView(APIView):

    def get(self,request,pk):

        question = get_object_or_404(AptitudeQuestion,id=pk)

        serializer = AptitudeSerializer(question)  
        return Response(data=serializer.data)

    def put(self,request,pk):

        form_data = request.data

        serializer = AptitudeSerializer(data=form_data)

        if serializer.is_valid():
            
            actual_data = serializer.validated_data
            qs = AptitudeQuestion.objects.filter(id=pk).update(**actual_data)
            return Response(data=serializer.data)
        else:
            return Response({"errors":serializer.errors})

    def delete(self,request,pk):

        qs =AptitudeQuestion.objects.filter(id=pk).delete()
        return Response({"Message":"Question deleted succssfully..."})

class AptitudeSubmissionCreateListView(APIView):

    def get(self, request):
        submissions = AptitudeSubmission.objects.all()

        serializer = AptitudeSubmissionSerializer(submissions, many=True )

        return Response(serializer.data)

    def post(self, request):
        serializer = AptitudeSubmissionSerializer(
            data=request.data
        )

        if serializer.is_valid():
            AptitudeSubmission.objects.create(
                **serializer.validated_data
            )

            return Response({
                "message": "Answer submitted successfully"
            })

        return Response({
            "errors": serializer.errors
        })


class AptitudeSubmissionRetrieveUpdateDeleteView(APIView):

    def get(self, request, id):
        submission = get_object_or_404(
            AptitudeSubmission,
            id=id
        )

        serializer = AptitudeSubmissionSerializer(submission)

        return Response(serializer.data)

    def put(self, request, id):
        submission = get_object_or_404(
            AptitudeSubmission,
            id=id
        )

        serializer = AptitudeSubmissionSerializer(
            data=request.data
        )

        if serializer.is_valid():
            AptitudeSubmission.objects.filter(
                id=id
            ).update(**serializer.validated_data)

            updated_submission = AptitudeSubmission.objects.get(
                id=id
            )

            response_serializer = AptitudeSubmissionSerializer(
                updated_submission
            )

            return Response(response_serializer.data)

        return Response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        submission = get_object_or_404(
            AptitudeSubmission,
            id=id
        )

        submission.delete()

        return Response({
            "message": "Submission deleted successfully"
        })