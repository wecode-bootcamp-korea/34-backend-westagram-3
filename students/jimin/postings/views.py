import json

from django.http        import JsonResponse
from django.views       import View
from core.utils         import login_decorator       

from users.models       import User
from postings.models    import Posting,Comment,Like
# Create your views here.

class PostingView(View) :
 @login_decorator
 def post(self,request):
    try:
         data = json.loads(request.body)
        
         Posting.objects.create(
             user    = request.user,
             img_url = data['img_url'],
             post    = data['post'],
             
         )
         return JsonResponse({"message":"SUCCESS"},status = 201)
    except KeyError:
         return JsonResponse({"message":"KEY_ERROR"},status=400)
 def get(self, request):
         return JsonResponse({'results':list( Posting.objects.values())},status=200)
    
class CommentView(View):  
     @login_decorator
     def post(self,request):
      try:
         data = json.loads(request.body)
         
         if not Posting.objects.filter(id = data['post_id']).exists():
                return JsonResponse({"MESSAGE":"NO_POST"}, status=400)
         
         Comment.objects.create(
             user    = request.user,
             post_id = data['post_id'],
             comment = data['comment'],
         )
         return JsonResponse({"message":"SUCCESS"})
      except KeyError:
         return JsonResponse({"message":"KEY_ERROR"},status=400)  
     
     def get(self, request):
        return JsonResponse({'comment_list':list( Comment.objects.filter('post_id'))},status=200)
    
class LikeView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            user    = request.user
            post_id = data.get('post_id',None)
            
            count = Like.objects.filter(post_id=post_id).count()
            
            if Like.objects.filter(user=user, post_id=post_id).exists() :
    
                Like.objects.filter(user=user, post_id=post_id).delete()
 
                return JsonResponse({'message':'LIKE_DELETE', 'likes' : count-1 }, status=200)

            Like.objects.create(
             user       = user,
             post_id    = post_id,
             
         )
            return JsonResponse({"message":"SUCCESS"})
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
        
    def get(self, request):
        return JsonResponse({'likes':list( Like.objects.values())},status=200)