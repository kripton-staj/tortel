from similarity_checker.pipeline import (jaccard_similarity,
                                         remove_stop_words_and_puncts,
                                         sim_hash, stemming, tokenization)


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

    def test_sim_hash(self):
        test_data = [['lg', 'dsn7cy', 'soundbar', 'subwoofer', 'zwart', 'soundbar',
                     'subwoofer', 'draadloz', 'subwoofer', '3,1', 'kanal',
                     'spraakbestur', 'wifi', 'bluetooth', 'breedt', '89', 'cm'],

                     ['lg', 'dsn7y', 'lg', 'soundbar', '3.1.2-kanal', 'subwoofer',
                      'geluidsbalk', 'nominal', 'uitgang', 'vermog', 'total', '380',
                      'watt', 'versterker', 'geintegreerd', 'wi-fi']]

        assert sim_hash(test_data) > 0.7


if __name__ == '__main__':
    """
    Data is defined here for now to test sim_hash and jaccard_similarity.
    """

    data = ["MEDION E23403-I3-512F8 kopen? | MediaMarkt OmschrijvingBeeldscherm:23,8"
            " inch (1920 x 1080)Processor:Intel Core i3-1005G1Werkgeheugen:8"
            " GBOpslag:512 GB SSDGrafische kaart:Intel UHD GraphicsBekijk jouw favoriete"
            " films en series of surf over het internet met deze Medion all-in-one-pc."
            " De all-in-one-pc heeft een groot scherm en levert goede prestaties dankzij"
            " de combinatie van een sterke processor, voldoende werkgeheugen en een snel"
            " opslagmedium. Het grote voordeel van een all-in-one is dat er geen aparte"
            " computerkast naast staat, maar dat de volledige computer in het scherm is"
            " verwerkt. Hierdoor plaats je het apparaat probleemloos op een door jou"
            " gewenste plaats zonder dat daar extra ruimte voor nodig is.Dit krijg je"
            " erbij:1x Adapter, 1x netsnoer, 1x handleiding, draadloos toetsenbord,"
            " draadloze muis ['/', '/nl/category/_computer-482710.html',"
            " '/nl/category/_desktops-642512.html', '/nl/category/_all-in-one-pc-s-642511.html']"
            " ('SpecificatiesProcessorProcessor:Intel Core i3-1005G1Processorsnelheid:1.20"
            " GHzProcessorsnelheid met turbo:3.40 GHzProcessor"
            " merk:Intel\\xc2\\xaeProcessormodel:Core\\xe2\\x84\\xa2 i3Aantal"
            " processorkernen:2Artikelnummer:1689300WerkgeheugenRAM-type:DDR4Werkgeheugen:8"
            " GBRAM-configuratie:1x 8 GBGeheugenuitbreiding:neeGeheugensnelheid:2666 MHzMax."
            " ondersteund geheugen:16 GBDisplayBeeldschermdiagonaal (cm/inch):60.5 cm / 23.8"
            " inchSchermtype:IPS (In-Plane Switching)Paneeltype:IPS (In-Plane Switching)"
            "Beeldschermkenmerken:Anti-reflectiveLed-backlight:jaTouchscreen:neeBeeldresolutie:Full"
            " HDBeeldschermdiagonaal (cm):60.5 cmBeeldschermdiagonaal (inch):23.8 inchResolutie:1920 "
            "x 1080Beeldverhouding:16:9GrafiekkaartGrafische kaart:UHD GraphicsFabrikant grafische"
            " kaart:IntelHarde schijfSolid State Drive (SSD):jaTotale opslagruimte:512 GB"
            " SSDOpslag:SSD , 512 GB , M.2 via SATAOpslag 2:SATAType opslag:SSDOpslagcapaciteit:512"
            " GBInterface opslag:M.2 via SATAInterface opslag 2:SATAMain boardChipset:SoCOptisch"
            " loopwerkOptische drive:neeConnectiviteitBluetooth:jaBluetooth-versie:5.1Wifi-standaarden:Wireless"
            " ACNear Field Communication:neeAansluitingen:2 x USB 2.0, 2 x USB 3.1, 1x HDMI, 1 x"
            " hoofdtelefoon-jack, 1x microfoon-jackWifi:jaGeluidLuidspreker:jaAantal"
            " luidsprekers:2UitvoeringBesturingssysteem:Windows 10 HomeKaartlezer:neeGeïntegreerde"
            " webcam:jaGeïntegreerde microfoon:jaType toetsenbord:QWERTYVerlichte toetsen:neeCamera"
            " resolutie:720 pVingerafdruksensor:neeTouchpad:neeVermogen netadapter:90 WOverige"
            " kenmerken:Studie, Dagelijks gebruik, Films- en series kijkenUpdatebeleidSoftware-updates"
            " vanuit fabrikant:OnbekendAanvullende update-informatie:Voor zover op de afbeeldingen apps"
            " worden getoond, geldt dat MediaMarkt niet kan garanderen dat de apps tijdens de volledige"
            " levensduur van het product goed zullen blijven functioneren. Dit hangt af van het beleid"
            " van de fabrikant.Update policy:OnbekendAlgemene eigenschappenType apparaat:All-in-one"
            " pcAfmetingen (B x H x D):54.2 cm x 41.8 cm x 15.2 cmKleur:ZilverBehuizing:MetaalBreedte:54.2"
            " cmHoogte:41.8 cmDiepte:15.2 cmGewicht:3.02 kgVerpakkingsinhoud:1x Adapter, 1x netsnoer,"
            " 1x handleiding, draadloos toetsenbord, draadloze muisFabrieksgarantie:2 jaarAanvullende"
            " garantie-informatie:2 jaar Pickup & ReturnToon alle specificaties',)",

            "Medion Akoya E23403-I3-512F8 All-in-one (4061275143621) - Computerstores.nl Intel"
            " Core i3-10045G1 8GB RAM – 512GB SSD Intel UHD Graphics (EAN: 4061275143621)"
            " ['https://www.computerstores.nl', 'https://www.computerstores.nl/product-categorie/coolblue/',"
            " 'https://www.computerstores.nl/product-categorie/coolblue/desktops/'] (None,)"]

    tokens = tokenization(data)
    tokens_without_sw = remove_stop_words_and_puncts(tokens)
    tokens_with_stemming = stemming(tokens_without_sw)

    jaccard_result = jaccard_similarity(tokens_with_stemming)
    simhash_result = sim_hash(tokens_with_stemming)
    print("jaccard:", jaccard_result, "simhash:", simhash_result)
