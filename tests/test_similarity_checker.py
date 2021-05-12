from similarity_checker.pipeline import (check_cosine_distance,
                                         remove_stop_words_and_puncts,
                                         stemming, tfidf_vectorizer,
                                         tokenization)


class TestSimilarityChecker:
    def test_tokenization(self):
        test_data = ["Rapoo 3920P Mluis Radiografisch Laser Goud,"
                     " Wit Artikelnummer: 1549450 Fabrikantnummer: 13347"
                     " EAN: 6943518933474 Technische specificaties"
                     " Zendmethode Radiografisch Interfaces USB Sensor"
                     " Laser Sensorresolutie 1600dpi Aantal toetsen",
                     "Rapoo 3920PGL Draadloze Muis Gegevens De 3920P"
                     " draadloze muis van Rapoo heeft een betrouwbare 5G"
                     " draadloze verbinding. Meer informatie Prijs € 22,95"
                     " Garantietyp"]

        actual = tokenization(test_data)
        expected = [['Rapoo', '3920P', 'Mluis', 'Radiografisch', 'Laser',
                     'Goud', ',', 'Wit', 'Artikelnummer', ':', '1549450',
                     'Fabrikantnummer', ':', '13347', 'EAN', ':',
                     '6943518933474', 'Technische', 'specificaties',
                     'Zendmethode', 'Radiografisch', 'Interfaces', 'USB',
                     'Sensor', 'Laser', 'Sensorresolutie', '1600dpi',
                     'Aantal', 'toetsen'],
                    ['Rapoo', '3920PGL', 'Draadloze', 'Muis', 'Gegevens',
                     'De', '3920P', 'draadloze', 'muis', 'van', 'Rapoo',
                     'heeft', 'een', 'betrouwbare', '5', 'G', 'draadloze',
                     'verbinding', '.', 'Meer', 'informatie', 'Prijs', '€',
                     '22,95', 'Garantietyp']]

        assert all([a == b for a, b in zip(actual, expected)])

    def test_remove_stop_words_and_puncts(self):
        test_data = [['Als', 'u', 'binnen', '2', 'maanden', 'na', 'uw',
                      'aankoop', 'dit', 'Tamron', 'objectief', 'registreert',
                      ',', 'krijgt', 'u', 'van', 'Tamron', '5', 'jaar',
                      'garantie', '.'],
                     ['Zolang', 'de', 'voorraad', 'strekt', ',', 'uitsluitend',
                      'op', 'producten', 'verkocht', 'en', 'verzonden', 'door',
                      'Fnac.be', '.']]

        actual = remove_stop_words_and_puncts(test_data)
        expected = [['2', 'maanden', 'aankoop', 'Tamron', 'objectief',
                     'registreert', 'krijgt', 'Tamron', '5', 'jaar',
                     'garantie'],
                    ['Zolang', 'voorraad', 'strekt', 'uitsluitend',
                     'producten', 'verkocht', 'verzonden', 'Fnac.be']]

        assert all([a == b for a, b in zip(actual, expected)])

    def test_stemming(self):
        test_data = [['55,4', 'maanden', 'aankoop', 'Tamron', 'krijgt', 'jaar'],
                     ['voorraad', 'strekt', 'producten', 'verzonden',
                      '55,4', 'Tamron']]

        actual = stemming(test_data)
        expected = [['55,4', 'maand', 'aankop', 'tamron', 'krijgt', 'jar'],
                    ['voorrad', 'strekt', 'product', 'verzond', '55,4',
                     'tamron']]

        assert all([a == b for a, b in zip(actual, expected)])


if __name__ == '__main__':
    data = [['lg', 'dsn7cy', 'soundbar', 'subwoofer', 'zwart', 'soundbar',
             'subwoofer', 'draadloz', 'subwoofer', '3,1', 'kanal',
             'spraakbestur', 'wifi', 'bluetooth', 'breedt', '89', 'cm'],
            ['lg', 'dsn7y', 'lg', 'soundbar', '3.1.2-kanal', 'subwoofer',
             'geluidsbalk', 'nominal', 'uitgang', 'vermog', 'total', '380',
             'watt', 'versterker', 'geintegreerd', 'wi-fi']]
    tfidf = tfidf_vectorizer(data)
    check_cosine_distance(tfidf)
