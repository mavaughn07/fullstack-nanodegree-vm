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

username = "Max Vaughn"
user1 = User(username="Max Vaughn")
session.add(user1)
session.commit()

category1 = Category(name="Snowboarding")

session.add(category1)
session.commit()

item2 = Item(name="Snowboard", description="""Snowboards are boards where both
    feet are secured to the same board, which are wider than skis, with the
    ability to glide on snow. Snowboards widths are between 6 and 12 inches or
    15 to 30 centimeters. Snowboards are differentiated from monoskis by the
    stance of the user. In monoskiing, the user stands with feet inline with
    direction of travel (facing tip of monoski/downhill) (parallel to long
    axis of board), whereas in snowboarding, users stand with feet transverse
    (more or less) to the longitude of the board. Users of such equipment may
    be referred to as snowboarders. Commercial snowboards generally require
    extra equipment such as bindings and special boots which help secure both
    feet of a snowboarder, who generally rides in an upright position. These
    types of boards are commonly used by people at ski hills or resorts for
    leisure, entertainment, and competitive purposes in the activity called
    snowboarding.""", category=category1, user=user1)

session.add(item2)
session.commit()


item1 = Item(name="Bindings", description="""Bindings are separate components
    from the snowboard deck and are very important parts of the total
    snowboard interface. The bindings' main function is to hold the rider's
    boot in place tightly to transfer their energy to the board. Most bindings
    are attached to the board with three or four screws that are placed in the
    center of the binding. Although a rather new technology from Burton
    called Infinite channel system uses two screws, both on the outsides of
    the binding. There are several types of bindings. Strap-in, step-in, and
    hybrid bindings are used by most recreational riders and all freestyle
    riders.""", category=category1, user=user1)

session.add(item1)
session.commit()

item2 = Item(name="Wax", description="""Ski wax is a material applied to the
    bottom of snow runners, including skis, snowboards, and toboggans, to
    improve their coefficient of friction performance under varying snow
    conditions. The two main types of wax used on skis are glide waxes and
    grip waxes. They address kinetic friction—to be minimized with a glide
    wax—and static friction—to be achieved with a grip wax. Both types of wax
    are designed to be matched with the varying properties of snow,
    including crystal type and size, and moisture content of the snow
    surface, which vary with temperature and the temperature history of the
    snow. Glide wax is selected to minimize sliding friction for both alpine
    and cross-country skiing. Grip wax (also called 'kick wax') provides
    on-snow traction for cross-country skiers, as they stride forward using
    classic technique.""", category=category1, user=user1)

session.add(item2)
session.commit()

item3 = Item(name="Boots", description="""Snowboard boots are mostly
    considered soft boots, though alpine snowboarding uses a harder boot
    similar to a ski boot. A boot's primary function is to transfer the
    rider's energy into the board, protect the rider with support, and keep
    the rider's feet warm. A snowboarder shopping for boots is usually
    looking for a good fit, flex, and looks. Boots can have different features
    such as lacing styles, heat molding liners, and gel padding that the
    snowboarder also might be looking for. Tradeoffs include rigidity versus
    comfort, and built in forward lean, versus comfort.""",
             category=category1, user=user1)

session.add(item3)
session.commit()

item4 = Item(name="Snowpants", description="""Ski pants, or salopettes, when
    part of a two-piece ski suit, is usually made in the same fabric and color
    as the corresponding ski jacket. It is sometimes in the form of
    bib-and-brace and the jacket is worn over it.""",
             category=category1, user=user1)

session.add(item4)
session.commit()


category2 = Category(name="Soccer")

session.add(category2)
session.commit()


item1 = Item(name="Soccer Ball", description="""A football, soccer ball, or
    association football ball is the ball used in the sport of association
    football. The name of the ball varies according to whether the sport is
    called 'football', 'soccer', or 'association football'. The ball's
    spherical shape, as well as its size, weight, and material composition,
    are specified by Law 2 of the Laws of the Game maintained by the
    International Football Association Board. Additional, more stringent,
    standards are specified by FIFA and subordinate governing bodies for the
    balls used in the competitions they sanction.""",
             category=category2, user=user1)

