
async def get_developers_string(developers):
    if developers:
        devs_string = ' | '.join([f'@{dev.username} ({dev.specialty.value})' if dev.username else f'@{dev.first_name} ({dev.specialty.value})' for dev in developers])
        return devs_string
    else:
        return ''
