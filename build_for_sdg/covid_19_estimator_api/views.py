from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, renderers
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .serializers import *
from rest_framework.response import Response
from .models import Logs
from datetime import datetime


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)


def estimator_covid(data):
    """

  :param data:
  :return:

  """
    reported_cases = data.get("reportedCases", 0)

    # challenge one
    best_case_currently_infected = reported_cases * 10
    worst_case_currently_infected = reported_cases * 50
    days = data.get("timeToElapse", 0)
    period_type = data.get("periodType", "days")

    if period_type == "weeks":
        days = int(days) * 7
    elif period_type == "months":
        days = int(days) * 30  # should be 30.5 but the instruction was that all decimal part should be discarded

    factor = int(days) // 3
    best_case_infections_by_requested_time = best_case_currently_infected * (2 ** factor)
    worst_case_infections_by_requested_time = worst_case_currently_infected * (2 ** factor)

    # challenge two
    best_case_severe_cases_by_requested_time = best_case_infections_by_requested_time * (15 / 100)
    worst_case_severe_cases_by_requested_time = worst_case_infections_by_requested_time * (15 / 100)

    total_hospital_beds = data.get("totalHospitalBeds")
    available_beds = (35 / 100) * total_hospital_beds
    best_case_hospital_beds_by_requested_time = available_beds - best_case_severe_cases_by_requested_time
    worst_case_hospital_beds_by_requested_time = available_beds - worst_case_severe_cases_by_requested_time

    # challenge three
    best_case_cases_for_icu_by_request_time = (5 / 100) * best_case_infections_by_requested_time
    worst_case_cases_for_icu_by_request_time = (5 / 100) * worst_case_infections_by_requested_time

    best_case_cases_for_ventilators_by_request_time = (2 / 100) * best_case_infections_by_requested_time
    worst_case_cases_for_ventilators_by_request_time = (2 / 100) * worst_case_infections_by_requested_time

    avg_daily_income_population = data.get("region").get("avgDailyIncomePopulation")
    print(avg_daily_income_population)
    avg_daily_income_in_usd = data.get("region").get("avgDailyIncomeInUSD")
    print(avg_daily_income_in_usd)

    best_case_dollars_in_flight = (
                                          best_case_infections_by_requested_time * avg_daily_income_population * avg_daily_income_in_usd) / days

    worst_case_dollars_in_flight = (
                                           worst_case_infections_by_requested_time * avg_daily_income_population * avg_daily_income_in_usd) / days

    output = {"data": data,

              "impact": {"currentlyInfected": int(best_case_currently_infected),
                         "infectionsByRequestedTime": int(best_case_infections_by_requested_time),
                         "severeCasesByRequestedTime": int(best_case_severe_cases_by_requested_time),
                         "hospitalBedsByRequestedTime": int(best_case_hospital_beds_by_requested_time),
                         "casesForICUByRequestedTime": int(best_case_cases_for_icu_by_request_time),
                         "casesForVentilatorsByRequestedTime": int(best_case_cases_for_ventilators_by_request_time),
                         "dollarsInFlight": int(best_case_dollars_in_flight)},

              "severeImpact": {"currentlyInfected": int(worst_case_currently_infected),
                               "infectionsByRequestedTime": int(worst_case_infections_by_requested_time),
                               "severeCasesByRequestedTime": int(worst_case_severe_cases_by_requested_time),
                               "hospitalBedsByRequestedTime": int(worst_case_hospital_beds_by_requested_time),
                               "casesForICUByRequestedTime": int(worst_case_cases_for_icu_by_request_time),
                               "casesForVentilatorsByRequestedTime": int(
                                   worst_case_cases_for_ventilators_by_request_time),
                               "dollarsInFlight": int(worst_case_dollars_in_flight)}
              }
    # json_output = json.dumps(output)

    return output


@api_view(['POST'])
@csrf_exempt
def estimator(request):
    """
    Returns an covid-19 impact estimate based on the input
    :param request:
    :return:
    """
    start = datetime.now()
    if request.method == "POST":
        print(request.data, "===========3333333333333=====")
        serialized_input_data = CovidSerializers(data=request.data)
        if serialized_input_data.is_valid():
            print(serialized_input_data.data, "ssssssf;;;;;;;;;;;;;;;;;;")
            output_data = estimator_covid(serialized_input_data.data)
            print(output_data, "Output DATA============")
            serialized_output_data = CovidSerializersResponse(data=output_data)
            print(serialized_output_data, "serialized output data==========")
            if serialized_output_data.is_valid():
                stop = datetime.now()
                execution_time = round((stop - start).total_seconds() * 1000)
                log = Logs(logs=f'{request.method} /api/v1/on-covid-19 200 {execution_time}ms').save()
                return Response(serialized_output_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_input_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
@renderer_classes([XMLRenderer])
def estimator_xml(request):
    """
    Returns an covid-19 impact estimate based on the input
    :param request:
    :return:
    """
    start = datetime.now()
    print(request.data, "===========3333333333333=====")
    serialized_input_data = CovidSerializers(data=request.data)
    if serialized_input_data.is_valid():
        print(serialized_input_data.data, "ssssssf;;;;;;;;;;;;;;;;;;")
        output_data = estimator_covid(serialized_input_data.data)
        print(output_data, "Output DATA============")
        serialized_output_data = CovidSerializersResponse(data=output_data)
        print(serialized_output_data, "serialized output data==========")
        if serialized_output_data.is_valid():
            stop = datetime.now()
            execution_time = round((stop - start).total_seconds() * 1000)
            log = Logs(logs=f'{request.method} /api/v1/on-covid-19 200 {execution_time}ms').save()
            return Response(serialized_output_data.data, status=status.HTTP_201_CREATED, content_type="application/xml")
    return Response(serialized_input_data.errors, status=status.HTTP_400_BAD_REQUEST, content_type="xml")


@api_view(['GET'])
@csrf_exempt
@renderer_classes([PlainTextRenderer])
def logs_text(request):
    start = datetime.now()
    stop = datetime.now()
    execution_time = round((stop - start).total_seconds() * 1000)
    log = Logs(logs=f'{request.method} /api/v1/on-covid-19 200 {int(execution_time)}ms').save()
    logs = Logs.objects.all()
    output = ""
    for l in logs:
        output += f'{l.logs} \n'

    return Response(output, status=status.HTTP_200_OK, content_type="application/text")
