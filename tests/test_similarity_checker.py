from tortel.similarity_checker.pipeline import (check_cosine_similarity,
                                                tokenization)


class TestSimilarityChecker:
    def test_similarity_check(self):
        set_tokens = tokenization(self.test_product_text())
        check_cosine_similarity(set_tokens)

    def test_product_text(self):
        test_data = [{"Rapoo 3920P Muis Radiografisch Laser Goud,"
                      " Wit Artikelnummer: 1549450 Fabrikantnummer: 13347"
                      " EAN: 6943518933474 Technische specificaties"
                      " Zendmethode Radiografisch Interfaces	USB Sensor"
                      "Laser Sensorresolutie	1600dpi Aantal toetsen"
                      "6 Kleur (specifiek)	Goud, Wit Gewicht	59g Hoogte"
                      "34mm Breedte	62mm Diepte	93mm Stroomverzorging"
                      "2x AA batterij (penlite), meegeleverd Geschikt voor"
                      "(muis/toetsenbord)	Rechtshandigen Soortnaam"
                      "Muis this an historic product which is not available,"
                      "thus not updated anymore"},
                     {"Rapoo 3920PGL Draadloze Muis Gegevens De 3920P "
                      "draadloze muis van Rapoo heeft een betrouwbare 5G"
                      "draadloze verbinding. Maak hem je beste vriend door"
                      "de knoppen zelf in te stellen met jou favoriete"
                      "functies.Wireless Laser Mouse Reliable 5G wireless"
                      "connection Surfree laser engine Powerful customized"
                      "function Nano receiver 4D scroll wheel Low voltage"
                      "alarm Reliable 5G wireless connection Reliable 5G"
                      "wireless transmission far away from the interference"
                      "of 2.4G wireless,bluetooth and WIFI device. Surfree"
                      "laser engine Adjustable high-definition laser engine"
                      "makes your mouse move freely on almost all surfaces"
                      "(even on glass). Powerful customized function Save time"
                      "by customized buttons such as Forward,Back,Tilt-wheel,"
                      "Zoom-in,Zoom-out etc to offer quick responses."
                      "Meer informatie Prijs € 22,95 Garantietype"
                      "Carry in Model	3920PGL Fabrikantnummer (MPN) 3920PGL"
                      "EAN 6943518933474 Merk Rapoo Fabrieksgarantie 2 jaar"}]

        set_product_text = set({})
        set1 = (test_data[0], test_data[1])
        set_product_text.add(set1)

        return set_product_text


if __name__ == '__main__':
    test1 = TestSimilarityChecker()
    test1.test_product_text()

