import unittest
from copy import deepcopy
from esculator.npv_calculation import (
    calculate_amount_contract_and_npv,
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
            amount_contract, npv = calculate_amount_contract_and_npv(
                contract_duration['years'],
                contract_duration['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(npv),
                _str(test_data['calculated'][i]['amountPerformance'])
            )

    def test_announcement_date_change(self):
        test_data = deepcopy(ANNOUNCEMENT_DATE_CHANGING)
        announcement_dates = test_data.pop('announcementDate')

        for i, announcement_date in enumerate(announcement_dates):

            amount_contract, npv = calculate_amount_contract_and_npv(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                test_data['yearlyPaymentsPercentage'],
                test_data['annualCostsReduction'],
                announcement_date,
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(npv),
                _str(test_data['calculated'][i]['amountPerformance'])
            )

    def test_payments_percentage_change(self):
        test_data = deepcopy(PAYMENTS_PERCENTAGE_CHANGING)
        payments_percentages = test_data.pop('yearlyPaymentsPercentage')

        for i, payments_percentage in enumerate(payments_percentages):

            amount_contract, npv = calculate_amount_contract_and_npv(
                test_data['contractDuration']['years'],
                test_data['contractDuration']['days'],
                payments_percentage,
                test_data['annualCostsReduction'],
                test_data['announcementDate'],
                test_data['NBUdiscountRate'],
            )
            self.assertEqual(
                _str(npv),
                _str(test_data['calculated'][i]['amountPerformance'])
            )


def _str(number, precision=11):
    if number.__class__.__name__ == 'Fraction':
        number = float(number)
    return '{:.{}f}'.format(number, precision)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
