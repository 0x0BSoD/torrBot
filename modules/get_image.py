from json import loads


def process_image(torr_data):
    tott_dict = loads(torr_data['data'])
    if 'rutracker.org' in tott_dict['comment'] and not torr_data['image_url']:
        pass