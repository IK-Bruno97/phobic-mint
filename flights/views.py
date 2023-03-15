from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from .models import Flight, Passenger, Airport


# Create your views here.
def handler_404(request, exception):
    template = loader.get_template('post_404.html')
    return HttpResponse(template.render({'exception': exception}, request), status=404)

def index(request):
    return render(request, 'index.html', {"flights": Flight.objects.all()})

def flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    #flight = Flight.objects.get(pk=flight_id)
    return render(request, 'flight.html', {"flight": flight, 
                                           "passengers": flight.passengers.all(),
                                           "non_passengers": Passenger.objects.exclude(flights=flight).all()
                                })

def book(request, flight_id):

    if request.method == 'POST':
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight.id)))
