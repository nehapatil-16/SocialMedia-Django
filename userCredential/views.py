# from django.shortcuts import render
# from userCredential.models import UserCredential

# # Create your views here.
# def registration_requests(request):
#     # Retrieve registration requests pending approval
#     registration_requests = UserCredential.objects.filter(is_approved=False)

#     return render(request, 'registration_requests.html', {'registration_requests': registration_requests})

# def approve_registration(request, user_id):
#     user = UserCredential.objects.get(pk=user_id)
#     user.is_approved = True
#     user.save()
#     # Redirect or add a success message

# def reject_registration(request, user_id):
#     user = UserCredential.objects.get(pk=user_id)
#     user.delete()  # Or mark as rejected, depending on your requirements
#     # Redirect or add a success message

