from datetime import timedelta
from openprocurement.auctions.geb.utils import calculate_certainly_business_date as ccbd


class Period(object):
    pass


class Date(object):
    pass


class AuctionDate(Date):
    name = 'auctionDate'

    def __init__(self):
        pass

    def __get__(self, instance, owner):
        self._date = ccbd(instance.rectificationPeriod.startDate, -timedelta(days=2))
        return self

    @property
    def date(self):
        return self._date


class TenderPeriod(Period):
    name = 'tenderPeriod'

    def __init__(self):
        self.working_days = False
        self.specific_hour = 20

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(self._endDate,
                                       -timedelta(days=10))
        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.rectificationPeriod.endDate
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'enquiryPeriod':
                self._startDate = ccbd(instance.enquiryPeriod.startDate,
                                       timedelta(days=2))
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionDate':
                self._startDate = ccbd(self.auctionDate.date,
                                       timedelta(days=5))
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=16))

                self._endDate = ccbd(instance.time,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class RectificationPeriod(Period):
    name = 'rectificationPeriod'

    def __init__(self):
        self.duration = timedelta(2)
        self.working_days = False

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(self._startDate, self.duration)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'tenderPeriod':
                self._endDate = instance.tenderPeriod.startDate
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'enquiryPeriod':
                self._endDate = instance.tenderPeriod.startDate
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'auctionDate':
                self._startDate = ccbd(instance.auctionDate.date, timedelta(days=3))
                self._endDate = ccbd(self._startDate, self.duration)
        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=18))

                self._endDate = ccbd(instance.time, -timedelta(days=14))
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class EnquiryPeriod(Period):
    name = 'enquiryPeriod'

    def __init__(self):
        self.working_days = False
        self.specific_hour = 20

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=14))

        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'tenderPeriod':
                self._startDate = ccbd(instance.tenderPeriod.startDate,
                                       -timedelta(days=2))
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionDate':
                self._startDate = ccbd(instance.auctionDate.date,
                                       timedelta(days=1))
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=18))

                self._endDate = ccbd(instance.time,
                                     -timedelta(days=1),
                                     specific_hour=self.specific_hour)
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class AuctionPeriod(Period):
    name = 'auctionPeriod'

    def __init__(self):
        self.default = 0

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'shouldStartAfter':
                self._shouldStartAfter = instance.time

        elif instance.period == 'rectificationPeriod':
                self._shouldStartAfter = ccbd(instance.time, timedelta(days=14))
        elif instance.period == 'tenderPeriod':
                self._shouldStartAfter = ccbd(instance.time, timedelta(days=14))
        elif instance.period == 'auctionDate':
                self._shouldStartAfter = ccbd(instance.time, timedelta(days=14))
        elif instance.period == 'enquiryPeriod':
            if instance.state == 'start':
                self._shouldStartAfter = ccbd(instance.time, timedelta(days=14))
            elif instance.state == 'end':
                self._shouldStartAfter = instance.time

        return self

    @property
    def shouldStartAfter(self):
        return self._shouldStartAfter


class Calculator(object):
    rectificationPeriod = RectificationPeriod()
    tenderPeriod = TenderPeriod()
    enquiryPeriod = EnquiryPeriod()
    auctionPeriod = AuctionPeriod()
    auctionDate = AuctionDate()

    def __init__(self, time, period, state):
        self.time = time
        self.period = period
        self.state = state
