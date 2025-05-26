import unittest

from evdutyapi.max_charging_current.max_charging_current_request import MaxChargingCurrentRequest
from ..terminals.terminal_response_builder import TerminalResponseBuilder


class MaxChargingCurrentRequestTest(unittest.TestCase):

    def test_from_terminal_response_removing_unmodifiable_fields(self):
        response = TerminalResponseBuilder.default().with_cost_local(None).build()

        request = MaxChargingCurrentRequest.from_terminal_response(response, 10)

        self.assertEqual('cost' in request, False)
        self.assertEqual('alternateCost' in request, False)
        self.assertEqual('sessionTimeLimits' in request, False)
        self.assertEqual('costLocal' in request, False)
        self.assertEqual(request['chargingProfile']['chargingRate'], 10)
        self.assertEqual(request['chargingProfile']['chargingRateUnit'], 'A')

    def test_from_terminal_response_keeping_cost_local_when_set(self):
        response = TerminalResponseBuilder.default().with_cost_local(0.1034).build()

        request = MaxChargingCurrentRequest.from_terminal_response(response, 10)

        self.assertEqual(request['costLocal'], 0.1034)
