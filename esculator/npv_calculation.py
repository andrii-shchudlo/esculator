from datetime import date
from fractions import Fraction


def calculate_days_with_payments(contract_duration, days_with_cost_reduction,
                                 days_per_year, npv_calculation_duration):

    first_period_duration = min(contract_duration, days_with_cost_reduction[0])
    full_periods_count, last_period_duration = divmod(contract_duration - first_period_duration, days_per_year)
    return [first_period_duration] + [days_per_year] * full_periods_count + \
           [last_period_duration] + [0] * (npv_calculation_duration + 1 - full_periods_count - 2)


def calculate_amount_contract_and_npv(contract_duration_years, contract_duration_days, yearly_payments_percentage,
                                      annual_costs_reduction, announcement_date, nbu_discount_rate,
                                      days_per_year=365, npv_calculation_duration=20):

    days_with_cost_reduction = [(date(announcement_date.year, 12, 31) - announcement_date).days] \
                               + [days_per_year] * npv_calculation_duration

    days_for_discount_rate = days_with_cost_reduction[:-1]
    days_for_discount_rate.append(days_per_year - days_for_discount_rate[0])

    discount_coefficient = []
    coefficient = 1
    for i in days_for_discount_rate:
        coefficient = Fraction(coefficient, (1 + Fraction(str(nbu_discount_rate)) * Fraction(i, days_per_year)))
        discount_coefficient.append(coefficient)

    days_with_payments = calculate_days_with_payments(
        contract_duration_years * days_per_year + contract_duration_days,
        days_for_discount_rate, days_per_year, npv_calculation_duration
    )

    contract = []
    for i, _ in enumerate(annual_costs_reduction):
        contract.append(Fraction(str(yearly_payments_percentage)) * Fraction(str(annual_costs_reduction[i]))
                        * Fraction(days_with_payments[i], days_for_discount_rate[i]))

    discounted_income = []
    for i, k in enumerate(annual_costs_reduction):
        discounted_income.append(discount_coefficient[i] * (Fraction(str(k)) * Fraction(days_for_discount_rate[i],
                                 days_with_cost_reduction[i]) - contract[i]))
    return sum(contract), sum(discounted_income)
