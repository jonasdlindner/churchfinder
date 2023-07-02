import requests
DEBUG = False


class ChurchfinderEvent:
    pass


class ChurchfinderClientError(Exception):
    pass


class ChurchfinderClient:
    # TODO handle status codes
    def __init__(self, protocol, hostname, port, api_version="v1"):
        self.languages = None
        self.eventTypes = None
        self.locations = None

        self.base_url = (
            protocol
            + "://"
            + hostname
            + ":"
            + str(port)
            + "/api/"
            + api_version
        )

    def _get(self, endpoint):
        return requests.get(self.base_url + "/" + endpoint).json()

    def _post(self, endpoint, data):
        resp = requests.post(self.base_url + "/" + endpoint + "/", data=data)
        if DEBUG: print("resp.status_code", resp.status_code)

    def getEventTypes(self):
        return self._get("eventtypes/")

    def getLocations(self):
        return self._get("locations/")

    def getLanguages(self):
        return self._get("languages/")

    def getEvents(self):
        return self._get("events/")

    def _getLanguageId(self, language):
        if self.languages is None:
            self.languages = self.getLanguages()

        langaugeId = ""
        for i in self.languages:
            if i["name"]==language:
                langaugeId = i["id"]
                break
        if langaugeId == "":
            raise ChurchfinderClientError("Need to set language")
        return langaugeId

    def _getEvenTypeId(self, eventType):
        if self.eventTypes is None:
            self.eventTypes = self.getEventTypes()

        eventTypeId = ""
        for i in self.eventTypes:
            if i["name"]==eventType:
                eventTypeId = i["id"]
                break
        if eventTypeId == "":
            raise ChurchfinderClientError("Need to  set event type")
        return eventTypeId

    def _getLocationId(self, location):
        if self.locations is None:
            self.locations = self.getLocations()
        locationId = ""
        for i in self.locations:
            if i["location_name"]==location:
                locationId = i["id"]
                break
        if locationId == "":
            raise ChurchfinderClientError("Need to set proper location")
        return locationId

    def postEvents(
        self,
        date,
        time,
        location,
        eventType="Heilige Messe",
        language="Deutsch",
        free_text="",
        location_sub_category="",
        memorial="",
        celebrant="",
        attendees=None,
        cancelled=False,
    ):

        languageId = self._getLanguageId(language)
        print("get Languages")
        eventTypeId = self._getEvenTypeId(eventType)
        print("get eventTypeId")
        locationId = self._getLocationId(location)
        print("get locationId")
        data = {
            'free_text': free_text,
            'date': date,
            'time': time,
            'location_sub_category': location_sub_category,
            'memorial': memorial,
            'celebrant': celebrant,
            'collection_id': None,
            'attendees': attendees,
            'event_type': eventTypeId,
            'location': locationId,
            'language': languageId,
            "cancelled": cancelled,
        }
        self._post("events", data)

if __name__ == "__main__":
    cfClient = ChurchfinderClient("http", "localhost", 8000)
    print(cfClient.getLocations())
    for day in range(1, 30):
        for hour in range(0, 24):
            for minute in range(0, 60):
                if day < 10:
                    day_str = "0" + str(day)
                else:
                    day_str = str(day)

                if hour < 10:
                    hour_str = "0" + str(hour)
                else:
                    hour_str = str(hour)

                if minute < 10:
                    minute_str = "0" + str(minute)
                else:
                    minute_str = str(minute)
                print(hour_str + ':' + minute_str)
                print(cfClient.postEvents(date='2023-03-'+ day_str, time=hour_str + ':' + minute_str+ ":00:00", location="Bruder Klaus"))
