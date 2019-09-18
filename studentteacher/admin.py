from django.contrib import admin
from studentteacher.models import User,Assignment,Submission,AssignRequest,Review,Message
# Register your models here.

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(AssignRequest)
admin.site.register(Review)
admin.site.register(Message)

