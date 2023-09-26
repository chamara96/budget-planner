def currency_convert(value):
    if value:
        return "Rs. {:,.0f}".format(value)
    return ""
