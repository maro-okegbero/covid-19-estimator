""""
estimator.py

@Author: Maro Okegbero
@Date: April 8, 2020
"""
import json


def estimator(data):
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
        days = days * 7
    elif period_type == "months":
        days = days * 30  # should be 30.5 but the instruction was that all decimal part should be discarded

    factor = days // 3
    best_case_infections_by_requested_time = best_case_currently_infected * (2 ** factor)
    worst_case_infections_by_requested_time = worst_case_currently_infected * (2 ** factor)

    # challenge two
    best_case_severe_cases_by_requested_time = best_case_infections_by_requested_time * (15 / 100)
    worst_case_severe_cases_by_requested_time = worst_case_infections_by_requested_time * (15 / 100)

    total_hospital_beds = data.get("totalHospitalBeds", 0)
    available_beds = (35 / 100) * total_hospital_beds
    best_case_hospital_beds_by_requested_time = available_beds - best_case_severe_cases_by_requested_time
    worst_case_hospital_beds_by_requested_time = available_beds - worst_case_severe_cases_by_requested_time

    # challenge three
    best_case_cases_for_icu_by_request_time = (5 / 100) * best_case_infections_by_requested_time
    worst_case_cases_for_icu_by_request_time = (5 / 100) * worst_case_infections_by_requested_time

    best_case_cases_for_ventilators_by_request_time = (2 / 100) * best_case_infections_by_requested_time
    worst_case_cases_for_ventilators_by_request_time = (2 / 100) * worst_case_infections_by_requested_time

    avg_daily_income_population = data.get("avgDailyIncomePopulation", 0)
    avg_daily_income_in_usd = data.get("avgDailyIncomeInUSD", 0)

    best_case_dollars_in_flight = int(best_case_infections_by_requested_time *
                                      avg_daily_income_population * avg_daily_income_in_usd * days)

    worst_case_dollars_in_flight = int(worst_case_infections_by_requested_time *
                                       avg_daily_income_population * avg_daily_income_in_usd * days)

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
                               "casesForVentilatorsByRequestedTime": worst_case_cases_for_ventilators_by_request_time,
                               "dollarsInFlight": worst_case_dollars_in_flight}
              }
    # json_output = json.dumps(output)

    return output
