from datetime import date
from fractions import Fraction


def calculate_days_with_payments(contract_duration, first_year_of_cost_reduction,
                                 days_per_year, npv_calculation_duration):
    """
    # Determine the number of days of the period with payments in favor of the participant
    """
    first_period_duration = min(contract_duration, first_year_of_cost_reduction)
    full_periods_count, last_period_duration = divmod(contract_duration - first_period_duration, days_per_year)
    return [first_period_duration] + [days_per_year] * full_periods_count + \
           [last_period_duration] + [0] * (npv_calculation_duration + 1 - full_periods_count - 2)


def calculate_days_for_discount_rate(days_per_year, announcement_date, npv_calculation_duration):
    """
    # Number of days of the period to calculate the discount rate
    :rtype list('int') (21 element)
    """
    days_for_discount_rate = [(date(announcement_date.year, 12, 31) - announcement_date).days] + \
                             [days_per_year] * npv_calculation_duration
    days_for_discount_rate = days_for_discount_rate[:-1]
    days_for_discount_rate.append(days_per_year - days_for_discount_rate[0])
    return days_for_discount_rate


def calculate_contract_price(annual_costs_reduction, yearly_payments_percentage,
                             days_with_payments, days_for_discount_rate):
    contract_prices = []
    for i in range(len(annual_costs_reduction)):
        contract_prices.append(Fraction(str(yearly_payments_percentage)) * Fraction(str(annual_costs_reduction[i]))
                               * Fraction(days_with_payments[i], days_for_discount_rate[i]))
    return contract_prices


def calculate_amount_performance(contract_duration_years, contract_duration_days,
                                 yearly_payments_percentage, annual_costs_reduction,
                                 announcement_date, nbu_discount_rate,
                                 days_per_year=365, npv_calculation_duration=20):
    """
       # Calculate npv
      :param contract_duration_years: Contract term (year)
      :param contract_duration_days: Contract term (days)
      :param yearly_payments_percentage: Fixed percentage of payments
      :param annual_costs_reduction: Reduce customer costs
      :param announcement_date: Date of the announcement
      :param nbu_discount_rate: NBU discount rate
      :param days_per_year: Days in year
      :param npv_calculation_duration: Periods
      :type contract_duration_years: int
      :type contract_duration_days: int
      :type yearly_payments_percentage: float
      :type annual_costs_reduction: list (21 element)
      :type announcement_date: datetime.date
      :type nbu_discount_rate: float
      :type days_per_year: int
      :type npv_calculation_duration: int
      :return: number of total discounted income (npv)
      :rtype: fractions.Fraction
    """
    days_for_discount_rate = calculate_days_for_discount_rate(days_per_year, announcement_date,
                                                              npv_calculation_duration)
    days_with_payments = calculate_days_with_payments(
        contract_duration_years * days_per_year + contract_duration_days,
        days_for_discount_rate[0], days_per_year, npv_calculation_duration
    )

    contract_prices = calculate_contract_price(annual_costs_reduction, yearly_payments_percentage,
                                               days_with_payments, days_for_discount_rate)

    discount_coefficient = []
    coefficient = 1
    for i in days_for_discount_rate:
        coefficient = Fraction(coefficient, (1 + Fraction(str(nbu_discount_rate)) * Fraction(i, days_per_year)))
        discount_coefficient.append(coefficient)

    discounted_income = []
    for i, k in enumerate(annual_costs_reduction):
        if i != npv_calculation_duration:
            discounted_income.append(discount_coefficient[i] * (Fraction(str(k)) * Fraction(days_for_discount_rate[i],
                                     days_for_discount_rate[i]) - contract_prices[i]))
        else:
            discounted_income.append(discount_coefficient[i] * (Fraction(str(k)) * Fraction(days_for_discount_rate[i],
                                     days_per_year) - contract_prices[i]))
    return sum(discounted_income)


def calculate_total_contract_price(contract_duration_years, contract_duration_days,
                                   yearly_payments_percentage, annual_costs_reduction, announcement_date,
                                   days_per_year=365, npv_calculation_duration=20):
    """
     # Calculate total contract price
    :param contract_duration_years: Contract term (year)
    :param contract_duration_days: Contract term (days)
    :param yearly_payments_percentage: Fixed percentage of payments
    :param annual_costs_reduction: Reduce customer costs
    :param announcement_date: Date of the announcement
    :param days_per_year: Days in year
    :param npv_calculation_duration: Periods
    :type contract_duration_years: int
    :type contract_duration_days: int
    :type yearly_payments_percentage: float
    :type annual_costs_reduction: list (21 element)
    :type announcement_date: datetime.date
    :type days_per_year: int
    :type npv_calculation_duration: int
    :return: number of total contract price
    :rtype: fractions.Fraction
    """
    days_for_discount_rate = calculate_days_for_discount_rate(days_per_year, announcement_date, npv_calculation_duration)

    days_with_payments = calculate_days_with_payments(
        contract_duration_years * days_per_year + contract_duration_days,
        days_for_discount_rate[0], days_per_year, npv_calculation_duration
    )

    contract_prices = calculate_contract_price(annual_costs_reduction, yearly_payments_percentage, days_with_payments,
                                               days_for_discount_rate)
    return sum(contract_prices)
