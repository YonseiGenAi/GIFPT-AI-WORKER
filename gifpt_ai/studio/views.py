from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudioTask
from .tasks import process_pdf_task

class UploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        prompt = request.data.get("prompt")

        if not file or not prompt:
            return Response({"error": "file and prompt are required"}, status=400)

        task = StudioTask.objects.create(file=file, prompt=prompt)
        process_pdf_task.delay(task.id)

        return Response({"message": "Task created", "task_id": task.id}, status=201)
