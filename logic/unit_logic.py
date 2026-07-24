UNIT_CATEGORIES = {
    'Length': {
        'Meters': 1.0,
        'Kilometers': 1000.0,
        'Centimeters': 0.01,
        'Millimeters': 0.001,
        'Miles': 1609.344,
        'Yards': 0.9144,
        'Feet': 0.3048,
        'Inches': 0.0254,
    },
    'Weight': {
        'Kilograms': 1.0,
        'Grams': 0.001,
        'Milligrams': 0.000001,
        'Pounds': 0.45359237,
        'Ounces': 0.028349523125,
        'Tonnes': 1000.0,
    },
    'Time': {
        'Seconds': 1.0,
        'Minutes': 60.0,
        'Hours': 3600.0,
        'Days': 86400.0,
        'Weeks': 604800.0,
    },
    'Area': {
        'Square Meters': 1.0,
        'Square Kilometers': 1_000_000.0,
        'Square Feet': 0.09290304,
        'Square Miles': 2_589_988.110336,
        'Acres': 4046.8564224,
        'Hectares': 10000.0,
    },
    'Speed': {
        'Meters/Second': 1.0,
        'Kilometers/Hour': 0.277778,
        'Miles/Hour': 0.44704,
        'Feet/Second': 0.3048,
        'Knots': 0.514444,
    },
    'Volume': {
        'Liters': 1.0,
        'Milliliters': 0.001,
        'Cubic Meters': 1000.0,
        'Gallons': 3.785411784,
        'Quarts': 0.946352946,
        'Cups': 0.2365882365,
    },
    'Data': {
        'Bytes': 1.0,
        'Kilobytes': 1024.0,
        'Megabytes': 1024.0 ** 2,
        'Gigabytes': 1024.0 ** 3,
        'Terabytes': 1024.0 ** 4,
    },
}

TEMPERATURE_UNITS = ('Celsius', 'Fahrenheit', 'Kelvin')


class UnitLogic:

    def get_units(self, category):

        if category == 'Temperature':
            return list(TEMPERATURE_UNITS)

        return list(UNIT_CATEGORIES[category].keys())


    def convert(self, category, value, from_unit, to_unit):

        if category == 'Temperature':
            return self._convert_temperature(value, from_unit, to_unit)

        units = UNIT_CATEGORIES.get(category)
        if not units or from_unit not in units or to_unit not in units:
            return None

        base_value = value * units[from_unit]
        return base_value / units[to_unit]


    def _convert_temperature(self, value, from_unit, to_unit):

        celsius = self._to_celsius(value, from_unit)
        if celsius is None:
            return None

        return self._from_celsius(celsius, to_unit)


    def _to_celsius(self, value, unit):

        if unit == 'Celsius':
            return value
        if unit == 'Fahrenheit':
            return (value - 32) * 5 / 9
        if unit == 'Kelvin':
            return value - 273.15

        return None


    def _from_celsius(self, celsius, unit):

        if unit == 'Celsius':
            return celsius
        if unit == 'Fahrenheit':
            return celsius * 9 / 5 + 32
        if unit == 'Kelvin':
            return celsius + 273.15

        return None