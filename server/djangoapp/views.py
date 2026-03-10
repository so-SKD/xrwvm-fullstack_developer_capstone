from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
import logging
import json
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate
from django.contrib.auth.models import User  # Import User model


# Get an instance of a logger
logger = logging.getLogger(__name__)


# User Registration View
@csrf_exempt
def register_user(request):
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        # Check if user already exists
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username,
             "error": "Already Registered"}
        )
    except User.DoesNotExist:
        # If not, simply log this is a new user
        logger.debug(f"{username} is a new user")

    # Create user in auth_user table
    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name,
        password=password, email=email
    )
    # Login the user
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# User Login View
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
        else:
            return JsonResponse({
                "userName": username,
                "status": "Invalid credentials"
            })

    return JsonResponse({"error": "POST request required"})


# User Logout View
def logout_request(request):
    logout(request)  # Terminate user session
    return JsonResponse({"userName": ""})  # Return empty username


# Update the `get_dealerships` render list of dealerships
def get_dealerships(request, state="All"):
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Get Cars View
def get_cars(request):
    logger.debug("Entering get_cars view")

    # Initialize data only if there are no CarMakes
    if CarMake.objects.count() == 0:
        logger.info("No car makes found, initiating data population.")
        initiate()

    # Fetch car models
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
        "CarModel": car_model.name, 
        "CarMake": car_model.car_make.name
        } 
        for car_model in car_models
    ]


    logger.debug(f"Retrieved {len(cars)} car models.")
    return JsonResponse({"CarModels": cars})


# Get Dealer Reviews View
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', "neutral")

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Get Dealer Details View
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Add Review View
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )

    return JsonResponse(
        {"status": 403, "message": "Unauthorized"}
    )
