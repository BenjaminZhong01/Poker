from django.test import TestCase
import poker

# Create your tests here.
if __name__ == "__main__":
    d = poker.get_deck()
    print(len(poker.card_list_to_string(d)))
    # print(poker.get_deck())
    print(poker.card_list_to_string(poker.random_draw_x_cards(5, d)))
    print(len(poker.card_list_to_string(d)))