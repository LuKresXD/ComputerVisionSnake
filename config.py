import cv2

food = [[cv2.imread("Pictures/Fruits/banana.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/blueberries.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/cherries.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/grapes.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/green-apple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/kiwi.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/lemon.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/mango.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/melon.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/peach.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/pear.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/pineapple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/red-apple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/strawberry.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/tangerine.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/watermelon.png", cv2.IMREAD_UNCHANGED)],
        [cv2.imread("Pictures/Vegetables/broccoli.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/carrot.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/cucumber.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/ear-of-corn.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/eggplant.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/hot-pepper.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/leafy-green.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/onion.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/potato.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Vegetables/tomato.png", cv2.IMREAD_UNCHANGED)],
        [cv2.imread("Pictures/Other/cheese.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/cookie.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/croissant.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/cut-of-meat.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/french-fries.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/hamburger.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/hot-dog.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/sandwich.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/taco.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Other/pizza.png", cv2.IMREAD_UNCHANGED)]]

cursor = cv2.imread("Pictures/GUI/cursor.png", cv2.IMREAD_UNCHANGED)
play = cv2.imread("Pictures/GUI/play.png", cv2.IMREAD_UNCHANGED)
restart = cv2.imread("Pictures/GUI/restart.png", cv2.IMREAD_UNCHANGED)
game_over = cv2.imread("Pictures/GUI/game_over.png", cv2.IMREAD_UNCHANGED)
coin = cv2.imread("Pictures/GUI/coin.png", cv2.IMREAD_UNCHANGED)
back = cv2.imread("Pictures/GUI/back.png", cv2.IMREAD_UNCHANGED)
shop = cv2.imread("Pictures/GUI/shop.png", cv2.IMREAD_UNCHANGED)
skin = cv2.resize(cv2.imread("Pictures/GUI/skin.png", cv2.IMREAD_UNCHANGED), (300, 320))
foodi = cv2.resize(cv2.imread("Pictures/GUI/food.png", cv2.IMREAD_UNCHANGED), (300, 320))

skin1 = cv2.imread("Pictures/GUI/skins/first.png", cv2.IMREAD_UNCHANGED)
skin2 = cv2.imread("Pictures/GUI/skins/second.png", cv2.IMREAD_UNCHANGED)
skin3 = cv2.imread("Pictures/GUI/skins/third.png", cv2.IMREAD_UNCHANGED)
skin4 = cv2.imread("Pictures/GUI/skins/fourth.png", cv2.IMREAD_UNCHANGED)
skin5 = cv2.imread("Pictures/GUI/skins/fifth.png", cv2.IMREAD_UNCHANGED)
skin6 = cv2.imread("Pictures/GUI/skins/sixth.png", cv2.IMREAD_UNCHANGED)
purchased = cv2.imread("Pictures/GUI/skins/purchased.png", cv2.IMREAD_UNCHANGED)

food1 = cv2.resize(cv2.imread("Pictures/GUI/vegetables.png", cv2.IMREAD_UNCHANGED), (308, 524))
food2 = cv2.resize(cv2.imread("Pictures/GUI/other.png", cv2.IMREAD_UNCHANGED), (308, 524))
food_purchased = cv2.resize(cv2.imread("Pictures/GUI/skins/purchased.png", cv2.IMREAD_UNCHANGED), (308, 524))

skins = [[(200, 200, 200), (50, 50, 50)],
         [(31, 64, 55), (200, 242, 153)],
         [(199, 195, 189), (80, 62, 44)],
         [(199, 167, 217), (220, 252, 255)],
         [(195, 96, 131), (145, 191, 46)],
         [(125, 92, 252), (251, 130, 106)],
         [(142, 153, 17), (125, 239, 56)]]
