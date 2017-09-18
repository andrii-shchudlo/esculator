import unittest
from copy import deepcopy
<<<<<<< HEAD
from esculator.npv_calculation import (
    calculate_amount_performance,
    calculate_total_contract_price,
)
from esculator.tests.npv_test_data import (
    CONTRACT_DURATION_CHANGING,
    ANNOUNCEMENT_DATE_CHANGING,
    PAYMENTS_PERCENTAGE_CHANGING,
)


class NPVCalculationTest(unittest.TestCase):
    """ NPV Calculation Test
        based on data from https://docs.google.com/spreadsheets/d/1kOz6bxob4Nmb0Es_W0TmbNznoYDcnwAKcSgxfPEXYGQ/edit#gid=1469973930
    """

    def test_contract_duration_change(self):
        test_data = deepcopy(CONTRACT_DURATION_CHANGING)
        contract_durations = test_data.pop('contractDuration')

        for i, contract_duration in enumerate(contract_durations):

            amount_perfomance = calculate_amount_performance(
                contract_duration['years'],
                contract_duration['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(amount_perfomance),
                _str(test_data['calculated'][i]['amountPerformance'])
            )

            amount_contract = calculate_total_contract_price(
                contract_duration['years'],
                contract_duration['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
            )
            self.assertEqual(
                _str(amount_contract),
                _str(test_data['calculated'][i]['amountContract'])
            )

    def test_announcement_date_change(self):
        test_data = deepcopy(ANNOUNCEMENT_DATE_CHANGING)
        announcement_dates = test_data.pop('announcementDate')

        for i, announcement_date in enumerate(announcement_dates):

            amount_perfomance = calculate_amount_performance(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                announcement_date,
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(amount_perfomance),
                _str(test_data['calculated'][i]['amountPerformance'])
            )

            amount_contract = calculate_total_contract_price(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                announcement_date,
            )
            self.assertEqual(
                _str(amount_contract),
                _str(test_data['calculated'][i]['amountContract'])
            )

    def test_payments_percentage_change(self):
        test_data = deepcopy(PAYMENTS_PERCENTAGE_CHANGING)
        payments_percentages = test_data.pop('yearlyPaymentsPercentage')

        for i, payments_percentage in enumerate(payments_percentages):

            amount_perfomance = calculate_amount_performance(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                payments_percentage,
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(amount_perfomance),
                _str(test_data['calculated'][i]['amountPerformance'])
            )

            amount_contract = calculate_total_contract_price(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                payments_percentage,
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
            )
            self.assertEqual(
                _str(amount_contract),
                _str(test_data['calculated'][i]['amountContract'])
            )


def _str(number, precision=11):
    if number.__class__.__name__ == 'Fraction':
        number = float(number)
    return '{:.{}f}'.format(number, precision)
=======
from fractions import Fraction
from esculator import npv, escp
from esculator.tests.data import (
    CONTRACT_DURATION, ANNOUNCEMENT_DATE, PAYMENTS_PERCENTAGE, BASE_BID,
)

class TestCalculationsMixin(object):
    __test__ = False  # nosetests directive

    def test_calculations(self):
        for i, val in enumerate(self.test_data['input']):
            self.bid[self.field_name] = val

            amount_perfomance = npv(
                self.bid['contractDuration']['years'],
                self.bid['contractDuration']['days'],
                self.bid['yearlyPaymentsPercentage'],
                self.bid['annualCostsReduction'],
                self.bid['announcementDate'],
                self.bid['NBUdiscountRate'],
            )

            self.assertTrue(isinstance(amount_perfomance, Fraction))

            expected = self.test_data['expected_results'][i]['amountPerformance']
            self.assertEqual(humanize(amount_perfomance), expected)

            amount_contract = escp(
                self.bid['contractDuration']['years'],
                self.bid['contractDuration']['days'],
                self.bid['yearlyPaymentsPercentage'],
                self.bid['annualCostsReduction'],
                self.bid['announcementDate'],
            )

            self.assertTrue(isinstance(amount_contract, Fraction))

            expected = self.test_data['expected_results'][i]['amountContract']
            self.assertEqual(humanize(amount_contract), expected)


class ContractDurationTest(TestCalculationsMixin, unittest.TestCase):
    __test__ = True
    field_name = 'contractDuration'
    test_data = CONTRACT_DURATION
    bid = deepcopy(BASE_BID)


class YearlyPaymentsPercentageTest(TestCalculationsMixin, unittest.TestCase):
    __test__ = True
    field_name = 'yearlyPaymentsPercentage'
    test_data = PAYMENTS_PERCENTAGE
    bid = deepcopy(BASE_BID)


class AnnouncementDateTest(TestCalculationsMixin, unittest.TestCase):
    __test__ = True
    field_name = 'announcementDate'
    test_data = ANNOUNCEMENT_DATE
    bid = deepcopy(BASE_BID)


def humanize(value, precision=11):
    value = float(value)
    return '{:.{}f}'.format(value, precision)
>>>>>>> 3602c84808252d01cea58cd7d0bbaf83f590dcf2


def suite():
    suite = unittest.TestSuite()
<<<<<<< HEAD
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
=======
    suite.addTest(unittest.makeSuite(ContractDurationTest))
>>>>>>> 3602c84808252d01cea58cd7d0bbaf83f590dcf2
    return suite


if __name__ == '__main__':
<<<<<<< HEAD
    unittest.main(defaultTest='suite')
=======
    unittest.main(defaultTest='suite')
>>>>>>> 3602c84808252d01cea58cd7d0bbaf83f590dcf2