session.add(item1)
session.commit()

item2 = Item(name="Cleats", description="""Cleats or studs are protrusions on
    the sole of a shoe, or on an external attachment to a shoe, that provide
    additional traction on a soft or slippery surface. They can be conical or
    blade-like in shape, and made of plastic, rubber or metal. The type worn
    depends on the environment of play, whether it be grass, ice, artificial
    turf, or other grounds.""", category=category2, user=user1)

session.add(item2)
session.commit()

item3 = Item(name="Goalie Gloves", description="""There are no other specific
    requirements, but goalkeepers are usually allowed to wear additional
    protective gear such as padded clothing. Most goalkeepers also wear
    gloves to protect their hands and enhance their grip of the ball.""",
             category=category2, user=user1)

session.add(item3)
session.commit()

item4 = Item(name="Shinguards", description="""A shin guard or shin pad is a
    piece of equipment worn on the front of a player’s shin to protect them
    from injury. These are commonly used in sports including association
    football, baseball, ice hockey, field hockey, lacrosse, cricket, mountain
    bike trials, and other sports. This is due to either being required by
    the rules/laws of the sport or worn voluntarily by the participants
    for protective measures.""", category=category2, user=user1)

session.add(item4)
session.commit()

category1 = Category(name="Baseball")

session.add(category1)
session.commit()


item1 = Item(name="Bat", description="""Four historically significant
    baseball bats showcased in the National Baseball Hall of Fame's traveling
    exhibit 'Baseball As America'. From left to right: bat used by Babe Ruth
    to hit his 60th home run during the 1927 season, bat used by Roger Maris
    to hit his 61st home run during the 1961 season, bat used by Mark McGwire
    to hit his 70th home run during the 1998 season, and the bat used by
    Sammy Sosa for his 66th home run during the same season. A baseball bat
    is a smooth wooden or metal club used in the sport of baseball to hit the
    ball after it is thrown by the pitcher. By regulation it may be no more
    than 2.75 inches(7.0 cm) in diameter at the thickest part and no more
    than 42 inches(1.067 m) in length. Although historically bats approaching
    3 pounds(1.4 kg) were swung,  today bats of 33 ounces(0.94 kg) are
    common, topping out at 34 ounces(0.96 kg) to 36 ounces(1.0 kg).""",
             category=category1, user=user1)

session.add(item1)
session.commit()

item2 = Item(name="Mitt", description="""A baseball glove or mitt is a large
    leather glove worn by baseball players of the defending team, which
    assists players in catching and fielding balls hit by a batter or thrown
    by a teammate. By convention, the glove is described by the handedness of
    the intended wearer, rather than the hand on which the glove is worn: a
    glove that fits on the left hand—used by a right-handed thrower—is called
    a right-handed(RH) or 'right-hand throw' (RHT) glove. Conversely, a
    left-handed glove(LH or LHT) is worn on the right hand, allowing the
    player to throw the ball with the left hand.""",
             category=category1, user=user1)

session.add(item2)
session.commit()

item3 = Item(name="Baseball", description="""A baseball is a ball used in the
    sport of the same name. The ball features a rubber or cork center,
    wrapped in yarn, and covered, in the words of the Official Baseball Rules
    'with two strips of white horsehide or cowhide, tightly stitched
    together.' It is 9–9​1⁄4 inches (229–235 mm) in circumference
    (​2 55⁄64–​2 15⁄16 in. or 73–75 mm in diameter), and masses from 5 to
    5​1⁄4 oz. (142 to 149 g). The yarn or string used to wrap the baseball
    can be up to one mile (1.6 km) in length. Some are wrapped in a
    plastic-like covering.""", category=category1, user=user1)

