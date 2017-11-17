from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Item, Category

engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
category1 = Category(name="Snowboarding")

session.add(category1)
session.commit()

item2 = Item(name="Snowboard", description="snowboard desc",
                     category=category1)

session.add(item2)
session.commit()


item1 = Item(name="Bindings", description="bindings desc",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Wax", description="wax desc",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Boots", description="boots desc",
                      category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Snowpants", description="snowpants desc",
                     category=category1)

session.add(item4)
session.commit()

# item5 = Item(name="Root Beer", description="16oz of refreshing goodness",
#                      price="$1.99", course="Beverage", category=category1)
#
# session.add(item5)
# session.commit()
#
# item6 = Item(name="Iced Tea", description="with Lemon",
#                      price="$.99", course="Beverage", category=category1)
#
# session.add(item6)
# session.commit()
#
# item7 = Item(name="Grilled Cheese Sandwich", description="On texas toast with American Cheese",
#                      price="$3.49", course="Entree", category=category1)
#
# session.add(item7)
# session.commit()
#
# item8 = Item(name="Veggie Burger", description="Made with freshest of ingredients and home grown spices",
#                      price="$5.99", course="Entree", category=category1)
#
# session.add(item8)
# session.commit()


# Menu for Super Stir Fry
category2 = Category(name="Soccer")

session.add(category2)
session.commit()


item1 = Item(name="Soccerball", description="With your choice of noodles vegetables and sauces",
                     category=category2)

session.add(item1)
session.commit()

item2 = Item(
    name="Cleats", description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     category=category2)

session.add(item3)
session.commit()

item4 = Item(name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
                     category=category2)

session.add(item4)
session.commit()

item5 = Item(name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     category=category2)

session.add(item5)
session.commit()

# item6 = Item(name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
#                      price="12", course="Entree", category=category2)
#
# session.add(item6)
# session.commit()


# Menu for Panda Garden
category1 = Category(name="Baseball")

session.add(category1)
session.commit()


item1 = Item(name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Gyoza", description="The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     category=category1)

session.add(item4)
session.commit()

# item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      price="$9.50", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()


# Menu for Thyme for that
category1 = Category(name="Tennis")

session.add(category1)
session.commit()


item1 = Item(name="Tres Leches Cake", description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Mushroom risotto", description="Portabello mushrooms in a creamy risotto",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Honey Boba Shaved Snow", description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi",
                     category=category1)

session.add(item3)
session.commit()

# item4 = Item(name="Cauliflower Manchurian", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
#                      price="$6.95", course="Appetizer", category=category1)
#
# session.add(item4)
# session.commit()
#
# item5 = Item(name="Aloo Gobi Burrito", description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
#                      price="$7.95", course="Entree", category=category1)
#
# session.add(item5)
# session.commit()
#
# item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      price="$6.80", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()


# Menu for Tony's Bistro
category1 = Category(name="Basketball")

session.add(category1)
session.commit()


item1 = Item(name="Shellfish Tower", description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Chicken and Rice", description="Chicken... and rice",
                     category=category1)

session.add(item2)
session.commit()

# item3 = Item(name="Mom's Spaghetti", description="Spaghetti with some incredible tomato sauce made by mom",
#                      price="$6.95", course="Entree", category=category1)
#
# session.add(item3)
# session.commit()
#
# item4 = Item(name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
#                      description="Milk, cream, salt, ..., Liquid nitrogen magic", price="$3.95", course="Dessert", category=category1)
#
# session.add(item4)
# session.commit()
#
# item5 = Item(name="Tonkatsu Ramen", description="Noodles in a delicious pork-based broth with a soft-boiled egg",
#                      price="$7.95", course="Entree", category=category1)
#
# session.add(item5)
# session.commit()


# Menu for Andala's
category1 = Category(name="Football")

session.add(category1)
session.commit()


item1 = Item(name="Lamb Curry", description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
                     category=category1)

session.add(item1)
session.commit()

# item3 = Item(name="Potstickers", description="Delicious chicken and veggies encapsulated in fried dough.",
#                      price="$6.50", course="Appetizer", category=category1)
#
# session.add(item3)
# session.commit()
#
# item4 = Item(name="Nigiri Sampler", description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
#                      price="$6.75", course="Appetizer", category=category1)
#
# session.add(item4)
# session.commit()
#
# item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      price="$7.00", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()


# Menu for Auntie Ann's
# category1 = Category(name="Auntie Ann\'s Diner' ")
#
# session.add(category1)
# session.commit()
#
# item9 = Item(name="Chicken Fried Steak", description="Fresh battered sirloin steak fried and smothered with cream gravy",
#                      price="$8.99", course="Entree", category=category1)
#
# session.add(item9)
# session.commit()
#
#
# item1 = Item(name="Boysenberry Sorbet", description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
#                      price="$2.99", course="Dessert", category=category1)
#
# session.add(item1)
# session.commit()
#
# item2 = Item(name="Broiled salmon", description="Salmon fillet marinated with fresh herbs and broiled hot & fast",
#                      price="$10.95", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()
#
# item3 = Item(name="Morels on toast (seasonal)", description="Wild morel mushrooms fried in butter, served on herbed toast slices",
#                      price="$7.50", course="Appetizer", category=category1)
#
# session.add(item3)
# session.commit()
#
# item4 = Item(name="Tandoori Chicken", description="Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
#                      price="$8.95", course="Entree", category=category1)
#
# session.add(item4)
# session.commit()
#
# item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      price="$9.50", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()
#
# item10 = Item(name="Spinach Ice Cream", description="vanilla ice cream made with organic spinach leaves",
#                       price="$1.99", course="Dessert", category=category1)
#
# session.add(item10)
# session.commit()
#
#
# # Menu for Cocina Y Amor
# category1 = Category(name="Cocina Y Amor ")
#
# session.add(category1)
# session.commit()
#
#
# item1 = Item(name="Super Burrito Al Pastor", description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla",
#                      price="$5.95", course="Entree", category=category1)
#
# session.add(item1)
# session.commit()
#
# item2 = Item(name="Cachapa", description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ",
#                      price="$7.99", course="Entree", category=category1)
#
# session.add(item2)
# session.commit()
#
#
# category1 = Category(name="State Bird Provisions")
# session.add(category1)
# session.commit()
#
# item1 = Item(name="Chantrelle Toast", description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms",
#                      price="$5.95", course="Appetizer", category=category1)
#
# session.add(item1)
# session.commit
#
# item1 = Item(name="Guanciale Chawanmushi", description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)",
#                      price="$6.95", course="Dessert", category=category1)
#
# session.add(item1)
# session.commit()
#
#
# item1 = Item(name="Lemon Curd Ice Cream Sandwich", description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews",
#                      price="$4.25", course="Dessert", category=category1)
#
# session.add(item1)
# session.commit()
