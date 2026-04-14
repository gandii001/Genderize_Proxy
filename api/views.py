from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
import requests
from datetime import datetime, timezone


# Create your views here.

#@api_view(['GET'])
#def get_gender_data(request, pk=None):
    
    # Check if we already have this name in our cache
 #   cache_key = f"gender_result_{pk.strip().lower()}"
  #  cached_data = cache.get(cache_key)
   # if cached_data:
    #    return Response(cached_data)
    

    
    #if pk is None or pk.strip() == " ":
     #       return Response({"status":"error", "message": "Name parameter cannot be empty"}, status=400)
    
    # 422 Validation:this will check if the pk fails string checks (e.g., contains numbers)
    #if not pk.isalpha():
     #   return Response({ "status": "error", "message": "Name must contain only letters" }, status=422)


    #url = f"https://api.Genderize_Proxy.io/?name={pk.strip()}"
    #try:
     #   response = requests.get(url, timeout=0.5)
        
      #  response.raise_for_status() #to check for http response
       # content = response.json()

        #if content["gender"] == "null" or content["count"] == 0:
         #    return Response({ "status": "error", "message": "No prediction available for the provided name" }, status=422)


        #processed_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        #name = pk
        #gender = content["gender"]
        #sample_size = content["count"]
        #probability = content["probability"]
        #if probability >= 0.7 and sample_size >= 100:
         #   is_confident = True
        #else:
         #   is_confident = False
        #print(gender,sample_size,probability,is_confident)
       # "status": "success",
        #,
       
       # data ={
        #"status": "success",
        #"data": {
        #"name": pk,
        #"gender": gender,
        #"probability": probability,
        #"sample_size": sample_size,
        #"is_confident": is_confident,
        #"processed_at": processed_at
        
#}
#}
 #       return Response(data)
  #  except requests.RequestException:
   #     return Response({ "status": "error", "message": "Bad gateway" }, status=502)

   

class classify_data(APIView):
     def get(self, request):
        
        name = request.GET.get("name")
        # Validation for 400 error
        if not name or not name.strip():
            return Response({"status":"error", "message": "Name parameter cannot be empty"}, status=400)
        
        # 422 Validation:this will check if the pk fails string checks(asin contains only strings) (e.g., contains numbers)
        if not name.replace("-", "").replace("'", "").isalpha():
            return Response({ "status": "error", "message": "Name must contain only letters" }, status=422)
        
        # checks for cached data
        cache_key = f"gender_result_{name.lower()}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)
        
        
        
        url = f"https://api.genderize.io/?name={name}"
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            content = response.json()

            if content.get("gender") == None or content.get("count") == 0:
             return Response({ "status": "error", "message": "No prediction available for the provided name" }, status=422)
            

            # Data Processing
            processed_data = self.format_response(name, content)
            
            # Save to cache for 24 hours(86400s)
            cache.set(cache_key, processed_data, 3)

            # Return the data
            return Response(processed_data)
        

        except requests.Timeout:
            return Response({"status": "error", "message": "External API timed out"}, status=504)
        except requests.RequestException:
            return Response({"status": "error", "message": "Bad gateway"}, status=502)
         
             
     def format_response(self, name, content ):
        processed_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        probability = content.get("probability")
        sample_size = content.get("count")

        if probability >= 0.7 and sample_size >= 100:
            is_confident = True
        else:
            is_confident = False

            
        data ={
            "status": "success",
            "data": {
            "name": name,
            "gender": content.get("gender"),
            "probability": probability,
            "sample_size":sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        
}
}
        return data
        
         
     

     