session.add(item3)
session.commit()

item4 = Item(name="Batting Helmet", description="""A batting helmet is worn
    by batters in the game of baseball or softball. It is meant to protect
    the batter's head from errant pitches thrown by the pitcher. A batter who
    is 'hit by pitch, ' due to an inadvertent wild pitch or a pitcher's
    purposeful attempt to hit him, may be seriously, even fatally,
    injured.""", category=category1, user=user1)

session.add(item4)
session.commit()

category1 = Category(name="Tennis")

session.add(category1)
session.commit()


item1 = Item(name="Tennis Racket", description="""A racket or racquet is a
    sports implement consisting of a handled frame with an open hoop across
    which a network of strings or catgut is stretched tightly. It is used
    for striking a ball or shuttlecock in games such as squash, tennis,
    racquetball, and badminton. Collectively, these games are known as racket
    sports. Racket design and manufacturing has changed considerably over
    the centuries.""", category=category1, user=user1)

session.add(item1)
session.commit()

item2 = Item(name="Tennis Ball", description="""A tennis ball is a ball
    designed for the sport of tennis. Tennis balls are fluorescent yellow at
    major sporting events, but in recreational play can be virtually any
    color. Tennis balls are covered in a fibrous felt which modifies their
    aerodynamic properties, and each has a white curvilinear oval covering
    it.""", category=category1, user=user1)

session.add(item2)
session.commit()


category1 = Category(name="Basketball")

session.add(category1)
session.commit()


item1 = Item(name="Basketball", description="""A basketball is a spherical
    ball used in basketball games. Basketballs typically range in size from
    very small promotional items only a few inches in diameter to extra
    large balls nearly a foot in diameter used in training exercises. For
    example, a youth basketball could be 27 inches (69 cm) in circumference,
    while a National Collegiate Athletic Association (NCAA) men's ball
    would be a maximum of 30 inches (76 cm) and an NCAA women's ball would be
    a maximum of 29 inches (74 cm). The standard for a basketball in the
    National Basketball Association (NBA) is 29.5 inches (75 cm) in
    circumference and for the Women's National Basketball Association (WNBA),
    a maximum circumference of 29 inches (74 cm). High school and junior
    leagues normally use NCAA, NBA or WNBA sized balls.""",
             category=category1, user=user1)

session.add(item1)
session.commit()

item2 = Item(name="Net", description="""The basket is a steel rim 18 inches
    (46 cm) diameter with an attached net affixed to a backboard that
    measures 6 by 3.5 feet (1.8 by 1.1 meters) and one basket is at each end
    of the court. The white outlined box on the backboard is 18 inches
    (46 cm) high and 2 feet (61 cm) wide. At almost all levels of
    competition, the top of the rim is exactly 10 feet (3.05 meters) above
    the court and 4 feet (1.22 meters) inside the baseline. While variation
    is possible in the dimensions of the court and backboard, it is
    considered important for the basket to be of the correct height – a rim
    that is off by just a few inches can have an adverse effect on
    shooting.""", category=category1, user=user1)

session.add(item2)
session.commit()


category1 = Category(name="Football")

session.add(category1)
session.commit()


item1 = Item(name="Pads", description="""Shoulder pads are a piece of
    protective equipment used in many contact sports such as American
    football, Canadian football, lacrosse and hockey. The first football
    shoulder pads were created by Princeton student L.P. Smock in 1877. These
    were made of leather and wool and were thin, light, and did not provide
    much protection. Additionally, they were sewn into the players' jerseys
    rather than being worn as a separate piece of equipment.  Allegedly Pop
    Warner was the first to have his players wear shoulder pads. When he was
    coaching at the Carlisle Indian Industrial School, he was the first one
    to use pads made of fiber rather than cotton.""",
             category=category1, user=user1)

session.add(item1)
session.commit()
