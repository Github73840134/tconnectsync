#!/usr/bin/env python3

import json
import unittest

from tconnectsync.eventparser.generic import Event
from tconnectsync.eventparser import events as eventtypes
from tconnectsync.eventparser.raw_event import RawEvent


class TestLidBgReadingTaken(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        # Real captured LID_BG_READING_TAKEN (eventCode 16) events, copied
        # verbatim. The two fixtures differ only in bgEntryType.
        self.fixtureManualEntry = {
            "deviceAssignmentId": "4ff6bebc-d4d6-4423-b123-eecfcf5a4238",
            "eventCode": 16,
            "sequenceGroup": 0,
            "sequenceNumber": 456822,
            "pumpDateTime": "2026-05-18T10:15:14",
            "eventProperties": {
                "bg": 151, "cgmCalibration": 0, "bgEntryType": 0,
                "iob": 1.1809407, "targetBg": 110, "isf": 30,
                "selectedIob": 1, "bgSourceType": 1,
            },
            "estimatedDateTime": "2026-05-18T10:15:14Z",
        }
        self.fixtureAutoPopulated = {
            "deviceAssignmentId": "4ff6bebc-d4d6-4423-b123-eecfcf5a4238",
            "eventCode": 16,
            "sequenceGroup": 0,
            "sequenceNumber": 394632,
            "pumpDateTime": "2026-04-30T11:57:36",
            "eventProperties": {
                "bg": 164, "cgmCalibration": 0, "bgEntryType": 1,
                "iob": 1.8189592, "targetBg": 110, "isf": 30,
                "selectedIob": 1, "bgSourceType": 1,
            },
            "estimatedDateTime": "2026-04-30T11:57:36Z",
        }

    def test_dispatches_to_correct_class(self):
        ev = Event(self.fixtureManualEntry)
        self.assertIsInstance(ev, eventtypes.LidBgReadingTaken)
        self.assertNotIsInstance(ev, RawEvent)

    def test_envelope_fields(self):
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.eventId, 16)
        self.assertEqual(ev.seqNum, 456822)

    def test_timestamp_preserves_wall_clock(self):
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.eventTimestamp.format('YYYY-MM-DDTHH:mm:ss'),
                         "2026-05-18T10:15:14")

    def test_bg_iob_targetbg_isf_round_trip(self):
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.BG, 151)
        self.assertAlmostEqual(ev.IOB, 1.1809407)
        self.assertEqual(ev.targetbg, 110)
        self.assertEqual(ev.ISF, 30)

        ev2 = Event(self.fixtureAutoPopulated)
        self.assertEqual(ev2.BG, 164)
        self.assertAlmostEqual(ev2.IOB, 1.8189592)
        self.assertEqual(ev2.targetbg, 110)
        self.assertEqual(ev2.ISF, 30)

    def test_selectediob_enum_resolves(self):
        # selectedIob:1 -> SwanIobMeal
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.selectediobRaw, 1)
        self.assertEqual(ev.selectediob,
                         eventtypes.LidBgReadingTaken.SelectediobEnum.SwanIobMeal)

    def test_bgentrytype_enum_resolves(self):
        # bgEntryType:0 -> ManualEntryByTheUserViaNumpad (0 not treated as missing)
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.bgentrytypeRaw, 0)
        self.assertEqual(
            ev.bgentrytype,
            eventtypes.LidBgReadingTaken.BgentrytypeEnum.ManualEntryByTheUserViaNumpad)

        # bgEntryType:1 -> AutoPopulatedBgUsingDexcomEgv
        ev2 = Event(self.fixtureAutoPopulated)
        self.assertEqual(ev2.bgentrytypeRaw, 1)
        self.assertEqual(
            ev2.bgentrytype,
            eventtypes.LidBgReadingTaken.BgentrytypeEnum.AutoPopulatedBgUsingDexcomEgv)

    def test_bgsourcetype_enum_resolves(self):
        # bgSourceType:1 -> RemoteEntry
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.bgsourcetypeRaw, 1)
        self.assertEqual(ev.bgsourcetype,
                         eventtypes.LidBgReadingTaken.BgsourcetypeEnum.RemoteEntry)

    def test_cgmcalibration_enum_resolves(self):
        # cgmCalibration:0 -> No (0 not treated as missing)
        ev = Event(self.fixtureManualEntry)
        self.assertEqual(ev.cgmcalibrationRaw, 0)
        self.assertEqual(ev.cgmcalibration,
                         eventtypes.LidBgReadingTaken.CgmcalibrationEnum.No)

    def test_todict_is_json_serializable(self):
        for fixture in (self.fixtureManualEntry, self.fixtureAutoPopulated):
            ev = Event(fixture)
            json.dumps(ev.todict())


if __name__ == "__main__":
    unittest.main()
