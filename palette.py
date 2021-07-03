classnames=["BACKGROUND", "candy", "egg tart", "french fries", "chocolate", "biscuit", "popcorn", "pudding", "ice cream", 
            "cheese butter", "cake", "wine", "milkshake", "coffee", "juice", "milk", "tea", "almond", "red beans", 
            "cashew", "dried cranberries", "soy", "walnut", "peanut", "egg", "apple", "date", "apricot", "avocado", 
            "banana", "strawberry", "cherry", "blueberry", "raspberry", "mango", "olives", "peach", "lemon", "pear", 
            "fig", "pineapple", "grape", "kiwi", "melon", "orange", "watermelon", "steak", "pork", "chicken duck", 
            "sausage", "fried meat", "lamb", "sauce", "crab", "fish", "shellfish", "shrimp", "soup", "bread", "corn", 
            "hamburger", "pizza", "hanamaki baozi", "wonton dumplings", "pasta", "noodles", "rice", "pie", "tofu", 
            "eggplant", "potato", "garlic", "cauliflower", "tomato", "kelp", "seaweed", "spring onion", "grape", 
            "ginger", "okra", "lettuce", "pumpkin", "cucumber", "white radish", "carrot", "asparagus", "bamboo shoots", 
            "broccoli", "celery stick", "cilantro mint", "snow peas", "cabbage", "bean sprouts", "onion", "pepper", 
            "green beans", "French beans", "king oyster mushroom", "shiitake", "enoki mushroom", "oyster mushroom", 
            "white button mushroom", "salad", "other ingredients"]

palette = [[0, 0, 0], [40, 100, 150], [80, 150, 200], [120, 200, 10], [160, 10, 60], [200, 60, 110], [50, 110, 160], [40, 160, 210], 
           [80, 210, 20], [120, 20, 70], [160, 70, 120], [200, 120, 170], [0, 170, 220], [40, 220, 30], [80, 30, 80], [120, 80, 130], 
           [160, 130, 180], [200, 180, 230], [50, 230, 40], [40, 90, 90], [80, 90, 140], [120, 140, 190], [160, 190, 0], [200, 50, 50], 
           [0, 50, 100], [90, 100, 150], [80, 200, 200], [170, 200, 10], [160, 70, 60], [200, 120, 110], [0, 110, 160], [90, 160, 260], 
           [80, 260, 40], [110, 60, 20], [210, 110, 120], [200, 150, 120], [255, 170, 200], [90, 160, 70], [20, 100, 40], [178, 60, 230], 
           [260, 230, 280], [100, 80, 30], [50, 200, 90], [140, 50, 20], [180, 30, 140], [120, 40, 290], [60, 150, 50], [200, 0, 50], 
           [60, 0, 140], [50, 50, 150], [30, 150, 200], [120, 255, 30], [160, 100, 20], [260, 40, 100], [20, 80, 140], [90, 100, 150], 
           [30, 170, 120], [120, 70, 140], [160, 20, 160], [100, 100, 190], [170, 0, 200], [90, 180, 30], [40, 140, 80], [120, 40, 120], 
           [120, 180, 130], [150, 100, 230], [0, 230, 40], [80, 30, 190], [100, 190, 40], [180, 120, 140], [0, 100, 220], [0, 50, 230],
           [100, 0, 60], [140, 50, 100], [40, 100, 200], [10, 240, 120], [160, 110, 260], [100, 20, 210], [120, 0, 10], [210, 10, 140], 
           [80, 80, 80],  [120, 120, 120],  [160, 160, 160], [200, 200, 200], [220, 220, 220], [40, 40, 40], [30, 160, 30], [130, 60, 130], 
           [200, 20, 200], [150, 150, 20], [20, 150, 250], [40, 40, 90], [230, 190, 40], [220, 40, 90], [60, 200, 40], [20, 200, 150], 
           [130, 200, 0], [160, 40, 100], [90, 100, 150], [180, 10, 240], [20, 170, 80], [20, 110, 255], [30, 220, 100], [140, 210, 160]]

def getlabel(idx):
   return classnames[idx]

def showcolor(idx):
   if type(idx) == str:          #ie when index == labelname
     idx = classnames.index(idx) 
   import matplotlib.pyplot as plt
   rgb = [i/255 for i in palette[idx]]
   plt.suptitle(classnames[idx],fontweight="bold")  #supertitle
   plt.title('(rgb = {})'.format(palette[idx]))  #print('I have {} {}'.format(a, b))
   plt.imshow([[rgb]])

def getcolor():
    color = {}
    for i, rgb in enumerate(palette):
        color[getlabel(i)] = rgb
    return color