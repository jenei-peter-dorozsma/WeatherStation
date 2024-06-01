# This file is part of the WeatherStation project
# and is licensed under the MIT License. For more details,
# see the LICENSE file in the root directory of this project or visit
# https://github.com/jenei-peter-dorozsma/WeatherStation

from datetime import datetime as dt

# Moon phase estimation based on this document:
# https://www.subsystems.us/uploads/9/8/9/4/98948044/moonphase.pdf


class MoonPhaseCalculator:
    def __init__(self, base_date=(2000, 1, 6)):
        self.base_date = base_date
        self.lunar_cycle = 29.5306

    def to_julian_date(self, year, month, day):
        if month in (1, 2):
            year = year - 1
            month = month + 12

        var_a = int(year / 100)
        var_b = int(var_a / 4)
        var_c = 2 - var_a + var_b
        var_e = int(365.25 * (year + 4716))
        var_f = int(30.6001 * (month + 1))
        julian_day = var_c + day + var_e + var_f - 1524.5

        return julian_day

    def moon_age_to_phase(self, moon_age):
        phases = {
            'New Moon': 'Moon1.png',
            'Waxing Crescent': 'Moon2.png',
            'First Quarter': 'Moon3.png',
            'Waxing Gibbous': 'Moon4.png',
            'Full Moon': 'Moon5.png',
            'Waning Gibbous': 'Moon6.png',
            'Last Quarter': 'Moon7.png',
            'Waning Crescent': 'Moon8.png'
        }

        if 0 <= moon_age <= 1:
            phase_index = 0
        elif 1 < moon_age < 7:
            phase_index = 1
        elif 7 <= moon_age <= 8:
            phase_index = 2
        elif 8 < moon_age < 15:
            phase_index = 3
        elif 15 <= moon_age <= 16:
            phase_index = 4
        elif 16 < moon_age < 22:
            phase_index = 5
        elif 22 <= moon_age <= 23:
            phase_index = 6
        elif 23 < moon_age < 29.5306:
            phase_index = 7

        phase_name = list(phases.keys())[phase_index]
        image_name = phases[phase_name]

        return (phase_name, image_name)

    def get_actual_moon_phase(self):
        year = dt.now().year
        month = dt.now().month
        day = dt.now().day

        return self.get_moon_phase(year, month, day)

    def get_moon_phase(self, year, month, day):
        # turn date into julian date
        jd_today = self.to_julian_date(year, month, day)
        # turn a known new moon date to  julian date
        jd_base_date = self.to_julian_date(
            self.base_date[0],
            self.base_date[1],
            self.base_date[2])

        # calulate the age of the moon
        jd_delta = jd_today - jd_base_date
        new_moons = jd_delta / self.lunar_cycle
        moon_age = (new_moons - int(new_moons)) * self.lunar_cycle

        return self.moon_age_to_phase(moon_age)


if __name__ == '__main__':
    moon_calculator = MoonPhaseCalculator()
    print(moon_calculator.get_actual_moon_phase())
