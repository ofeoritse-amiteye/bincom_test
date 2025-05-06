from django.shortcuts import render, redirect
from bincom_test import settings
from bincom_app.models import PollingUnit, AnnouncedPuResults, Party, Lga
from .forms import ResultForm
from django.utils import timezone
from django.db.models import Sum

# Create your views here.
def p1(request):
    records1 = PollingUnit.objects.all()
    if records1.exists():
        return render(request, 'p1.html', {'records1': records1})
    else:
        return render(request, 'p1.html', {'error': 'No record found'})
    
def results(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        records1 = PollingUnit.objects.all()
        records = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=id)
        if records.exists():
            return render(request, 'p1.html', {'records': records, 'records1':records1, 'id':id})
        else:
            return render(request, 'p1.html', {'error': 'No record found', 'records1':records1})
        
def get_client_ip(request):
    """Get client IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # client’s IP
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
        
def submit_result(request):
    if request.method == 'POST':
            results =AnnouncedPuResults()
            results.polling_unit_uniqueid = request.POST.get('polling_unit_id')
            results.party_abbreviation = request.POST.get('party_abbreviation')
            results.party_score = request.POST.get('party_score')
            results.entered_by_user = request.POST.get('entered_by')
            results.date_entered = timezone.now()
            results.user_ip_address = get_client_ip(request)
            results.save()
            return redirect('submit_result')
    else:
        records1 = PollingUnit.objects.all()
        party= Party.objects.all()
    return render(request, 'p3.html', {'records1': records1, 'party': party})



def page2(request):
    if request.method == 'POST':
        id = request.POST.get('polling_unit_id')
        records=Lga.objects.all()
        units = PollingUnit.objects.filter(lga_id=id).values_list('uniqueid', flat=True)
        results = (AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=units).values('party_abbreviation').annotate(total_score=Sum('party_score')))
        print(units)
        if results.exists():
            return render(request, 'p2.html', {'result': results, 'records': records,'id':id})
        else:
            return render(request, 'p2.html', {'error': 'No record found', 'records': records})
    records=Lga.objects.all()
    return render(request, 'p2.html',{'records': records})