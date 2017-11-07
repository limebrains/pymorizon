from morizon.category import get_category
from morizon.offer import get_offer_data

url = 'https://www.morizon.pl/do-wynajecia/mieszkania/warszawa/stary-mokotow/?ps[number_of_rooms_from]=2&ps[number_of_rooms_to]=4'

offers = get_category(url=url)
print(len(offers))
for el in offers:
    print(el)

for urls_from_offers in offers:
    data = get_offer_data(urls_from_offers)
    print(urls_from_offers, ' ')
    print(data)
