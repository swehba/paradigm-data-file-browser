class Geolocation:
    def __init__(self, latitude=0.0, longitude=0.0, altitude=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __repr__(self):
        return f'Geolocation(latitude={self.latitude}, longitude={self.longitude}, altitude={self.longitude})'

    def __str__(self):
        return f'(lat={self.latitude:0.6}, lon={self.longitude:0.6}, alt={self.altitude:0.6})'
